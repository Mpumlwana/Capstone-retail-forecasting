# 📊 Exploratory Data Analysis Report — Rossmann Retail Sales

*Task 2 — Exploratory Data Analysis | CPUT Data Science Capstone*

---

## 📦 Dataset Overview

- 🏪 **1,115 stores** across Germany — daily sales records
- 📅 **Date range:** 1 January 2013 — 31 July 2015 (2 years and 7 months)
- 🔢 **Total records analysed:** 1,017,155
- 💶 **Average daily sales per store:** €5,774
- ✅ Source: `cleaned_data.csv` — fully cleaned and merged dataset from Task 1

---

## 🎯 Purpose of EDA

Before building any forecasting model, we need to deeply understand the data. EDA answers the question: *what patterns exist in this data that a model should learn from?* Each chart in this task was designed to answer a specific business question about Rossmann's retail sales behaviour.

---

## 📈 Chart 1 — Total Daily Sales Over Time

**Business question:** How do sales trend across 2.5 years, and are there obvious seasonal patterns?

### Key Findings:
- **Regular weekly dips to near zero** appear throughout the entire dataset — these are Sundays when almost all Rossmann stores in Germany are closed
- **A major spike around January 2014** reaching approximately €16 million in a single day across all stores — this is the Christmas and New Year period
- **Smaller spikes around mid-2013 and mid-2014** correspond to Easter periods
- **The overall baseline is stable** — normal trading days consistently generate between €6 million and €12 million total across all stores

### Implication for Model:
The model must learn three recurring patterns: the weekly Sunday low, the annual Christmas spike, and the Easter bump.

---

## 📅 Chart 2 — Average Sales by Day of Week

**Business question:** Which days of the week are consistently the busiest?

### Key Findings:

| Day | Average Sales | Observation |
|---|---|---|
| Monday | €7,809 | Busiest day — captures Sunday overflow demand |
| Tuesday | ~€7,000 | Strong trading day |
| Wednesday | ~€6,600 | Slightly quieter mid-week |
| Thursday | ~€6,200 | Quietest weekday |
| Friday | ~€6,700 | Small bump before the weekend |
| Saturday | ~€5,800 | Shorter trading hours reduce sales |
| Sunday | €204 | Near zero — almost all stores closed |

### Implication for Model:
`DayOfWeek` is one of the most powerful predictive features. Monday is 38 times higher than Sunday.

---

## 📆 Chart 3 — Average Sales by Month

**Business question:** Are there consistent seasonal patterns across the calendar year?

### Key Findings:
- **December is the peak month** — averaging €6,800 per store per day
- **July shows a clear bump** — around €6,000, likely summer holiday shopping
- **November begins the pre-Christmas build-up**
- **January and May are the quietest months**

### Implication for Model:
Month is a useful but moderate feature — 26% range between best and worst month.

---

## 🏷️ Chart 4 — Effect of Promotions on Sales

**Business question:** Do promotions actually increase sales, and by how much?

### Key Findings:

| Condition | Average Sales | Difference |
|---|---|---|
| No Promotion | €4,406 | Baseline |
| Promotion Running | €7,992 | **+81% increase** |

### Implication for Model:
`Promo` is the strongest feature in the dataset. An 81% sales increase on promotion days means any model that ignores promotions will be dramatically inaccurate.

---

## 🏪 Chart 5 — Average Sales by Store Type

**Business question:** Do different store formats perform differently?

### Key Findings:

| Store Type | Average Sales | Observation |
|---|---|---|
| a | ~€5,750 | Standard performance |
| b | ~€10,061 | Nearly double every other type |
| c | ~€5,700 | Standard performance |
| d | ~€5,600 | Standard performance |

### Implication for Model:
`StoreType` is a strong feature — type b stores behave fundamentally differently from the rest.

---

## 🏙️ Chart 6 — Competition Distance vs Sales

**Business question:** Does having a competitor nearby hurt a store's sales?

### Key Findings:
- **Stores with competitors closest (0–500m) actually have the highest average sales** — around €6,200
- **Sales remain relatively flat across all distance ranges**
- The clustering effect explains this — competing stores grouped together attract more overall foot traffic

### Implication for Model:
`CompetitionDistance` is a weak feature — small variation across all distance ranges.

---

## 🔍 Summary of Key Findings

| Feature | Effect on Sales | Model Priority |
|---|---|---|
| Promo | +81% on promotion days | ⭐⭐⭐⭐⭐ Critical |
| DayOfWeek | Monday 38x higher than Sunday | ⭐⭐⭐⭐⭐ Critical |
| StoreType | Type b earns 74% more than average | ⭐⭐⭐⭐ Strong |
| Month | December 26% above January | ⭐⭐⭐ Moderate |
| CompetitionDistance | Less than 15% variation across all ranges | ⭐ Weak |

---

## 🚀 Next Steps

- Use EDA findings to guide feature selection in `03_modelling.ipynb`
- Include `Promo`, `DayOfWeek`, `StoreType`, and `Month` as priority features
- Train and compare 5 forecasting models: ARIMA, Exponential Smoothing, Random Forest, XGBoost, LSTM
- Select the best model based on MAE, RMSE, and MAPE

---

## 🛠️ Tools Used

`Python` · `pandas` · `numpy` · `matplotlib` · `seaborn` · `Jupyter Notebook`

---
*📌 This report was generated as part of Task 2 — Exploratory Data Analysis of the CPUT Data Science Capstone Project.*