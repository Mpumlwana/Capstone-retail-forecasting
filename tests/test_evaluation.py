import pandas as pd
import pytest

from src.evaluation import mae, mape, evaluate, seasonal_naive, select_best_model


def make_frame():
    """Two stores, 15 days of sales, with 3 January missing on purpose."""
    days = pd.date_range('2015-01-01', periods=15, freq='D').drop(pd.Timestamp('2015-01-03'))
    parts = []
    for store, factor in [(1, 10), (2, 100)]:
        parts.append(pd.DataFrame({'Store': store, 'Date': days,
                                   'Sales': [d.day * factor for d in days]}))
    return pd.concat(parts, ignore_index=True)


def baseline_for(result, store, date):
    row = result[(result['Store'] == store) & (result['Date'] == pd.Timestamp(date))]
    return row['Baseline_Prediction'].iloc[0]


def test_TC006_scores_match_hand_calculation():
    """REQ-002 | Unit | Actual [100,200], predicted [110,180]: MAE 15, RMSE 15.81, MAPE 10"""
    scores = evaluate([100, 200], [110, 180])
    assert scores['MAE'] == pytest.approx(15)
    assert scores['RMSE'] == pytest.approx(15.8114, abs=0.001)
    assert scores['MAPE'] == pytest.approx(10)


def test_TC007_mape_ignores_days_with_zero_sales():
    """REQ-002 | Unit (edge case) | A zero actual would divide by zero, so it is skipped"""
    assert mape([0, 100], [50, 110]) == pytest.approx(10)


def test_TC008_mape_rejects_all_zero_actuals():
    """REQ-002 | Unit (edge case) | Nothing to measure, so it must refuse"""
    with pytest.raises(ValueError):
        mape([0, 0], [1, 2])


def test_TC009_mismatched_lengths_are_rejected():
    """REQ-002 | Unit (edge case) | Two lists of different length cannot be compared"""
    with pytest.raises(ValueError):
        mae([1, 2], [1])


def test_TC010_baseline_uses_same_weekday_last_week():
    """REQ-002 | Unit | 9 Jan must get what 2 Jan sold, for each store separately"""
    result = seasonal_naive(make_frame())
    assert baseline_for(result, 1, '2015-01-09') == 20      # 2 Jan x 10
    assert baseline_for(result, 2, '2015-01-09') == 200     # 2 Jan x 100
    first_week = result[result['Date'] < pd.Timestamp('2015-01-08')]
    assert first_week['Baseline_Prediction'].isna().all()


def test_TC011_baseline_stays_empty_when_the_day_is_missing():
    """REQ-002 | Unit (edge case) | 3 Jan is missing, so 10 Jan has no baseline"""
    result = seasonal_naive(make_frame())
    assert pd.isna(baseline_for(result, 1, '2015-01-10'))
    assert pd.isna(baseline_for(result, 2, '2015-01-10'))


def test_TC012_baseline_does_not_add_or_remove_rows():
    """REQ-002 | Unit | The join must keep exactly the same rows"""
    frame = make_frame()
    assert len(seasonal_naive(frame)) == len(frame)


def test_TC013_best_model_follows_the_selection_rule():
    """REQ-002 | Unit | B has the lower MAE but misses the 20% threshold, so A wins"""
    results = {'A': {'MAE': 5, 'RMSE': 6, 'MAPE': 12},
               'B': {'MAE': 3, 'RMSE': 4, 'MAPE': 25}}
    best, needs_tuning = select_best_model(results, 20)
    assert best == 'A'
    assert needs_tuning == ['B']


def test_TC014_no_model_qualifies():
    """REQ-006 | Unit (edge case) | If every model misses the threshold, none is selected"""
    results = {'A': {'MAE': 5, 'RMSE': 6, 'MAPE': 12},
               'B': {'MAE': 3, 'RMSE': 4, 'MAPE': 25}}
    best, needs_tuning = select_best_model(results, 5)
    assert best is None
    assert set(needs_tuning) == {'A', 'B'}