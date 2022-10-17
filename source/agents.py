from .qmr_exchange import Agent, Simulator
import random

class RandomMarketTaker(Agent):
    def __init__(self,name,tickers, aum=10_000,prob_buy=.2,prob_sell=.2,qty_per_order=1,seed=None):
        Agent.__init__(self, name, tickers, aum)
        if  prob_buy + prob_sell> 1:
            raise ValueError("Sum of probabilities cannot be greater than 1.") 
        self.prob_buy = prob_buy
        self.prob_sell = prob_sell
        self.qty_per_order = qty_per_order
        self.tickers
        self.aum = aum

        # Allows for setting a different independent seed to each instance
        self.random = random
        if seed is not None:
            self.random.seed = seed

    
    def next(self):
        for ticker in self.tickers:
            action = random.choices(
                ['buy','close',None], weights=[self.prob_buy, self.prob_sell, 1 - self.prob_buy - self.prob_sell])[0]
            if action == 'buy':
                self.market_buy(ticker,self.qty_per_order)
            elif action == 'close':
                self.exchange.market_sell(ticker,self.get_position(ticker),self.name)


class SmartMarketTaker(Agent):
    def __init__(self,name,tickers, aum=10_000, strategy=None, qty_per_order=1, seed=None):
        Agent.__init__(self, name, tickers, aum)

        if strategy == None:
            raise ValueError("This is a SmartMarketTaker, strategy cannot be None. Use NaiveMarketMaker instead.")

        self.strategy = strategy
        self.qty_per_order = qty_per_order
        self.tickers
        self.aum = aum

        # Allows for setting a different independent seed to each instance
        self.random = random
        if seed is not None:
            self.random.seed = seed

    
    def next(self):
        for ticker in self.tickers:
            
            # Get current price history
            ticker_history = self.exchange.get_price_bars(ticker=ticker)['close'][0]
            # Use strategy to determine action
            weights = self.strategy.evaluate(ticker_history)

            action = random.choices(
                ['buy','close',None], weights=weights)[0]
            if action == 'buy':
                self.market_buy(ticker,self.qty_per_order)
            elif action == 'close':
                self.exchange.market_sell(ticker,self.get_position(ticker),self.name)


class NaiveMarketMaker(Agent):
    def __init__(self, name, tickers, aum, spread_pct=.005, qty_per_order=1):
        Agent.__init__(self, name, tickers, aum)
        self.qty_per_order = qty_per_order
        self.tickers = tickers
        self.spread_pct = spread_pct
        self.aum = aum

    def next(self):
        for ticker in self.tickers:
            price = self.exchange.get_latest_trade(ticker).price
            self.cancel_all_orders(ticker)
            self.limit_buy(ticker, price * (1-self.spread_pct/2), qty=self.qty_per_order)
            self.limit_sell(ticker, price * (1+self.spread_pct/2), qty=self.qty_per_order)