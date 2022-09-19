from datetime import datetime
from decimal import Decimal
from typing import List
import pandas as pd
from enum import Enum
from ._utils import get_datetime_range, get_random_string

class OrderSide(Enum):
    BUY = 'buy'
    SELL = 'sell'


class LimitOrder():
    def __init__(self, ticker, price, qty, creator, side, dt=None):
        self.id = get_random_string()
        self.ticker: str = ticker
        self.price: Decimal = price
        self.type: OrderSide = side
        self.qty: int = qty
        self.creator: str = creator
        self.dt: datetime = dt if dt else datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'ticker': self.ticker,
            'price': self.price,
            'qty': self.qty,
            'creator': self.creator,
            'dt': self.dt
        }

    def __repr__(self):
        return f'<LimitOrder: {self.ticker} {self.qty}@{self.price}>'

    def __str__(self):
        return f'<LimitOrder: {self.ticker} {self.qty}@{self.price}>'


class OrderBook():
    def __init__(self, ticker):
        self.ticker = ticker
        self.bids: List[LimitOrder] = []
        self.asks: List[LimitOrder] = []

    def __repr__(self):
        return f'<OrderBook: {self.ticker}>'

    def __str__(self):
        return f'<OrderBook: {self.ticker}>'
    


    @property
    def df(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return {
            'bids': pd.DataFrame.from_records([b.to_dict() for b in self.bids]),
            'asks': pd.DataFrame.from_records([a.to_dict() for a in self.asks])
        }


class Trade():
    def __init__(self, ticker, qty, price, buyer, seller, dt=None):
        self.ticker = ticker
        self.qty = qty
        self.price = price
        self.buyer = buyer
        self.seller = seller
        self.dt = dt if dt else datetime.now()

    def __repr__(self):
        return f'<Trade: {self.ticker} {self.qty}@{self.price} {self.dt}>'

    def to_dict(self):
        return {
            'dt': self.dt,
            'ticker': self.ticker,
            'qty': self.qty,
            'price': self.price,
            'buyer': self.buyer,
            'seller': self.seller
        }


class Exchange():
    def __init__(self, datetime= None):
        self.books = {}
        self.trade_log: List[Trade] = []
        self.datetime = datetime
        self.agents_aum_updates = []

    def __str__(self):
        return ', '.join(ob for ob in self.books)

    def create_asset(self, ticker: str, seed_price=100, seed_bid=None, seed_ask=None):
        self.books[ticker] = OrderBook(ticker)
        seed_bid = seed_bid if seed_bid else seed_price * 0.99
        seed_ask = seed_ask if seed_ask else seed_price * 1.01
        self._process_trade(ticker, 1, seed_price, 'init_seed', 'init_seed',)
        self.limit_buy(ticker, seed_bid, 10, 'init_seed')
        self.limit_sell(ticker, seed_ask, 10, 'init_seed')


    def get_order_book(self, ticker: str):
        return self.books[ticker]

    def _process_trade(self, ticker, qty, price, buyer, seller):
        self.trade_log.append(
            Trade(ticker, qty, price, buyer, seller,self.datetime)
        )
        self.agents_aum_updates.extend([[buyer,-qty*price],[seller,qty*price]])
        
    

    def get_latest_trade(self, ticker):
        return next(trade for trade in self.trade_log[::-1] if trade.ticker == ticker)

    def get_trades(self, ticker):
        return pd.DataFrame.from_records([t.to_dict() for t in self.trade_log if t.ticker == ticker]).set_index('dt').sort_index()

    def get_quotes(self, ticker):
        # TODO: if more than one order has the best price, add the quantities.
        # TODO: check if corresponding quotes exist in order to avoid exceptions
        best_bid = self.books[ticker].bids[0]
        best_ask = self.books[ticker].asks[0]
        quotes = {
            'ticker': ticker,
            'bid_qty': best_bid.qty,
            'bid_p': best_bid.price,
            'ask_qty': best_ask.qty,
            'ask_p': best_ask.price,
        }
        return quotes

    def get_best_bid(self, ticker):
        if self.books[ticker].bids:
            return self.books[ticker].bids[0]

    def get_best_ask(self, ticker):
        if self.books[ticker].asks:
            return self.books[ticker].asks[0]

    def get_midprice(self, ticker):
        quotes = self.get_quotes(ticker)
        return (quotes['bid_p'] + quotes['ask_p']) / 2

    def limit_buy(self, ticker: str, price: float, qty: int, creator: str):
        price = round(price,2)
        # check if we can match trades before submitting the limit order
        while qty > 0:
            best_ask = self.get_best_ask(ticker)
            if best_ask and price >= best_ask.price:
                trade_qty = min(qty, best_ask.qty)
                self._process_trade(ticker, trade_qty,
                                    best_ask.price, creator, best_ask.creator)
                qty -= trade_qty
                self.books[ticker].asks[0].qty -= trade_qty
                self.books[ticker].asks = [
                    ask for ask in self.books[ticker].asks if ask.qty > 0]
            else:
                break
        queue = len(self.books[ticker].bids)
        for idx, order in enumerate(self.books[ticker].bids):
            if price > order.price:
                queue = idx
                break
        new_order = LimitOrder(ticker, price, qty, creator, OrderSide.BUY, self.datetime)
        self.books[ticker].bids.insert(queue, new_order)
        return new_order


    def limit_sell(self, ticker: str, price: float, qty: int, creator: str):
        price = round(price,2)
        # check if we can match trades before submitting the limit order
        while qty > 0:
            best_bid = self.get_best_bid(ticker)
            if best_bid and price <= best_bid.price:
                trade_qty = min(qty, best_bid.qty)
                self._process_trade(ticker, trade_qty,
                                    best_bid.price, best_bid.creator, creator)
                qty -= trade_qty
                self.books[ticker].bids[0].qty -= trade_qty
                self.books[ticker].bids = [
                    bid for bid in self.books[ticker].bids if bid.qty > 0]
            else:
                break
        queue = len(self.books[ticker].asks)
        for idx, order in enumerate(self.books[ticker].asks):
            if price < order.price:
                queue = idx
                break
        new_order = LimitOrder(ticker, price, qty, creator, OrderSide.SELL, self.datetime)
        self.books[ticker].asks.insert(queue, new_order)
        return new_order

    def cancel_order(self, id):
        for book in self.exchange.books:
            bid = next(([idx,o] for idx, o in enumerate(self.exchange.books[book].bids) if o.id == id),None)
            if bid:
                self.exchange.books[book].bids[bid[0]]
                self.exchange.books[book].bids.pop(bid[0])
                return bid
            ask = next(([idx,o] for idx, o in enumerate(self.exchange.books[book].asks) if o.id == id),None)
            if ask:
                self.exchange.books[book].asks.pop(ask[0])
                return ask
        return None

    def cancel_all_orders(self, agent, ticker):
        self.books[ticker].bids = [b for b in self.books[ticker].bids if b.creator != agent]
        self.books[ticker].asks = [a for a in self.books[ticker].asks if a.creator != agent]
        return None

    def market_buy(self, ticker: str, qty: int, buyer: str):
        for idx, ask in enumerate(self.books[ticker].asks):
            trade_qty = min(ask.qty, qty)
            self.books[ticker].asks[idx].qty -= trade_qty
            qty -= trade_qty
            self._process_trade(ticker, trade_qty,
                                ask.price, buyer, ask.creator)
            if qty == 0:
                break
        self.books[ticker].asks = [
            ask for ask in self.books[ticker].asks if ask.qty > 0]

    def market_sell(self, ticker: str, qty: int, seller: str):
        for idx, bid in enumerate(self.books[ticker].bids):
            trade_qty = min(bid.qty, qty)
            self.books[ticker].bids[idx].qty -= trade_qty
            qty -= trade_qty
            self._process_trade(ticker, trade_qty,
                                bid.price, bid.creator, seller)
            if qty == 0:
                break
        self.books[ticker].bids = [
            bid for bid in self.books[ticker].bids if bid.qty > 0]

    def _set_datetime(self, dt):
        self.datetime = dt



class Agent():
    def __init__(self, name, tickers, aum=10_000):
        self.name = name
        self.tickers = tickers
        self.exchange:Exchange = None
        self.aum = aum

    def __repr__(self):
        return f'<Agent: {self.name}>'

    def __str__(self):
        return f'<Agent: {self.name}>'

    def get_latest_trade(self, ticker):
        return self.exchange.get_latest_trade(ticker)

    def get_best_bid(self, ticker):
        return self.exchange.get_best_bid(ticker)

    def get_best_ask(self, ticker):
        return self.exchange.get_best_ask(ticker)
    
    def get_latest_trade(self, ticker):
        return self.exchange.get_latest_trade(ticker)
        
    def get_midprice(self, ticker):
        return self.get_midprice(ticker)

    def get_order_book(self,ticker):
        return self.exchange.get_order_book(ticker)

    def get_quotes(self,ticker):
        return self.exchange.get_quotes(ticker)

    def get_trades(self, ticker):
        return self.exchange.get_trades(ticker)

    def market_buy(self, ticker, qty):
        return self.exchange.market_buy(ticker, qty, self.name)

    def market_sell(self, ticker, qty):
        return self.exchange.market_sell(ticker, qty, self.name)

    def limit_buy(self, ticker, price, qty):
        return self.exchange.limit_buy(ticker,price,qty,self.name)

    def limit_sell(self, ticker, price, qty):
        return self.exchange.limit_sell(ticker,price,qty,self.name)

    def _set_exchange(self,exchange):
        self.exchange = exchange

    def cancel_order(self, id):
        self.exchange.cancel_order(id=id)

    def cancel_all_orders(self, ticker):
        self.exchange.cancel_all_orders(self.name,ticker)

    def next(self):  
        pass

class Simulator():
    def __init__(self, from_date=datetime(2022,1,1), to_date=datetime(2022,12,31), time_unit='day'):
        self.datetime_range = iter(get_datetime_range(from_date,to_date,time_unit))
        self.dt = from_date
        self.agents = []
        self.exchange = Exchange(datetime=from_date)

    
    def add_agent(self,agent:Agent):
        # TODO: check that no existing agent already has the same name
        agent._set_exchange(self.exchange)
        self.agents.append(agent)

    def next(self):
        try:
            self.exchange._set_datetime(self.dt)
            for agent in self.agents:
                agent.next()
            self.dt = next(self.datetime_range)
            self.__update_agents_aum()
            return True
        except StopIteration:
            return False
    def run(self):
        while True:
            if not self.next():
                break

    def get_price_bars(self, bar_size='1D'):
        df = self.trades.resample(bar_size).agg({'price': 'ohlc', 'qty': 'sum'})
        df.columns = df.columns.droplevel()
        df.rename(columns={'qty':'volume'},inplace=True)
        return df

    @property
    def trades(self):
        return pd.DataFrame.from_records([t.to_dict() for t in self.exchange.trade_log]).set_index('dt')

    def __update_agents_aum(self):
        for update in self.exchange.agents_aum_updates:
            agent_idx = self.__get_agent_index(update[0])
            # Check if not None because initial seed is not an agent
            if agent_idx:
                self.agents[agent_idx].aum += update[1]
        self.exchange.agents_aum_updates = []


    def __get_agent_index(self,agent_name):
        return next((index for (index, d) in enumerate(self.agents) if d.name == agent_name), None)