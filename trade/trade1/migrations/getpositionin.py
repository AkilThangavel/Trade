from ib_insync import *
util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

positionHolding = (ib.positions())
ib.disconnect()