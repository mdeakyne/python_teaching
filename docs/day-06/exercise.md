```markdown
## Task 1 – EASY (5 min): Merge Authors and Books

**Goal:** Merge `authors.csv` and `books.csv` so each book record includes the author's country.

**Instructions:**
1. Load `authors.csv` and `books.csv` into `authors_df` and `books_df`.
2. Merge them using the `author_id` column.
3. Use an **inner join**.

**Skeleton Code:**
```python
import pandas as pd

# Load datasets
authors_df = pd.read_csv("authors.csv")
books_df = pd.read_csv("books.csv")

# Merge DataFrames
merged_books = pd.merge(
    books_df,
    authors_df[["author_id", "country"]],
    on="author_id",
    how="inner"
)

# View result
print(merged_books.head())
```

**Expected Output:**
A DataFrame that contains columns from `books.csv` plus an extra column `country` showing where each author is from. Only books with matching authors will be present.


---

## Task 2 – MEDIUM (7 min): Add Sales Data to Book Info

**Goal:** Combine book and sales data to see each sale’s book title and genre.

**Instructions:**
1. Use your merged book-author DataFrame from Task 1 (`merged_books`).
2. Load `sales.csv` into a DataFrame (`sales_df`).
3. Merge sales and book data using **left join**: all sales should be kept, even if a book entry is missing.
4. Select relevant columns: `sale_id`, `date`, `title`, `genre`, `quantity`, `total_amount`.

**Skeleton Code:**
```python
# Load sales data
sales_df = pd.read_csv("sales.csv")

# Merge sales with book info
sales_with_books = pd.merge(
    sales_df,
    merged_books[["book_id", "title", "genre"]],
    on="book_id",
    how="left"
)

# Select relevant columns
result_df = sales_with_books[["sale_id", "date", "title", "genre", "quantity", "total_amount"]]

print(result_df.head())
```

**Expected Output:**
A table where each sale has the book's title and genre listed alongside quantity and total_amount. Missing book entries (if any) will have `NaN` for those fields.


---

## Task 3 – MEDIUM-HARD (10 min): Integrate Reviews and Calculate Average Ratings per Sale

**Goal:** Combine sales, books, authors, and reviews into one report, then calculate an average rating for books in each sale.

**Instructions:**
1. Build upon your `sales_with_books` DataFrame from Task 2.
2. Load `reviews.csv` into `reviews_df`.
3. Merge reviews with sales data so that review ratings match the books in sales.
4. Group by `sale_id` and calculate the average rating for all books in that sale.
5. Produce a final DataFrame with: `sale_id`, `date`, `title`, `country`, `quantity`, `total_amount`, and `avg_rating`.

**Skeleton Code:**
```python
# Load reviews
reviews_df = pd.read_csv("reviews.csv")

# Merge reviews with sales-books DataFrame
sales_reviews = pd.merge(
    sales_with_books,
    reviews_df[["book_id", "rating"]],
    on="book_id",
    how="left"
)

# Calculate average rating per sale
avg_rating_per_sale = sales_reviews.groupby("sale_id")["rating"].mean().reset_index()
avg_rating_per_sale.rename(columns={"rating": "avg_rating"}, inplace=True)

# Merge average rating back into sales data
final_report = pd.merge(
    sales_with_books,
    avg_rating_per_sale,
    on="sale_id",
    how="left"
)

print(final_report.head())
```

**Expected Output:**
A DataFrame containing complete sale information joined with book title, author country, and an `avg_rating` column summarizing the average rating for the books sold in that transaction. Transactions without reviews display `NaN` in `avg_rating`.
```