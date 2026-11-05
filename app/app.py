import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.inventory import inventory_plan
from src.evaluation import evaluate

DATA_DIR = ROOT / 'app' / 'dashboard_data'
FILES = {'test': 'test_predictions.csv', 'future': 'future_forecast.csv',
         'plan': 'inventory_plan.csv', 'comparison': 'model_comparison.csv'}
Z_BY_LEVEL = {'90%': 1.28, '95%': 1.65, '99%': 2.33}

st.set_page_config(page_title='Retail Demand and Reorder Planner', layout='wide')


@st.cache_data
def load_data():
    missing = [f for f in FILES.values() if not (DATA_DIR / f).exists()]
    if missing:
        return None, missing
    data = {
        'test': pd.read_csv(DATA_DIR / FILES['test'], parse_dates=['Date']),
        'future': pd.read_csv(DATA_DIR / FILES['future'], parse_dates=['Date']),
        'plan': pd.read_csv(DATA_DIR / FILES['plan']),
        'comparison': pd.read_csv(DATA_DIR / FILES['comparison']),
    }
    return data, []


data, missing = load_data()
if data is None:
    st.error(f"Missing data files: {missing}. "
             "Run: python -m src.build_dashboard_data")
    st.stop()

st.title('Retail Demand Forecast and Reorder Planner')
st.caption('Proof of concept on the public Rossmann dataset. '
           'Values are Euros of sales, not units of stock.')

stores = sorted(data['future']['Store'].unique())
with st.sidebar:
    st.header('Settings')
    store = st.selectbox('Store', stores)
    lead_time = st.slider('Supplier lead time (days)', 1, 14, 5)
    level = st.selectbox('Service level (protection against running out)',
                         list(Z_BY_LEVEL), index=1)
    review = st.slider('One order covers (days of demand)', 7, 28, 14)

fut = data['future'][data['future']['Store'] == store].sort_values('Date')
hist = data['test'][data['test']['Store'] == store].sort_values('Date')
errors = (hist['Sales'] - hist['Predicted']).values

try:
    plan = inventory_plan(fut['Predicted'].values, errors,
                          lead_time, Z_BY_LEVEL[level], review)
except ValueError as problem:
    st.error(f'Could not calculate the plan: {problem}')
    st.stop()

st.subheader(f'Store {store}')
c1, c2, c3, c4 = st.columns(4)
c1.metric('Average daily demand', f"€{plan['avg_daily_demand']:,.0f}")
c2.metric('Safety stock', f"€{plan['safety_stock']:,.0f}")
c3.metric('Reorder point', f"€{plan['reorder_point']:,.0f}")
c4.metric('Order quantity', f"€{plan['order_qty']:,.0f}")
st.write(f"When stock on hand falls to **€{plan['reorder_point']:,.0f}**, "
         f"place an order. It arrives in **{lead_time} days**.")

left, right = st.columns(2)

with left:
    st.markdown('**Forecast: next 30 days**')
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.bar(fut['Date'], fut['Predicted'], color='steelblue')
    ax.set_ylabel('Predicted sales (€)')
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.markdown('**How accurate was the model? Actual vs predicted (last 60 days of the test period)**')
    recent = hist.tail(60)
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(recent['Date'], recent['Sales'], label='Actual', color='black')
    ax.plot(recent['Date'], recent['Predicted'], label='Predicted',
            color='darkorange')
    ax.set_ylabel('Sales (€)')
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    try:
        m = evaluate(hist['Sales'], hist['Predicted'])
        st.caption(f"This store, Apr to Jul 2015: MAE €{m['MAE']:,.0f} | "
                   f"MAPE {m['MAPE']:.1f}%")
    except ValueError:
        st.caption('Not enough sales history to score this store.')

st.markdown('**Model comparison (all stores, same test rows)**')
st.dataframe(data['comparison'], hide_index=True)

with st.expander('Assumptions and limitations'):
    st.write(
        '- No promotions or school holidays are assumed in the 30-day forecast.\n'
        '- Values are Euros of sales, not units of stock.\n'
        '- The model was tested on April to July 2015 only.\n'
        '- Lead time, service level and order size are settings, not facts.\n'
        '- This is a proof of concept, not a production system.')