import pandas as pd

STORETYPE_MAP = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
ASSORTMENT_MAP = {'a': 0, 'b': 1, 'c': 2}

FEATURES = ['Store', 'DayOfWeek', 'Year', 'Month', 'DayOfMonth', 'WeekOfYear',
            'Promo', 'SchoolHoliday', 'StoreType_encoded',
            'Assortment_encoded', 'CompetitionDistance', 'Promo2']


def add_features(df):
    needed = ['Date', 'Store', 'Promo', 'SchoolHoliday', 'StoreType',
              'Assortment', 'CompetitionDistance', 'Promo2']
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = df.copy()
    out['Date'] = pd.to_datetime(out['Date'])
    out['DayOfWeek'] = out['Date'].dt.dayofweek + 1
    out['Year'] = out['Date'].dt.year
    out['Month'] = out['Date'].dt.month
    out['DayOfMonth'] = out['Date'].dt.day
    out['WeekOfYear'] = out['Date'].dt.isocalendar().week.astype(int)
    out['StoreType_encoded'] = out['StoreType'].map(STORETYPE_MAP)
    out['Assortment_encoded'] = out['Assortment'].map(ASSORTMENT_MAP)

    if out[['StoreType_encoded', 'Assortment_encoded']].isna().any().any():
        raise ValueError("Unknown StoreType or Assortment value")
    return out