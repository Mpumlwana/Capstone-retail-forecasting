# 🤖 Cape Peninsula University of Technology — Data Science Capstone

Welcome! This repository contains my full Capstone Project for the **Postgraduate Diploma in ICT (AI and Data Science stream)** at Cape Peninsula University of Technology — covering the complete data science pipeline, from data cleaning and exploratory analysis to machine learning, model evaluation and an interactive dashboard.

---

## 👋 About This Project

Small retail businesses across South Africa — from spaza shops to independent stores — make stock decisions based on gut feeling. This leads to two costly problems: overstocking ties up money in products that sit on shelves, while stockouts mean losing sales because shelves are empty.

This project builds an **AI-Driven Retail Demand Forecasting and Inventory Optimisation System** that analyses historical sales data, predicts future demand, and automatically calculates when and how much to reorder — so small business owners stop guessing and start making decisions backed by data.

For every task, you'll find:

- 🐍 A Jupyter notebook with all the code used to complete it
- 📊 Output files generated along the way (cleaned datasets, charts, saved models)
- 📝 A report covering everything done and why
- 💭 A reflection covering what I learned and challenges I faced

---

## 🗂️ Project Structure

```
Capstone-retail-forecasting/
│
├── data/                              # Datasets (not uploaded to GitHub)
│   ├── train.csv                      # Rossmann daily sales — 1M+ records
│   ├── store.csv                      # Store characteristics and metadata
│   ├── cleaned_data.csv               # Final merged and cleaned dataset
│   └── inventory_recommendations.csv  # Task 4 output (older method, kept as history)
│
├── src/                               # Reusable modules, matching the Design Phase
│   ├── features.py                    # Module 1: Feature Engineering
│   ├── forecasting.py                 # Module 2: time split + XGBoost tuning
│   ├── evaluation.py                  # Module 3: MAE / RMSE / MAPE, baseline, model selection
│   ├── inventory.py                   # Module 4: safety stock, reorder point, order quantity
│   └── build_dashboard_data.py        # Prepares the four files the dashboard reads
│
├── app/                               # Module 5: Dashboard
│   ├── app.py                         # Streamlit dashboard
│   └── dashboard_data/                # Small CSV files the dashboard reads
│
├── tests/                             # Automated tests (pytest), being added
│
├── notebooks/                         # One notebook per task
│   ├── 01_data_cleaning.ipynb         # Task 1: Data Cleaning & Preparation
│   ├── data_cleaning_report.md
│   ├── data_cleaning_reflection.md
│   ├── 02_EDA.ipynb                   # Task 2: Exploratory Data Analysis
│   ├── eda_report.md
│   ├── eda_reflection.md
│   ├── 03_modelling.ipynb             # Task 3: 5 Forecasting Models
│   ├── modelling_report.md
│   ├── modelling_reflection.md
│   ├── 04_inventory.ipynb             # Task 4: Inventory Optimisation Engine
│   ├── inventory_report.md
│   ├── inventory_reflection.md
│   ├── 05_implementation_evaluation.ipynb  # Implementation Part 1: baseline + tuning
│   ├── implementation_report.md
│   ├── implementation_reflection.md
│   ├── dashboard_report.md            # Implementation Part 2: dashboard
│   └── dashboard_reflection.md
│
├── models/                            # Saved trained models
│   ├── xgboost_model.pkl              # Task 3 settings — 22.77% MAPE
│   ├── xgboost_tuned.pkl              # Tuned model — 15.03% MAPE
│   └── label_encoder.pkl              # Saved LabelEncoder (holds the Assortment mapping only)
│
├── evidence/                          # Screenshots of test, evaluation and dashboard results
├── outputs/                           # Charts and visualisations
├── requirements.txt                   # Python packages needed by src/ and app/
└── README.md                          # You are here
```

---

## ✅ Tasks Overview

### 🟢 Phase 1 — Data Foundation

| # | Task | Status |
|---|---|---|
| 1 | 🧹 Data Cleaning & Preparation | ✅ Done |
| 2 | 🔍 Exploratory Data Analysis (EDA) | ✅ Done |

### 🟢 Phase 2 — Modelling & Inventory

| # | Task | Status |
|---|---|---|
| 3 | 🤖 Model Training & Comparison (5 models) | ✅ Done |
| 4 | 📦 Inventory Optimisation Engine | ✅ Done |

### 🟡 Phase 3 — Implementation & Testing/Evaluation

| # | Task | Status |
|---|---|---|
| 5 | 🧩 Reusable modules in `src/` (design modules 1–4) | ✅ Done |
| 6 | 📏 Seasonal-naive baseline + tuning (REQ-002, REQ-006) | ✅ Done |
| 7 | 🌐 Streamlit Interactive Dashboard (REQ-004) | ✅ Done (runs locally) |
| 8 | 🧪 Automated tests and defect log | ⏳ In Progress |
| 9 | 📝 Final Implementation & Testing/Evaluation report | ⬜ Not Started |

---

## 🤖 Results

### Implementation results (test set: April to July 2015)

| Model | MAE | RMSE | MAPE |
|---|---|---|---|
| Seasonal naive (baseline: same as last week) | €2,369 | €3,541 | 34.59% |
| XGBoost (Task 3 settings) | €1,581 | €2,384 | 22.77% |
| **XGBoost (tuned) ✅ Selected** | **€1,122** | **€1,977** | **15.03%** |

