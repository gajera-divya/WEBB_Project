# 📈 Stock & Portfolio Dashboard

A powerful interactive dashboard built with **Streamlit** for analyzing individual stocks and multi-asset portfolios. The app offers technical indicator overlays, portfolio performance insights, and portfolio optimization features using modern financial libraries.

---

## ✨ Features

### 📉 Single Stock Analysis
- Fetch historical data using a custom API fetcher
- Plot interactive candlestick charts with volume
- Apply technical indicators:
  - Moving Averages
  - RSI, MACD, Bollinger Bands
  - Stochastic Oscillator, Ichimoku Cloud
  - Fibonacci Levels
- Export data as CSV

### 📊 Portfolio Analysis
- Enter multiple tickers and weights
- View cumulative return and drawdown metrics
- Pie chart of portfolio allocation
- Calculate daily returns, VaR, and max drawdown

### ⚙️ Portfolio Optimization
- Optimize for maximum Sharpe ratio using mean-variance theory
- Visualize:
  - Optimized weights
  - Efficient Frontier
  - Expected return and volatility

### 📊 Correlation Analysis
- Heatmap of correlation matrix between selected assets
- Select chart themes: plotly, dark, ggplot, etc.

---

## ⚡ Tech Stack
- **Python**
- **Streamlit** for the web UI
- **Plotly** for interactive charts
- **Pandas / NumPy** for data manipulation
- **Seaborn / Matplotlib** for advanced visuals 

---

## 📝 File Structure
```bash
.
├── db/market_data.db                       # SQLite database storage
├── app.py                      # Entry point
├── stock_mode.py              # Single stock mode logic
├── portfolio_mode.py          # Portfolio analysis & optimization
├── plot_utils.py              # All charting functions
├── fetcher.py                 # Data retrieval logic
├── technical_indicators.py    # Indicator calculations
├── portfolio_analysis.py      # Portfolio stats and metrics
├── portfolio_optimizer.py     # Optimization + efficient frontier
├── custom_ui.py               # Reusable UI functions and styling
```

## ▶️ Running the App

Install the dependencies and run:
```bash
pip install -r requirements.txt
streamlit run app.py
```


