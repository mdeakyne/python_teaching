## Task 1 – EASY (5 min): Load and Preview Books Data

**Goal:** Reinforce loading CSV data and basic Pandas inspection.

**Instructions:**
1. Load `books.csv` into a Pandas DataFrame.
2. Display the first 5 rows.
3. Show the list of unique genres.

**Skeleton Code:**
```python
import pandas as pd

# Step 1: Load the books.csv dataset
books_df = pd.read_csv("books.csv")

# Step 2: Preview first few rows
# YOUR CODE HERE

# Step 3: Display unique genres
# YOUR CODE HERE
```

**Success Criteria:**
- DataFrame loads successfully from CSV.
- Console output shows 5-row preview.
- Unique genres printed as a list/Series.

**Expected Output:**
- Printed table with first 5 books (columns: book_id, title, author_id, author_name, genre, price, publication_year, pages).
- Printed list of genres, e.g., `['Fiction', 'Non-Fiction', 'Science', ...]`.


---

## Task 2 – MEDIUM (7 min): Compute Author-Level Sales Summary

**Goal:** Create summary metrics by merging datasets.

**Instructions:**
1. Load `sales.csv` and `books.csv`.
2. Merge them to align each sale with the `author_name`.
3. Group by `author_name` and calculate:
   - Total units sold
   - Total revenue (`sum` of `total_amount`)
4. Sort results by total revenue (descending) and display top 5 authors.

**Skeleton Code:**
```python
import pandas as pd

# Load datasets
books_df = pd.read_csv("books.csv")
sales_df = pd.read_csv("sales.csv")

# Merge on book_id
# merged_df = ...

# Group by author_name and aggregate
# author_sales = ...

# Sort and display top 5
# top_authors = ...
```

**Expected Output:**
- A table with top 5 authors, columns: `author_name`, `total_units_sold`, `total_revenue`.
- Sorted from highest revenue to lowest.


---

## Task 3 – MEDIUM-HARD (10 min): Integrate Reviews into Dashboard Data

**Goal:** Produce author performance table including ratings, ready for Dash display.

**Instructions:**
1. Load `books.csv`, `sales.csv`, and `reviews.csv`.
2. Merge all three so each review is linked to a book and its author.
3. From merged data, compute:
   - Total units sold per author
   - Average rating per author
   - Number of reviews per author
4. Create a Pandas DataFrame sorted by average rating (descending).
5. Ensure numeric formatting (2 decimal places for rating; currency for revenue if included).
6. Print result — this will be used as a data source for a Dash `DataTable`.

**Skeleton Code:**
```python
import pandas as pd

# Load datasets
books_df = pd.read_csv("books.csv")
sales_df = pd.read_csv("sales.csv")
reviews_df = pd.read_csv("reviews.csv")

# Step 1: Merge sales with books to get author_name
# sales_books_df = ...

# Step 2: Merge reviews with books to get author_name
# reviews_books_df = ...

# Step 3: Aggregate sales
# author_sales = ...

# Step 4: Aggregate reviews
# author_reviews = ...

# Step 5: Combine aggregates into one DataFrame
# author_perf_df = ...

# Step 6: Sort and format
# author_perf_df = ...
```

**Expected Output:**
- Printed table with columns:
  - `author_name`
  - `total_units_sold`
  - `avg_rating`
  - `num_reviews`
- Sorted by `avg_rating` descending, highest at top.
- Ratings displayed with 2 decimal places, e.g., `4.57`.