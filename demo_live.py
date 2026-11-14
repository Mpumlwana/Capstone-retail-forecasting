"""Live demo helper (run from the project root: python demo_live.py).

Shows three things, using the project's own saved model and code:
  1. The saved tuned XGBoost model answering a NEW input (not a pre-computed file).
  2. A bad input (unknown store type) being rejected.
  3. A bad input (empty forecast) being rejected.
"""
import joblib
import numpy as np
import pandas as pd

from src.features import add_features, FEATURES
from src.inventory import inventory_plan

model = joblib.load('models/xgboost_tuned.pkl')


def store1_row(date, promo, store_type='c'):
    """One day for Store 1 (type c, assortment a, competition 1270 m, no Promo2)."""
    return pd.DataFrame({
        'Date': [date], 'Store': [1], 'Promo': [promo], 'SchoolHoliday': [0],
        'StoreType': [store_type], 'Assortment': ['a'],
        'CompetitionDistance': [1270.0], 'Promo2': [0]})


def predict(date, promo):
    features = add_features(store1_row(date, promo))
    return float(np.clip(model.predict(features[FEATURES]), 0, None)[0])


print('1. Live model prediction - Store 1, Monday 3 August 2015')
for promo in (0, 1):
    label = 'with promotion' if promo else 'no promotion'
    print(f'   {label:<15}: predicted sales = EUR {predict("2015-08-03", promo):,.0f}')

print()
print('2. Bad input - unknown store type "z"')
try:
    add_features(store1_row('2015-08-03', 0, store_type='z'))
except ValueError as problem:
    print(f'   Rejected: {problem}')

print()
print('3. Bad input - empty forecast')
try:
    inventory_plan([], [])
except ValueError as problem:
    print(f'   Rejected: {problem}')