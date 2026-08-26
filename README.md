🤖 Cape Peninsula University of Technology — Data Science Capstone

Welcome! This repository contains my full Capstone Project for the Postgraduate Diploma in ICT (AI and Data Science stream) at Cape Peninsula University of Technology — covering the complete data science pipeline, from data cleaning and exploratory analysis to machine learning, model evaluation and an interactive dashboard.

👋 About This Project

Small retail businesses across South Africa — from spaza shops to independent stores — make stock decisions based on gut feeling. This leads to two costly problems: overstocking ties up money in products that sit on shelves, while stockouts mean losing sales because shelves are empty.

This project builds an AI-Driven Retail Demand Forecasting and Inventory Optimisation System that analyses historical sales data, predicts future demand, and automatically calculates when and how much to reorder — so small business owners stop guessing and start making decisions backed by data.

For every task, you'll find:

🐍 A Jupyter notebook with all the code used to complete it
📊 Output files generated along the way (cleaned datasets, charts, saved models)
📝 A report (data_cleaning_report.md) covering everything done and why
💭 A reflection (data_cleaning_reflection.md) covering what I learned and challenges I faced
🗂️ Project Structure
Capstone-retail-forecasting/
│
├── data/                           # Raw and cleaned datasets (not uploaded to GitHub)
│   ├── train.csv                   # Rossmann daily sales — 1M+ records
│   ├── store.csv                   # Store characteristics and metadata
│   └── cleaned_data.csv            # Final merged and cleaned dataset
│
├── notebooks/                      # One notebook per task
│   ├── 01_data_cleaning.ipynb      # Task 1: Data Cleaning & Preparation
│   ├── data_cleaning_report.md     # Task 1: Full technical report
│   ├── data_cleaning_reflection.md # Task 1: Personal reflection
│   ├── 02_EDA.ipynb                # Task 2: Exploratory Data Analysis
│   └── 03_modelling.ipynb          # Task 3: Forecasting Models
│
├── models/                         # Saved trained models
├── outputs/                        # Charts and visualisations
└── README.md                       # You are here
✅ Tasks Overview
🟢 Phase 1 — Data Foundation
#	Task	Status
1	🧹 Data Cleaning & Preparation	✅ Done
2	🔍 Exploratory Data Analysis (EDA)	⏳ In Progress
🟡 Phase 2 — Modelling
#	Task	Status
3	📈 ARIMA Forecasting Model	⬜ Not Started
4	📉 Exponential Smoothing Model	⬜ Not Started
5	🌲 Random Forest Model	⬜ Not Started
6	⚡ XGBoost Model	⬜ Not Started
7	🧠 LSTM Neural Network	⬜ Not Started
🔴 Phase 3 — Deployment
#	Task	Status
8	🏆 Model Comparison & Selection	⬜ Not Started
9	📦 Inventory Optimisation Engine	⬜ Not Started
10	🌐 Streamlit Interactive Dashboard	⬜ Not Started
🛠️ Tools & Technologies

Show Image Show Image Show Image Show Image Show Image Show Image

Libraries used: pandas · numpy · matplotlib · seaborn · scikit-learn · xgboost · statsmodels · tensorflow · streamlit

📊 Dataset

Source: Rossmann Store Sales — Kaggle

This is a real-world retail dataset from Rossmann, a European pharmacy and retail chain with 1,115 stores. It contains daily sales records spanning over 2.5 years — making it ideal for training and validating demand forecasting models before applying the same pipeline to a South African retail context.

🎓 About CPUT

This capstone is part of the Postgraduate Diploma in ICT at Cape Peninsula University of Technology, Faculty of Informatics and Design, Department of Information Technology.

📬 Connect With Me

Feel free to connect or reach out if you'd like to discuss this project!

Lakhikhaya Mpumlwana Show Image

⭐ This repository is actively updated as tasks are completed throughout the capstone project.