# Day 2: DataFrame Basics – Creating & Inspecting Data

## Introduction

Imagine you’ve just joined **Page Turner Analytics**, a team helping a chain of bookstores understand their business better. Yesterday, you learned how to set up your Python environment and work with synthetic DataFrames. Today, you get to work with *real* bookstore data—loading information from CSV files and taking your first steps in exploring it. By the end, you’ll be able to load a dataset, peek into its structure, understand what’s inside, and prepare it for deeper analysis.

---

## Core Content

### 1. Loading Data from CSV Files

In real-world analytics, data often arrives in CSV format—simple text files with columns separated by commas. In our case, the bookstore provides separate CSVs for books, authors, sales, and reviews.

We’ll use **pandas**’ `read_csv()` method to read these files into Python DataFrames. A DataFrame is like a table in Excel, but with powerful built-in methods for analysis.

Using the `books.csv` dataset:
- **Why it matters:** The moment you load your data, you unlock the ability to use pandas’ tools for data cleaning and visualization. If the data is wrong, everything downstream will be wrong.

Example:
```python
import pandas as pd

books = pd.read_csv('books.csv')  # Load book information
```

---

### 2. Inspecting DataFrames

Once loaded, your first step is inspection—understanding the shape, column names, and data types. Pandas has handy methods for this:

- `head()` – shows the first N rows (default 5)  
- `tail()` – shows the last N rows  
- `info()` – shows column names, non-null counts, and data types  
- `describe()` – gives summary statistics for numeric columns

**Bookstore analogy:** If the DataFrame is your store's inventory list, `head()` is like glancing at the first few lines to check the format, while `describe()` is like getting a quick report of average book prices and ranges.

Why it matters:
- Data inspection prevents analysis errors.
- Helps detect missing values, inconsistent formats, or unexpected data types.

---

### 3. Understanding Indexes and Columns

Every DataFrame has:
- **Columns** – named data fields (e.g., `title`, `price`)
- **Index** – row labels, usually integers starting at 0 unless set differently

You can rename columns to make them easier to work with. Long or messy names slow you down in coding.

From our source example:
```python
carsales.columns = ['month', 'sales']
```
Similarly, in our book dataset, shortening column names can make analysis more readable.

---

## Code Examples

### Example 1 – Load and Peek at Books
```python
import pandas as pd

# Load books dataset
books = pd.read_csv('books.csv')

# See the first 5 rows
print(books.head())
# Expected Output: First 5 book records with titles, authors, genres, etc.

# Check the last 3 rows
print(books.tail(3))
# Expected Output: Last 3 book records
```

---

### Example 2 – Summarizing Sales Data
```python
sales = pd.read_csv('sales.csv')

# Overview of DataFrame
print(sales.info())
# Expected: Column names, count of non-null values, and data types

# Basic statistics
print(sales.describe())
# Expected: Summary of quantity, unit_price, total_amount (mean, min, max)
```

---

### Example 3 – Renaming Columns for Easier Use
```python
reviews = pd.read_csv('reviews.csv')

# Original column names
print(reviews.columns)
# Expected Output: Index(['review_id', 'book_id', 'customer_id', 'rating', 'review_date', 'verified_purchase'], dtype='object')

# Rename for shorter names
reviews.columns = ['id', 'book', 'customer', 'rating', 'date', 'verified']
print(reviews.head(2))
# Expected Output: Now columns show as 'id', 'book', 'customer', ...
```

---

## Common Pitfalls

1. **Forgetting to Inspect Data Before Analysis**  
   Many beginners jump straight into calculations without checking for missing or malformed data. Always use `head()` and `info()` first.

2. **Not Renaming Unwieldy Column Names**  
   Long column names make code harder to read and type. Rename them once at the start.

3. **Assuming Index Contains Meaningful Data**  
   Pandas default index is just row numbers. If your dataset has an identifier column (like `book_id`), set it as the index with `set_index()` when needed.

---

## Practice Checkpoint ✅

By now, you should be able to:

- **Load** data from CSV files into a pandas DataFrame.  
- **Inspect** the first and last few rows, data types, and basic statistics.  
- **Rename columns** to more convenient names for analysis.

---