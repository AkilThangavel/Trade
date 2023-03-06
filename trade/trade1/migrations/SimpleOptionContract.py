from ib_insync import *

ib=IB()
ib.connect("127.0.0.1", 7497, clientId=13)
contract=Option("SPX","20230103", 3820,"C","SMART")
ib.qualifyContracts(contract)
order= LimitOrder("BUY",1, 4.8)
trade=ib.placeOrder(contract,order)
print(trade)