from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest

from src.features import add_features, FEATURES

ROOT = Path(__file__).resolve().parent.parent
CLEANED = ROOT / 'data' / 'cleaned_data.csv'
DASH = ROOT / 'app' / 'dashboard_data'
MODEL = ROOT / 'models' / 'xgboost_tuned.pkl'

KEY_COLUMNS = ['Store', 'DayOfWeek', 'Date', 'Sales', 'Customers', 'Open', 'Promo',
               'SchoolHoliday', 'StoreType', 'Assortment', 'CompetitionDistance', 'Promo2']

needs_data = pytest.mark.skipif(
    not CLEANED.exists(), reason='data/cleaned_data.csv is not in the repository')


@pytest.fixture(scope='module')
def cleaned():
    return pd.read_csv(CLEANED, usecols=KEY_COLUMNS, low_memory=False, parse_dates=['Date'])


@needs_data
def test_TC027_no_missing_values_in_key_columns(cleaned):
    """REQ-005 | Integration (data) | The cleaning step must leave no empty cells in the columns we use"""
    assert cleaned[KEY_COLUMNS].isna().sum().sum() == 0


@needs_data
def test_TC028_no_duplicate_store_days(cleaned):
    """REQ-005 | Integration (data) | One row per store per day"""
    assert cleaned.duplicated(subset=['Store', 'Date']).sum() == 0


@needs_data
def test_TC029_no_negative_sales_or_customers(cleaned):
    """REQ-005 | Integration (data) | Negative sales cannot happen in real life"""
    assert (cleaned['Sales'] < 0).sum() == 0
    assert (cleaned['Customers'] < 0).sum() == 0


@needs_data
def test_TC030_no_open_store_with_zero_sales(cleaned):
    """REQ-005 | Integration (data) | The 54 illogical rows removed in Task 1 must stay removed"""
    assert ((cleaned['Open'] == 1) & (cleaned['Sales'] == 0)).sum() == 0


@needs_data
def test_TC031_dataset_size_dates_and_stores(cleaned):
    """REQ-005 | Integration (data) | 1,017,155 rows, 1,115 stores, 1 Jan 2013 to 31 Jul 2015"""
    assert len(cleaned) == 1017155
    assert cleaned['Store'].nunique() == 1115
    assert cleaned['Date'].min() == pd.Timestamp('2013-01-01')
    assert cleaned['Date'].max() == pd.Timestamp('2015-07-31')


@needs_data
@pytest.mark.skipif(not MODEL.exists(), reason='tuned model file is missing')
def test_TC032_saved_model_gives_one_finite_prediction_per_row():
    """REQ-001 | Integration | Real data through add_features and the saved tuned model"""
    sample = pd.read_csv(CLEANED, nrows=500, low_memory=False,
                         usecols=['Date', 'Store', 'Promo', 'SchoolHoliday', 'StoreType',
                                  'Assortment', 'CompetitionDistance', 'Promo2'])
    predictions = joblib.load(MODEL).predict(add_features(sample)[FEATURES])
    assert len(predictions) == 500
    assert np.isfinite(predictions).all()


def test_TC033_inventory_plan_covers_every_store_sensibly():
    """REQ-003 | Integration | 1,115 unique stores, no empty values, reorder point above safety stock"""
    plan = pd.read_csv(DASH / 'inventory_plan.csv')
    assert len(plan) == 1115
    assert plan['Store'].is_unique
    assert plan.isna().sum().sum() == 0
    assert (plan['reorder_point'] > 0).all()
    assert (plan['reorder_point'] >= plan['safety_stock']).all()


def test_TC034_future_forecast_is_complete_and_never_negative():
    """REQ-003 | Integration | 1,115 stores x 30 days, 1 to 30 August 2015, no negative sales"""
    future = pd.read_csv(DASH / 'future_forecast.csv', parse_dates=['Date'])
    assert len(future) == 33450
    assert future['Store'].nunique() == 1115
    assert future['Date'].nunique() == 30
    assert future['Date'].min() == pd.Timestamp('2015-08-01')
    assert future['Date'].max() == pd.Timestamp('2015-08-30')
    assert future['Predicted'].notna().all()
    assert (future['Predicted'] >= 0).all()


def test_TC035_comparison_table_shows_tuned_model_best():
    """REQ-002 | Integration | Tuned XGBoost beats the first XGBoost, which beats the baseline"""
    table = pd.read_csv(DASH / 'model_comparison.csv').set_index('Model')
    assert len(table) == 3
    tuned = table.loc['XGBoost (tuned)', 'MAE']
    old = table.loc['XGBoost (Task 3 settings)', 'MAE']
    baseline = table.loc['Seasonal naive (baseline)', 'MAE']
    assert tuned < old < baseline


def test_TC036_inventory_plan_follows_the_design_formulas():
    """REQ-003 | Integration | Safety stock and reorder point agree with the formulas (5-day lead, z 1.65) to within rounding"""
    plan = pd.read_csv(DASH / 'inventory_plan.csv')
    expected_ss = 1.65 * plan['demand_std'] * np.sqrt(5)
    expected_rop = plan['avg_daily_demand'] * 5 + plan['safety_stock']
    assert (plan['safety_stock'] - expected_ss).abs().max() < 1.0
    assert (plan['reorder_point'] - expected_rop).abs().max() < 1.0


def test_TC037_predictions_only_cover_the_test_period():
    """REQ-002 | Integration | No look-ahead: test predictions start on 1 April 2015"""
    test = pd.read_csv(DASH / 'test_predictions.csv', parse_dates=['Date'])
    assert len(test) == 136029
    assert test['Date'].min() == pd.Timestamp('2015-04-01')
    assert test['Date'].max() == pd.Timestamp('2015-07-31')
    assert (test['Predicted'] >= 0).all()