import re
import datetime as dt
import csv
correctSignal = []
wrongSignal = []
falseList = []
signalvercount = 0 
recNotCorrect =[]



def signal_converstion(signalTriggered):
    global signalvercount, wrongSignal
    signalvercount += 1
    try:
        verifySignal = signalTriggered.split()[1]
        if (verifySignal.isnumeric()):
            signalDict = {}
            bsVar = signalTriggered.split(maxsplit=1)[0].upper()
            if bsVar == "BTO":
                signalDict["buyorsell"] = "BUY" 
            elif bsVar == "STC":
                signalDict["buyorsell"] = "SELL"
            tickerName = signalTriggered.split()[2].upper()
            signalDict["tickername"] = tickerName
            strikePrice = re.findall(r"[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)+[c,p,P,C]", signalTriggered)[0]
            onlyStrikePrice = strikePrice[0]
            signalDict["strikeprice"] = onlyStrikePrice
            cpVar = re.findall(r"[0-9][c,p,P,C]", signalTriggered)
            cpVar = re.findall(r"[c,p,P,C]", cpVar[0])
            signalDict["callorput"] = cpVar[0].upper()
            contractDate = re.findall("[0-9]{0,2}/[0-9]{0,2}/\d\d\d\d|[0-9]{0,2}/[0-9]{0,2} ", signalTriggered)[0]
            contractDate = contractDate.lstrip().rstrip()
            if len(contractDate) < 6:
                contractDate += "/2023"
            contractDate = contractDate.split("/")
            contractDate[1] = str(contractDate[1]).zfill(2)
            contractDate[0] = str(contractDate[0]).zfill(2)
            contractDate = "2023"+contractDate[0]+ contractDate[1]
            signalDict["contractdate"] = contractDate
            bssPrice = re.findall(r"@[ +-]?([0-9]+([.][0-9]*)?|[.][0-9]+)", signalTriggered)[0][0]
            signalDict["buysellprice"] = float(bssPrice)
            correctSignal.append(signalDict)
        elif (verifySignal.isnumeric()) == False:
            signalDict = {}
            bsVar = signalTriggered.split(maxsplit=1)[0].upper()
            if bsVar == "BTO":
                signalDict["buyorsell"] = "BUY"
            elif bsVar == "STC":
                signalDict["buyorsell"] = "SELL"
            tickerName = signalTriggered.split()[1].upper()
            signalDict["tickername"] = tickerName
            strikePrice = re.findall(r"[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)+[c,p,P,C]", signalTriggered)[0]
            onlyStrikePrice = strikePrice[0]
            signalDict["strikeprice"] = onlyStrikePrice
            cpVar = re.findall(r"[0-9][c,p,P,C]", signalTriggered)
            cpVar = re.findall(r"[c,p,P,C]", cpVar[0])
            signalDict["callorput"] = cpVar[0].upper()
            contractDate = re.findall("[0-9]{0,2}/[0-9]{0,2}/\d\d\d\d|[0-9]{0,2}/[0-9]{0,2} ", signalTriggered)[0]
            contractDate = contractDate.lstrip().rstrip()
            if len(contractDate) < 6:
                contractDate += "/2023"
            contractDate = contractDate.split("/")
            print(contractDate)
            contractDate = dt.date(int(contractDate[2]), int(contractDate[0]), int(contractDate[1]))
            print(contractDate)
            contractDate[1] = str(contractDate[1]).zfill(2)
            contractDate[0] = str(contractDate[0]).zfill(2)
            contractDate = contractDate[2]+contractDate[0]+ contractDate[1]
            signalDict["contractdate"] = contractDate
            bssPrice = re.findall(r"@[ +-]?([0-9]+([.][0-9]*)?|[.][0-9]+)", signalTriggered)[0][0]
            signalDict["buysellprice"] = float(bssPrice)
            correctSignal.append(signalDict)
    except Exception as e: 
        # wrongSignal.append("signalDict")
        # if "BTO" in signalTriggered or  "STC" in signalTriggered:
        #     recNotCorrect.append(signalTriggered)
        # else:
        #     falseList.append(signalTriggered)
        print(e)


with open('Bull.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        signal_converstion(lines[3].rstrip())

with open('bull1.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        signal_converstion(lines[3].rstrip())

with open('testsig1.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        signal_converstion(lines[3].rstrip())
print("Total posted signals", signalvercount)
print("Total correct Signals : ", len(correctSignal))
print("Total wrong Signals : ", len(wrongSignal))
print("Total recNotCorrect Signals : ", len(recNotCorrect))
# signal_converstion("BTO 8 BA 140C 10/7 @ 1.45 @NANDO Alert")
# signal_converstion("STC TSLA 630P 5/20@ 1.18 @here")



with open('filtered_text_message.txt', 'w') as f:
    for line in falseList:
        f.write(str(line))
        f.write('\n')