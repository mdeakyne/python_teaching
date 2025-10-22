# Day 4: Data Cleaning – Handling Missing Reviews

## Introduction
At Page Turner Analytics, accurate data is everything. Imagine we’re preparing a report for the marketing team, but the *reviews.csv* file has some gaps—missing ratings, empty review dates, or unverified purchase flags left blank. Just like missing pages make a book incomplete, missing values in our datasets can break our analysis or lead us to wrong conclusions.  
In the past few lessons, you learned how to load and inspect CSV files, check data types, and run basic statistics. Today, we’ll take it further—learning how to **find missing values**, **decide whether to fill or drop them**, and **clean up data for analysis**.

---

## Identifying Missing Values
Missing data often appears as `NaN` (Not a Number) in Pandas. In our book analogy, these are like entries where the “chapter” is missing—context disappears. In review data, this could be an absent rating or blank review date.

Pandas makes spotting these gaps easy:
- **`isnull()` / `isna()`** – flags missing values as `True`.
- **`sum()`** – counts them.

Why it matters:  
Any calculation (like average rating per genre) might break or mislead if missing ratings aren’t handled. Think of running a “favorite author contest” without knowing all the votes—it wouldn’t be fair.

---

## Dropping vs Filling Missing Data
We have two primary strategies:

1. **Dropping Rows/Columns (`dropna`)**  
   Useful when missing data is small and we don’t want guesses.  
   Example: A few reviews have no rating—these can be excluded.

2. **Filling Missing Values (`fillna`)**  
   Best when missing data is frequent and we can use a sensible default.  
   Example: If `verified_purchase` is missing, we might fill with `"Unknown"`.

Analogy: Dropping is like removing damaged books from display; filling is like replacing a missing page with a note to explain.

---

## Converting Data Types
Sometimes columns have the wrong data type due to missing or irregular entries.  
Example: The `rating` column might be loaded as `object` instead of numeric because some rows have blanks.

We must:
- Convert ratings to `float` or `int` for averaging.
- Turn date strings into `datetime` for sorting.

---

## Cleaning Strings
String-based columns (like `" verified_purchase "`) may have extra spaces or inconsistent cases. This is like having author names printed in different font sizes—it looks messy and makes grouping harder.

We can use:
- `.str.strip()` – remove leading/trailing spaces.
- `.str.lower()` – make all entries lowercase.
- `.str.title()` – title-case names consistently.

---

## Code Examples

### 1. Finding Missing Values
```python
import pandas as pd

# Load reviews data
reviews = pd.read_csv("reviews.csv")

# Check total missing values per column
print(reviews.isnull().sum())

# Expected output (example):
# review_id            0
# book_id              0
# customer_id          0
# rating              12   # 12 missing ratings
# review_date          5   # 5 missing dates
# verified_purchase    8   # 8 missing purchase flags
```

---

### 2. Dropping Missing Ratings
```python
# Drop rows where rating is missing
clean_reviews = reviews.dropna(subset=["rating"])

print(f"Original reviews: {len(reviews)}, Clean reviews: {len(clean_reviews)}")

# Expected output:
# Original reviews: 500, Clean reviews: 488
```

---

### 3. Filling Missing Values and Cleaning Data
```python
# Fill missing verified_purchase with 'Unknown'
reviews["verified_purchase"] = reviews["verified_purchase"].fillna("Unknown")

# Convert rating to numeric
reviews["rating"] = pd.to_numeric(reviews["rating"], errors="coerce")

# Convert review_date to datetime
reviews["review_date"] = pd.to_datetime(reviews["review_date"], errors="coerce")

# Clean string spacing/case
reviews["verified_purchase"] = reviews["verified_purchase"].str.strip().str.title()

print(reviews.head())
```
**Expected result:**  
`verified_purchase` is now consistently capitalized, ratings are numeric, and dates are proper `datetime` objects.

---

## Common Pitfalls
1. **Dropping too much data** – Beginners sometimes drop entire columns with few missing values, losing valuable information. **Avoid:** Check proportion before deciding.
2. **Filling without thinking** – Using defaults blindly can distort analysis, e.g., replacing missing ratings with 5 stars inflates averages. **Avoid:** Use only logical defaults.
3. **Forgetting to convert types** – Running numeric calculations on strings will cause errors or wrong results. **Avoid:** Confirm types with `.dtypes` before operations.

---

## Practice Checkpoint
By the end of this lesson, you should be able to:
- [ ] Identify missing values in a DataFrame using Pandas methods.
- [ ] Decide when to drop or fill missing entries depending on the dataset size and importance.
- [ ] Convert data types and clean strings for accurate analysis.

---
**Tip:** Just like a neatly arranged bookstore helps customers find what they want faster, clean datasets help us find insights without confusion.