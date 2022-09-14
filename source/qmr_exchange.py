from datetime import datetime
from decimal import Decimal
from typing import List
import pandas as pd
from enum import Enum


class OrderSide(Enum):
    BUY = 'buy'
    SELL = 'sell'


class LimitOrder():
    def __init__(self, ticker, price, qty, creator, side):
        self.ticker: str = ticker
        self.price: Decimal = price
        self.type: OrderSide = side
        self.qty: int = qty
        self.creator: str = creator
        self.dt: datetime = datetime.now()

    def to_dict(self):
        return {
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
        return {
            'bids': pd.DataFrame.from_records([b.to_dict() for b in self.bids]),
            'asks': pd.DataFrame.from_records([a.to_dict() for a in self.asks])
        }


class Trade():
    def __init__(self, ticker, qty, price, buyer, seller, dt=None):
        dt = dt if dt else datetime.now()
        self.ticker = ticker
        self.qty = qty
        self.price = price
        self.buyer = buyer
        self.seller = seller
        self.dt = dt

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
    def __init__(self):
        self.books = {}
        self.trade_log: List[Trade] = []

    def __str__(self):
        return ', '.join(ob for ob in self.books)

    def create_asset(self, ticker: str, seed_price=100, seed_bid=None, seed_ask=None):
        self.books[ticker] = OrderBook(ticker)
        seed_bid = seed_bid if seed_bid else seed_price * 0.99
        seed_ask = seed_ask if seed_ask else seed_price * 1.01
        self._process_trade(ticker, 1, seed_price, 'init_seed', 'init_seed',)
        self.limit_buy(ticker, seed_bid, 1, 'init_seed')
        self.limit_sell(ticker, seed_ask, 1, 'init_seed')

    def get_order_book(self, ticker: str):
        return self.books[ticker]

    def _process_trade(self, ticker, qty, price, buyer, seller):
        self.trade_log.append(
            Trade(ticker, qty, price, buyer, seller)
        )

    def get_latest_trade(self, ticker):
        """Returns the latest trade of a given ticker

        Args:
            ticker (_type_): _description_

        Returns:
            _type_: _description_
        """
        return next(trade for trade in self.trade_log[::-1] if trade.ticker == ticker)

    def get_trades(self, ticker):
        return pd.DataFrame.from_records([t.to_dict() for t in self.trade_log if t.ticker == ticker]).set_index('dt')

    def get_quotes(self, ticker):
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
        new_order = LimitOrder(ticker, price, qty, creator, OrderSide.BUY)
        self.books[ticker].bids.insert(queue, new_order)
        return new_order

    def limit_sell(self, ticker: str, price: float, qty: int, creator: str):
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
        new_order = LimitOrder(ticker, price, qty, creator, OrderSide.SELL)
        self.books[ticker].asks.insert(queue, new_order)
        return new_order

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
