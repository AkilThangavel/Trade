import re
discordMessages = ["BTO SPX 3860p 1/10 @ 3.8 ", "STC SPX 3860p 1/10 @ 3.8 ", "STC SPX 3870p 1/10 @ 3.8 "]
signalLis = []
executedOrders = {}


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


for msg in discordMessages:
    signalMsg = msg
    if signalMsg not in signalLis:
        signalLis.append(signalMsg)
        convSignal = signal_converstion(signalMsg)
        if convSignal["buyorsell"] == "BUY":
            setUpFund =  500
            limitPrice = convSignal["buysellprice"] * 100
            setUpQuantity = int(setUpFund//limitPrice)
            convSignal["quantity"] = setUpQuantity
            # ib_trade_signal(convSignal)
            executedOrders[convSignal["tickername"] + convSignal["strikeprice"] + convSignal["callorput"] + convSignal["contractdate"]] = convSignal["quantity"]
            print("BUY")
        elif convSignal["buyorsell"] == "SELL":
            if executedOrders[convSignal["tickername"] + convSignal["strikeprice"] + convSignal["callorput"] + convSignal["contractdate"]]:
                convSignal["quantity"] = executedOrders[convSignal["tickername"] + convSignal["strikeprice"] + convSignal["callorput"] + convSignal["contractdate"]]
                # ib_trade_signal(convSignal)
            print("SELL")
        else:
            pass