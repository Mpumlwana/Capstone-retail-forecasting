# 🛠️ Implementation Report: Modules, Baseline and Tuning

*Implementation Phase, Part 1 | CPUT Data Science Capstone*

---

## 📦 Overview

- 🧩 **Four reusable modules** were written in `src/`, matching the Design Phase modules
- 📏 A **seasonal-naive baseline** was built, as the design requires
- 🎯 **XGBoost was tuned** after it missed the accuracy threshold (REQ-006)
- 🧪 Every module was checked against a result worked out by hand
- 📓 Notebook: `05_implementation_evaluation.ipynb`

---

## 🧩 Modules Written

| File | Design Module | What it does |
|---|---|---|
| `src/features.py` | Module 1: Feature Engineering | Builds the 12 model features and rejects missing columns or unknown store types |
| `src/forecasting.py` | Module 2: Model Trainer | Time-based train/test split, and the XGBoost tuning loop |
| `src/evaluation.py` | Module 3: Model Evaluator | MAE, RMSE, MAPE, the seasonal-naive baseline, and model selection |
| `src/inventory.py` | Module 4: Inventory Optimiser | Safety stock, reorder point and order quantity, with input validation |

---

## ✅ Checks Against Hand-Calculated Results

| Module | Input | Hand-calculated result | Program result | Match |
|---|---|---|---|---|
| Inventory | forecast 100 per day, errors ±10, lead time 5, z 1.65 | Safety stock 36.9, reorder point 536.9, order quantity 1,400 | 36.90, 536.90, 1,400 | ✅ |
| Evaluation | actual [100, 200], predicted [110, 180] | MAE 15, RMSE 15.81, MAPE 10% | 15.0, 15.81, 10.0 | ✅ |
| Model selection | A (MAE 5, MAPE 12), B (MAE 3, MAPE 25), threshold 20 | A is selected, B needs tuning | `('A', ['B'])` | ✅ |
| Features | 31 July 2015 and 1 August 2015 | Friday and Saturday, weeks 31 and 31 | 5 and 6, 31 and 31 | ✅ |
| Time split | split date 1 August 2015 | 1 training row, 1 test row | 1 and 1 | ✅ |
| Edge case | split date 1 January 2013, which is the first date in the data | Rejected, because nothing is left for training | ValueError raised | ✅ |

---

## 🔧 Changes From the Task 4 Inventory Calculation

Reviewing the Design Phase showed three differences between the Task 4 notebook and the approved design. They were fixed in `src/inventory.py`.

| Item | Task 4 notebook | Approved design | Now |
|---|---|---|---|
| Demand spread used for safety stock | Spread of the predicted values | Standard deviation of the forecast error (actual minus forecast) | Forecast error |
| Lead time | 7 days | 5 days | 5 days (default) |
| Order quantity | Not produced | Average demand × review period | Produced (14-day review period is an assumption) |

---

## 📏 Seasonal-Naive Baseline

The baseline predicts that a store sells the same as it did on the same weekday one week earlier. It was built by moving each date forward 7 days and joining on store and date, not by shifting rows, because some store-days are missing from the data.

- Rows before and after building the baseline: **1,017,155 and 1,017,155** (nothing lost or added)
- Test rows: **136,029**
- Test rows with no sale 7 days earlier: **2**, which were left out for **both** models
- Rows scored: **136,027**

---

## 🎯 Tuning (REQ-006)

The accuracy threshold was set at **MAPE below 20%**. The Design Phase gives no number, so this is a **project assumption**.

XGBoost scored 22.77% MAPE, above the threshold, so the tuning step was run.

### Three separate sets of data

| Data | Dates | Rows | Used for |
|---|---|---|---|
| Tuning part | Jan 2013 to Dec 2014 | 780,778 | Training each trial model |
| Validation part | Jan to Mar 2015 | 100,348 | Choosing the settings |
| Test set | Apr to Jul 2015 | 136,027 | Scoring the final model once |

### Round 1 (maximum 400 trees)

| max_depth | learning_rate | trees used | validation MAE |
|---|---|---|---|
| 8 | 0.10 | 400 | 866.62 |
| 6 | 0.10 | 400 | 959.59 |
| 8 | 0.05 | 400 | 991.83 |
| 6 | 0.05 | 400 | 1,145.00 |

All four models used the full 400 trees, so early stopping never triggered. The best result also sat at the edge of the grid (the deepest trees and the fastest learning rate tried). Both points showed the search was cut short, so a second round was run.

### Round 2 (maximum 1,000 trees)

| max_depth | learning_rate | trees used | validation MAE |
|---|---|---|---|
| 8 | 0.2 | 422 | **795.83** |
| 10 | 0.1 | 644 | 846.54 |
| 8 | 0.1 | 567 | 851.03 |
| 10 | 0.2 | 254 | 919.10 |

Early stopping worked in this round (254 to 644 trees). The original Task 3 settings (100 trees, depth 6, learning rate 0.1) scored a validation MAE of **1,338.88** on the same data, so the tuned settings were about **40.6% lower** on validation.

The validation months were used both to stop training early and to choose the winner, so the validation figure is slightly optimistic. The test set is the honest measure.

---

## 📊 Final Results on the Test Set (Apr to Jul 2015)

| Model | MAE | RMSE | MAPE |
|---|---|---|---|
| Seasonal naive (baseline) | 2,368.85 | 3,541.40 | 34.59% |
| XGBoost (Task 3 settings) | 1,580.64 | 2,384.14 | 22.77% |
| **XGBoost (tuned)** | **1,121.78** | **1,976.71** | **15.03%** |

- The tuned model's MAE is about **52.6% lower than the baseline** and **29.0% lower than the Task 3 XGBoost**.
- The tuned model is the only one below the 20% threshold, so it is the selected model under the design's selection rule.
- The test set was scored **once**, after the settings were chosen on validation data.

---

## ⚠️ Limitations

1. The 20% threshold is a project assumption, not a value from the design.
2. The test period is four months (April to July 2015), so it does not cover a full year or the Christmas peak.
3. ARIMA, Exponential Smoothing and LSTM were tested on Store 1 only in Task 3. They have **not yet** been compared with XGBoost on the same data, so the five-model comparison is not yet like-for-like.
4. Values are Euros of sales, not units of stock.
5. The settings search was small (two rounds of four combinations each).

---

## 🚀 Next Steps

- Build the live Streamlit dashboard (REQ-004)
- Write automated tests and capture the results as evidence
- Run a like-for-like comparison on Store 1 for all models
- Recalculate the inventory plan using the tuned model

---

## 🛠️ Tools Used

`Python` · `pandas` · `numpy` · `xgboost` · `joblib` · `Jupyter Notebook`

---
*📌 This report was generated as part of the Implementation Phase (Part 1) of the CPUT Data Science Capstone Project.*