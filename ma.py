import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Model:
    '''
    Moving strategy tries to identify trends in the asset and make decisions based on this. 
    When we notice a positive trend in the short MA compared to long MA we buy and visa versa
    '''
    def __init__(self, df, short_window, long_window, initial_cash=1000):
        # Calculate moving averages
        
        self.short_window = short_window  # Short-term moving average
        self.long_window = long_window  # Long-term moving average
        self.df = df
        self.initial_cash = initial_cash

    def generate_indicators(self):
        self.df["Short_MA"] = self.df["Close"].rolling(window=self.short_window).mean()
        self.df["Long_MA"] = self.df["Close"].rolling(window=self.long_window).mean()

    def generate_signal(self):
        # Generate signals
        self.df["Signal"] = 0
        self.df.loc[(self.df["Short_MA"] > self.df["Long_MA"]) , "Signal"] = 1  # Buy signal
        self.df.loc[self.df["Short_MA"] <= self.df["Long_MA"], "Signal"] = -1  # Sell signal

    def backtest(self, verbose=True):
        currency_holding = self.initial_cash
        asset_holding = 0
        
        self.generate_indicators()
        self.generate_signal()
        self.df["Assets"] = 0
        
        for ind in range(len(self.df.index)):
            
            signal = self.df["Signal"].iloc[ind]
            price = self.df["Close"].iloc[ind]
            if signal == 1:
                # We want to buy
                if currency_holding >= price:
                    currency_holding = currency_holding - price
                    asset_holding += 1

                    if verbose:
                        print("Buying")
                        print(f"Cash: {currency_holding}")
                        print(f"Stock value: {asset_holding * price}")
                        print(f"Total: {currency_holding + (asset_holding * price)}")

            else:
                # We want to sell all
                if asset_holding > 0:
                    currency_holding = currency_holding + (asset_holding * price)
                    asset_holding = 0

                    if verbose:
                        print("Selling")
                        print(f"Cash: {currency_holding}")
                        print(f"Stock value: {asset_holding * price}")
                        print(f"Total: {currency_holding + (asset_holding * price)}")
        
        return currency_holding + (asset_holding * price) 

    def generate_plot(self):
        # Plot the results
        plt.figure(figsize=(14, 7))
        plt.plot(self.df.index, self.df["Close"], label="Close Price", alpha=0.75)
        plt.plot(self.df.index, self.df["Short_MA"], label=f"{self.short_window}-Day MA", linestyle="--", alpha=0.75)
        plt.plot(self.df.index, self.df["Long_MA"], label=f"{self.long_window}-Day MA", linestyle="--", alpha=0.75)
     
    def highlight_signals(self):
        # Highlight buy/sell signals
        buy_signals = self.df[self.df["Signal"] == 1]
        sell_signals = self.df[self.df["Signal"] == -1]
        plt.scatter(buy_signals.index, buy_signals["Close"], label="Buy Signal", marker="^", color="green", alpha=1)
        plt.scatter(sell_signals.index, sell_signals["Close"], label="Sell Signal", marker="v", color="red", alpha=1)

    def generate_labels_and_legend(self):
        # Add labels and legend
        plt.title("Moving Average Crossover Strategy")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(alpha=0.3)

    def plot_results(self):
        self.generate_plot()
        self.highlight_signals()
        plt.show()
    


        
    
    
