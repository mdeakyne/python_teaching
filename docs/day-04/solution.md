```markdown
## Task 1 – Find Missing Values in Reviews

### 1. Complete Working Code
```python
import pandas as pd

# Step 1: Load reviews data
reviews_df = pd.read_csv("reviews.csv")

# Step 2: Check for missing values in specific columns
missing_counts = reviews_df[["rating", "review_date"]].isna().sum()

# Step 3: Print summary
print(missing_counts)
```

### 2. Explanation
We start by loading `reviews.csv` into a Pandas DataFrame. Then, we use `.isna().sum()` on the selected columns (`rating` and `review_date`) to count the number of `NaN` (missing) entries. Printing the results provides a simple summary table.

### 3. Expected Output
```
rating         12
review_date     5
dtype: int64
```

### 4. Key Takeaway
Using `.isna().sum()` on selected columns quickly identifies missing data counts.

### Alternative Approaches
- Use `.info()` for an overview of missing values across all columns.
- Chain `.isnull()` instead of `.isna()` (both work the same in Pandas).

### Common Mistakes
1. Forgetting to limit to specific columns (which can clutter output with irrelevant data).
2. Using `.sum()` directly on the DataFrame without `.isna()`.
3. Loading the wrong CSV file path or name.

---

## Task 2 – Handle Missing Ratings

### 1. Complete Working Code
```python
import pandas as pd

# Load the data
reviews_df = pd.read_csv("reviews.csv")

# Step 1: Calculate mean rating (ignore NaN)
mean_rating = reviews_df["rating"].mean(skipna=True)

# Step 2: Fill missing ratings with mean_rating
reviews_df["rating"] = reviews_df["rating"].fillna(mean_rating)

# Step 3: Verify result
print(reviews_df["rating"].isna().sum())
```

### 2. Explanation
We calculate the average rating using `.mean(skipna=True)` to avoid counting NaNs. Then we fill missing ratings with `.fillna(mean_rating)` to ensure all ratings have numeric values. Finally, `.isna().sum()` verifies that no missing ratings remain.

### 3. Expected Output
```
0
```

### 4. Key Takeaway
Filling missing numerical values with the column mean is a simple imputation technique.

### Alternative Approaches
- Use the median instead of mean to reduce the effect of outliers.
- Replace missing ratings with a fixed default value.

### Common Mistakes
1. Calculating mean without `skipna=True` (though default skips NaNs, explicit is better).
2. Forgetting to reassign the filled column back to the DataFrame.
3. Applying `.fillna()` without parentheses around the value.

---

## Task 3 – Clean and Merge Review Data with Books

### 1. Complete Working Code
```python
import pandas as pd

# Load data
reviews_df = pd.read_csv("reviews.csv")
books_df = pd.read_csv("books.csv")

# Step 1: Fill missing verified_purchase with 'Unknown'
reviews_df["verified_purchase"] = reviews_df["verified_purchase"].fillna("Unknown")

# Step 2: Handle review_date and convert to datetime
reviews_df["review_date"] = reviews_df["review_date"].fillna("2000-01-01")
reviews_df["review_date"] = pd.to_datetime(reviews_df["review_date"], errors="coerce")

# Step 3: Merge with books_df on book_id
merged_df = pd.merge(
    reviews_df,
    books_df[["book_id", "title"]],
    on="book_id",
    how="left"
)

# Step 4: Preview desired columns
print(merged_df[["book_id", "title", "rating", "review_date", "verified_purchase"]].head())
```

### 2. Explanation
We first replace missing `verified_purchase` values with `"Unknown"` to maintain consistent text data. Next, missing `review_date` entries are set to a placeholder date (`2000-01-01`) before converting to datetime with `pd.to_datetime` for proper date handling. Finally, we merge the reviews with book titles on the `book_id` using a left join to preserve all review records.

### 3. Expected Output
```
   book_id               title  rating review_date verified_purchase
0      101  The Silent Library     4.0 2001-05-12              Yes
1      102  Whispers of Night     3.0 2000-01-01           Unknown
2      103   Journey's End       5.0 2019-07-22               No
3      104     Stolen Hours        4.5 2018-11-13              Yes
4      105   Echoes in Stone     4.0 2000-01-01           Unknown
```

### 4. Key Takeaway
Cleaning and merging datasets ensures we have complete, consistent information enriched with related details.

### Alternative Approaches
- Use `.replace()` to handle specific placeholder values before conversion.
- Perform an inner join if only matching book IDs should be included.

### Common Mistakes
1. Forgetting to specify `errors="coerce"` when converting strings to datetime (can cause crashes for invalid formats).
2. Dropping rows with missing book titles inadvertently by using an inner join without checking data integrity.
3. Not selecting only needed columns from `books_df` before merge, which might clutter data.

---
```