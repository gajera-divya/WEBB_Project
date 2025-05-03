# 📈 Technical Analysis & Portfolio Web App

A comprehensive **Streamlit web application** for performing **technical analysis** on individual stocks and evaluating **portfolio performance** using real-time market data from Yahoo Finance. The app includes a broad suite of technical indicators, interactive charts, and portfolio statistics.

---

## 🚀 Features

### 📊 Single Stock Analysis
- Pulls stock data via **Yahoo Finance**
- Applies key technical indicators:
  - Moving Averages (MA)
  - Relative Strength Index (RSI)
  - Bollinger Bands
  - MACD
  - Stochastic Oscillator
  - Ichimoku Cloud
  - Fibonacci Levels
- Visualizes data with interactive Plotly charts

### 📁 Portfolio Analysis
- Input multiple stock tickers
- View:
  - Cumulative Returns
  - Annualized Volatility
  - Sharpe Ratio
  - Correlation Matrix (heatmap)
- Compare performance side by side

---

## 🧱 Project Structure

```bash
technical-analysis-app/
├── app.py                      # Main Streamlit app
├── fetcher.py                  # Handles data download & caching (e.g., via SQLite)
├── technical_indicators.py     # All technical indicator functions (ta, pandas-based)
├── requirements.txt            # List of required Python libraries
├── README.md                   # Project documentation
├── database.db                 # SQLite database for local caching (auto-generated)
