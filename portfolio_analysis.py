import pandas as pd

def parse_weights(input_str, tickers):
    try:
        if not input_str.strip():
            return {ticker: 1/len(tickers) for ticker in tickers}  # Equal weights

        raw_weights = dict(item.split(":") for item in input_str.split(","))
        weights = {k.strip().upper(): float(v.strip()) for k, v in raw_weights.items()}
        total = sum(weights.values())

        if not all(t in tickers for t in weights):
            return None  # Invalid weights
        return {k: v / total for k, v in weights.items()}  # Normalize
    except:
        return None

def combine_portfolio_data(portfolio_data):
    combined_df = pd.DataFrame()
    for ticker, df in portfolio_data.items():
        df = df[["Date", "Close"]].rename(columns={"Close": ticker})
        combined_df = pd.merge(combined_df, df, on="Date", how="outer") if not combined_df.empty else df
    combined_df.set_index("Date", inplace=True)
    return combined_df.sort_index().ffill()

def calculate_portfolio_metrics(daily_returns, weights_dict):
    weight_series = pd.Series(weights_dict)
    portfolio_daily_returns = daily_returns.mul(weight_series, axis=1).sum(axis=1)
    cumulative = (1 + portfolio_daily_returns).cumprod()
    volatility = portfolio_daily_returns.std() * (252 ** 0.5)
    sharpe = (portfolio_daily_returns.mean() / portfolio_daily_returns.std()) * (252 ** 0.5)
    return portfolio_daily_returns, cumulative, volatility, sharpe
