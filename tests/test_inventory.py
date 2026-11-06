import pytest

from src.inventory import inventory_plan, safety_stock, reorder_point

FORECAST = [100] * 10
ERRORS = [10, -10] * 5


def test_TC001_hand_calculated_plan():
    """REQ-003 | Unit | By hand: 1.65 x 10 x sqrt(5) = 36.9, then 100 x 5 + 36.9 = 536.9"""
    plan = inventory_plan(FORECAST, ERRORS, lead_time_days=5, z=1.65, review_period_days=14)
    assert plan['avg_daily_demand'] == pytest.approx(100)
    assert plan['demand_std'] == pytest.approx(10)
    assert plan['safety_stock'] == pytest.approx(36.895, abs=0.01)
    assert plan['reorder_point'] == pytest.approx(536.895, abs=0.01)
    assert plan['order_qty'] == pytest.approx(1400)
    assert safety_stock(1.65, 10, 5) == pytest.approx(36.895, abs=0.01)
    assert reorder_point(100, 5, 36.895) == pytest.approx(536.895, abs=0.01)


def test_TC002_no_forecast_error_means_no_safety_stock():
    """REQ-003 | Unit | If the forecast is never wrong, no cushion is needed"""
    plan = inventory_plan(FORECAST, [0] * 10, lead_time_days=5, z=1.65)
    assert plan['safety_stock'] == pytest.approx(0)
    assert plan['reorder_point'] == pytest.approx(500)


def test_TC003_longer_lead_time_raises_reorder_point():
    """REQ-003 | Unit | Waiting longer for a delivery means ordering earlier"""
    short = inventory_plan(FORECAST, ERRORS, lead_time_days=5)
    long = inventory_plan(FORECAST, ERRORS, lead_time_days=10)
    assert long['reorder_point'] > short['reorder_point']


def test_TC004_higher_service_level_raises_safety_stock():
    """REQ-003 | Unit | More protection needs a bigger cushion"""
    low = inventory_plan(FORECAST, ERRORS, z=1.28)
    high = inventory_plan(FORECAST, ERRORS, z=2.33)
    assert high['safety_stock'] > low['safety_stock']


@pytest.mark.parametrize('forecast, errors, lead, z', [
    ([], [1], 5, 1.65),                 # empty forecast
    ([100], [], 5, 1.65),               # empty errors
    ([100, float('nan')], [1], 5, 1.65),  # not-a-number in forecast
    ([100, -5], [1], 5, 1.65),          # negative forecast
    ([100], [1], 0, 1.65),              # lead time of zero
    ([100], [1], 5, -1),                # negative z
])
def test_TC005_invalid_inputs_are_rejected(forecast, errors, lead, z):
    """REQ-003 | Unit (edge case) | Nonsense input must stop with a clear error"""
    with pytest.raises(ValueError):
        inventory_plan(forecast, errors, lead_time_days=lead, z=z)