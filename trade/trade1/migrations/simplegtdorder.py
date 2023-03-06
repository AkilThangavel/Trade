from ib_insync import *
import datetime as dt
from zoneinfo import ZoneInfo
dt1 = dt.datetime.now() + dt.timedelta(0,59)
dt1 = dt1.replace(tzinfo=ZoneInfo('America/Denver'))
ib=IB()
ib.connect("127.0.0.1", 7497, clientId=130)
contract=Option("LMT","20230127", 455,"C","SMART")
ib.qualifyContracts(contract)


print(dt1)
order= LimitOrder("BUY",1, 3.10)
trade=ib.placeOrder(contract,order)
print(trade)
ib.disconnect()


