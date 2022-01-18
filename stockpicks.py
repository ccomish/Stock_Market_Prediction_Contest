from yahoo_fin import stock_info as yf
import datetime
import os
import csv
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.dates as mdates

def calculatePriceChange(ticker, delta):
    if delta == 0:
        currentStockPrice = yf.get_live_price(ticker)
    else:
        priceDataNow = yf.get_data(ticker, start_date = f'{datetime.date.today()-datetime.timedelta(days=delta)}', index_as_date=True, interval="1d")
        currentStockPrice = priceDataNow.iloc[0]['close']
    priceDataOriginal = yf.get_data(ticker, start_date = "2022-01-10", index_as_date=True, interval="1d")
    originalStockPrice = priceDataOriginal.iloc[0]['close']
    priceChange = ((currentStockPrice / originalStockPrice) - 1) * 100
    return priceChange

def calculateReturn(input, dayDelta):
    returnSum = 0
    shortCoefficient = 1
    for element in input:
        returnSum += calculatePriceChange(element, dayDelta) * (shortCoefficient)
        shortCoefficient *= -1
    return returnSum/2


def calculateStandings():
    with open("/Users/cartercomish/coding_classes/Stock_Contest/savedData.csv", "r", encoding="utf-8", errors = "ignore") as f:
        latestReturn = f.readlines()[-1]
        latestReturn = latestReturn.split(",")
        f.close()
    standings = [[float(latestReturn[0]), "Carter"], [float(latestReturn[1]), "Nolan"], [float(latestReturn[2]), "Stuart"]]
    standings.sort(reverse=True)
    return standings


def standingsDetails(standings, choiceList):
    detailedStandingsList = []
    for standing in standings:
        if standing[1] == "Carter":
            detailedStandingsList.append(["Carter", calculatePriceChange(choiceList[0][0], 0), choiceList[0][0], -calculatePriceChange(choiceList[0][1], 0), choiceList[0][1], calculateReturn(choiceList[0], 0)])
        elif standing[1] == 'Nolan':
             detailedStandingsList.append(["Nolan", calculatePriceChange(choiceList[1][0], 0), choiceList[1][0], -calculatePriceChange(choiceList[1][1], 0), choiceList[1][1], calculateReturn(choiceList[1], 0)])       
        elif standing[1] == 'Stuart':
            detailedStandingsList.append(["Stuart", calculatePriceChange(choiceList[2][0], 0), choiceList[2][0], -calculatePriceChange(choiceList[2][1], 0), choiceList[2][1], calculateReturn(choiceList[2], 0)])
    return detailedStandingsList            

def sendUpdateMessage(targetGroup, targetText):
    os.system('osascript /Users/cartercomish/coding_classes/Stock_Contest/savedData.csv {} "{}"'.format(targetGroup, targetText))

def appendData(choiceList, dateDeltaList):
    
    #dataDict = {'Carter': [carterReturn], 'Nolan':[nolanReturn], 'Stuart':[stuartReturn], 'Date':[datetime.date.today()]}
    #df = pd.DataFrame(dataDict)
    #df.to_csv('savedData.csv', index=False )
    priceHistory = pd.read_csv("/Users/cartercomish/coding_classes/Stock_Contest/savedData.csv", header=0)
    with open("/Users/cartercomish/coding_classes/Stock_Contest/savedData.csv", "a", newline='') as f:
        for delta in dateDeltaList:
            entry = []
            for choice in choiceList:
                entry.append(calculateReturn(choice, delta))
            entry.append(datetime.date.today()-datetime.timedelta(days=delta))
            write = csv.writer(f)
            write.writerow(entry)
        f.close()


def plotData():
    df = pd.read_csv("/Users/cartercomish/coding_classes/Stock_Contest/savedData.csv", skipinitialspace=True, header=0)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)


    a = df['Carter']
    b = df['Nolan']
    c = df['Stuart']
    date = df['Date']

    plt.plot(date, a, label='Carter')
    plt.plot(date, b, label='Nolan')
    plt.plot(date, c, label = 'Stuart')

    plt.title('2022 Stock Prediction Contest')
    plt.xlabel('Date')
    plt.ylabel('Total Return %')
    plt.legend(loc=9)
    plt.xticks(rotation=45)
    #plt.autoscale(enable=True, axis='both', tight=None)

    plt.tight_layout()
    plt.savefig('/Users/cartercomish/Desktop/Plots/stockplot.png')

def updateMessage(detailedStandings):
    first_place_statement = f"{detailedStandings[0][0]} is in 1st place with a return of {detailedStandings[0][1]:.2f}% on his long pick, {detailedStandings[0][2]}, and a return of {detailedStandings[0][3]:.2f}% on his short pick, {detailedStandings[0][4]}, for a total return of {detailedStandings[0][5]:.2f}%\n\n"
    second_place_statement = f"{detailedStandings[1][0]} is in 2nd place with a return of {detailedStandings[1][1]:.2f}% on his long pick, {detailedStandings[1][2]}, and a return of {detailedStandings[1][3]:.2f}% on his short pick, {detailedStandings[1][4]}, for a total return of {detailedStandings[1][5]:.2f}%\n\n"
    third_place_statement = f"{detailedStandings[2][0]} is in 3rd place with a return of {detailedStandings[2][1]:.2f}% on his long pick, {detailedStandings[2][2]}, and a return of {detailedStandings[2][3]:.2f}% on his short pick, {detailedStandings[2][4]}, for a total return of {detailedStandings[2][5]:.2f}%\n\n"
    message = first_place_statement + second_place_statement + third_place_statement
    return message 
    
if __name__ == "__main__":
    carterChoices = ['MSFT', 'AMC']
    nolanChoices = ['TCF.CN', 'RIVN']
    stuartChoices = ['ATZ.TO', 'PLUG']
    choiceList = [carterChoices, nolanChoices, stuartChoices]
    
    if datetime.date.today().weekday() == 6:
        dateDeltaList = [22, 15, 8, 0]
    else:
        dateDeltaList = [21, 14, 7, 0]

    appendData(choiceList, dateDeltaList)
    message = updateMessage(standingsDetails(calculateStandings(), choiceList))
    plotData()
    groupChat = 'SpeculativePlays'
    '''
    sendUpdateMessage(groupChat, message)
    
    if datetime.date.today().strftime("%Y") == "2023":
        message = f'Congratulations {standingsDetails(calculateStandings(), choiceList)[0][0]}, you have won the stock picking contest of 2022. {standingsDetails(calculateStandings(), choiceList)[1][0]} and {standingsDetails(calculateStandings(), choiceList)[2][0]} owe you a beer.'
        os.system('osascript send.scpt {} "{}"'.format(groupChat, message))
    '''
    