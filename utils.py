import pandas as pd
import numpy as np
import yfinance as yf

def sample_data(start, end, seed=None):
        if seed:
               np.random.seed(seed)
        dates = pd.date_range(start=start, end=end)
        prices = 100 + np.cumsum(np.random.randn(len(dates)))   # Random walk as example prices
        return {"Date": dates, "Close": prices}

def generate_sample_dataframe(data):
        # Create a DataFrame
        if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
        try:
                data.set_index("Date", inplace=True)
        except:
                pass
        return data
        
def fetch_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data
