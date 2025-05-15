# stock_mode.py
import streamlit as st
import pandas as pd
from fetcher import get_data
import datetime
from technical_indicators import (
    add_moving_averages, add_rsi, add_bollinger_bands,
    add_macd, add_stochastic, add_ichimoku, get_fibonacci_levels
)

from plot_utils import plot_price_chart, plot_indicators_with_price, plot_line_chart

def run_single_stock_mode():
    ticker = st.sidebar.text_input("Ticker", "AAPL").upper()
    start = st.sidebar.date_input(
        "Start Date", 
        value=datetime.date(2005, 1, 1), 
        min_value=datetime.date(1990, 1, 1), 
        max_value=datetime.date.today()
    )

    end = st.sidebar.date_input(
        "End Date", 
        value=datetime.date.today(), 
        min_value=datetime.date(1990, 1, 1), 
        max_value=datetime.date.today()
    )

    with st.sidebar.expander("Technical Indicators"):
        indicators = st.multiselect("Select Indicators", [
            "Moving Averages", "RSI", "Bollinger Bands", "MACD",
            "Stochastic Oscillator", "Ichimoku Cloud", "Fibonacci Levels"
        ])


    if st.sidebar.button("Analyze"):
        try:
            df = get_data(ticker, str(start), str(end))
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)

            if "Moving Averages" in indicators:
                df = add_moving_averages(df)
            if "RSI" in indicators:
                df = add_rsi(df)
            if "Bollinger Bands" in indicators:
                df = add_bollinger_bands(df)
            if "MACD" in indicators:
                df = add_macd(df)
            if "Stochastic Oscillator" in indicators:
                df = add_stochastic(df)
            if "Ichimoku Cloud" in indicators:
                df = add_ichimoku(df)
            fib_levels = get_fibonacci_levels(df) if "Fibonacci Levels" in indicators else {}

            tabs = st.tabs(["\U0001F4C9 Price Chart", "\U0001F4CA Indicators"])

            with tabs[0]:
                plot_price_chart(df, ticker)
                st.download_button("\U0001F4C5 Download Data", df.to_csv().encode(),
                                   f"{ticker}_data.csv", "text/csv")

            with tabs[1]:
                plot_indicators_with_price(df, indicators, fib_levels, ticker)

                if "MACD" in indicators and "MACD" in df.columns:
                    plot_line_chart(df[["MACD", "MACD_Signal"]], "MACD")

                if "RSI" in indicators:
                    rsi_cols = [col for col in df.columns if col.startswith("RSI")]
                    plot_line_chart(df[rsi_cols], "RSI")

                if "Stochastic Oscillator" in indicators:
                    plot_line_chart(df[["Stoch_K", "Stoch_D"]], "Stochastic Oscillator")

        except Exception as e:
            st.error(f"Error loading {ticker}: {e}")
