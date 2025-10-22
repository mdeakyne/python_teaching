## Task 1 – Find Missing Values in Reviews (Easy – ~5 min)

**Goal:** Identify missing ratings and review dates in `reviews.csv`.

**Instructions:**  
1. Load the `reviews.csv` file into a Pandas DataFrame.  
2. Check how many missing values exist for `rating` and `review_date`.  
3. Display a small summary table of missing counts.

**Skeleton Code:**
```python
import pandas as pd

# Step 1: Load reviews data
reviews_df = pd.read_csv("reviews.csv")

# Step 2: Check for missing values in specific columns
missing_counts = reviews_df[["rating", "review_date"]]._____()

# Step 3: Print summary
print(missing_counts)
```

**Success Criteria:**  
The output shows the number of missing entries in `rating` and `review_date` columns.

**Expected Output Example:**
```
rating         12
review_date     5
dtype: int64
```


---

## Task 2 – Handle Missing Ratings (Medium – ~7 min)

**Goal:** Replace missing ratings with the average rating, then check results.

**Instructions:**  
1. Load the `reviews.csv` into a DataFrame.  
2. Calculate the mean rating ignoring missing values.  
3. Fill missing values in `rating` with this mean.  
4. Confirm no missing ratings remain.

**Skeleton Code:**
```python
import pandas as pd

reviews_df = pd.read_csv("reviews.csv")

# Step 1: Calculate mean rating
mean_rating = reviews_df["rating"]._____(skipna=True)

# Step 2: Fill missing ratings with mean_rating
reviews_df["rating"] = reviews_df["rating"].fillna(_____)

# Step 3: Verify result
print(reviews_df["rating"].isna().sum())
```

**Expected Output Hint:**  
- The final print should display `0` (no missing ratings left).  
- The DataFrame's `rating` column should now contain integer/float values without `NaN`.


---

## Task 3 – Clean and Merge Review Data with Books (Medium-Hard – ~10 min)

**Goal:** Perform multi-step cleaning on `reviews.csv` and combine with `books.csv`.

**Instructions:**  
1. Load both `reviews.csv` and `books.csv` into DataFrames.  
2. Fill missing `verified_purchase` values with `"Unknown"`.  
3. Convert `review_date` to datetime format. Handle missing dates by filling with `"2000-01-01"`.  
4. Merge cleaned reviews with book titles from `books.csv` using `book_id`.  
5. Display a preview of `book_id`, `title`, `rating`, `review_date`, and `verified_purchase`.

**Skeleton Code:**
```python
import pandas as pd

reviews_df = pd.read_csv("reviews.csv")
books_df = pd.read_csv("books.csv")

# Step 1: Fill missing verified_purchase
reviews_df["verified_purchase"] = reviews_df["verified_purchase"].fillna("_____")

# Step 2: Handle review_date and convert to datetime
reviews_df["review_date"] = reviews_df["review_date"].fillna("_____-__-__")
reviews_df["review_date"] = pd.to_datetime(reviews_df["review_date"], errors="coerce")

# Step 3: Merge with books_df
merged_df = pd.merge(reviews_df, books_df[["book_id", "title"]], on="book_id", how="_____")

# Step 4: Preview desired columns
print(merged_df[["book_id", "title", "rating", "review_date", "verified_purchase"]].head())
```

**Expected Output Hint:**  
- The preview shows 5 rows containing: `book_id`, corresponding `title`, cleaned `rating`, datetime-formatted `review_date`, and no missing `verified_purchase` entries.
```
book_id   title                rating   review_date  verified_purchase
101       The Silent Library   4.0      2001-05-12   Yes
...
```