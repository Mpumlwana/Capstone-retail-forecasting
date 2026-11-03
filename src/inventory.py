import numpy as np


def _validate(forecast, errors, lead_time_days, z, review_period_days):
    forecast = np.asarray(forecast, dtype=float)
    errors = np.asarray(errors, dtype=float)
    if forecast.size == 0 or errors.size == 0:
        raise ValueError("forecast and errors must not be empty")
    if np.isnan(forecast).any() or np.isnan(errors).any():
        raise ValueError("forecast and errors must not contain NaN")
    if (forecast < 0).any():
        raise ValueError("forecast must not contain negative values")
    if lead_time_days <= 0 or review_period_days <= 0:
        raise ValueError("lead time and review period must be positive")
    if z < 0:
        raise ValueError("z must not be negative")
    return forecast, errors


def safety_stock(z, demand_std, lead_time_days):
    return z * demand_std * np.sqrt(lead_time_days)


def reorder_point(avg_daily_demand, lead_time_days, safety_stock_value):
    return avg_daily_demand * lead_time_days + safety_stock_value


def order_quantity(avg_daily_demand, review_period_days):
    return avg_daily_demand * review_period_days


def inventory_plan(forecast, errors, lead_time_days=5, z=1.65, review_period_days=14):
    forecast, errors = _validate(forecast, errors, lead_time_days, z, review_period_days)
    avg_daily_demand = float(np.mean(forecast))
    demand_std = float(np.std(errors))
    ss = float(safety_stock(z, demand_std, lead_time_days))
    rop = float(reorder_point(avg_daily_demand, lead_time_days, ss))
    return {
        "avg_daily_demand": avg_daily_demand,
        "demand_std": demand_std,
        "safety_stock": ss,
        "reorder_point": rop,
        "order_qty": float(order_quantity(avg_daily_demand, review_period_days)),
    }