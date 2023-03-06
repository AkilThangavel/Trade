from ibapi.client import *
from ibapi.wrapper import *

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = 1001
        print("NextValidId:", orderId)
        mycontract = Contract()
        mycontract.symbol = "AAPL"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"
        self.reqContractDetails(orderId, mycontract)
        
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract, )
        myorder = Order()
        myorder.orderId = reqId
        myorder.action = "BUY"
        myorder.orderType = "MKT"
        myorder.totalQuantity = 1
        myorder.Transmit = True 
        self.placeOrder(reqId, contractDetails.contract, myorder)
        self.disconnect()


app = TestApp()
app.connect("127.0.0.1", 7497, 1000)
app.run()