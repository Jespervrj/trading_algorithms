# GENERAL INFORMATION
This project implements statistical tools to illustrate how to use various trading strategies on assets

## Trading strategies used
* Buy and hold  
* Trend following
* Mean reversion  

### Buy and hold
This is merely a benchmark for the the latter strategies. The strategy simply buys the assets on the initial date and holds until end

### Trend following
This strategy tried to identify trends in the market by leveraging a short term and a long terms moving average. If the short terms moving average is different from the long term moving average we assume a trend and generates a buy/sell signal based on this

### Mean Reversion
Assuming market volatility will converge to the historical mean, this strategy applies the RSI and Boillinger Bnads to produce buy / sell signals

## Setup
To create the project I am using the following commands

Create virtual env
`python3 -m venv .venv`

Activate venv
`source .venv/bin/activate`

Update pip
`python3 -m pip install --upgrade pip`

Install packages (Numpy, Pandas, Matplotlib, Yfinance)
`pip install -r requirements.txt`

## Run
To backtest run
`python3 -m main`

The main file allows for different tickers as well as sample data
Furthermore we can plot results by using the 
`model.plot_results()`


