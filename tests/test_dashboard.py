import re
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parent.parent / 'app' / 'app.py'


def euros(text):
    return int(re.sub(r'[^\d]', '', text))


def open_page():
    return AppTest.from_file(str(APP), default_timeout=60).run()


def test_TC038_page_loads_with_four_number_cards():
    """REQ-004 | System | The page opens without an error and shows four cards"""
    page = open_page()
    assert not page.exception
    assert len(page.metric) == 4


def test_TC039_longer_lead_time_raises_the_reorder_point_on_the_page():
    """REQ-004 | System | Move the lead time slider from 5 to 10 days"""
    page = open_page()
    before = euros(page.metric[2].value)
    page.sidebar.slider[0].set_value(10).run()
    assert not page.exception
    assert euros(page.metric[2].value) > before


def test_TC040_higher_service_level_raises_the_safety_stock_on_the_page():
    """REQ-004 | System | Change the service level from 95% to 99%"""
    page = open_page()
    before = euros(page.metric[1].value)
    page.sidebar.selectbox[1].set_value('99%').run()
    assert not page.exception
    assert euros(page.metric[1].value) > before


def test_TC041_order_size_changes_only_the_order_quantity():
    """REQ-004 | System | One order covers 28 days instead of 14: quantity rises, reorder point does not move"""
    page = open_page()
    rop_before = euros(page.metric[2].value)
    qty_before = euros(page.metric[3].value)
    page.sidebar.slider[1].set_value(28).run()
    assert not page.exception
    assert euros(page.metric[2].value) == rop_before
    assert euros(page.metric[3].value) > qty_before