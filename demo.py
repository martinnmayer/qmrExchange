from qmr_exchange import Exchange
import time


exchange = Exchange()
exchange.create_asset('AAPL')
exchange.limit_buy('AAPL',100,2,creator='pepe')

# time.sleep(1)
exchange.limit_buy('AAPL',98,2,creator='pepe')
exchange.limit_buy('AAPL',99,2,creator='pepe')
exchange.limit_buy('AAPL',91,2,creator='pepe')

exchange.limit_sell('AAPL',102,2,creator='martin')
exchange.limit_sell('AAPL',99,2,creator='martin')

# Check order book
print(exchange.get_order_book('AAPL'))
print(exchange.get_order_book('AAPL').df['bids'])
print(exchange.get_order_book('AAPL').df['asks'])
