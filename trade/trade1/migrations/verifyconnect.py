import requests
import json
import re
from zoneinfo import ZoneInfo
import datetime as dt
import logging


def retrieve_messages(channelid):
    headers = {
        'authorization': 'NjU2NDcxODMwMjEwNTQzNjY2.GR4hN2.Q7s91wNFmxsEQtwGNuTYKyWrTHDLggkZEESDPo'
    }
    r = requests.get(
        f'https://discord.com/api/v9/channels/{channelid}/messages?limit=100',headers=headers
        )
    jsonn = json.loads(r.text)
    return (jsonn)


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
            contractDate = contractDate[2]+contractDate[0]+ contractDate[1]
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
            contractDate = contractDate[2]+contractDate[0]+ contractDate[1]
            signalDict["contractdate"] = contractDate
            bssPrice = re.findall(r"@[ +-]?([0-9]+([.][0-9]*)?|[.][0-9]+)", signalTriggered)[0][0]
            signalDict["buysellprice"] = float(bssPrice)
            return signalDict
    except Exception as e: 
        # logging.exception("Error occurred")
        return None





count = 0
channelIds = [738943464259059752, 972215994770673664, 952916697008984154, 1058040359038492712]
signalLis = []
executedOrders = {}
logging.warning("Started Listing to Discord Signal")
while count < 1:
    try:
        print(len(signalLis))
        for channel in channelIds:
            discordMessages = retrieve_messages(channel)[-5::1]
            for msg in discordMessages:
                signalMsg = msg["content"]
                if signalMsg not in signalLis:
                    signalLis.append(signalMsg)
                    convSignal = signal_converstion(signalMsg)
                    if convSignal["buyorsell"] == "BUY":
                        setUpFund =  500
                        limitPrice = convSignal["buysellprice"] * 100
                        setUpQuantity = int(setUpFund//limitPrice)
                        convSignal["quantity"] = setUpQuantity
                        executedOrders[convSignal["tickername"] + convSignal["strikeprice"] + convSignal["callorput"] + convSignal["contractdate"]] = convSignal["quantity"]
                        print(convSignal, signalMsg)
                    elif convSignal["buyorsell"] == "SELL":
                        if executedOrders[convSignal["tickername"] + convSignal["strikeprice"] + convSignal["callorput"] + convSignal["contractdate"]]:
                            convSignal["quantity"] = executedOrders[convSignal["tickername"] + convSignal["strikeprice"] + convSignal["callorput"] + convSignal["contractdate"]]
                            print(convSignal, signalMsg)
                    else:
                        pass
    except:
        pass
