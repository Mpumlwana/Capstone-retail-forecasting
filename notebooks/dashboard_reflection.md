# 💭 Dashboard Reflection: Live Reorder Planner

*Implementation Phase, Part 2 | CPUT Data Science Capstone*

---

## 🧠 What I Did

I turned the static dashboard picture from my Design Phase into a working Streamlit page. First I prepared the results for all 1,115 stores into four small files. Then I built a page where a store manager picks a store, changes the lead time, service level and order size, and sees the forecast, how accurate the model was, and the reorder plan.

---

## 💡 What I Learned

### A dashboard should run tested code, not just show a picture
When I changed the lead time from 5 to 10 days, the safety stock grew by about 1.41 times, which is the square root of 2, exactly as the formula says. That showed me the page is using the same inventory module I checked by hand, so what the manager sees comes from code I can trust.

### Prepare once, show many times
Running the model for every store each time someone opens the page would be slow. Preparing the results into small files first makes the page fast, and it means the dashboard is easy to run on another computer.

### Test with very different examples
I tried Store 1 and Store 262. Store 262 sells about six times as much, and the same code worked for both. Checking more than one case gave me more confidence than checking only one.

### Results must be compared fairly
Store 262 has a bigger Euro error than Store 1, but a smaller percentage error. The percentage is the fair way to compare stores of different sizes.

### New results replace old results
My dashboard numbers are different from Task 4. Three things changed together: the model, the lead time and the way I measure demand spread. I now know I must only use the current numbers in my report and explain why the old ones changed.

### Folder names can hide files
My `.gitignore` ignores any folder called `data`. If I had saved the dashboard files in `app/data`, they would never have reached GitHub, and the page would not run for anyone else. I called the folder `dashboard_data` and checked with `git ls-files` that all five files were tracked.

---

## 😤 Challenges I Faced

- **Choosing the tool.** I asked whether to use Power BI instead. My approved design names Streamlit, the formulas would have had to be rewritten in another language, and a marker could not run a Power BI file without the software. I kept Streamlit and I plan to build a Power BI version afterwards for my portfolio.
- **Too many new ideas at once.** In the tuning step I got lost. Using the story of practice questions, a mock test and a real exam helped me understand it.

---

## ⚠️ Limitations I Need to Be Honest About

- The forecast assumes no promotions, but promotions raise sales by about 81%.
- The values are Euros of sales, not units of stock.
- I could not check the August forecasts against real August data.
- The dashboard shows pre-computed results. It does not call the model live like my design describes.
- I have not tested it with real users yet, and it has no automated test of its own.

---

## 🔗 How This Connects to the Real Problem

The real problem was a small shop owner guessing when to order stock. This page lets them pick a store and see when to reorder, with the settings they can change. The numbers are not ready to use as real orders because they are in Euros, but the full path from data to a decision now works.

---

## 🔄 What I Would Do Differently

- Build the dashboard data step earlier, so I could test with real screens sooner.
- Add a promotion switch to the dashboard, so the manager can plan for promotion days.
- Ask a real shop owner to try it.

---

## ➡️ What Comes Next

Automated tests with saved results, the defect log, and the final report for the Implementation and Testing/Evaluation submission.

---
*📌 This reflection was written as part of the Implementation Phase (Part 2) of the CPUT Data Science Capstone Project.*