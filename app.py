# app.py
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

from custom_ui import (
    apply_custom_styling, create_main_header
)
from stock_mode import run_single_stock_mode
from portfolio_mode import run_portfolio_mode


# ------------------ Page Config ------------------
st.set_page_config(layout="wide", page_title="\U0001F4C8 Stock & Portfolio Dashboard")
apply_custom_styling()
create_main_header("\U0001F4CA Stock & Portfolio Dashboard")

mode = st.sidebar.radio("Select Mode", ["Single Stock", "Portfolio"])

# ------------------ Charting Functions ------------------

def plot_price_chart(df, ticker):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03,
        row_heights=[0.75, 0.25], specs=[[{"type": "candlestick"}], [{"type": "bar"}]]
    )

    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name='Price',
        increasing_line_color='green', decreasing_line_color='red',
        showlegend=False
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=df.index, y=df['Volume'], name='Volume',
        marker_color='rgba(0, 0, 200, 0.85)', showlegend=False
    ), row=2, col=1)

    fig.update_layout(
        title=f"{ticker} – Candlestick & Volume", template="plotly_white",
        height=700, xaxis_rangeslider_visible=False,
        margin=dict(t=40, b=20), hovermode="x unified"
    )
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    st.plotly_chart(fig, use_container_width=True)

def plot_line_chart(df, title):
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col))
    fig.update_layout(title=title, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

def plot_correlation_heatmap(corr_matrix, chart_style):
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.columns,
        colorscale='RdBu_r', zmin=-1, zmax=1,
        text=corr_matrix.round(2).values, texttemplate="%{text}",
        colorbar=dict(title="Correlation")
    ))

    fig.update_layout(
        title="Portfolio Correlation Matrix", template=chart_style,
        height=600, width=800, margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig

def plot_indicators_with_price(df, indicators, fib_levels, ticker):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'], name='Close',
        line=dict(color='black', width=2)
    ))

    ma_colors = {
        'MA20': 'orange', 'MA50': 'blue',
        'MA100': 'purple', 'MA200': 'brown'
    }
    if "Moving Averages" in indicators:
        for ma_col, color in ma_colors.items():
            if ma_col in df.columns:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[ma_col], name=ma_col,
                    line=dict(color=color, width=2)
                ))

    if "Bollinger Bands" in indicators and "BB_High" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["BB_High"], name="BB High",
            line=dict(color="red", width=1.5, dash="dot")
        ))
        fig.add_trace(go.Scatter(
            x=df.index, y=df["BB_Low"], name="BB Low",
            line=dict(color="red", width=1.5, dash="dot")
        ))

    if "Ichimoku Cloud" in indicators and "Ichimoku_A" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Ichimoku_A"], name="Ichimoku A",
            line=dict(color="teal", width=1.5)
        ))
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Ichimoku_B"], name="Ichimoku B",
            fill='tonexty', fillcolor='rgba(0,128,128,0.2)',
            line=dict(color="darkcyan", width=1.5)
        ))

    if "Fibonacci Levels" in indicators and fib_levels:
        for lvl, val in fib_levels.items():
            fig.add_hline(
                y=val, line_dash="dot", line_color="gray",
                annotation_text=f"Fib {lvl}", annotation_position="top right"
            )

    fig.update_layout(
        title=f"{ticker} – Price + Indicators", template="plotly_white",
        height=600, margin=dict(t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------ Modes ------------------

if mode == "Single Stock":
    run_single_stock_mode()

elif mode == "Portfolio":
    run_portfolio_mode()
