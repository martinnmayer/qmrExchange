
# avocardio 17-10-2022
# SmartMarketTaker strategies

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class MovingAverageCrossover():
    def __init__(self, short_window, long_window, debug=False):
        self.short_window = short_window
        self.long_window = long_window
        self.buy_probability = 0
        self.sell_probability = 0
        self.debug = debug
        self.history = []

    def evaluate(self, price_history):
        self.history.append(price_history)

        history = pd.DataFrame(self.history, dtype='float64').iloc[:, 0]
        
        if self.debug == True:
            history = pd.DataFrame(price_history, dtype='float64').iloc[:, 0]

        weights = [self.buy_probability, self.sell_probability, abs(round(1 - self.buy_probability - self.sell_probability, 2))]

        if len(history) < self.long_window:
            return weights

        # Calculate the short and long moving averages
        short_mavg = history.rolling(window=self.short_window, min_periods=1, center=False).mean()
        long_mavg = history.rolling(window=self.long_window, min_periods=1, center=False).mean()

        if self.debug == True:
            plt.figure(figsize=(20, 10))
            plt.subplot(2, 1, 1)
            plt.plot(short_mavg, label='Short Moving Average')
            plt.plot(long_mavg, label='Long Moving Average')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(history, label='Price History')
            plt.legend()
            plt.show()

        # If the short moving average crosses the long moving average, buy the stock
        if short_mavg[len(short_mavg) -1] > long_mavg[len(long_mavg)-1]:
            if short_mavg[len(short_mavg)-2] > long_mavg[len(long_mavg)-2]:
                if self.debug == True:
                    print(len(history), weights)
                return weights

            buy_probability = 0.9
            sell_probability = 0.05

            weights = [buy_probability, sell_probability, abs(round(1 - buy_probability - sell_probability, 2))]

        # Else, if the long moving average is greater than the short moving average, sell the stock
        elif short_mavg[len(short_mavg)-1] < long_mavg[len(long_mavg)-1]:
            if short_mavg[len(short_mavg)-2] < long_mavg[len(long_mavg)-2]:
                if self.debug == True:
                    print(len(history), weights)
                return weights

            buy_probability = 0.05
            sell_probability = 0.9

            weights = [buy_probability, sell_probability, abs(round(1 - buy_probability - sell_probability, 2))]

        if self.debug == True:
            print(len(history), weights)
        return weights