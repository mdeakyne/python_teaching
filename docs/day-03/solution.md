## 📝 Day 3 – Data Selection & Filtering Solutions

---

### Task 1 – Easy: Selecting Columns for Key Book Info

#### 1. Complete Working Code
```python
import pandas as pd

# Load the books dataset
books_df = pd.read_csv("books.csv")

# Select the required columns: title, genre, price
selected_columns_df = books_df[["title", "genre", "price"]]

# Display the first 5 rows
print(selected_columns_df.head())
```

#### 2. Explanation
We first load the `books.csv` into a DataFrame and then use bracket indexing with a list of column names to select only the `title`, `genre`, and `price` columns. Finally, we use `.head()` to view the first 5 entries for a quick overview.

#### 3. Expected Output
Example:
```
                   title    genre  price
0    The Hobbit          Fantasy   8.99
1    1984               Dystopian  12.50
2    Good Omens         Fantasy   9.50
3    The Martian        Sci-Fi   14.75
4    Coraline          Fantasy    6.80
```

#### 4. Key Takeaway
Column selection is straightforward in Pandas by passing a list of column names to the DataFrame.

**Alternative Approaches:**
- Use `.loc[:, ["title", "genre", "price"]]` for clearer intent when selecting all rows and specific columns.

**Common Mistakes:**
1. Misspelling column names (must match exactly, including case).
2. Forgetting to enclose multiple column names in a list.
3. Using incorrect file paths or forgetting to import `pandas`.

---

### Task 2 – Medium: Finding Affordable Fantasy Books

#### 1. Complete Working Code
```python
import pandas as pd

# Load the books dataset
books_df = pd.read_csv("books.csv")

# Filter for Fantasy genre
fantasy_books_df = books_df[books_df["genre"] == "Fantasy"]

# Apply price filter for books under $10
affordable_fantasy_df = fantasy_books_df[fantasy_books_df["price"] < 10]

# Display first 10 results
print(affordable_fantasy_df.head(10))
```

#### 2. Explanation
We build our filter step-by-step: first select only the rows with genre `"Fantasy"`, then further subset to prices below 10. This chain of filtering ensures we get only budget-friendly fantasy books.

#### 3. Expected Output
Example:
```
        title    genre  price  author_id
0     The Hobbit Fantasy  8.99     101
2     Good Omens Fantasy  9.50     102
4     Coraline  Fantasy  6.80     101
...
```

#### 4. Key Takeaway
Combining multiple filters in Pandas requires careful use of logical operators and parentheses.

**Alternative Approaches:**
- Apply both conditions in one step:
  ```python
  affordable_fantasy_df = books_df[(books_df["genre"] == "Fantasy") & (books_df["price"] < 10)]
  ```

**Common Mistakes:**
1. Using `and` instead of `&` for Pandas boolean indexing.
2. Omitting parentheses around conditions when combining them.
3. Using a string for price comparison instead of numeric values.

---

### Task 3 – Medium-Hard: High-Rated Affordable Books from Specific Author

#### 1. Complete Working Code
```python
import pandas as pd

# Load datasets
books_df = pd.read_csv("books.csv")
authors_df = pd.read_csv("authors.csv")
reviews_df = pd.read_csv("reviews.csv")

# Find author_id for Neil Gaiman
gaiman_id = authors_df[authors_df["full_name"] == "Neil Gaiman"]["author_id"].iloc[0]

# Filter books for this author and price under $15
gaiman_books_df = books_df[(books_df["author_id"] == gaiman_id) & (books_df["price"] < 15)]

# Merge with reviews to get ratings (match on book_id)
books_with_reviews = pd.merge(gaiman_books_df, reviews_df, on="book_id", how="inner")

# Filter for books with rating >= 4.5
top_gaiman_books_df = books_with_reviews[books_with_reviews["rating"] >= 4.5]

# Display selected columns
print(top_gaiman_books_df[["title", "price", "rating"]])
```

#### 2. Explanation
We locate `author_id` for Neil Gaiman in `authors_df`, filter `books_df` for this ID and price limit, then merge with `reviews_df` to attach ratings. Finally, we select only rows with ratings 4.5 or higher and display the relevant columns.

#### 3. Expected Output
Example:
```
         title   price  rating
12    Coraline   6.80    4.6
13  American Gods  13.50    4.7
```

#### 4. Key Takeaway
Merging multiple datasets allows you to combine attributes (like ratings) for complex filtering.

**Alternative Approaches:**
- Use `.query()` for more readable filtering:
  ```python
  gaiman_books_df = books_df.query("author_id == @gaiman_id and price < 15")
  ```
- Chaining merges with `.merge()` multiple times if you need more datasets.

**Common Mistakes:**
1. Forgetting to merge on the correct key (`book_id`).
2. Misidentifying `author_id` due to missing `.iloc[0]` when extracting the single value.
3. Using wrong comparison operators (`>` instead of `>=`) for rating filtering.

---