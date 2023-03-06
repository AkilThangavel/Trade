from ib_insync import *
import datetime as dt 
from zoneinfo import ZoneInfo
import re
import requests
import json

ib=IB()
ib.connect("127.0.0.1", 7497, clientId=131)


def retrieve_messages(channelid):
    headers = {
        'authorization': 'NjU2NDcxODMwMjEwNTQzNjY2.GjZ4hN.n57uUhed5xWb7huPyxlT-PSBFJhe2T3M9aV5LM'
    }
    r = requests.get(
    f'https://discord.com/api/v9/channels/{channelid}/messages?limit=10',headers=headers
    )
    return (r)



def checkpoint_discord(channelid):
    data = retrieve_messages(channelid)
    count = 1
    while count < 11:
        if data.status_code != 200:
            data = retrieve_messages(channelid)
            print("Discord Error try ", count)
            count += 1
        else:
            # print(data)
            print("##################################----------------------------################################")
            jsonn = json.loads(data.text)
            return jsonn
            



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
            print(contractDate)
            contractDate[1] = str(contractDate[1]).zfill(2)
            contractDate[0] = str(contractDate[0]).zfill(2)
            contractDate = 2023+contractDate[0]+ contractDate[1]
            signalDict["contractdate"] = contractDate
            bssPrice = re.findall(r"@[ +-]?([0-9]+([.][0-9]*)?|[.][0-9]+)", signalTriggered)[0][0]
            signalDict["buysellprice"] = float(bssPrice)
            return signalDict
    except Exception as e: 
        # logging.exception("Error occurred")
        return None


def ib_trade_buy_signal(convSignal):
    try:
        convSignal["quantity"] = 1600
        contract=Option(convSignal["tickername"],convSignal["contractdate"], float(convSignal["strikeprice"]),convSignal["callorput"],"NSE")
        contract = ib.qualifyContracts(contract)[0]
        dt1 = dt.datetime.now() + dt.timedelta(seconds=40)
        dt1 = dt1.replace(tzinfo=ZoneInfo('America/Denver'))
        order= LimitOrder(convSignal["buyorsell"], convSignal["quantity"], convSignal["buysellprice"], tif='GTD',goodTillDate=dt1.strftime("%Y%m%d %H:%M:%S"))
        trade=ib.placeOrder(contract,order) 
        print(trade)
    except Exception as e:
        print(e, "BUHY######################") 
        pass

def ib_trade_sell_signal(convSignal):
    try:
        convSignal["quantity"] = 1600
        contract=Option(convSignal["tickername"],convSignal["contractdate"], float(convSignal["strikeprice"]),convSignal["callorput"],"NSE")
        ib.qualifyContracts(contract)
        order = MarketOrder("SELL", convSignal["quantity"])
        trade=ib.placeOrder(contract,order) 
    except Exception as e:
        print(e, "######################")
        pass


def setup_quantity(convSignal):
    try:
        setUpFund =  500
        bsPrice =  convSignal["buysellprice"] 
        contractBSPrice = bsPrice * 100
        quantity = setUpFund //contractBSPrice
        convSignal["quantity"] = quantity
        return convSignal
    except:
        convSignal["quantity"] = 1
        return convSignal

def verify_and_place_order(signalReceived):
    try:
        signalConvered = signal_converstion(signalReceived)
        print(signalConvered)
        if signalConvered["buyorsell"] == "BUY":
            signalConvered = setup_quantity(signalConvered)
            ib_trade_buy_signal(signalConvered) 
        elif signalConvered["buyorsell"] == "SELL":
            contract=Option(signalConvered["tickername"],signalConvered["contractdate"], float(signalConvered["strikeprice"]),signalConvered["callorput"],"NSE")
            contract = ib.qualifyContracts(contract)
            positionHolding = (ib.positions())
            for i in positionHolding:
                if i.contract in contract:
                    signalConvered["quantity"] = i.position
                    ib_trade_sell_signal(signalConvered)
        
        print("------------------------------------------------------------")
    except Exception as e:
        print(signalReceived, "VP###############################")




# convSignal = {}
# convSignal["buyorsell"] = "BUY"
# convSignal["tickername"] = "ITC"
# convSignal["contractdate"] = "20230223"
# convSignal["strikeprice"] = 342.5
# convSignal["callorput"] = "C"
# convSignal["quantity"] = 1
# convSignal["buysellprice"] = 10.50
# ib_trade_buy_signal(convSignal)
# verify_and_place_order("BTO SPY 390p 1/27 @ 1.64 **(Starter Position, don't size up here)**")
# for i in range(10000):
#     checkpoint_discord(738943464259059752)
channelIds = [738943464259059752, 1058040359038492712, 952916697008984154]
signalLis = []


verify_and_place_order("Bto 2 ITC 342.5c 2/23 @ 10.50")
# count = 0
# while True:
#     try:
#         import time
#         time.sleep(1)
#         for channel in channelIds:
#             discordMessages = checkpoint_discord(channel)
#             print("number of scan today - ", count)
#             count += 1
#             if discordMessages:
#                 for msg in discordMessages:
#                     msgDatetime = re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}", msg["timestamp"])[0]
#                     msgDatetime = (dt.datetime.strptime(msgDatetime, '%Y-%m-%dT%H:%M:%S'))
#                     msgDatetime = (msgDatetime.date())
#                     currentdt = dt.date.today() 
#                     if currentdt == msgDatetime:
#                         signalMsg = msg["content"]
#                         if signalMsg not in signalLis:
#                             signalLis.append(signalMsg)
#                             if "BTO" in msg["content"] or "STC" in msg["content"] or "Bto" in msg["content"] or "Stc" in msg["content"]:
#                                 print("##############################")
#                                 print(msg["content"])
#                                 print("##############################")
#                                 print("\n")
#                                 print("\n")
#                                 verify_and_place_order(signalMsg)
#                             else:
#                                 print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#                                 print( msg["content"])
#                                 print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#                                 print("\n")
#                                 print("\n")
#     except Exception as e:
#         print("Unknown Signal", e)
ib.disconnect() 