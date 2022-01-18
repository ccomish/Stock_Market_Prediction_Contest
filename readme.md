# Stock Market Contest
## Introduction
A group of friends and I make a friendly bet on the stock market each year. We each provide a stock for a "long" pick and a "short" pick. The person who has the highest return at the end of the year is the winner. This year, the contest started on January 10th, 2021

### General Info
This program is run on the first of every month using crontab locally on my machine. Using yahoo-fin, it checks market data for each selected stock and calculates the total return 3 weeks ago, 2 weeks ago, a week ago and the current return for each contestant and saves the data to a csv file. The program calculates the standings of the contest and provides a message desribing the current results. The csv file is then plotted using matplot lib. Using applescript, the message and an image of the results plot are sent to an iMessage group containing the people involved in the contest. 
The contest is tracked weekly buyt results are provided monthly to the contestants. On January 1st 2023, a message will be generated to inform the group of the winner of the contest.