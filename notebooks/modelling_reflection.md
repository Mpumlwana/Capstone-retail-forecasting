# 💭 Modelling Reflection — Task 3

*Task 3 — Forecasting Models | CPUT Data Science Capstone*
*Date Completed: August 2026*

---

## 🧠 What I Did

In this task I trained five different forecasting models on the Rossmann retail sales dataset — Random Forest, XGBoost, Exponential Smoothing, ARIMA, and LSTM. For each model I prepared the data in the format it required, trained it on data from January 2013 to March 2015, tested it on data from April to July 2015, and measured its accuracy using MAE, RMSE, and MAPE. I then compared all five models fairly and selected XGBoost as the recommended model for the system.

---

## 💡 What I Learned

### Feature engineering is as important as the model itself

Before I could train any model, I had to transform the data. Breaking the Date column into Year, Month, DayOfMonth, and WeekOfYear was not just a technical step — it was the step that made time patterns visible to the model. Without it, the model would have no way of knowing that December is always busier than January. I now understand that a great model trained on poorly engineered features will always lose to a simple model trained on well-engineered features.

### Different models need data in completely different formats

This was one of the biggest surprises of the task. Random Forest and XGBoost simply needed a flat table of rows and columns. Exponential Smoothing and ARIMA needed the Date column set as the index with a frequency tag. LSTM needed the data reshaped into 3D sequences and scaled between 0 and 1. Learning to prepare data for each model's specific requirements is a fundamental data science skill — not just knowing how to use the model itself.

### The train/test split must respect time

I now understand why a random split would have been wrong for this dataset. If I had randomly shuffled the data before splitting, the model might have trained on July 2015 data and been tested on January 2013 data — learning from the future to predict the past. In a real deployment that is impossible. The time-based split ensures the evaluation reflects how the model would actually perform in production.

### Comparing models requires a fair context

When Exponential Smoothing scored 15.76% MAPE and XGBoost scored 22.77%, my first instinct was to pick Exponential Smoothing. But looking more carefully, Exponential Smoothing only predicted one store while XGBoost predicted 1,115 stores simultaneously. The comparison was unfair as stated. This taught me that model selection is never just about the numbers — context always matters. A model that scores slightly worse but works at scale is often more valuable than one that scores perfectly on a single case.

### LSTM loss decreasing across epochs confirms real learning

Watching the LSTM training output — loss dropping from 0.1019 in epoch 1 to 0.0446 in epoch 10, with val_loss also dropping consistently — gave me a concrete understanding of what "a model learning" actually looks like in practice. The fact that validation loss decreased alongside training loss confirmed the model was not memorising — it was genuinely finding patterns that generalise to unseen data.

---

## 😤 Challenges I Faced

### The MAPE infinity problem

When I first ran Random Forest, MAPE showed as `inf%`. I did not immediately understand why. The reason was division by zero — some rows in the test set had Sales = 0 for closed stores, and dividing by zero produces infinity. The fix was to filter those rows out before calculating MAPE. This taught me to always check the edge cases in my data before applying formulas.

### Installing tensorflow

Tensorflow was not installed in my environment and had to be installed separately. It is a large package and took several minutes to download. This taught me that in professional data science environments, dependencies are managed carefully upfront so the team does not hit unexpected installation issues mid-project.

### Exponential Smoothing index error

The first attempt at training Exponential Smoothing failed with a ValueError about unsupported index. The fix was to set the Date column as the DataFrame index and assign a daily frequency tag. This taught me that statistical time series models have very specific expectations about how data is structured — they need to know the time spacing between observations before they can forecast forward.

### Duplicate results in the comparison table

When I first printed the comparison table, Exponential Smoothing and XGBoost each appeared twice because those cells had been run more than once, appending duplicate entries to the results list. I fixed this by rebuilding the results list manually from the known values. This taught me to be careful about notebook cell execution order — running a cell twice can have unintended side effects.

---

## 🔗 How This Connects to the Real Problem

Every model in this notebook was ultimately trying to answer one question for a small South African shop owner: how many units will I sell next week?

XGBoost's 22.77% MAPE means that on a day when the shop actually sells 100 units, the model predicts somewhere between 77 and 123 units on average. That is accurate enough to make a meaningful stock ordering decision. Without this model, the owner would guess — and guessing in retail leads to either running out of stock and losing sales, or overstocking and tying up cash in products that sit on shelves.

The promotion finding from EDA directly translated into model performance here. Because Promo was included as a feature, the model knows to predict significantly higher sales on promotion days. This is the single biggest contribution the model makes to the real business problem.

---

## 🔄 What I Would Do Differently

If I were repeating this task I would do two things differently.

First, I would tune the hyperparameters more carefully — particularly for XGBoost. We used default-ish settings (n_estimators=100, max_depth=6). Running a grid search across different combinations of these values would likely bring MAPE below 20% for the all-stores model.

Second, I would train Exponential Smoothing on all 1,115 stores and average the results, giving a fairer like-for-like comparison against XGBoost. This would tell us definitively whether the statistical approach beats machine learning when applied at the same scale.

---

## ➡️ What Comes Next

With the XGBoost model trained and saved, the next step is to use its predictions to build the inventory optimisation engine — calculating reorder points and safety stock levels for each store based on the forecasted demand. After that comes the Streamlit dashboard where a shop owner can enter their store details and receive a demand forecast and reorder recommendation in real time.

---
*📌 This reflection was written as part of Task 3 — Forecasting Models of the CPUT Data Science Capstone Project.*