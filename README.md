# 📈 Streamlit Stock & Portfolio Analysis App

An interactive **Streamlit** web app for **single-stock** and **portfolio-level** financial analysis. This app pulls historical data, applies a wide range of **technical indicators**, and visualizes performance and risk metrics for better investment insights.

---

## 🚀 Features

### 📊 Single Stock Mode
- Fetch and visualize price data from Yahoo Finance
- Apply technical indicators:
  - Moving Averages
  - RSI
  - Bollinger Bands
  - MACD
  - Stochastic Oscillator
  - Ichimoku Cloud
  - Fibonacci Levels
- Interactive price charts with Plotly

### 📁 Portfolio Mode
- Analyze multiple stocks at once
- View:
  - Cumulative Returns
  - Annualized Volatility
  - Sharpe Ratio
  - Correlation Matrix (heatmap)
- Compare performance side-by-side

---

## 🧱 Tech Stack

- **Frontend**: Streamlit
- **Data Sources**: Yahoo Finance via `yfinance`
- **Indicators**: `ta` (Technical Analysis Library)
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Caching & Storage**: SQLite via `fetcher.py`

---

## 📂 Project Structure

