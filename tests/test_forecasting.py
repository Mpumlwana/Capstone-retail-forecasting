import numpy as np
import pandas as pd
import pytest

from src.forecasting import time_split, tune_xgboost


def make_days():
    return pd.DataFrame({'Date': pd.date_range('2015-01-01', periods=10, freq='D'),
                         'Sales': range(10)})


def test_TC021_split_puts_each_date_on_the_right_side():
    """REQ-002 | Unit | Dates before the split date train, the split date and later test"""
    train, test = time_split(make_days(), '2015-01-06')
    assert len(train) == 5 and len(test) == 5
    assert train['Date'].max() < pd.Timestamp('2015-01-06')
    assert test['Date'].min() == pd.Timestamp('2015-01-06')


def test_TC022_no_date_appears_in_both_sets():
    """REQ-002 | Unit | No look-ahead, and no rows lost"""
    frame = make_days()
    train, test = time_split(frame, '2015-01-06')
    assert set(train['Date']).isdisjoint(set(test['Date']))
    assert len(train) + len(test) == len(frame)


def test_TC023_split_date_before_all_data_is_rejected():
    """REQ-002 | Unit (edge case) | Nothing would be left for training"""
    with pytest.raises(ValueError):
        time_split(make_days(), '2014-01-01')


def test_TC024_split_date_after_all_data_is_rejected():
    """REQ-002 | Unit (edge case) | Nothing would be left for testing"""
    with pytest.raises(ValueError):
        time_split(make_days(), '2016-01-01')


def test_TC025_split_on_the_first_date_is_rejected():
    """REQ-002 | Unit (edge case) | The same mistake as evidence A05: training set would be empty"""
    with pytest.raises(ValueError):
        time_split(make_days(), '2015-01-01')


def test_TC026_tuning_returns_a_sorted_table_within_the_tree_limit():
    """REQ-006 | Unit | Best settings first, and never more trees than allowed"""
    rng = np.random.default_rng(0)
    X = pd.DataFrame({'a': rng.random(300), 'b': rng.random(300)})
    y = X['a'] * 10 + X['b']
    results = tune_xgboost(X[:200], y[:200], X[200:], y[200:],
                           depths=(2, 3), learning_rates=(0.3,), max_trees=50)
    assert list(results.columns) == ['max_depth', 'learning_rate', 'n_trees',
                                     'valid_MAE', 'seconds']
    assert len(results) == 2
    assert results['valid_MAE'].is_monotonic_increasing
    assert (results['n_trees'] <= 50).all()