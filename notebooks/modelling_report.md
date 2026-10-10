# 🤖 Modelling Report — Forecasting Model Comparison

*Task 3 — Forecasting Models | CPUT Data Science Capstone*

---

## 📦 Dataset Overview

- 🏪 **1,115 stores** — Rossmann retail chain, Germany
- 🔢 **Total records:** 1,017,155
- 📅 **Training set:** 881,126 rows — January 2013 to March 2015
- 📅 **Test set:** 136,029 rows — April 2015 to July 2015
- ⚙️ **Features used:** 12
- 🎯 **Target:** Daily Sales in Euros

---

## 🎯 Objective

To train and compare five forecasting models on the Rossmann retail sales dataset, identify the best performer, and recommend a model for deployment in the AI-Driven Retail Demand Forecasting and Inventory Optimisation System.

---

## ⚙️ Feature Engineering

Before training, the raw dataset was prepared through two steps:

### Date Features Extracted
| New Feature | Source | What It Captures |
|---|---|---|
| Year | Date column | Long-term trends across 2013–2015 |
| Month | Date column | Seasonal patterns — December peak, July bump |
| DayOfMonth | Date column | End-of-month spending patterns |
| WeekOfYear | Date column | Weekly positioning within the year |

### Text Columns Encoded
| Original Column | Encoded Column | Example |
|---|---|---|
| StoreType (a/b/c/d) | StoreType_encoded | c → 2 |
| Assortment (a/b/c) | Assortment_encoded | a → 0 |

### Final Feature Set (12 features)
`Store` · `DayOfWeek` · `Year` · `Month` · `DayOfMonth` · `WeekOfYear` · `Promo` · `SchoolHoliday` · `StoreType_encoded` · `Assortment_encoded` · `CompetitionDistance` · `Promo2`

---

## 🔀 Train/Test Split

A time-based split was used — not a random split — because this is time series data. Training on future data to predict the past would be unrealistic.

| Set | Rows | Date Range |
|---|---|---|
| Training | 881,126 (87%) | January 2013 — March 2015 |
| Test | 136,029 (13%) | April 2015 — July 2015 |

---

## 📏 Evaluation Metrics

All models were evaluated using three metrics:

| Metric | What It Measures | Lower Is Better |
|---|---|---|
| MAE (Mean Absolute Error) | Average error in Euros per store per day | ✅ |
| RMSE (Root Mean Squared Error) | Average error — penalises large mistakes more heavily | ✅ |
| MAPE (Mean Absolute Percentage Error) | Average error as a percentage of actual sales | ✅ |

MAPE was calculated only on rows where actual Sales > 0 to avoid division by zero on closed-store days.

---

## 🤖 Model 1 — Random Forest

**Type:** Machine Learning — Ensemble of Decision Trees

**How it works:** Builds 100 independent decision trees, each trained on a random subset of features and rows. Predictions are made by averaging all 100 trees.

**Parameters used:**
- n_estimators = 100
- max_depth = 10
- random_state = 42
- n_jobs = -1

**Results:**
| Metric | Value |
|---|---|
| MAE | €1,739 |
| RMSE | €2,668 |
| MAPE | 26.28% |

**Scope:** All 1,115 stores

---

## ⚡ Model 2 — XGBoost

**Type:** Machine Learning — Gradient Boosted Trees

**How it works:** Builds trees sequentially. Each new tree focuses specifically on correcting the mistakes made by the previous trees. This boosting approach produces more accurate results than independent trees.

**Parameters used:**
- n_estimators = 100
- max_depth = 6
- learning_rate = 0.1
- random_state = 42

**Results:**
| Metric | Value |
|---|---|
| MAE | €1,581 |
| RMSE | €2,384 |
| MAPE | 22.77% |

**Scope:** All 1,115 stores

---

## 📈 Model 3 — Exponential Smoothing

**Type:** Statistical — Time Series

**How it works:** Weights recent sales more heavily than older sales, with weights decreasing exponentially going further back in time. Explicitly models both trend and weekly seasonality.

**Parameters used:**
- seasonal_periods = 7
- trend = 'add'
- seasonal = 'add'

**Results:**
| Metric | Value |
|---|---|
| MAE | €801 |
| RMSE | €1,270 |
| MAPE | 15.76% |

**Scope:** Store 1 only

---

## 📉 Model 4 — ARIMA

**Type:** Statistical — Time Series

**How it works:** Uses three components — AutoRegression (past values predict future), Integration (removes drift), and Moving Average (corrects based on past errors).

**Parameters used:**
- order = (7, 1, 1)

**Results:**
| Metric | Value |
|---|---|
| MAE | €1,381 |
| RMSE | €2,020 |
| MAPE | 17.63% |

**Scope:** Store 1 only

---

## 🧠 Model 5 — LSTM

**Type:** Deep Learning — Neural Network

**How it works:** A neural network with memory cells that learn which past values to remember and which to forget. Reads 7-day sequences to predict the 8th day.

**Architecture:**
- LSTM layer: 50 units
- LSTM layer: 25 units
- Dense output layer: 1 unit
- Epochs: 10
- Batch size: 32

**Results:**
| Metric | Value |
|---|---|
| MAE | €1,477 |
| RMSE | €1,924 |
| MAPE | 19.97% |

**Scope:** Store 1 only

---

## 🔍 Final Model Comparison

| Model | MAE | RMSE | MAPE | Scope |
|---|---|---|---|---|
| Exponential Smoothing | €801 | €1,270 | **15.76%** | Store 1 only |
| ARIMA | €1,381 | €2,020 | 17.63% | Store 1 only |
| LSTM | €1,477 | €1,924 | 19.97% | Store 1 only |
| XGBoost | €1,581 | €2,384 | 22.77% | All 1,115 stores |
| Random Forest | €1,739 | €2,668 | 26.28% | All 1,115 stores |

---

## 🏆 Model Selection

### Best for single-store forecasting: Exponential Smoothing (15.76% MAPE)
### Best for all-store forecasting: XGBoost (22.77% MAPE)

### ✅ Recommended Model: XGBoost

**Reasons:**
1. **Scalability** — one model predicts all 1,115 stores without retraining per store
2. **Performance** — 22.77% MAPE is strong across all stores simultaneously
3. **Practicality** — can be updated with new data without rebuilding from scratch
4. **Feature richness** — uses all 12 features including promotions and store type
5. **Industry standard** — XGBoost consistently performs among the top models on structured retail data worldwide

---

## 💾 Saved Outputs

| File | Location | Contents |
|---|---|---|
| `xgboost_model.pkl` | `models/` | Trained XGBoost model |
| `label_encoder.pkl` | `models/` | Fitted LabelEncoder for StoreType and Assortment |
| `07_model_comparison.png` | `outputs/` | Bar chart comparing all 5 models |

---

## 🚀 Next Steps

- Build the inventory optimisation engine using XGBoost predictions
- Calculate reorder points and safety stock levels per store
- Build the Streamlit interactive dashboard
- Validate model on new data as it becomes available

---

## 🛠️ Tools Used

`Python` · `pandas` · `numpy` · `scikit-learn` · `xgboost` · `statsmodels` · `tensorflow` · `joblib` · `matplotlib` · `Jupyter Notebook`

---
*📌 This report was generated as part of Task 3 — Forecasting Models of the CPUT Data Science Capstone Project.*