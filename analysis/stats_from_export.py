# zap-groups
# Author: Thyago Mota
# Description: Extracts basic stats from a single WhatsApp group export
# Date: August 2, 2020

import re

EXPORT_FILE_NAME = "sample2.txt"

# open sample file
f_in = open(EXPORT_FILE_NAME, "rt")

# ignore 1st line
f_in.readline()

# initialize stats maps
senderStats = {}
dateStats   = {}

# initialize control variables
text = ""

# read one line at a time
for line in f_in:

    # strip last character from the line
    line = line.strip()

    # check if line begins with a date
    if re.match("^[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,2}", line):

        # extract date
        data = line.split(" - ")
        if len(data) < 2:
            continue
        date = data[0].split(",")[0]

        # extract sender
        senderAndMessage = data[1].split(": ")
        if len(senderAndMessage) < 2:
            continue
        sender = senderAndMessage[0]
        if re.match("^\+[0-9]{1,2}", sender):

            # udpate sender stats
            if sender not in senderStats:
                senderStats[sender] = 0
            senderStats[sender] += 1

            # update date stats
            if date not in dateStats:
                dateStats[date] = 0
            dateStats[date] += 1

            # extract message
            message = senderAndMessage[1]

            # update text
            text += message + " "
        else:
            continue
    else:
        text += line + " "

# close sample file
f_in.close()

# print date stats
print(dateStats)
total = 0
for date in dateStats:
    total += dateStats[date]
print(str(total) + " messages with dates!")

# print sender stats
print(senderStats)
total = 0
topSender = None
topTotal = 0
for sender in senderStats:
    total += senderStats[sender]
    if senderStats[sender] > topTotal:
        topTotal = senderStats[sender]
        topSender = sender
print(str(total) + " messages with sender info!")
print(topSender + " was top sender with " + str(topTotal) + " messages!")

# print text messages
text = text.strip()
print(text)
