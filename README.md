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
│   └── inventory_recommendations.csv  # Reorder point and safety stock per store
│
├── notebooks/                         # One notebook per task
│   ├── 01_data_cleaning.ipynb         # Task 1: Data Cleaning & Preparation
│   ├── data_cleaning_report.md        # Task 1: Full technical report
│   ├── data_cleaning_reflection.md    # Task 1: Personal reflection
│   ├── 02_EDA.ipynb                   # Task 2: Exploratory Data Analysis
│   ├── eda_report.md                  # Task 2: Full technical report
│   ├── eda_reflection.md              # Task 2: Personal reflection
│   ├── 03_modelling.ipynb             # Task 3: All 5 Forecasting Models
│   ├── modelling_report.md            # Task 3: Full technical report
│   ├── modelling_reflection.md        # Task 3: Personal reflection
│   ├── 04_inventory.ipynb             # Task 4: Inventory Optimisation Engine
│   ├── inventory_report.md            # Task 4: Full technical report
│   └── inventory_reflection.md        # Task 4: Personal reflection
│
├── models/                            # Saved trained models
│   ├── xgboost_model.pkl              # Best all-store model — 22.77% MAPE
│   └── label_encoder.pkl              # Saved LabelEncoder (holds the Assortment mapping only)
│
├── outputs/                           # Charts and visualisations
│   ├── 01_sales_over_time.png
│   ├── 02_sales_by_day.png
│   ├── 03_sales_by_month.png
│   ├── 04_promo_effect.png
│   ├── 05_sales_by_storetype.png
│   ├── 06_competition_distance.png
│   ├── 07_model_comparison.png
│   └── 09_stock_simulation_store1.png
│
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
| 5 | 🌐 Streamlit Interactive Dashboard | ⬜ Not Started |

### 🔴 Phase 3 — Deployment

| # | Task | Status |
|---|---|---|
| 6 | 🚀 Model Deployment & Final Submission | ⬜ Not Started |

---

## 🤖 Model Results Summary

Five models were trained and compared in `03_modelling.ipynb`:

| Model | MAE | RMSE | MAPE | Scope |
|---|---|---|---|---|
| Exponential Smoothing | €801 | €1,270 | 15.76% | Store 1 only |
| ARIMA | €1,381 | €2,020 | 17.63% | Store 1 only |
| LSTM | €1,477 | €1,924 | 19.97% | Store 1 only |
| **XGBoost ✅ Selected** | **€1,581** | **€2,384** | **22.77%** | **All 1,115 stores** |
| Random Forest | €1,739 | €2,668 | 26.28% | All 1,115 stores |

**Selected model: XGBoost** — best performance across all 1,115 stores simultaneously. Scales without retraining per store.

---

## 📦 Inventory Engine Summary

`04_inventory.ipynb` uses the saved XGBoost model to forecast 30 days of demand (1–30 August 2015) for all 1,115 stores, then calculates a **Reorder Point** and **Safety Stock** for each store.

| Measure | Value |
|---|---|
| Stores covered | 1,115 |
| Predictions generated | 33,450 |
| Assumed lead time | 7 days |
| Assumed service level | 95% (Z-score 1.65) |
| Average safety stock per store | €9,043 |
| Average reorder point per store | €42,627 |

**Formulas used:**
- Safety Stock = Z × Standard Deviation of demand × √Lead Time
- Reorder Point = Average Daily Demand × Lead Time + Safety Stock

**Known limitations** (full detail in `inventory_report.md`):
- Values are in **Euros of sales, not units of stock**
- **Sunday zeros** make demand look more variable, which inflates safety stock
- Future **promotions were assumed to be zero**
- Forecasts could not be checked against real August 2015 sales
- The stock simulation chart uses assumed starting stock and order size

---

## 🛠️ Tools & Technologies

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-3.0-darkblue?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-2.4-lightblue?logo=numpy)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-orange?logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-red?logo=xgboost)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)

Libraries used: `pandas` · `numpy` · `matplotlib` · `seaborn` · `scikit-learn` · `xgboost` · `statsmodels` · `tensorflow` · `joblib` · `streamlit`

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