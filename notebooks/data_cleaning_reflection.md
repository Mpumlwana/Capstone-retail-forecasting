# 💭 Data Cleaning Reflection — Task 1

*Task 1 — Data Cleaning & Preparation | CPUT Data Science Capstone*

---

## 🧠 What I Did

In this task I loaded the Rossmann Store Sales dataset from Kaggle — over one million daily sales records from 1,115 retail stores. I worked with two separate files, inspected both for quality issues, fixed every problem I found, merged them into one complete dataset, and saved the result ready for analysis. Every decision I made is documented in the report.

---

## 💡 What I Learned

### Real data always has problems — even "clean" datasets

I assumed a Kaggle competition dataset would be ready to use. It was not. It had mixed data types, missing values across multiple columns, a date stored as plain text, and rows that were logically impossible. This taught me to always inspect data before touching it, no matter where it comes from.

### Missing values have different meanings

Before this task I thought every missing value meant something went wrong. Now I understand they fall into two categories:

- **Genuinely unknown** — like the 3 missing competition distances. The data should exist but was never recorded.
- **Not applicable** — like the 544 missing Promo2 values. Those stores simply do not run recurring promotions, so there is nothing to record.

Treating both the same way would have been wrong. The fix you choose must match the reason the value is missing.

### Data types are not just technical details

The `Date` column looked perfectly fine to me — "2015-07-31" makes complete sense as a date. But Python saw it as just a word. It could not calculate the distance between two dates or extract the month from it. Converting it to `datetime64` was a small change that unlocked everything the forecasting model will need to understand time patterns.

### Always confirm your fixes worked

After fixing the missing values I ran the missing value check again to confirm every column showed zero. This habit — verifying after every fix — is something I will carry into every task going forward. No assumption, only evidence.

---

## 😤 Challenges I Faced

### File path error on load

The biggest early frustration was a `FileNotFoundError` when loading the CSV files. Python was looking in the wrong folder because my notebook was not running from the expected location. I solved it by running `os.getcwd()` to check exactly where Python was working from, then adjusted the paths accordingly. It taught me that knowing where your code runs is just as important as the code itself.

### ChainedAssignmentError in pandas 3.0

When I tried to fix missing values using `inplace=True`, pandas threw a `ChainedAssignmentError`. In newer versions of pandas this approach no longer works — you must reassign the result back to the column directly. Once I understood why — pandas now uses copy-on-write to protect data integrity — the fix made sense and I updated every line accordingly.

---

## 🔗 How This Connects to the Real Problem

Everything in this notebook serves one purpose — making sure the forecasting model learns from data that is accurate and trustworthy.

If I had left the date as text, the model could not learn seasonal patterns. If I had left the missing values unfixed, it would have gaps in its understanding of certain stores. If I had kept the 54 illogical rows, it would have learned that open stores sometimes earn nothing — which is not true and would have weakened its predictions.

A small shop owner in South Africa is going to trust this system to tell them when to reorder stock. That trust is only justified if the model learned from clean, honest data. That is why this task matters.

---

## 🔄 What I Would Do Differently

If I were repeating this task I would write a single `validate_data()` function at the start that runs all checks — missing values, duplicates, data types and logical consistency — in one go rather than as separate cells. This would make it faster to rerun on new data and easier for someone else reading the notebook to follow the logic.

---

## ➡️ What Comes Next

With `cleaned_data.csv` saved, the next step is **Exploratory Data Analysis** in `02_EDA.ipynb`. I will visualise sales trends over time, explore how promotions affect revenue, identify seasonal and weekly patterns, and understand how store characteristics relate to performance. These insights will directly shape the features used to train the forecasting models.

---
*📌 This reflection was written as part of Task 1 — Data Cleaning & Preparation of the CPUT Data Science Capstone Project.*