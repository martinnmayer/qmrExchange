import plotly.graph_objects as go
import pandas as pd

def plot_bars(df):
    fig = go.Figure(data=go.Ohlc(x=df.index,
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close']))
    fig.update_layout(
        autosize=False,
        width=1000,
        height=800)
    fig.show()