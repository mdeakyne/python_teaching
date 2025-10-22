# Day 7: Time Series Basics – Daily Book Sales Trends

## Introduction
Imagine you’re the analytics lead at **Page Turner Analytics**. The CEO wants to know how book sales are trending over time—are weekends better than weekdays, do certain months always outperform others, and how stable are sales week-to-week?  
Building on what you’ve already learned—cleaning strings, grouping data, calculating summaries—we’ll add something new: **time series analysis**.  
By the end of this lesson, you’ll know how to parse dates, resample sales data into weekly and monthly totals, and calculate rolling averages to spot trends at a glance.

---

## Core Content

### 1. Parsing Datetime Columns
In our `sales.csv`, the `date` column currently stores dates as strings.  
To work with time series in pandas, we need to convert this column to a **datetime** object and set it as our index.

Why does this matter?  
Imagine trying to analyze "weekly trends" without an actual date type—you’d be stuck doing messy string slicing instead of using pandas’ powerful time tools.

> **Source concept:** In the source material, the dataset's hourly counts become more meaningful when indexed by time—same idea here, but with daily sales.

---

### 2. Resampling for Weekly/Monthly Views
Daily sales data can be noisy. Resampling aggregates data over specific time periods, like weeks or months, to reveal bigger patterns.

Bookstore analogy: If you look at sales every single day, holiday spikes can distract you. But grouping by month brings out seasonality patterns, like summer dips or December booms.

Pandas makes this easy:  
- `.resample('W')` → weekly totals  
- `.resample('M')` → monthly totals

---

### 3. Rolling Averages and Trend Detection
Rolling averages smooth short-term fluctuations, showing clearer trends.

In business terms: Think of a moving average as your “trend lens.” Instead of reacting to one day’s bad sales, you see whether the broader trend is up, down, or steady.

> **Inspired by source material:** Just as comparing casual vs. registered user counts helped spot subtle patterns, rolling averages help you notice small but meaningful changes in book sales.

---

## Code Examples

### Example 1: Parsing Dates and Setting Index
```python
import pandas as pd

# Load sales data
sales = pd.read_csv('sales.csv')

# Parse date column to datetime
sales['date'] = pd.to_datetime(sales['date'])

# Set date as index for time series operations
sales.set_index('date', inplace=True)

print(sales.index)  # Expected output: DatetimeIndex([...], dtype='datetime64[ns]', freq=None)
```

---

### Example 2: Resampling Daily Sales to Weekly Totals
```python
# Calculate total quantity sold per week
weekly_sales = sales['quantity'].resample('W').sum()

print(weekly_sales.head())
# Expected output (example):
# date
# 2023-01-01     125
# 2023-01-08     210
# 2023-01-15     188
# 2023-01-22     202
# 2023-01-29     175
# Freq: W-SUN, Name: quantity, dtype: int64
```

---

### Example 3: Calculating a Rolling 4-Week Average
```python
# Rolling mean over a 4-week window
weekly_sales_ma4 = weekly_sales.rolling(window=4).mean()

print(weekly_sales_ma4.head(8))
# Expected output: smoothed sales values over 4-week moving window
```

---

## Common Pitfalls

1. **Not converting date strings before resampling**  
   - If you skip `pd.to_datetime`, resample will fail or produce incorrect results.
   - **Fix:** Always ensure your date column is converted before time series ops.

2. **Forgetting to set the datetime column as the index**  
   - Without a datetime index, `.resample()` doesn’t know which column to use.
   - **Fix:** Use `set_index('date')` before resampling.

3. **Misinterpreting rolling averages**  
   - Beginners sometimes think they’ll see the same daily values—they won’t: rolling averages smooth them.
   - **Fix:** Remember rolling functions delay complete averages until the window is filled.

---

## Practice Checkpoint

By now, you should be able to:

- ✅ Parse string-formatted dates into pandas datetime objects  
- ✅ Resample daily book sales into weekly or monthly summaries  
- ✅ Apply rolling averages to detect underlying trends in noisy sales data  

> **Next up:** We’ll use these trend tools to compare genres and identify seasonal bestsellers—critical for marketing and inventory planning.