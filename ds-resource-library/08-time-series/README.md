# 08 · Time Series & Forecasting

> Predicting the future from ordered-in-time data — demand, revenue, traffic,
> sensors. Deceptively tricky because the usual ML assumptions break.

---

## 📌 What it is & why it matters

Time series data is ordered by time, and observations are correlated across time
(autocorrelation), so standard train/test shuffling and i.i.d. assumptions don't
hold. Forecasting drives inventory, staffing, capacity planning, finance, and
anomaly detection. Getting the **validation** and **uncertainty** right matters
more than the model.

---

## 🧠 Core concepts

- **Components:** trend, seasonality, cyclicity, noise; decomposition.
- **Stationarity** — many models assume it; differencing to achieve it; ADF test.
- **Autocorrelation** — ACF/PACF plots for model identification.
- **Classic models:** moving averages, exponential smoothing (ETS), **ARIMA/SARIMA**.
- **ML/DL approaches:** feature-based ML (lags, rolling windows) + gradient
  boosting; deep models (LSTM, N-BEATS, Temporal Fusion Transformer); **foundation
  models** (TimeGPT, Chronos, TimesFM).
- **Validation:** **forward-chaining / rolling-origin** backtesting — never shuffle
  time.
- **Prediction intervals** — decisions need uncertainty, not just point forecasts.
- **Pitfalls:** leakage via future-aggregated features, ignoring holidays/regime
  changes.

---

## 📚 Best resources

### Books (free)
- **Forecasting: Principles and Practice (FPP3)** — Hyndman & Athanasopoulos, the
  definitive free forecasting book: https://otexts.com/fpp3/

### Tools & docs
- **Nixtla** — modern, fast forecasting stack (`statsforecast`, `mlforecast`,
  `neuralforecast`, TimeGPT): https://github.com/Nixtla
- **Darts** (unit8) — one API for many models + probabilistic forecasting:
  https://unit8co.github.io/darts/
- **Prophet** (Meta) — easy, robust for business series with seasonality/holidays:
  https://facebook.github.io/prophet/
- **sktime** — scikit-learn-style time series: https://www.sktime.net/
- **statsmodels** (ARIMA/ETS): https://www.statsmodels.org/

### Videos
- **Krish Naik — Time Series playlist** (ARIMA, LSTM, hands-on).

---

## 💻 Code example

```python
import numpy as np
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

# Build a daily series with trend + weekly seasonality.
dates = pd.date_range("2023-01-01", periods=365, freq="D")
y = 50 + np.arange(365) * 0.1 + 10 * np.sin(2 * np.pi * np.arange(365) / 7)
df = pd.DataFrame({"unique_id": "series_1", "ds": dates, "y": y})

sf = StatsForecast(models=[AutoARIMA(season_length=7)], freq="D")
sf.fit(df)
forecast = sf.predict(h=14, level=[95])     # 14-day forecast WITH 95% intervals
print(forecast.head())
# columns: unique_id, ds, AutoARIMA, AutoARIMA-lo-95, AutoARIMA-hi-95
```

> 🔑 Always backtest with **rolling-origin** evaluation and report **prediction
> intervals**, not just point forecasts.

---

## 🌍 Real-world use cases

- **Demand & inventory forecasting** — retail, supply chain.
- **Capacity & staffing** — call centers, cloud autoscaling.
- **Finance** — revenue forecasting, risk, algorithmic signals.
- **Anomaly detection** — fraud, equipment failure (predictive maintenance).
- **Energy** — load forecasting.

---

## 🛠️ Hands-on project ideas

1. Forecast a real series (e.g., retail sales) with **ARIMA vs Prophet vs
   LightGBM** and compare with rolling backtests.
2. Build a **prediction-interval** dashboard (point + uncertainty bands).
3. Try a **foundation model** (TimeGPT/Chronos) zero-shot vs a tuned classic model.

---

## 🗺️ Suggested learning path

1. Components & decomposition → 2. Stationarity & ACF/PACF → 3. ARIMA/ETS (FPP3)
→ 4. Prophet for business series → 5. ML approach (lags + boosting) →
6. Backtesting & intervals → 7. Deep/foundation models.
