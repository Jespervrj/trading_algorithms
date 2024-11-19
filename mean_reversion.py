import matplotlib.pyplot as plt
from scipy.stats import norm

class Model():
    '''
    Mean Reversion strategy assumes that prices will revet into the historical mean. 
    This means in practice that when an assets rises quickly, we will sell our position and visa versa
    The makes this strategy a careful approach to market volatility where we might miss out on big winning but might also avoid big losses 
    '''
    def __init__(self, df, window, initial_cash=1000, rsi_low=30, rsi_high=70):
        self.df = df
        self.window = window
        self.initial_cash = initial_cash
        self.rsi_low=rsi_low, 
        self.rsi_high=rsi_high

    # Generate rolling mean, rolling std, and z-score
    def generate_indicators(self):
        self.df['RollingMean'] = self.df['Close'].rolling(window=self.window).mean()
        self.df['RollingStd'] = self.df['Close'].rolling(window=self.window).std()
        self.df['ZScore'] = (self.df['Close'] - self.df['RollingMean']) / self.df['RollingStd']
        return self.df
    
    # <>_conf being a float 0 <= x <= 1  representing the statistical confidence to base signal decisions on
    def generate_thresholds(self, signal_conf):
        signal_threshold = norm.ppf(1 - (1 - signal_conf) / 2)
        
        return signal_threshold

    # Function to calculate Bollinger Bands
    def calculate_bollinger_bands(self, num_std_dev):
        self.df['MA'] = self.df['Close'].rolling(window=self.window).mean()
        self.df['STD'] = self.df['Close'].rolling(window=self.window).std()
        self.df['Upper_Band'] = self.df['MA'] + (self.df['STD'] * num_std_dev)
        self.df['Lower_Band'] = self.df['MA'] - (self.df['STD'] * num_std_dev)

    # Function to calculate RSI
    def calculate_rsi(self):
        delta = self.df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.window).mean()
        rs = gain / loss
        self.df['RSI'] = 100 - (100 / (1 + rs))
        
    # Backtest mean reversion strategy
    def backtest(self, signal_confidence=.95):
        self.generate_indicators()
        signal_threshold = self.generate_thresholds(signal_confidence)
        self.calculate_bollinger_bands(signal_threshold)
        self.calculate_rsi()
        
        self.df['Position'] = 0  # 1 for Buy, -1 for Sell, 0 for Neutral
        self.df.loc[(self.df['Close'] < self.df['Lower_Band']) & (self.df['RSI'] < self.rsi_low), 'Position'] = 1  # Buy
        self.df.loc[(self.df['Close'] > self.df['Upper_Band']) & (self.df['RSI'] > self.rsi_high), 'Position'] = -1  # Sell
        
        # Calculate returns
        self.df['DailyReturn'] = self.df['Close'].pct_change()
        self.df['StrategyReturn'] = self.df['Position'].shift(1) * self.df['DailyReturn']
        
        # Simulate portfolio value
        self.df['PortfolioValue'] = (1 + self.df['StrategyReturn']).cumprod() * self.initial_cash
        return self.df['PortfolioValue'].iloc[-1]
    
    # Plot results
    def plot_results(self):
        plt.figure(figsize=(14, 7))
        
        # Price and rolling mean
        plt.subplot(2, 1, 1)
        plt.plot(self.df['Close'], label='Close Price', color='blue')
        plt.plot(self.df['RollingMean'], label='Rolling Mean', color='orange')
        plt.fill_between(self.df.index, self.df['RollingMean'] - self.df['RollingStd'], 
                        self.df['RollingMean'] + self.df['RollingStd'], color='lightgray', alpha=0.5)
        plt.legend()
        plt.title('Price and Rolling Statistics')
        
        # Portfolio value
        plt.subplot(2, 1, 2)
        plt.plot(self.df['PortfolioValue'], label='Strategy Portfolio Value', color='green')
        plt.axhline(self.initial_cash, linestyle='--', color='red', label='Initial Capital')
        plt.legend()
        plt.title('Portfolio Value Over Time')
        
        plt.tight_layout()
        plt.show()