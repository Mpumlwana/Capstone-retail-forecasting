# 💭 Exploratory Data Analysis Reflection — Task 2

*Task 2 — Exploratory Data Analysis | CPUT Data Science Capstone*
*Date Completed: August 2026*

---

## 🧠 What I Did

In this task I loaded the cleaned dataset from Task 1 and used Python to draw six charts that each answered a specific business question about Rossmann's retail sales. I explored how sales change over time, which days and months perform best, how promotions affect revenue, how store types differ, and whether nearby competition hurts sales. Each chart was saved into the outputs folder and will be used as evidence in the Testing Phase submission.

---

## 💡 What I Learned

### EDA is about asking questions, not just drawing charts

Before this task I thought EDA was simply about making visualisations. After completing it I understand that every chart must have a purpose — a specific business question it is designed to answer. A chart without a question is just decoration. A chart with a clear question is a business insight.

### The results were not always what I expected

The competition distance chart surprised me the most. I expected stores far from competitors to perform better — common sense suggests less competition means more customers for you. But the data showed the opposite: stores closest to competitors actually had the highest sales. Learning about the clustering effect changed how I think about retail competition entirely.

### Some features matter far more than others

Before drawing the charts, I assumed all features would contribute roughly equally to a forecast. After the EDA it is clear that `Promo` and `DayOfWeek` are dramatically more powerful than anything else. The 81% sales increase on promotion days and the 38-times difference between Monday and Sunday are not subtle signals — they are the dominant patterns in this entire dataset.

### Visualising data reveals things numbers alone cannot

When I looked at the raw numbers from describe() in Task 1, I could see the average sales were around €5,774. But I could not see the weekly Sunday dips, the Christmas spike, or the way promotions nearly double revenue. Charts turned those numbers into stories. This is why EDA always comes before modelling.

### groupby() is one of the most powerful pandas tools

Almost every chart in this notebook started with `df.groupby()`. This command groups rows by a category and calculates a summary for each group. Learning to think in terms of "group by X and then measure Y" is a fundamental data science skill I will use in every project going forward.

---

## 😤 Challenges I Faced

### The FutureWarning from seaborn

When drawing the promotions chart, seaborn showed a FutureWarning about the `palette` parameter being deprecated. I learned that warnings in Python are not the same as errors — the chart drew correctly. The fix was simple: add `hue=` and `legend=False` to the barplot call, which is the updated syntax seaborn now expects.

### Understanding scientific notation on the y-axis

The first chart showed values like `1e7` on the y-axis which I did not immediately understand. I learned that `1e7` means 10,000,000. Once I understood this, reading the chart became straightforward.

### Choosing the right bucket sizes for competition distance

When creating the competition distance chart I had to decide how to split distances into meaningful groups. I chose six buckets based on logical real-world distance thresholds — walking distance, short drive, medium distance, and far away. This required thinking about what the distances actually mean in a retail context, not just picking arbitrary numbers.

---

## 🔗 How This Connects to the Real Problem

Every chart in this notebook serves one ultimate purpose — helping a small South African retail business owner make better stock decisions.

The promotion finding is the most directly actionable. If a shop owner is planning a promotion next week, our model will predict demand approximately 81% higher than a normal day. That means they need to order significantly more stock in advance. Without this insight, they would order normal quantities, run out mid-promotion, and lose exactly the sales they were trying to generate.

The day-of-week finding is equally important. Knowing Mondays are consistently the busiest means a small business should ensure maximum stock at the start of each week. A model that treats all days equally will understock on Mondays and overstock on quieter days — exactly the problem this project is designed to solve.

---

## 🔄 What I Would Do Differently

If I were repeating this task I would add two more charts. First, a chart showing sales by `Assortment` type to check whether the product range a store carries affects its performance. Second, a correlation heatmap showing which numeric features are most strongly related to sales — this would give mathematical confirmation of the visual patterns and make feature selection for Task 3 more rigorous.

---

## ➡️ What Comes Next

With the EDA complete, I now know which features matter most: `Promo`, `DayOfWeek`, `StoreType`, and `Month`. The next task is to train and compare five forecasting models — ARIMA, Exponential Smoothing, Random Forest, XGBoost, and LSTM — and select the best performer based on MAE, RMSE, and MAPE.

---
*📌 This reflection was written as part of Task 2 — Exploratory Data Analysis of the CPUT Data Science Capstone Project.*