from ta.trend import MACD
from ta.momentum import StochasticOscillator
from ta.trend import IchimokuIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def add_moving_averages(df, windows=[20, 50]):
    for window in windows:
        df[f"MA{window}"] = df["Close"].rolling(window=window).mean()
    return df

def add_bollinger_bands(df, window=20, std_dev=2):
    bb = BollingerBands(close=df["Close"], window=window, window_dev=std_dev)
    df["BB_High"] = bb.bollinger_hband()
    df["BB_Low"] = bb.bollinger_lband()
    df["BB_Mid"] = bb.bollinger_mavg()
    return df

def add_rsi(df, window=14):
    rsi = RSIIndicator(close=df["Close"], window=window)
    df[f"RSI_{window}"] = rsi.rsi()
    return df

def add_ichimoku(df, tenkan=9, kijun=26, senkou=52):
    ichi = IchimokuIndicator(high=df["High"], low=df["Low"],
                             window1=tenkan, window2=kijun, window3=senkou)
    df["Ichimoku_A"] = ichi.ichimoku_a()
    df["Ichimoku_B"] = ichi.ichimoku_b()
    return df

def add_stochastic(df, window=14, smooth_k=3, smooth_d=3):
    stoch = StochasticOscillator(high=df["High"], low=df["Low"], close=df["Close"],
                                  window=window, smooth_window=smooth_k)
    df["Stoch_K"] = stoch.stoch()
    df["Stoch_D"] = stoch.stoch_signal()
    return df

def add_macd(df, fast=12, slow=26, signal=9):
    macd = MACD(close=df["Close"], window_fast=fast, window_slow=slow, window_sign=signal)
    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()
    df["MACD_Diff"] = macd.macd_diff()
    return df

def get_fibonacci_levels(df):
    max_price = df["Close"].max()
    min_price = df["Close"].min()
    diff = max_price - min_price
    levels = [0.0, 0.236, 0.382, 0.5, 0.618, 1.0]
    return {f"{int(lvl*100)}%": max_price - lvl * diff for lvl in levels}
