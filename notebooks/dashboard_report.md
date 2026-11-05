# 🌐 Dashboard Report: Live Reorder Planner (REQ-004)

*Implementation Phase, Part 2 | CPUT Data Science Capstone*

---

## 📦 Overview

- 🖥️ A **live Streamlit dashboard** (`app/app.py`) lets a store manager pick a store and see its forecast, accuracy and reorder plan
- 🧮 The plan on screen is calculated by **`src/inventory.py`**, the module that was checked by hand
- 📁 Results for all **1,115 stores** are prepared once by `src/build_dashboard_data.py`
- 📸 Evidence: screenshots A09 to A13 in the `evidence/` folder
- 🎯 Requirements: **REQ-004** (dashboard) and **REQ-003** (inventory plan for every store)

---

## 🎯 Objective

To replace the static dashboard mockup from the Design Phase with a working page, so a non-technical store manager can see forecasts and inventory recommendations in one view.

---

## ⚙️ Step 1: Preparing the Dashboard Data

`python -m src.build_dashboard_data` loads the tuned model and the cleaned data, then saves four small files into `app/dashboard_data/`:

| File | Contents |
|---|---|
| `test_predictions.csv` | Actual and predicted sales for April to July 2015 |
| `future_forecast.csv` | The 30-day forecast (1 to 30 August 2015) for every store |
| `inventory_plan.csv` | Reorder plan for every store |
| `model_comparison.csv` | Baseline, Task 3 XGBoost and tuned XGBoost on the same rows |

The folder is called `dashboard_data` and not `data` because `.gitignore` excludes any folder named `data`. These small files must be in the repository so that anyone can run the dashboard.

### Output of the build step (evidence A09)

| Item | Value |
|---|---|
| Test rows saved | 136,029 |
| Future rows saved | 33,450 (1,115 stores × 30 days) |
| Stores in the plan | 1,115 (0 skipped) |
| Rows in the comparison | 136,027 |

The three-model comparison printed by this step matches the notebook exactly (tuned MAE 1,121.78, baseline MAE 2,368.85), so the result was reproduced from a second, independent run.

### How the inventory plan is calculated

| Setting | Value | Source |
|---|---|---|
| Model | Tuned XGBoost | Implementation Part 1 |
| Demand spread | Standard deviation of forecast error (actual minus predicted) on the April to July 2015 test period | Design Phase |
| Lead time | 5 days (adjustable on the dashboard) | Design Phase |
| Service level | 95%, z = 1.65 (adjustable) | Assumption |
| Order covers | 14 days of demand (adjustable) | Assumption |
| Promotions and school holidays in the forecast | Assumed 0 | Assumption |

---

## 🖥️ Step 2: The Dashboard

Run with `python -m streamlit run app/app.py`.

### What the user can change (sidebar)

| Control | Range |
|---|---|
| Store | Any of the 1,115 stores |
| Supplier lead time | 1 to 14 days (default 5) |
| Service level | 90%, 95% or 99% (z = 1.28, 1.65, 2.33) |
| One order covers | 7 to 28 days of demand (default 14) |

### What the user sees

- Four number cards: average daily demand, safety stock, reorder point, order quantity
- A sentence in plain words: when stock falls to the reorder point, place an order
- A bar chart of the next 30 days of predicted sales
- A line chart of actual against predicted sales for the last 60 days of the test period, with that store's MAE and MAPE
- The three-model comparison table
- An expandable box listing the assumptions and limitations

### Built-in safeguards

- If a data file is missing, the page shows a message that says how to rebuild it, and does not crash
- Slider limits stop impossible lead times
- If `inventory_plan` rejects an input, its error message is shown to the user
- If a store has too little history to score, the page says so

---

## 📸 Evidence

| ID | File | What it shows |
|---|---|---|
| A09 | `A09_dashboard_data_build.png` | Output of the data preparation step |
| A10 | `A10_dashboard_store1_default.png` | Store 1 with default settings |
| A11 | `A11_dashboard_lead_time_10.png` | Store 1 with lead time changed to 10 days |
| A12 | `A12_dashboard_store262.png` | Store 262 with default settings |
| A13 | `A13_inventory_plan_summary.png` | Highest, lowest and overall summary of reorder points |

