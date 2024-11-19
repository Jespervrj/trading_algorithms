import math
import pandas as pd

class Model():
    def __init__(self, df, initial_cash=1000):
        self.df = df
        self.initial_cash = initial_cash

    def backtest(self, verbose=True):
        # Buy and hold
        initial_price = self.df["Close"].iloc[0]
        final_price = self.df["Close"].iloc[-1]
        if verbose:
            print(f"Initial price: {initial_price}")
            print(f"Final price: {final_price}")
        
        value_end = self.initial_cash * final_price/initial_price 
        return value_end