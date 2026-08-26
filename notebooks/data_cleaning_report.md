# 🧹 Data Cleaning Report — Rossmann Retail Sales Dataset

*Task 1 — Data Cleaning & Preparation | CPUT Data Science Capstone*

---

## 📦 Dataset Overview

- 🏪 **1,115 stores** across Germany, recorded daily over 2.5 years
- 📅 **Date range:** 1 January 2013 — 31 July 2015
- 📋 **Two files loaded:** `train.csv` (sales records) and `store.csv` (store info)
- 🔢 **Raw rows:** 1,017,209 in train | 1,115 in store
- ✅ **Final cleaned rows:** 1,017,155 across 18 columns after merging

---

## 📂 Files Loaded

| File | Rows | Columns | Description |
|---|---|---|---|
| `train.csv` | 1,017,209 | 9 | Daily sales records per store |
| `store.csv` | 1,115 | 10 | Store characteristics and metadata |
| `cleaned_data.csv` | 1,017,155 | 18 | Final merged and cleaned output |

---

## 🛠️ Cleaning Steps Performed

### ⚠️ Step 1 — Fix Mixed Data Type Warning

The `StateHoliday` column contained mixed data — some rows stored as numbers, some as letters. Pandas raised a `DtypeWarning` on load.

**Fix:** Reloaded the file with two extra parameters:
- `low_memory=False` — reads the full file before deciding column types
- `dtype={'StateHoliday': str}` — forces StateHoliday to always load as text

**Result:** Warning resolved ✅

---

### 🔍 Step 2 — Missing Values Check

**Train file — perfectly clean:**

| Column | Missing Values |
|---|---|
| All 9 columns | 0 |

**Store file — several columns affected:**

| Column | Missing | % | Fix Applied |
|---|---|---|---|
| CompetitionDistance | 3 | 0.27% | Filled with median distance |
| CompetitionOpenSinceMonth | 354 | 31.75% | Filled with 0 (unknown) |
| CompetitionOpenSinceYear | 354 | 31.75% | Filled with 0 (unknown) |
| Promo2SinceWeek | 544 | 48.79% | Filled with 0 (not applicable) |
| Promo2SinceYear | 544 | 48.79% | Filled with 0 (not applicable) |
| PromoInterval | 544 | 48.79% | Filled with "None" (not applicable) |

**Reasoning:**
- `CompetitionDistance` — only 3 stores affected, median used to avoid distortion from extreme values
- `CompetitionOpenSince` columns — opening date simply unknown, filled with 0 as placeholder
- `Promo2` columns — naturally empty for the 544 stores that do not run a recurring promotion

**Result:** All missing values resolved ✅

---

### 👯 Step 3 — Duplicate Records

| File | Duplicates Found | Action |
|---|---|---|
| train.csv | 0 | None required |
| store.csv | 0 | None required |

**Result:** No duplicates anywhere ✅

---

### 📅 Step 4 — Date Column Type Fix

The `Date` column was stored as plain text (`str`). Python cannot extract time-based patterns from a text column — it cannot understand months, seasons or the distance between two dates.

**Fix:** Converted using `pd.to_datetime()`

| Before | After |
|---|---|
| `str` (plain text) | `datetime64` (real date) |

**Date range confirmed:** 1 January 2013 → 31 July 2015 ✅

---

### 🚫 Step 5 — Remove Illogical Records

Four logical checks were performed on the train data:

| Check | Result | Action |
|---|---|---|
| Closed stores showing sales | 0 rows | None required |
| Open stores with zero sales | 54 rows | ⚠️ Removed |
| Negative sales values | 0 rows | None required |
| Negative customer counts | 0 rows | None required |

**Why the 54 rows were removed:** A store marked as open with zero sales does not represent a real trading day. Keeping these rows would teach the model that open stores sometimes earn nothing — a misleading pattern that would reduce forecast accuracy.

**Result:** 54 rows removed, 1,017,155 clean rows remaining ✅

---

### 📊 Step 6 — Statistical Validation

Key statistics were checked to confirm all values are realistic:

**Sales (Euros):**

| Statistic | Value |
|---|---|
| Average daily sales | €5,774 |
| Minimum | €0 |
| Maximum | €41,551 |
| Standard deviation | €3,849 |

**Customers:**

| Statistic | Value |
|---|---|
| Average daily customers | 633 |
| Minimum | 0 |
| Maximum | 7,388 |

**Competition Distance (metres):**

| Statistic | Value |
|---|---|
| Average distance | 5,397m |
| Closest competitor | 20m |
| Furthest competitor | 75,860m |

✅ All values are realistic — no further action required

---

### 🔗 Step 7 — Merge the Two Files

The cleaned `train` and `store` files were merged into one dataset using the `Store` column as the shared key. A left join was used to keep all sales records and attach the matching store information to each row.

| Before merge | After merge |
|---|---|
| Train: 9 columns | Combined: 18 columns |
| Store: 10 columns | Rows unchanged: 1,017,155 |

---

## 🔍 Key Insights

1. 📋 **Train data was cleaner than expected** — zero missing values and zero duplicates is rare in real-world datasets. Rossmann clearly maintained consistent daily recording across all stores.
2. 🏪 **Store data reflected real business diversity** — the CompetitionDistance range from 20m to 75,860m shows Rossmann operates in very different environments, from busy city centres to isolated rural areas.
3. ⚠️ **Not all missing values are errors** — the 544 missing Promo2 values were not gaps in data quality but simply stores that do not run recurring promotions. Understanding context before fixing is critical.
4. 📅 **Date format matters enormously** — a date stored as text is useless for a forecasting model. Converting it to datetime unlocks the ability to extract months, seasons and weekly cycles.

---

## 💾 Output

The final cleaned and merged dataset was saved as:
data/cleaned_data.csv


This file is the starting point for all subsequent notebooks.

---

## 🚀 Next Steps

- Load `cleaned_data.csv` in `02_EDA.ipynb`
- Visualise sales trends over time, by store type, and by promotion status
- Identify seasonal patterns and weekly cycles that will inform feature engineering
- Check the relationship between competition distance and sales performance

---

## 🛠️ Tools Used

`Python` · `pandas` · `numpy` · `Jupyter Notebook`

---
*📌 This report was generated as part of Task 1 — Data Cleaning & Preparation of the CPUT Data Science Capstone Project.*