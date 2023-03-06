import requests
import json
import datetime as dt
import re 
import logging



def signal_converstion(signalTriggered):
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
            strikePrice = re.findall(r"[0-9]+[c,p,C,P]", signalTriggered)[0]
            onlyStrikePrice = re.findall(r"[0-9]+", strikePrice)[0]
            signalDict["strikeprice"] = onlyStrikePrice
            cpVar = re.findall(r"[c,p,P,C]", strikePrice)[0].upper()
            signalDict["callorput"] = cpVar
            contractDate = re.findall("[0-9]{0,2}/[0-9]{0,2}/\d\d\d\d|[0-9]{0,2}/[0-9]{0,2} ", signalTriggered)[0]
            contractDate = contractDate.lstrip().rstrip()
            if len(contractDate) < 6:
                contractDate += "/2022"
            contractDate = contractDate.split("/")
            contractDate[1] = str(contractDate[1]).zfill(2)
            contractDate[0] = str(contractDate[0]).zfill(2)
            contractDate = contractDate[1]+contractDate[0]+ contractDate[2]
            signalDict["contractdate"] = contractDate
            bssPrice = re.findall(r"@[ +-]?([0-9]+([.][0-9]*)?|[.][0-9]+)", signalTriggered)[0][0]
            signalDict["buysellprice"] = float(bssPrice)
            return signalDict
        elif (verifySignal.isnumeric()) == False:
            signalDict = {}
            bsVar = signalTriggered.split(maxsplit=1)[0].upper()
            if bsVar == "BTO":
                signalDict["buyorsell"] = "BUY"
            elif bsVar == "STC":
                signalDict["buyorsell"] = "SELL"
            tickerName = signalTriggered.split()[1].upper()
            signalDict["tickername"] = tickerName
            strikePrice = re.findall(r"[0-9]+[c,p,C,P]", signalTriggered)[0]
            onlyStrikePrice = re.findall(r"[0-9]+", strikePrice)[0]
            signalDict["strikeprice"] = onlyStrikePrice
            cpVar = re.findall(r"[c,p,P,C]", strikePrice)[0].upper()
            signalDict["callorput"] = cpVar
            contractDate = re.findall("[0-9]{0,2}/[0-9]{0,2}/\d\d\d\d|[0-9]{0,2}/[0-9]{0,2} ", signalTriggered)[0]
            contractDate = contractDate.lstrip().rstrip()
            if len(contractDate) < 6:
                contractDate += "/2022"
            contractDate = contractDate.split("/")
            contractDate[1] = str(contractDate[1]).zfill(2)
            contractDate[0] = str(contractDate[0]).zfill(2)
            contractDate = contractDate[2]+contractDate[0]+ contractDate[1]
            signalDict["contractdate"] = contractDate
            bssPrice = re.findall(r"@[ +-]?([0-9]+([.][0-9]*)?|[.][0-9]+)", signalTriggered)[0][0]
            signalDict["buysellprice"] = float(bssPrice)
            return signalDict
    except Exception as e: 
        logging.exception("Error occurred")
        return 



def retrieve_messages(channelid):
    headers = {
        'authorization': 'NjU2NDcxODMwMjEwNTQzNjY2.GR4hN2.Q7s91wNFmxsEQtwGNuTYKyWrTHDLggkZEESDPo'
    }
    r = requests.get(
        f'https://discord.com/api/v9/channels/{channelid}/messages?limit=100',headers=headers
        )
    jsonn = json.loads(r.text)
    return (jsonn)



    

print(signal_converstion("STC TSLA 122c 12/30 @ 1.20 from .53 <@&893405144337772594> "))

currentdt = dt.datetime.now() - dt.timedelta(hours=5, minutes=80)
lastestSignals = []
executedSignals = []
allowedUsernames = []
channelLis = [738943464259059752, 972215994770673664, 952916697008984154]
count = 0
while True:
    for channel in channelLis:
        rawMessages = retrieve_messages(channel)  
        for msg in rawMessages:
            msgDatetime = re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}", msg["timestamp"])[0]
            msgDatetime = (dt.datetime.strptime(msgDatetime, '%Y-%m-%dT%H:%M:%S'))
            if currentdt < msgDatetime:
                if msg['content'] not in lastestSignals:
                    if "BTO" in msg['content'] or "STC" in msg['content']:
                        sc = signal_converstion(msg["content"])
                        if sc:
                            if sc not in lastestSignals:
                                lastestSignals.append(sc)

    print(lastestSignals)
    print("############################################")
            if fnSignal:
                executedSignals.append(i)
                print(fnSignal)
                print("Placed "+ fnSignal["buyorsell"] + " on "+fnSignal["tickername"] + "Strike Price" + fnSignal["strikeprice"]+ fnSignal["callorput"] + fnSignal["contractdate"]+ fnSignal["buysellprice"])
    count += 1

