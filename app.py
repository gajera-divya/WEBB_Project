import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from fetcher import get_data
from technical_indicators import (
    add_moving_averages, add_rsi, add_bollinger_bands, add_macd,
    add_stochastic, add_ichimoku, get_fibonacci_levels
)

st.set_page_config(layout="wide")
st.title("📈 Stock & Portfolio App")

mode = st.sidebar.radio("Select Mode", ["Single Stock", "Portfolio"])

# ---------- SIMPLE PLOTLY GRAPH ----------
def plot_price_chart(df, fib_levels, indicators, ticker):
    fig = go.Figure()

    # Close price
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close', line=dict(color='black')))

    # Moving Averages — explicitly selected
    for ma_col in ['MA20', 'MA50', 'MA100', 'MA200']:
        if ma_col in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[ma_col], name=ma_col))

    # Bollinger Bands
    if "BB_High" in df.columns and "BB_Low" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["BB_High"], name="BB High", line=dict(dash='dot')))
        fig.add_trace(go.Scatter(x=df.index, y=df["BB_Low"], name="BB Low", line=dict(dash='dot')))

    # Ichimoku
    if "Ichimoku_A" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["Ichimoku_A"], name="Ichimoku A", line=dict(dash='dot')))
    if "Ichimoku_B" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["Ichimoku_B"], name="Ichimoku B", line=dict(dash='dot')))

    # Fibonacci levels
    if "Fibonacci Levels" in indicators:
        for lvl, val in fib_levels.items():
            fig.add_hline(y=val, line_dash="dot", line_color="gray", annotation_text=f"Fib {lvl}")

    fig.update_layout(
        title=f"{ticker} – Price Chart + Indicators",
        template="plotly_white",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)



def plot_line_chart(df, title):
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col))
    fig.update_layout(title=title, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ---------- SINGLE STOCK MODE ----------
if mode == "Single Stock":
    ticker = st.sidebar.text_input("Ticker", "AAPL").upper()
    start = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end = st.sidebar.date_input("End Date", pd.to_datetime("today"))

    indicators = st.sidebar.multiselect("Indicators", [
        "Moving Averages", "RSI", "Bollinger Bands", "MACD",
        "Stochastic Oscillator", "Ichimoku Cloud", "Fibonacci Levels"
    ])

    if st.sidebar.button("Analyze"):
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

        plot_price_chart(df, fib_levels, indicators, ticker)

        if "MACD" in indicators and "MACD" in df.columns:
            plot_line_chart(df[["MACD", "MACD_Signal"]], "MACD")

        if "RSI" in indicators:
            rsi_cols = [col for col in df.columns if col.startswith("RSI")]
            plot_line_chart(df[rsi_cols], "RSI")

        if "Stochastic Oscillator" in indicators:
            plot_line_chart(df[["Stoch_K", "Stoch_D"]], "Stochastic Oscillator")

# ---------- PORTFOLIO MODE ----------
elif mode == "Portfolio":
    tickers_input = st.sidebar.text_area("Tickers (comma-separated)", "AAPL, MSFT, TSLA")
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    start = st.sidebar.date_input("Start", pd.to_datetime("2023-01-01"))
    end = st.sidebar.date_input("End", pd.to_datetime("today"))

    metrics = st.sidebar.multiselect("Metrics", [
        "Cumulative Returns", "Daily Volatility", "Sharpe Ratio", "Correlation Matrix"
    ])

    if st.sidebar.button("Analyze Portfolio"):
        portfolio_data = {}
        for ticker in tickers:
            try:
                df = get_data(ticker, str(start), str(end))
                df["Date"] = pd.to_datetime(df["Date"])
                df = df.sort_values("Date")
                portfolio_data[ticker] = df
            except Exception as e:
                st.error(f"{ticker}: {e}")

        combined_df = pd.DataFrame()
        for ticker in tickers:
            if ticker in portfolio_data:
                df = portfolio_data[ticker][["Date", "Close"]].rename(columns={"Close": ticker})
                combined_df = pd.merge(combined_df, df, on="Date", how="outer") if not combined_df.empty else df

        if not combined_df.empty:
            combined_df.set_index("Date", inplace=True)
            combined_df = combined_df.sort_index().ffill()

            st.subheader("Portfolio Prices")
            st.plotly_chart(px.line(combined_df, title="Portfolio Close Prices"), use_container_width=True)

            daily_returns = combined_df.pct_change().dropna()

            if "Cumulative Returns" in metrics:
                cumulative = (1 + daily_returns).cumprod()
                st.subheader("Cumulative Returns")
                st.plotly_chart(px.line(cumulative), use_container_width=True)

            volatility = (daily_returns.std() * (252 ** 0.5)).rename("Annualized Volatility")
            sharpe = ((daily_returns.mean() / daily_returns.std()) * (252 ** 0.5)).rename("Sharpe Ratio")
            correlation = daily_returns.corr()

            # Side-by-side columns for Volatility and Sharpe
            if "Daily Volatility" in metrics or "Sharpe Ratio" in metrics:
                col1, col2 = st.columns(2)

                if "Daily Volatility" in metrics:
                    with col1:
                        st.subheader("📊 Annualized Volatility")
                        st.bar_chart(volatility)

                if "Sharpe Ratio" in metrics:
                    with col2:
                        st.subheader("📈 Sharpe Ratios")
                        st.bar_chart(sharpe)

            # Correlation Matrix as Heatmap
            if "Correlation Matrix" in metrics:
                st.subheader("📌 Correlation Matrix (Heatmap)")
                import seaborn as sns
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots()
                sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)

