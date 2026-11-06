import pandas as pd
import pytest

from src.features import add_features, FEATURES


def make_rows():
    return pd.DataFrame({
        'Date': ['2015-07-31', '2015-08-01', '2015-08-02'],
        'Store': [1, 1, 1],
        'Promo': [1, 0, 0],
        'SchoolHoliday': [0, 0, 0],
        'StoreType': ['c', 'b', 'd'],
        'Assortment': ['a', 'b', 'c'],
        'CompetitionDistance': [1270.0, 1270.0, 1270.0],
        'Promo2': [0, 0, 0],
    })


def test_TC015_date_is_split_into_the_right_parts():
    """REQ-001 | Unit | 31 Jul 2015 is a Friday in week 31; 2 Aug 2015 is a Sunday, still week 31"""
    out = add_features(make_rows())
    friday, sunday = out.iloc[0], out.iloc[2]
    assert (friday['DayOfWeek'], friday['Year'], friday['Month'],
            friday['DayOfMonth'], friday['WeekOfYear']) == (5, 2015, 7, 31, 31)
    assert (sunday['DayOfWeek'], sunday['Month'], sunday['DayOfMonth'],
            sunday['WeekOfYear']) == (7, 8, 2, 31)


def test_TC016_letters_become_the_numbers_the_model_was_trained_on():
    """REQ-001 | Unit | StoreType a,b,c,d = 0,1,2,3 and Assortment a,b,c = 0,1,2"""
    out = add_features(make_rows())
    assert list(out['StoreType_encoded']) == [2, 1, 3]
    assert list(out['Assortment_encoded']) == [0, 1, 2]


def test_TC017_missing_column_is_rejected():
    """REQ-001 | Unit (edge case) | A table without Promo must stop with a clear error"""
    with pytest.raises(ValueError):
        add_features(make_rows().drop(columns=['Promo']))


def test_TC018_unknown_store_type_is_rejected():
    """REQ-001 | Unit (edge case) | A store type the model never saw must not pass silently"""
    rows = make_rows()
    rows.loc[0, 'StoreType'] = 'z'
    with pytest.raises(ValueError):
        add_features(rows)


def test_TC019_the_original_table_is_not_changed():
    """REQ-001 | Unit | add_features must work on a copy"""
    rows = make_rows()
    add_features(rows)
    assert 'Year' not in rows.columns
    assert rows.loc[0, 'Date'] == '2015-07-31'


def test_TC020_feature_list_and_order_match_the_trained_model():
    """REQ-001 | Unit | The model expects exactly these 12 columns in this order"""
    expected = ['Store', 'DayOfWeek', 'Year', 'Month', 'DayOfMonth', 'WeekOfYear',
                'Promo', 'SchoolHoliday', 'StoreType_encoded',
                'Assortment_encoded', 'CompetitionDistance', 'Promo2']
    assert FEATURES == expected
    out = add_features(make_rows())
    assert list(out[FEATURES].columns) == expected