---

## 📊 Results

### Three dashboard views

| | Store 1 (lead 5) | Store 1 (lead 10) | Store 262 (lead 5) |
|---|---|---|---|
| Average daily demand | €3,303 | €3,303 | €19,917 |
| Safety stock | €4,935 | €6,979 | €13,951 |
| Reorder point | €21,452 | €40,014 | €113,534 |
| Order quantity | €46,249 | €46,249 | €278,832 |
| Store MAE (Apr to Jul 2015) | €753 | €753 | €2,185 |
| Store MAPE (Apr to Jul 2015) | 15.8% | 15.8% | 9.1% |

### What these show

- **The page follows the formulas.** Doubling the lead time from 5 to 10 days multiplied Store 1's safety stock by about 1.41 (4,935 to 6,979), which is the square root of 2, as the formula says. The reorder point rose and the order quantity did not change, which is also correct.
- **It handles very different stores.** Store 262 has about six times the demand of Store 1, and the same code gave a sensible plan for both.
- **Accuracy varies by store.** The model's percentage error was lower for Store 262 (9.1%) than for Store 1 (15.8%), even though the Euro error is larger for Store 262 because it sells more.

### Reorder points across all 1,115 stores (A13)

| Measure | Value |
|---|---|
| Highest | Store 262: €113,534 |
| 2nd highest | Store 1114: €99,346 |
| 3rd highest | Store 817: €91,282 |
| Lowest | Store 543: €11,620 |
| 2nd lowest | Store 198: €11,690 |
| Average | €32,446 |
| Median | €30,844 |
| 25th to 75th percentile | €25,211 to €37,354 |

---

## 🔧 Changes From the Task 4 Results

The dashboard numbers differ from Task 4 because **three things changed together**: the tuned model replaced the first XGBoost, the lead time is now 5 days instead of 7, and demand spread now uses forecast error instead of the spread of the predictions.

| Measure | Task 4 (older method) | Dashboard (current) |
|---|---|---|
| Store 1 reorder point | €36,277 | €21,452 |
| Store 262 reorder point | €133,986 | €113,534 |
| Average reorder point, all stores | €42,627 | €32,446 |
| Lowest reorder point | Store 841: €22,219 | Store 543: €11,620 |
| Store 1 average forecast demand | €4,025 per day | €3,303 per day |

Only the current column is used as a result in this submission. The two models also forecast different levels of demand for August 2015, and because the dataset ends on 31 July 2015 there is no real August data to say which is closer.

---

## 🔀 Deviations From the Approved Design

| Design | Implementation | Reason |
|---|---|---|
| The dashboard can trigger a new forecast request through the forecasting layer, described as REST-style endpoints | The dashboard reads forecasts that were prepared in advance. Only the inventory calculation runs live, using `src/inventory.py`. | Simpler and faster for a proof of concept, and the design itself notes that the proof of concept used direct function calls |
| Units sold per SKU | Euros of sales per store | Rossmann provides sales in Euros and no product-level units |
| Optional hosting on Streamlit Community Cloud | Runs locally only | Not required, and not completed in the time available |

---

## ⚠️ Limitations

1. The 30-day forecast assumes **no promotions and no school holidays**. Earlier analysis showed promotions raise sales by about 81%, so promotion days will be under-forecast.
2. Values are **Euros of sales, not units of stock**.
3. The forecasts could **not be checked against real August 2015 sales**.
4. The model was tested on **four months only** (April to July 2015).
5. The **order size (14 days)** and **service level (95%)** are assumptions that the user can change.
6. The dashboard has **not been tested with real users** and has **no automated test of its own yet**.
7. The dashboard does not re-train or call the model live. It shows pre-computed results.

---

## 🚀 Next Steps

- Run and record the automated tests, and capture the results as evidence
- Complete the defect log from the problems found during implementation
- Write the final Implementation and Testing/Evaluation report
- Build a Power BI version from the same four CSV files for a portfolio

---

## 🛠️ Tools Used

`Python` · `Streamlit` · `pandas` · `numpy` · `matplotlib` · `joblib` · `xgboost`

---
*📌 This report was generated as part of the Implementation Phase (Part 2) of the CPUT Data Science Capstone Project.*