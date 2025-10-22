## 📝 Day 3 Hands-On Exercises – Data Selection & Filtering

### Task 1 – Easy: Selecting Columns for Key Book Info
You need a quick view of all book titles, their genres, and prices.

**Instructions:**
1. Load `books.csv` into a DataFrame named `books_df`.
2. Select only the `title`, `genre`, and `price` columns.
3. Display the first 5 rows.

**Code Skeleton:**
```python
import pandas as pd

# Load the books dataset
books_df = pd.read_csv("books.csv")

# Select the required columns
selected_columns_df = books_df[["<column1>", "<column2>", "<column3>"]]

# Display the first 5 rows
print(selected_columns_df.head())
```

**Success Criteria:**
- Output contains 3 columns: `title`, `genre`, `price`
- First 5 rows match the dataset’s column names exactly

**Expected Output (Example Description):**
A small table showing book titles, their genres, and prices (numeric values in the `price` column).


---

### Task 2 – Medium: Finding Affordable Fantasy Books
The shop wants to promote budget-friendly fantasy reads.

**Instructions:**
1. Start with `books_df` from Task 1.
2. Filter for books where:
   - `genre` is `"Fantasy"`
   - `price` is less than 10
3. Show the first 10 results.

**Code Skeleton:**
```python
# Filter for Fantasy genre
fantasy_books_df = books_df[books_df["genre"] == "<genre_value>"]

# Apply price filter
affordable_fantasy_df = fantasy_books_df[fantasy_books_df["price"] < <price_limit>]

# Display first 10 results
print(affordable_fantasy_df.head(10))
```

**Expected Output (Example Description):**
A list of up to 10 fantasy books, each with price under 10, clearly showing their titles, genres, and prices.


---

### Task 3 – Medium-Hard: High-Rated Affordable Books from Specific Author
You’ve identified an author whose books the shop wants to market. Let’s combine all the data.

**Instructions:**
1. Load `authors.csv` and `reviews.csv` into DataFrames (`authors_df`, `reviews_df`).
2. Find the `author_id` for `"Neil Gaiman"` in `authors_df`.
3. From `books_df`, select books that:
   - Belong to this author
   - Have price under 15
4. Merge these books with `reviews_df` to include `rating`.
5. Filter for books with a rating >= 4.5.
6. Display the resulting books with columns: `title`, `price`, `rating`.

**Code Skeleton:**
```python
# Load datasets
authors_df = pd.read_csv("authors.csv")
reviews_df = pd.read_csv("reviews.csv")

# Find author_id for Neil Gaiman
gaiman_id = authors_df[authors_df["full_name"] == "<author_name>"]["author_id"].iloc[0]

# Filter books for this author and price under limit
gaiman_books_df = books_df[(books_df["author_id"] == gaiman_id) & (books_df["price"] < <price_limit>)]

# Merge with reviews to get ratings
books_with_reviews = pd.merge(gaiman_books_df, reviews_df, on="book_id", how="inner")

# Filter for high ratings
top_gaiman_books_df = books_with_reviews[books_with_reviews["rating"] >= <rating_limit>]

# Display selected columns
print(top_gaiman_books_df[["title", "price", "rating"]])
```

**Expected Output (Example Description):**
A table listing Neil Gaiman’s books under $15 that have an average rating of 4.5 or more — showing the title, price, and rating side-by-side.