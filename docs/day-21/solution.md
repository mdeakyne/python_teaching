## Task 1 – EASY: Load and Preview Books Data

### 1. Complete Working Code
```python
import pandas as pd

# Step 1: Load the books.csv dataset
books_df = pd.read_csv("books.csv")

# Step 2: Preview first few rows
print("First 5 rows of books dataset:")
print(books_df.head())

# Step 3: Display unique genres
unique_genres = books_df['genre'].unique()
print("\nUnique genres:")
print(unique_genres)
```

### 2. Explanation
We load the CSV into a Pandas DataFrame using `pd.read_csv()`. The `head()` method previews the first five rows, while `.unique()` is applied to the `genre` column to get all distinct genres.

### 3. Expected Output
```
First 5 rows of books dataset:
   book_id              title  author_id      author_name       genre  price  publication_year  pages
0        1       The Lost City          1     Alice Monroe     Fiction  12.99             2018    320
1        2  Science of Cooking          2     John Smith  Non-Fiction  18.50             2020    220
...

Unique genres:
['Fiction' 'Non-Fiction' 'Science' 'Biography']
```

### 4. Key Takeaway
Pandas makes it simple to load CSV data and quickly view structural and categorical information.

**Alternative Approaches:**
- Use `pd.read_excel()` if the file is Excel format.
- Use `.value_counts()` on `genre` to see frequency distribution.

**Common Mistakes:**
1. Forgetting to set the correct file path for CSV.
2. Misusing `.unique()` on non-existent columns (typo in column name).
3. Not checking for extra spaces or case inconsistencies in genre values.


---

## Task 2 – MEDIUM: Compute Author-Level Sales Summary

### 1. Complete Working Code
```python
import pandas as pd

# Load datasets
books_df = pd.read_csv("books.csv")
sales_df = pd.read_csv("sales.csv")

# Merge on book_id to get author_name alongside sales data
merged_df = sales_df.merge(books_df[['book_id', 'author_name']], on='book_id', how='left')

# Group by author_name and calculate aggregates
author_sales = merged_df.groupby('author_name').agg(
    total_units_sold=pd.NamedAgg(column='quantity', aggfunc='sum'),
    total_revenue=pd.NamedAgg(column='total_amount', aggfunc='sum')
).reset_index()

# Sort by total_revenue descending
top_authors = author_sales.sort_values(by='total_revenue', ascending=False).head(5)

print("Top 5 Authors by Revenue:")
print(top_authors)
```

### 2. Explanation
We merge `sales.csv` with `books.csv` on `book_id` to add `author_name` to each sale record. Grouping by `author_name` allows summation of quantities and revenues, producing aggregated statistics per author. Sorting by revenue yields the top performers.

### 3. Expected Output
```
Top 5 Authors by Revenue:
     author_name  total_units_sold  total_revenue
3  Alice Monroe               850       14350.50
1     John Smith               740       13200.00
2   Kate Morris               500        9600.75
...
```

### 4. Key Takeaway
Merging and grouping in Pandas is powerful for building summary tables from multiple datasets.

**Alternative Approaches:**
- Use `merge()` with `suffixes` to distinguish similar column names.
- Use `pivot_table` for flexible multi-metric aggregations.

**Common Mistakes:**
1. Merging on the wrong key, causing mismatched or duplicated rows.
2. Using `sum()` directly without `groupby`, yielding global totals only.
3. Forgetting to reset the index after `groupby` if iteration/display requires regular indexing.


---

## Task 3 – MEDIUM-HARD: Integrate Reviews into Dashboard Data

### 1. Complete Working Code
```python
import pandas as pd

# Load datasets
books_df = pd.read_csv("books.csv")
sales_df = pd.read_csv("sales.csv")
reviews_df = pd.read_csv("reviews.csv")

# Step 1: Merge sales with books to get author_name
sales_books_df = sales_df.merge(books_df[['book_id', 'author_name']], on='book_id', how='left')

# Step 2: Merge reviews with books to get author_name
reviews_books_df = reviews_df.merge(books_df[['book_id', 'author_name']], on='book_id', how='left')

# Step 3: Aggregate sales per author
author_sales = sales_books_df.groupby('author_name').agg(
    total_units_sold=pd.NamedAgg(column='quantity', aggfunc='sum')
).reset_index()

# Step 4: Aggregate reviews per author
author_reviews = reviews_books_df.groupby('author_name').agg(
    avg_rating=pd.NamedAgg(column='rating', aggfunc='mean'),
    num_reviews=pd.NamedAgg(column='rating', aggfunc='count')
).reset_index()

# Step 5: Combine aggregates into one DataFrame
author_perf_df = pd.merge(author_sales, author_reviews, on='author_name', how='outer')

# Step 6: Sort by average rating descending
author_perf_df = author_perf_df.sort_values(by='avg_rating', ascending=False)

# Format columns
author_perf_df['avg_rating'] = author_perf_df['avg_rating'].round(2)

print("Author Performance Table for Dashboard:")
print(author_perf_df)
```

### 2. Explanation
We separately merge sales and reviews with book data to add author names to each record type. Sales data is aggregated for `total_units_sold`, while reviews are aggregated to compute average ratings and review counts. We merge these aggregates into one table, sort by rating, and format numeric values for display.

### 3. Expected Output
```
Author Performance Table for Dashboard:
    author_name  total_units_sold  avg_rating  num_reviews
4     Kate Morris             500        4.85          220
2     Alice Monroe            850        4.57          320
0     John Smith              740        4.40          180
...
```

### 4. Key Takeaway
By joining and aggregating multiple datasets, you can create comprehensive performance metrics for dashboard visualizations.

**Alternative Approaches:**
- Use `pd.concat()` if merging on identical structures rather than keys.
- Apply `pivot_table()` with multiple values and functions to integrate metrics in one go.

**Common Mistakes:**
1. Forgetting to round ratings for consistent display in dashboards.
2. Using inner joins might drop authors without reviews; outer joins preserve all.
3. Not handling missing data (NaN) that can appear after merges, especially for authors with sales but no reviews or vice versa.