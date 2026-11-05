import os
import joblib
import numpy as np
import pandas as pd

from src.features import add_features, FEATURES
from src.evaluation import evaluate, seasonal_naive
from src.inventory import inventory_plan

TEST_START = '2015-04-01'
FORECAST_DAYS = 30
OUT_DIR = 'app/dashboard_data'


def build(data_path='data/cleaned_data.csv',
          model_path='models/xgboost_tuned.pkl',
          old_model_path='models/xgboost_model.pkl',
          out_dir=OUT_DIR, lead_time_days=5, z=1.65, review_period_days=14):
    os.makedirs(out_dir, exist_ok=True)
    model = joblib.load(model_path)

    df = pd.read_csv(data_path, low_memory=False)
    df['Date'] = pd.to_datetime(df['Date'])
    df = add_features(df)

    # Part 1: actual vs predicted for the test months (Apr-Jul 2015)
    test = df[df['Date'] >= TEST_START].copy()
    test['Predicted'] = np.clip(model.predict(test[FEATURES]), 0, None).round(1)
    test[['Store', 'Date', 'Sales', 'Predicted']].to_csv(
        f'{out_dir}/test_predictions.csv', index=False)

    # Part 2: forecast for the 30 days after the data ends
    store_info = (df.sort_values('Date')
                    .groupby('Store')[['StoreType', 'Assortment',
                                       'CompetitionDistance', 'Promo2']]
                    .first().reset_index())
    dates = pd.date_range(df['Date'].max() + pd.Timedelta(days=1),
                          periods=FORECAST_DAYS, freq='D')
    future = pd.DataFrame({'Date': dates}).merge(store_info, how='cross')
    future['Promo'] = 0
    future['SchoolHoliday'] = 0
    future = add_features(future)
    future['Predicted'] = np.clip(model.predict(future[FEATURES]), 0, None).round(1)
    future[['Store', 'Date', 'Predicted']].to_csv(
        f'{out_dir}/future_forecast.csv', index=False)

    # Part 3: inventory plan for every store, using forecast errors
    test['Error'] = test['Sales'] - test['Predicted']
    errors = {s: g['Error'].values for s, g in test.groupby('Store')}
    plans, skipped = [], []
    for store, fut in future.groupby('Store'):
        if store not in errors:
            skipped.append(store)
            continue
        plan = inventory_plan(fut['Predicted'].values, errors[store],
                              lead_time_days, z, review_period_days)
        plan['Store'] = store
        plans.append(plan)
    plans_df = pd.DataFrame(plans).round(1)
    plans_df.to_csv(f'{out_dir}/inventory_plan.csv', index=False)

    # Part 4: model comparison on identical rows
    base = seasonal_naive(df)
    cmp_rows = base[base['Date'] >= TEST_START].dropna(
        subset=['Baseline_Prediction']).copy()
    cmp_rows['Old'] = joblib.load(old_model_path).predict(cmp_rows[FEATURES])
    cmp_rows['Tuned'] = model.predict(cmp_rows[FEATURES])
    table = []
    for name, col in [('Seasonal naive (baseline)', 'Baseline_Prediction'),
                      ('XGBoost (Task 3 settings)', 'Old'),
                      ('XGBoost (tuned)', 'Tuned')]:
        metrics = evaluate(cmp_rows['Sales'], cmp_rows[col])
        table.append({'Model': name, **{k: round(v, 2) for k, v in metrics.items()}})
    comparison = pd.DataFrame(table)
    comparison.to_csv(f'{out_dir}/model_comparison.csv', index=False)

    print(f"Test rows saved:     {len(test):,}")
    print(f"Future rows saved:   {len(future):,}")
    print(f"Stores in plan:      {len(plans_df):,}  (skipped: {len(skipped)})")
    print(f"Comparison rows:     {len(cmp_rows):,}\n")
    print(comparison.to_string(index=False))


if __name__ == '__main__':
    build()