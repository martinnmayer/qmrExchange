![GitHub Repo stars](https://img.shields.io/github/stars/QMResearch/qmrExchange?style=social)
![GitHub](https://img.shields.io/github/license/QMResearch/qmrExchange)
![Twitter URL](https://img.shields.io/twitter/url?url=https%3A%2F%2Ftwitter.com%2FQMRMayer)
![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC_QUSm4desE-V3o68ovcZWg)

<!-- <p align="center" background-color='red' width="100%">
    <img width="33%" src="https://www.qmr.ai/wp-content/uploads/2022/03/qmr_logo.png">
</p> -->

# 🚀qmrExchange🚀
**[🌐 Company Website](https://www.qmr.ai) / [🗎 Documentation](https://qmresearch.github.io/qmrExchange/source/index.html)**  


- [🚀qmrExchange🚀](#qmrexchange)
  - [qmrExchange Overview](#qmrexchange-overview)
  - [Use cases for qmrExchange](#use-cases-for-qmrexchange)
  - [Potential Research Topics with qmrExchange](#potential-research-topics-with-qmrexchange)
    - [Market-Making Algorithms](#market-making-algorithms)
    - [Optimal Execution Algorithms](#optimal-execution-algorithms)
    - [Adversarial Algorithms](#adversarial-algorithms)
  - [Basig usage of qmrExchange](#basig-usage-of-qmrexchange)
    - [Import required libraries](#import-required-libraries)
    - [Declare basic parameters for the simulation](#declare-basic-parameters-for-the-simulation)
    - [Instantiate a Simulator](#instantiate-a-simulator)
    - [Add trading agents](#add-trading-agents)
    - [Run the simulation](#run-the-simulation)
    - [Plot the results](#plot-the-results)
  - [Project Documentation](#project-documentation)

## qmrExchange Overview
The qmrExchange project is an open-source financial markets exchange simulator that realistically mimics all the main components of modern trading venues. It allows us to test and quantify the behavior of different agents in a laboratory and isolated environment without the high noise-to-signal ratio that is otherwise unavoidable in live settings.
By creating a completely functioning trading venue whose access is only granted to a finite and known number of agents or trading algorithms, qmrExchange enables analyzing causation and quantifying the impact of each agent in a way that is otherwise unfeasible.


## Use cases for qmrExchange
The implementation of qmrExchange closely resembles the backend of most FIFO trading exchanges and replicates the market microstructure of the most popular venues. As a consequence, the system is especially useful for:
- Teaching, studying, and researching topics related to market microstructure and algorithmic trading.
- Estimating the impact of new regulations and how they affect each type of agent
- Implementing and analyzing market-making and high-frequency trading algorithms
-	Creating algorithmic trading challenges and tournaments both for university students and industry professionals alike


## Potential Research Topics with qmrExchange
Due to its precise resemblance to real-life trading venues, qmrExchange is perfectly suited for researching plenty of topics, such as:
### Market-Making Algorithms
By implementing a finite number of market participants, such as institutional investors and indicator-based trading algorithms, market-making algorithms can be studied. For a rigorous implementation, refer to Avellaneda & Stoikov (2008)
### Optimal Execution Algorithms
qmrExchange is an ideal environment for implementing, testing, and quantifying the market impact of different execution algorithms. By creating a laboratory, sterile and isolated venue whose market participants and their behavior is known with absolute certainty, optimal execution algorithms can be easily implemented, researched, and calibrated. For a formal presentation of such an algorithm, refer to Almgren & Chriss (1999).
### Adversarial Algorithms
Much like in the spirit of General Adversarial Networks and Game Theory, an implementation where a profit-maximizing agent’s behavior is calibrated based on the predefined behavior of other market participants is possible. For an interesting introduction to game theory applied to financial markets, refer to Allen & Morris (2022).

## Basig usage of qmrExchange
### Import required libraries

```python
from source.qmr_exchange import Exchange
from random import Random
from source.qmr_exchange import Exchange, Simulator
from source.agents import RandomMarketTaker, NaiveMarketMaker
from datetime import datetime
```

### Declare basic parameters for the simulation
qmrExchange allows for simulating multiple tickers at once, for statistical arbitrage and high-frequency-trading simulations. In the present case, we simulate 2 weeks worth of 1 minute data (24/7 trading).

```python
from_date = datetime(2022,1,1)
to_date = datetime(2022,1,15)
time_interval = 'minute'
tickers = ['XYZ']
```

### Instantiate a Simulator

```python
sim = Simulator(from_date, to_date,time_interval)
sim.exchange.create_asset(tickers[0])
```

### Add trading agents
- We add a naive market maker that creates both buy and sell orders in each period. It quotes buy and sell prices based on the last traded price and the specified spread percentage.
- We add a market taker that randomly buys and sells (based on the defined probabilities) on each period by means of market ordes (hence the word 'taker').


```python
mm = NaiveMarketMaker(name='market_maker', tickers=tickers, aum=1_000, spread_pct=0.005, qty_per_order=4)
sim.add_agent(mm)

mt = RandomMarketTaker(name='market_taker', tickers=tickers, aum=1_000, prob_buy=.2, prob_sell=.2, qty_per_order=1,seed=42)
sim.add_agent(mt)
```

### Run the simulation

```python
sim.run()
```

Retrieve all executed trades of our simulation

```python
sim.trades
```

```
| dt                  | ticker   |   qty |   price | buyer        | seller       |
|:--------------------|:---------|------:|--------:|:-------------|:-------------|
| 2022-01-01 00:00:00 | XYZ      |     1 |  100    | init_seed    | init_seed    |
| 2022-01-01 00:04:00 | XYZ      |     1 |  100.25 | market_taker | market_maker |
| 2022-01-01 00:10:00 | XYZ      |     1 |  100    | market_maker | market_taker |
| 2022-01-01 00:11:00 | XYZ      |     0 |   99.75 | market_maker | market_taker |
| 2022-01-01 00:13:00 | XYZ      |     0 |   99.5  | market_maker | market_taker |
| 2022-01-01 00:14:00 | XYZ      |     0 |   99.25 | market_maker | market_taker |
| 2022-01-01 00:15:00 | XYZ      |     1 |   99.5  | market_taker | market_maker |
| 2022-01-01 00:16:00 | XYZ      |     1 |   99.75 | market_taker | market_maker |
| 2022-01-01 00:18:00 | XYZ      |     2 |   99.5  | market_maker | market_taker |
| 2022-01-01 00:19:00 | XYZ      |     0 |   99.25 | market_maker | market_taker |
| 2022-01-01 00:20:00 | XYZ      |     0 |   99    | init_seed    | market_taker |
| 2022-01-01 00:21:00 | XYZ      |     1 |   99.25 | market_taker | market_maker |
| 2022-01-01 00:22:00 | XYZ      |     1 |   99    | init_seed    | market_taker |
| 2022-01-01 00:24:00 | XYZ      |     1 |   99.25 | market_taker | market_maker |
| 2022-01-01 00:25:00 | XYZ      |     1 |   99.5  | market_taker | market_maker |
| 2022-01-01 00:27:00 | XYZ      |     2 |   99.25 | market_maker | market_taker |
| 2022-01-01 00:28:00 | XYZ      |     1 |   99.5  | market_taker | market_maker |
| 2022-01-01 00:30:00 | XYZ      |     1 |   99.25 | market_maker | market_taker |
| 2022-01-01 00:38:00 | XYZ      |     0 |   99    | market_maker | market_taker |
| 2022-01-01 00:39:00 | XYZ      |     0 |   98.75 | market_maker | market_taker |
```

Group asset price in fixed 15 Minute OHLCV Bars

```python
df_15min = sim.get_price_bars(ticker=tickers[0],bar_size='15Min')
df_15min
```

```
Output:

| dt                  |   open |   high |   low |   close |   volume |
|:--------------------|-------:|-------:|------:|--------:|---------:|
| 2022-01-01 00:00:00 | 100    | 100.25 | 99.25 |   99.25 |        3 |
| 2022-01-01 00:15:00 |  99.5  |  99.75 | 99    |   99.5  |       11 |
| 2022-01-01 00:30:00 |  99.25 |  99.25 | 98.5  |   98.75 |        2 |
| 2022-01-01 00:45:00 |  98.5  |  98.5  | 98    |   98.24 |        2 |
| 2022-01-01 01:00:00 |  97.99 |  98.73 | 97.99 |   98.23 |        9 |
| 2022-01-01 01:15:00 |  98.48 |  99.23 | 98.48 |   99.23 |       11 |
| 2022-01-01 01:30:00 |  99.48 | 100.23 | 99.48 |   99.73 |        9 |
| 2022-01-01 01:45:00 |  99.48 |  99.48 | 98.98 |   98.98 |        2 |
| 2022-01-01 02:00:00 |  99.23 |  99.73 | 98.73 |   99.73 |        9 |
| 2022-01-01 02:15:00 |  99.48 |  99.48 | 98.73 |   98.73 |        5 |
| 2022-01-01 02:30:00 |  98.98 |  99.73 | 98.98 |   99.23 |       10 |
| 2022-01-01 02:45:00 |  98.98 |  99.98 | 98.98 |   99.73 |        8 |
| 2022-01-01 03:00:00 |  99.98 |  99.98 | 99.73 |   99.73 |        4 |
| 2022-01-01 03:15:00 |  99.48 |  99.73 | 99.48 |   99.73 |        5 |
| 2022-01-01 03:30:00 |  99.48 |  99.73 | 98.98 |   99.73 |        4 |
| 2022-01-01 03:45:00 |  99.48 |  99.73 | 99.23 |   99.23 |        5 |
| 2022-01-01 04:00:00 |  99.48 |  99.73 | 99.23 |   99.73 |        9 |
| 2022-01-01 04:15:00 |  99.98 |  99.98 | 99.23 |   99.48 |        7 |
| 2022-01-01 04:30:00 |  99.23 |  99.73 | 98.98 |   99.73 |        5 |
| 2022-01-01 04:45:00 |  99.98 | 100.23 | 99.73 |   99.73 |        7 |
```

Retrieve a dataframe of an agents holding at each period of time
```python
mt_holdings = sim.get_portfolio_history('market_taker')
mm_holdings = sim.get_portfolio_history('market_maker')
```

```
| dt                  |    XYZ |    cash |     aum |
|:--------------------|-------:|--------:|--------:|
| 2022-01-01 00:00:00 |   0    | 1000    | 1000    |
| 2022-01-01 00:01:00 |   0    | 1000    | 1000    |
| 2022-01-01 00:02:00 |   0    | 1000    | 1000    |
| 2022-01-01 00:03:00 |   0    | 1000    | 1000    |
| 2022-01-01 00:04:00 | 100.25 |  899.75 | 1000    |
| 2022-01-01 00:05:00 | 100.25 |  899.75 | 1000    |
| 2022-01-01 00:06:00 | 100.25 |  899.75 | 1000    |
| 2022-01-01 00:07:00 | 100.25 |  899.75 | 1000    |
| 2022-01-01 00:08:00 | 100.25 |  899.75 | 1000    |
| 2022-01-01 00:09:00 | 100.25 |  899.75 | 1000    |
| 2022-01-01 00:10:00 |   0    |  999.75 |  999.75 |
| 2022-01-01 00:11:00 |   0    |  999.75 |  999.75 |
| 2022-01-01 00:12:00 |   0    |  999.75 |  999.75 |
| 2022-01-01 00:13:00 |   0    |  999.75 |  999.75 |
| 2022-01-01 00:14:00 |   0    |  999.75 |  999.75 |
| 2022-01-01 00:15:00 |  99.5  |  900.25 |  999.75 |
| 2022-01-01 00:16:00 | 199.5  |  800.5  | 1000    |
| 2022-01-01 00:17:00 | 199.5  |  800.5  | 1000    |
| 2022-01-01 00:18:00 |   0    |  999.5  |  999.5  |
| 2022-01-01 00:19:00 |   0    |  999.5  |  999.5  |
```

### Plot the results

Create a candlestick chart for the asset price.

```python
from source.helpers import plot_bars
df_15min = sim.get_price_bars(ticker=tickers[0], bar_size='15Min')
plot_bars(df_15min)
```
![image info](misc/plot.png)

Plot the assets under management of each agent

```python
import plotly.express as px
import pandas as pd

df_plot = pd.DataFrame()
df_plot['Market Maker'] = mm_holdings['aum']
df_plot['Market Taker'] = mt_holdings['aum']
fig = px.line(df_plot,labels={'variable':'Agents','value':'Assets Under Management','dt':'Date'})
fig.show()
```
![image info](misc/aum_plot.png)




## Project Documentation
In order to further explore the project, take a look at our documentation:
[🗎 Documentation](https://qmresearch.github.io/qmrExchange/source/index.html)

