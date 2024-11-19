from utils import generate_sample_dataframe, sample_data, fetch_data
from ma import Model as Ma
from buy_and_hold import Model as BuyAndHold
from mean_reversion import Model as MeanReversion


# Main function
def main():

    # Generate data
    start = "2020-01-01"
    end = "2023-12-31"
    ticker = "TSLA" # AAPL, MSFT, NVDA

    data = fetch_data(ticker, start, end)
    data = data['Close'] 
    data.columns=['Close']
    #data = sample_data(start, end)
    df = generate_sample_dataframe(data)
    
    # Initialize models
    bah = BuyAndHold(df=df)
    ma = Ma(
        df=df,
        short_window=10, 
        long_window=20
    )
    
    mr = MeanReversion(
        df=df,
        window=20
        )

    # Simulate trade strategy
    result1 = bah.backtest(verbose=False)
    result2 = ma.backtest(verbose=False)
    result3 = mr.backtest(signal_confidence=.95)

    #ma.plot_results()
    #mr.plot_results()
 
    print(f"Buy and hold: {result1}. Ma: {result2}. Mr: {result3}")

# Run the script
if __name__ == "__main__":
    main()