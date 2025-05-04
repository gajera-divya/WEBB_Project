import numpy as np
import pandas as pd
from scipy.optimize import minimize

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
    
def get_portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.dot(weights, mean_returns)
    risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return returns, risk

def optimize_portfolio(mean_returns, cov_matrix, risk_free_rate=0.01):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)

    def neg_sharpe(weights, mean_returns, cov_matrix):
        ret, vol = get_portfolio_performance(weights, mean_returns, cov_matrix)
        return - (ret - risk_free_rate) / vol

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    init_guess = num_assets * [1. / num_assets, ]

    result = minimize(
        neg_sharpe, init_guess, args=args, method='SLSQP',
        bounds=bounds, constraints=constraints
    )
    return result




def efficient_frontier(mean_returns, cov_matrix, num_points=50):
    results = {'Return': [], 'Risk': [], 'Sharpe': [], 'Weights': []}
    for r in np.linspace(0.01, 0.5, num_points):
        constraints = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: np.dot(x, mean_returns) - r}
        )
        bounds = tuple((0, 1) for _ in mean_returns)
        init_guess = len(mean_returns) * [1. / len(mean_returns), ]

        result = minimize(
            lambda w: np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))),
            init_guess, method='SLSQP',
            bounds=bounds, constraints=constraints
        )
        if result.success:
            risk = np.sqrt(np.dot(result.x.T, np.dot(cov_matrix, result.x)))
            results['Return'].append(r)
            results['Risk'].append(risk)
            results['Sharpe'].append((r - 0.01) / risk)
            results['Weights'].append(result.x)

    return pd.DataFrame(results)
