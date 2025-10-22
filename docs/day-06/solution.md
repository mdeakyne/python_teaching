## Task 1 – EASY: Merge Authors and Books

### 1. Complete Working Code
```python
import pandas as pd

# Load datasets from CSV files
authors_df = pd.read_csv("authors.csv")
books_df = pd.read_csv("books.csv")

# Merge books and authors to add author's country to each book record
merged_books = pd.merge(
    books_df,
    authors_df[["author_id", "country"]],
    on="author_id",
    how="inner"  # Inner join: only keep books with matching authors
)

# Display the first few rows of the merged DataFrame
print(merged_books.head())
```

### 2. Explanation
We read both datasets into DataFrames and used `pd.merge()` to join them based on the `author_id` column present in both. An inner join ensures that only books with matching authors are kept, adding the `country` column from the authors dataset to the book records.

### 3. Expected Output
Example:
```
   book_id                   title  author_id       author_name     genre  price  publication_year  pages    country
0        1            Ocean's Call          10   Alice Marlowe   Fiction  14.99              2018    320    Canada
1        2  Quantum Realities         12   Bao Liu          Sci-Fi    19.99              2020    410    China
2        3     The Silent Forest        11   Carla Ruiz        Mystery  12.50              2015    250    Spain
...
```

### 4. Key Takeaway
Merging datasets on a common key quickly enriches records with additional attributes from related data.

---

**Alternative Approaches**:
- Use `DataFrame.join()` if the key is set as an index in both DataFrames.
- Use `merge()` with `suffixes` to avoid column name clashes in case multiple columns overlap.

**Common Mistakes**:
1. Using `outer` join when only valid matches are needed, which results in unwanted NaN values.
2. Forgetting to select only necessary columns from `authors_df`, causing redundant data in the merged DataFrame.
3. Mismatched datatypes for `author_id` across DataFrames causing empty merges.

---

## Task 2 – MEDIUM: Add Sales Data to Book Info

### 1. Complete Working Code
```python
import pandas as pd

# Load datasets
authors_df = pd.read_csv("authors.csv")
books_df = pd.read_csv("books.csv")
sales_df = pd.read_csv("sales.csv")

# Merge books with authors to add country info
merged_books = pd.merge(
    books_df,
    authors_df[["author_id", "country"]],
    on="author_id",
    how="inner"
)

# Merge sales with book info
sales_with_books = pd.merge(
    sales_df,
    merged_books[["book_id", "title", "genre"]],
    on="book_id",
    how="left"  # Keep all sales, even if no matching book
)

# Select relevant columns for output
result_df = sales_with_books[["sale_id", "date", "title", "genre", "quantity", "total_amount"]]

print(result_df.head())
```

### 2. Explanation
We first reuse the merged dataset from Task 1, then join sales data with book details using a left join so that all sales records remain in the result. We limit the result to columns that are meaningful for sales analysis.

### 3. Expected Output
Example:
```
   sale_id        date              title    genre  quantity  total_amount
0       101  2023-01-14     Ocean's Call  Fiction        2        29.98
1       102  2023-01-15  Quantum Realities  Sci-Fi        1        19.99
2       103  2023-01-16  The Silent Forest Mystery        3        37.50
...
```

### 4. Key Takeaway
Left joins preserve all records from the primary dataset, making them ideal when you need to keep unmatched records for further investigation.

---

**Alternative Approaches**:
- Use `merge()` inside a function that accepts file paths for reusability.
- Perform the join on multiple keys if needed (e.g., `book_id` and `unit_price` for strict matching).

**Common Mistakes**:
1. Forgetting to use `how="left"`, unintentionally filtering out some sales.
2. Selecting too many columns from merged_books, making the result unnecessarily large.
3. Typos in column names leading to `KeyError`.

---

## Task 3 – MEDIUM-HARD: Integrate Reviews and Calculate Average Ratings per Sale

### 1. Complete Working Code
```python
import pandas as pd

# Load datasets
authors_df = pd.read_csv("authors.csv")
books_df = pd.read_csv("books.csv")
sales_df = pd.read_csv("sales.csv")
reviews_df = pd.read_csv("reviews.csv")

# Merge books with authors
merged_books = pd.merge(
    books_df,
    authors_df[["author_id", "country"]],
    on="author_id",
    how="inner"
)

# Merge sales with book info (including country)
sales_with_books_full = pd.merge(
    sales_df,
    merged_books[["book_id", "title", "genre", "country"]],
    on="book_id",
    how="left"
)

# Merge reviews with sales-books DataFrame to add ratings
sales_reviews = pd.merge(
    sales_with_books_full,
    reviews_df[["book_id", "rating"]],
    on="book_id",
    how="left"
)

# Calculate average rating per sale_id
avg_rating_per_sale = (
    sales_reviews.groupby("sale_id")["rating"]
    .mean()
    .reset_index()
    .rename(columns={"rating": "avg_rating"})
)

# Merge average rating back into sales data
final_report = pd.merge(
    sales_with_books_full,
    avg_rating_per_sale,
    on="sale_id",
    how="left"
)

# Final view: selected columns for report
final_report_view = final_report[["sale_id", "date", "title", "country", "quantity", "total_amount", "avg_rating"]]

print(final_report_view.head())
```

### 2. Explanation
We combined all necessary datasets step-by-step: books with authors for country, sales with enriched book data, and reviews to attach ratings to each book sold. By grouping by `sale_id` and averaging ratings, we computed a sale-level rating, then merged this back to the full sales dataset for reporting.

### 3. Expected Output
Example:
```
   sale_id        date              title  country  quantity  total_amount  avg_rating
0       101  2023-01-14     Ocean's Call   Canada        2        29.98        4.5
1       102  2023-01-15  Quantum Realities China        1        19.99        4.0
2       103  2023-01-16  The Silent Forest Spain        3        37.50        NaN
...
```

### 4. Key Takeaway
Stepwise merges and group-by operations allow you to integrate diverse datasets and produce meaningful aggregated metrics.

---

**Alternative Approaches**:
- Use `pd.concat()` for datasets with similar structure and merge after consolidating.
- Utilize `DataFrame.assign()` for quick column creation post-merge.

**Common Mistakes**:
1. Averaging ratings without handling NaN values, which can skew results.
2. Forgetting to merge `country` into the sales dataset before final output.
3. Confusing inner vs. left join semantics, leading to loss of data in ratings analysis.