- All three were scored on the **same 136,027 rows** (2 rows with no sale 7 days earlier were left out for every model).
- The tuned settings were chosen on **validation data (Jan–Mar 2015)**, and the test set was scored **once**.
- The 20% MAPE threshold used for selection is a **project assumption**, because the Design Phase gives no number.

### Task 3 five-model comparison (history)

| Model | MAE | RMSE | MAPE | Scope |
|---|---|---|---|---|
| Exponential Smoothing | €801 | €1,270 | 15.76% | Store 1 only |
| ARIMA | €1,381 | €2,020 | 17.63% | Store 1 only |
| LSTM | €1,477 | €1,924 | 19.97% | Store 1 only |
| XGBoost | €1,581 | €2,384 | 22.77% | All 1,115 stores |
| Random Forest | €1,739 | €2,668 | 26.28% | All 1,115 stores |

⚠️ This table is **not like-for-like**: three models were scored on Store 1 only and two on all stores. A fair comparison on the same data is still to be done.

---

## 🌐 Dashboard

A live Streamlit page where a store manager picks a store and sees its forecast, how accurate the model was, and its reorder plan.

**What the user can change:** store, supplier lead time (1–14 days), service level (90% / 95% / 99%) and how many days of demand one order covers (7–28).

**What the user sees:** average daily demand, safety stock, reorder point, order quantity, a 30-day forecast chart, an actual-vs-predicted chart with that store's error, the model comparison table, and a list of assumptions.

The reorder plan on screen is calculated live by `src/inventory.py`.

| | Store 1 (lead 5) | Store 1 (lead 10) | Store 262 (lead 5) |
|---|---|---|---|
| Average daily demand | €3,303 | €3,303 | €19,917 |
| Safety stock | €4,935 | €6,979 | €13,951 |
| Reorder point | €21,452 | €40,014 | €113,534 |
| Order quantity | €46,249 | €46,249 | €278,832 |

Screenshots are in `evidence/` (A09 to A13).

---

## 📦 Inventory Plan (current method)

`src/build_dashboard_data.py` uses the **tuned** model to forecast 30 days (1–30 August 2015) for all 1,115 stores and calculates a plan for each, following the approved Design Phase.

| Measure | Value |
|---|---|
| Stores covered | 1,115 |
| Lead time | 5 days (adjustable) |
| Service level | 95% (Z-score 1.65, adjustable) |
| Average reorder point per store | €32,446 |
| Median reorder point per store | €30,844 |
| Highest reorder point | Store 262: €113,534 |
| Lowest reorder point | Store 543: €11,620 |

**Formulas:**
- Safety Stock = Z × Standard Deviation of forecast error × √Lead Time
- Reorder Point = Average Daily Demand × Lead Time + Safety Stock
- Order Quantity = Average Daily Demand × Review Period (14 days is an assumption)

🕰️ **History:** the Task 4 notebook used the first XGBoost model, a 7-day lead time and the spread of the predictions, which gave an average reorder point of €42,627. Those numbers are superseded by the table above.

**Known limitations:**
- Values are in **Euros of sales, not units of stock**
- The 30-day forecast assumes **no promotions and no school holidays**
- Forecasts could not be checked against real August 2015 sales
- The test period covers four months, not a full year
- The dashboard shows pre-computed results and does not call the model live

---

## 🛠️ Tools & Technologies

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-3.0-darkblue?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-2.4-lightblue?logo=numpy)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-orange?logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-red?logo=xgboost)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)

Libraries used: `pandas` · `numpy` · `matplotlib` · `seaborn` · `scikit-learn` · `xgboost` · `statsmodels` · `tensorflow` · `joblib` · `streamlit` · `pytest`

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Mpumlwana/Capstone-retail-forecasting.git
   cd Capstone-retail-forecasting
   ```
2. Install the packages for the modules and dashboard:
   ```bash
   pip install -r requirements.txt
   ```
   Notebook 03 also needs `statsmodels` and `tensorflow`, and the notebooks need `jupyter` and `seaborn`.
3. **To run only the dashboard:** the four files it reads are already in `app/dashboard_data/`:
   ```bash
   python -m streamlit run app/app.py
   ```
4. **To rebuild everything from the raw data:** download `train.csv` and `store.csv` from Kaggle into a `data/` folder, run notebook `01_data_cleaning.ipynb` (it creates `data/cleaned_data.csv`), then:
   ```bash
   python -m src.build_dashboard_data
   ```
5. **To run the automated tests** (once added):
   ```bash
   python -m pytest tests -v
   ```

---

## 📊 Dataset

**Source:** [Rossmann Store Sales — Kaggle](https://www.kaggle.com/competitions/rossmann-store-sales/data)

This is a real-world retail dataset from Rossmann, a European pharmacy and retail chain with 1,115 stores. It contains daily sales records spanning over 2.5 years — making it ideal for training and validating demand forecasting models before applying the same pipeline to a South African retail context.

---

## 🎓 About CPUT

This capstone is part of the **Postgraduate Diploma in ICT** at [Cape Peninsula University of Technology](https://www.cput.ac.za), Faculty of Informatics and Design, Department of Information Technology.

---

## 📬 Connect With Me

Feel free to connect or reach out if you'd like to discuss this project!

**Lakhikhaya Mpumlwana**
[![GitHub](https://img.shields.io/badge/GitHub-Mpumlwana-black?logo=github)](https://github.com/Mpumlwana)

---

⭐ *This repository is actively updated as tasks are completed throughout the capstone project.*