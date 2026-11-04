# 💭 Implementation Reflection: Modules, Baseline and Tuning

*Implementation Phase, Part 1 | CPUT Data Science Capstone*

---

## 🧠 What I Did

I moved my notebook code into four modules that match my Design Phase, checked each one against a result I worked out by hand, built a seasonal-naive baseline, and tuned XGBoost after it missed my accuracy goal.

---

## 💡 What I Learned

### Notebook code is not the same as a designed system
My design had five modules, but my work was in notebooks. Writing the modules showed me that a notebook is a workbook, while modules can be reused by the dashboard and by tests.

### A model must beat a simple guess
The seasonal-naive baseline ("same as last week") scored 34.59% MAPE. The tuned XGBoost scored 15.03%. Without the baseline I would not know whether my model is actually good.

### Three roles for data
Training data teaches the model, validation data helps me choose settings, and test data is used once at the end. If I chose settings by looking at the test results, the final score would not be honest.

### Early stopping tells me when a search is too small
In round 1 every model used all 400 trees, so early stopping never triggered. That told me my search was cut short. Round 2 fixed it.

### Check my work against the design
Comparing my Task 4 notebook with my Design Phase showed three differences, including the way I calculated safety stock. I had used the spread of the predictions, but my design uses the forecast error. I fixed it and wrote down the change.

### Check results by hand
Each module was tested with a small example that I calculated by hand first. When the program gave the same numbers, I could trust the code.

---

## 😤 Challenges I Faced

- **The split error.** A confusing line of code split my data at its first date, which left nothing for training. The guard I wrote in `time_split` stopped it with a clear message. I kept it as evidence of an edge-case test.
- **Understanding tuning.** I got lost when too many new ideas came at once. Thinking of it as practice questions, a mock test and a real exam helped.

---

## ⚠️ Limitations I Need to Be Honest About

- My 20% threshold is an assumption. My design does not give a number.
- The test period is only four months.
- My other four models have not yet been compared with XGBoost on the same data.
- My numbers are in Euros, not units.

---

## 🔗 How This Connects to the Real Problem

A shop owner will only trust a forecast if it is clearly better than guessing. The tuned model is about 52.6% better than a "same as last week" guess, measured by average error. The modules also mean the dashboard can use the same trusted code.

---

## 🔄 What I Would Do Differently

I would write the modules and their checks at the start, before building the notebook. I would also write my accuracy threshold down before running any model.

---

## ➡️ What Comes Next

The live dashboard, the automated tests, and a fair comparison of all five models on the same store.

---
*📌 This reflection was written as part of the Implementation Phase (Part 1) of the CPUT Data Science Capstone Project.*