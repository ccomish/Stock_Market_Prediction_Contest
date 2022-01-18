
on run {groupChat, targetMessageToSend}
	tell application "Messages"
		set theAttachement to POSIX file "/Users/cartercomish/Desktop/Plots/stockplot.png"
		set targetChat to groupChat
		set targetMessage to targetMessageToSend
		send targetMessage to chat targetChat
		send file theAttachement to chat targetChat
	end tell
end run