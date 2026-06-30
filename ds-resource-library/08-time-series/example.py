"""
Example — Time Series forecasting (ML approach, leak-free backtest)
===================================================================
Runnable. Deps: numpy, pandas, scikit-learn

You don't always need ARIMA/Prophet -- lag features + a regressor is a strong,
flexible baseline. The CRUCIAL part is honest evaluation: rolling-origin
backtesting that never lets the future leak into the past.

Run: python example.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

# Build a daily series: trend + weekly seasonality + noise.
n = 400
t = np.arange(n)
y = 50 + 0.08 * t + 8 * np.sin(2 * np.pi * t / 7) + np.random.default_rng(0).normal(0, 2, n)
s = pd.Series(y)


def make_lag_features(series: pd.Series, lags=(1, 2, 7, 14)) -> pd.DataFrame:
    df = pd.DataFrame({"y": series})
    for lag in lags:
        df[f"lag_{lag}"] = series.shift(lag)        # only PAST values -> no leak
    df["roll7"] = series.shift(1).rolling(7).mean()  # shift(1) first = no leak
    return df.dropna()


df = make_lag_features(s)
X, target = df.drop(columns="y"), df["y"]

# Rolling-origin backtest: train on past, test on the next block. Repeat.
horizon = 30
errors = []
for start in range(len(df) - horizon * 3, len(df) - horizon, horizon):
    Xtr, ytr = X.iloc[:start], target.iloc[:start]
    Xte, yte = X.iloc[start:start + horizon], target.iloc[start:start + horizon]
    model = HistGradientBoostingRegressor(max_iter=200).fit(Xtr, ytr)
    mae = mean_absolute_error(yte, model.predict(Xte))
    errors.append(mae)
    print(f"  fold train<={start:3d}: MAE = {mae:.2f}")

print("=" * 60)
print(f"Mean backtest MAE: {np.mean(errors):.2f}  (vs series std {s.std():.2f})")
print("=" * 60)
print("Lesson: NEVER shuffle time. Use lag/rolling features built only from the")
print("past, and validate with rolling-origin backtests. For production, also try")
print("statsforecast (AutoARIMA), Prophet, or foundation models (TimeGPT/Chronos).")
