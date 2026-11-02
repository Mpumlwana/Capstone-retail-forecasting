# 💭 Inventory Optimisation Reflection: Task 4

*Task 4: Inventory Optimisation Engine | CPUT Data Science Capstone*

---

## 🧠 What I Did

In this task I used the XGBoost model from Task 3 to forecast demand for all 1,115 stores for the 30 days after the dataset ends. I then turned those forecasts into a reorder point and a safety stock for every store, saved the results to a CSV file, and drew a stock simulation for Store 1 to see how the reorder rule behaves.

---

## 💡 What I Learned

### A forecast is only useful when it leads to a decision

In Task 3 the model told me how much a store would sell. That is not what a shop owner needs. They need to know when to order and how much buffer to keep. This task showed me how a forecast becomes an action through two numbers: the reorder point and the safety stock.

### Reorder point and safety stock mean different things

The **reorder point** is the stock level at which to place an order. It covers the demand expected during the delivery wait, plus the safety buffer. The **safety stock** is the extra cushion for demand that is higher than expected. A larger Z-score gives more protection but ties up more money in stock.

### A reorder point is a stock level, not a sales total

I first compared the reorder point with a chart of cumulative sales, and my explanation of that chart was wrong. Cumulative sales only goes up, so it cannot show when stock is low. The correct picture is a stock chart that falls as the store sells and jumps up when a delivery arrives. Drawing it the right way made the idea clear, and I now understand why the reorder point has to be compared with stock on hand.

### Saved models must be used exactly as they were trained

Loading the model reminded me that the inputs have to match training exactly: same 12 features, same order, same encoding. A model fed differently encoded data would give wrong answers without showing an error.

### Check claims before writing them

I assumed Store 4 was a type b store because its reorder point was high. When I checked, it was type c. High demand is not explained by store type alone. I learned to verify an explanation against the data before putting it in a report.

---

## 😤 Challenges I Faced

### Files saved with the wrong extension
Loading the model failed with `FileNotFoundError`. By listing the folder I found the files were saved as `.pk1` (number one) instead of `.pkl` (letter L). I renamed them. A small typo can stop a whole notebook, so checking file names is a habit I will keep.

### The label encoder did not work
`le.transform()` failed with an error about an unseen label `'d'`. In Task 3 I reused one LabelEncoder for two columns, so it only remembered the last one (Assortment). I fixed it by writing the mappings by hand with `.map()`, using the same numbers the model was trained on. In future I will use one encoder per column and save each one.

### Understanding the future feature table
Building 33,450 rows (1,115 stores × 30 days) with a loop took some thought. I had to decide what to do about information I do not have for the future, such as promotions. I assumed none, and I have noted this as a limitation.

---

## ⚠️ Limitations I Need to Be Honest About

- My numbers are **Euros of sales, not units of stock**, so they are not yet usable as a real order quantity.
- **Sunday zeros** make demand look more variable than it is, which makes safety stock larger than necessary.
- I **assumed no promotions** in August, but my EDA showed promotions raise sales by about 81%.
- I **could not check the forecasts against real August 2015 sales** because the dataset ends on 31 July.
- The **stock simulation** uses an assumed starting stock and order size. It illustrates the rule and is not a measured result.

---

## 🔗 How This Connects to the Real Problem

The problem I started with was a small shop owner guessing how much stock to order. This task is the first point where the system gives a concrete answer: a trigger level to order at and a buffer to keep. The numbers are not ready to use yet, because they are in Euros and not units, but the method is in place and the stock simulation shows how the rule behaves.

---

## 🔄 What I Would Do Differently

- Calculate the standard deviation on **trading days only**, so Sundays do not inflate the safety stock.
- Add **planned promotions** as an input when forecasting.
- Convert Euro values into **units** using product prices.
- Use a **separate encoder for each column** from the start, and save each one.

---

## ➡️ What Comes Next

The next step is the Streamlit dashboard, where a shop owner can pick a store, see the forecast, and see its reorder point and safety stock.

---
*📌 This reflection was written as part of Task 4: Inventory Optimisation Engine of the CPUT Data Science Capstone Project.*