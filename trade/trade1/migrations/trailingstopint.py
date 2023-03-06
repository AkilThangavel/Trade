from ib_insync import *
# Buy (parent) order

ib=IB()
ib.connect("127.0.0.1", 7497, clientId=131)
# contract=Option("ITC", "20230223", 382.5, "C","NSE")
# ib.qualifyContracts(contract)
# order = MarketOrder("SELL", 1600)
# buyOrder=ib.placeOrder(contract,order) 
# print((buyOrder  ))
# buyOrder = ib.LimitOrder("BUY", count, price, orderId = buyOrderId, transmit = False)
  
# Sell order (adjustable stop loss)
# sellOrder = Order()
# sellOrder.action = "SELL"
# sellOrder.orderType = "STP"
# sellOrder.orderId 
# sellOrder.auxPrice = 9
# sellOrder.totalQuantity = 1600
 
# # Adjustable parameters
# sellOrder.triggerPrice = 7
# sellOrder.adjustedOrderType = "TRAIL"
# sellOrder.adjustableTrailingUnit = 1 # (trailing %)
# sellOrder.adjustedTrailingAmount = 1.0 # 10%
# sellOrder.parentId = buyOrder.orderId
# sellOrder.transmit = True
  
# buyTrade = ib.placeOrder(contract, buyOrder)
# sellTrade = ib.placeOrder(contract, sellOrder)

def place_long_bracket_order_with_market_on_close_take_profit():
    
    contract=Option("ITC", "20230223", 382.5, "C","NSE")
    ib.qualifyContracts(contract)
    order = MarketOrder("SELL", 1600)
    buyOrder=ib.placeOrder(contract,order) 
    print((buyOrder  ))
    contract=Option("ITC", "20230223", 382.5, "C","NSE")
    ib.qualifyContracts(contract)
    current_price = 2.50
    # buyOrder=ib.placeOrder(contract,order) 
    stock = contract

    stop_loss_price = current_price * 0.98  # Stop loss if stock goes down by 2%
    stop_loss_price = round(stop_loss_price, 2)
    take_profit_price = current_price * 1.02
    take_profit_price = round(take_profit_price, 2)
    bracket = BracketOrder(buyOrder, takeProfit= take_profit_price,
                                    stopLoss=stop_loss_price)
    for ord in bracket:
        ib.placeOrder(contract, ord)
    
    buyOrder=ib.placeOrder(contract,bracket) 




place_long_bracket_order_with_market_on_close_take_profit()

# #This will be our main or "parent" order
# parent = Order()
# parent.orderId = 150
# parent.action = "BUY"
# parent.orderType = "LMT"
# parent.totalQuantity = 1600
# parent.lmtPrice = 4.0
# parent.transmit = False

# stopLoss = Order()
# stopLoss.orderId = 151
# stopLoss.action = "SELL" 
# stopLoss.orderType = "TRAIL"
# stopLoss.auxPrice = 1.0
# stopLoss.trailStopPrice = 4.00
# stopLoss.totalQuantity = 1600
# stopLoss.parentId = 150
# stopLoss.transmit = True

# bracketOrder = [parent, stopLoss]
# print(bracketOrder)






ib.disconnect()