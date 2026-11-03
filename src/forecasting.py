import time
import pandas as pd
import xgboost as xgb


def time_split(df, split_date, date_col='Date'):
    split = pd.Timestamp(split_date)
    train = df[df[date_col] < split]
    test = df[df[date_col] >= split]
    if train.empty or test.empty:
        raise ValueError("split_date leaves the train or test set empty")
    return train, test


def tune_xgboost(X_train, y_train, X_valid, y_valid,
                 depths=(6, 8), learning_rates=(0.1, 0.05),
                 max_trees=400, seed=42):
    rows = []
    for depth in depths:
        for lr in learning_rates:
            start = time.time()
            model = xgb.XGBRegressor(
                n_estimators=max_trees, max_depth=depth, learning_rate=lr,
                random_state=seed, n_jobs=-1,
                early_stopping_rounds=30, eval_metric='mae')
            model.fit(X_train, y_train,
                      eval_set=[(X_valid, y_valid)], verbose=False)
            rows.append({'max_depth': depth, 'learning_rate': lr,
                         'n_trees': model.best_iteration + 1,
                         'valid_MAE': round(model.best_score, 2),
                         'seconds': round(time.time() - start)})
    return pd.DataFrame(rows).sort_values('valid_MAE').reset_index(drop=True)