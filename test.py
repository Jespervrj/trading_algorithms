from utils import generate_sample_dataframe, sample_data
from ma import Model as Ma
from buy_and_hold import Model as BuyAndHold
from mean_reversion import Model as MeanReversion

def monte_carlo(interations=1000):
    res1 = 0
    res2 = 0
    res3 = 0
    for i in range(1000):
        # Generate data
        start = "2020-01-01"
        end = "2023-12-31"
        data = sample_data(start, end)
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
        result3, r = mr.backtest(entry_confidence=.95, exit_confidence=0.6)
        
        res1 += result1
        res2 += result2
        res3 += result3
