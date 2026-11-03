import numpy as np
import pandas as pd


def _as_arrays(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_true.shape != y_pred.shape:
        raise ValueError("y_true and y_pred must have the same length")
    if y_true.size == 0:
        raise ValueError("inputs must not be empty")
    return y_true, y_pred


def mae(y_true, y_pred):
    y_true, y_pred = _as_arrays(y_true, y_pred)
    return float(np.mean(np.abs(y_true - y_pred)))


def rmse(y_true, y_pred):
    y_true, y_pred = _as_arrays(y_true, y_pred)
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mape(y_true, y_pred):
    y_true, y_pred = _as_arrays(y_true, y_pred)
    mask = y_true > 0
    if not mask.any():
        raise ValueError("MAPE needs at least one actual value above zero")
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def evaluate(y_true, y_pred):
    return {"MAE": mae(y_true, y_pred),
            "RMSE": rmse(y_true, y_pred),
            "MAPE": mape(y_true, y_pred)}


def seasonal_naive(df, store_col="Store", date_col="Date",
                   target_col="Sales", season_days=7):
    lagged = df[[store_col, date_col, target_col]].copy()
    lagged[date_col] = lagged[date_col] + pd.Timedelta(days=season_days)
    lagged = lagged.rename(columns={target_col: "Baseline_Prediction"})
    return df.merge(lagged, on=[store_col, date_col], how="left")


def select_best_model(results, accuracy_threshold):
    qualifying = {name: m for name, m in results.items()
                  if m["MAPE"] < accuracy_threshold}
    needs_tuning = [name for name in results if name not in qualifying]
    if not qualifying:
        return None, needs_tuning
    best = min(qualifying, key=lambda name: qualifying[name]["MAE"])
    return best, needs_tuning