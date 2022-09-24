import plotly.graph_objects as go
import pandas as pd

def plot_bars(df):
    """Returns a plotly OHLC chart.

    Args:
        df (dataframe): the dataframe containing the OHLCV data created by the simulation.
    """
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