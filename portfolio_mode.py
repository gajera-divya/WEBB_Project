import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime
from fetcher import get_data
from portfolio_analysis import (
    parse_weights, combine_portfolio_data, calculate_portfolio_metrics
)
from portfolio_optimizer import optimize_portfolio, efficient_frontier
from plot_utils import plot_correlation_heatmap

def run_portfolio_mode():
    tickers_input = st.sidebar.text_area("Tickers (comma-separated)", "AAPL, MSFT, TSLA")
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
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

    with st.sidebar.expander("Portfolio Settings"):
        weights_input = st.text_input("Custom Weights (e.g., AAPL:0.5, MSFT:0.3, TSLA:0.2)", "")
        investment_years = st.slider("Investment Duration (Years)", 0.25, 5.0, 1.0, step=0.25)

    if st.sidebar.button("Analyze Portfolio") and tickers:
        portfolio_data = {}
        for ticker in tickers:
            try:
                df = get_data(ticker, str(start), str(end))
                df["Date"] = pd.to_datetime(df["Date"])
                portfolio_data[ticker] = df.sort_values("Date")
            except Exception as e:
                st.error(f"{ticker}: {e}")

        if not portfolio_data:
            st.error("No valid data retrieved. Please check tickers or date range.")
            return

        weights = parse_weights(weights_input, tickers)
        if weights is None:
            st.warning("Invalid weights input. Defaulting to equal weights.")
            weights = {ticker: 1 / len(tickers) for ticker in tickers}

        combined_df = combine_portfolio_data(portfolio_data)
        daily_returns = combined_df.pct_change().dropna()
        cumulative = (1 + daily_returns).cumprod()

        portfolio_daily_returns, portfolio_cum_returns, \
            portfolio_volatility, _ = calculate_portfolio_metrics(
                daily_returns, weights
            )

        mean_returns = daily_returns.mean() * 252
        cov_matrix = daily_returns.cov() * 252

        weighted_returns = daily_returns.mul(pd.Series(weights), axis=1).sum(axis=1)
        portfolio_cum = (1 + weighted_returns).cumprod()

        tabs = st.tabs([
            "\U0001F4C8 Prices", 
            "\U0001F4CA Performance",
            "\u2699\ufe0f Optimization", 
            "\U0001F4C9 Correlation"
        ])

        # Prices Tab
        with tabs[0]:
            st.subheader("Portfolio Close Prices")
            st.plotly_chart(px.line(combined_df, title="Portfolio Close Prices"),
                            use_container_width=True)
            st.download_button("\U0001F4C5 Download Data", combined_df.to_csv().encode(),
                               "portfolio_data.csv", "text/csv")

        # Performance Tab
        with tabs[1]:
            st.subheader("\U0001F4C8 Cumulative Returns (%)")
            fig = go.Figure()
            for ticker in tickers:
                fig.add_trace(go.Scatter(
                    x=portfolio_cum.index,
                    y=(cumulative[ticker] - 1) * 100,
                    mode="lines", name=ticker
                ))
            fig.add_trace(go.Scatter(
                x=portfolio_cum.index, y=(portfolio_cum - 1) * 100,
                mode="lines+markers", name="Portfolio",
                line=dict(color="black", dash="dot"),
                marker=dict(symbol="diamond", size=4)
            ))
            fig.update_layout(
                yaxis_title="Cumulative Return (%)",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)

            peak = portfolio_cum.cummax()
            drawdown = (portfolio_cum - peak) / peak
            max_drawdown = drawdown.min()
            var_95 = weighted_returns.quantile(0.05)

            col1, col2 = st.columns(2)
            col1.metric("\U0001F4C9 Max Drawdown", f"{max_drawdown:.2%}")
            col2.metric("\u26A0\ufe0f 95% VaR (1D)", f"{var_95:.2%}")

            st.subheader("\U0001F4C8 Asset Allocation")
            fig = px.pie(
                names=list(weights.keys()), 
                values=list(weights.values()),
                title="Portfolio Weights"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Optimization Tab
        with tabs[2]:
            st.subheader("⚙️ Portfolio Optimization")

            opt_result = optimize_portfolio(mean_returns, cov_matrix)
            opt_weights = pd.Series(opt_result.x, index=mean_returns.index)

            opt_return = np.dot(opt_weights, mean_returns)
            opt_risk = np.sqrt(np.dot(opt_weights.T, np.dot(cov_matrix, opt_weights)))

            scaled_return = opt_return * investment_years
            scaled_risk = opt_risk * np.sqrt(investment_years)

            opt_returns_series = daily_returns @ opt_weights
            opt_var = opt_returns_series.quantile(0.05)
            opt_cvar = opt_returns_series[opt_returns_series <= opt_var].mean()

            col1, col2 = st.columns(2)
            col1.metric("📈 Projected Return", f"{scaled_return:.2%}")
            col2.metric("📉 Expected Volatility", f"{scaled_risk:.2%}")

            col3, col4 = st.columns(2)
            col3.metric("⚠️ VaR (95%)", f"{opt_var:.2%}")
            col4.metric("🔻 CVaR (95%)", f"{opt_cvar:.2%}")

            # Show optimal weights before efficient frontier
            st.subheader("📊 Optimal Weights")
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(
                    names=opt_weights.index, 
                    values=opt_weights.values,
                    title="Optimized Portfolio Weights", 
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### Allocation Breakdown")
                st.dataframe(pd.DataFrame({
                    "Asset": opt_weights.index,
                    "Weight": opt_weights.values
                }).set_index("Asset").style.format({"Weight": "{:.2%}"}))

            st.subheader("📈 Efficient Frontier")
            frontier_df = efficient_frontier(mean_returns, cov_matrix)
            fig = px.scatter(
                frontier_df, x="Risk", y="Return", color="Sharpe",
                title="Efficient Frontier"
            )
            fig.add_scatter(
                x=[opt_risk], y=[opt_return], mode="markers+text",
                name="Optimal", marker=dict(color="red", size=10),
                text=["Optimal"], textposition="top center"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Correlation Tab
        with tabs[3]:
        
            st.subheader("📊 Correlation Matrix")
            corr_matrix = daily_returns.corr()
            corr_fig = plot_correlation_heatmap(corr_matrix, chart_style="plotly_white")
            st.plotly_chart(corr_fig, use_container_width=True)