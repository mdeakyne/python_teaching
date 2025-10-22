```markdown
# Day 3 – Data Selection & Filtering: Finding the Right Books

## Introduction
Imagine you work at **Page Turner Analytics**, helping a bookshop decide what to promote next month. Yesterday, you learned how to inspect your data and calculate basic statistics. But looking at *all* books at once can be overwhelming. Often, you need to **zoom in** on a specific set of books—such as those under $10, in the "Fantasy" genre, and with ratings above 4. Today, we’ll learn how to select columns and rows precisely, filter your data by conditions, and combine multiple criteria using boolean logic.

---

## Selecting Columns and Rows

When working with `pandas` DataFrames, you rarely want to see *every* column and row at once. This is where **column selection** and `loc`/`iloc` come in.

- **Column selection**: Like picking just the "title" and "price" fields from a spreadsheet.
- **`loc`**: Selects rows and columns *by label* (names). Think: "Show me the price of the book called 'The Great Adventure'."
- **`iloc`**: Selects rows and columns *by position* (numbers). Think: "Show me the second row and first column."

📖 **Why it matters**: In a large bookstore inventory, you don’t carry around *all* details—just the ones relevant to your analysis. The source material showed how selecting one column (`loc[3, 'count']`) gives laser focus on particular data points. Remember, pandas uses **zero-based indexing**, so row index 3 is actually the **fourth** row.

---

## Filtering Data with Boolean Indexing

Boolean indexing means selecting rows where a condition is `True`. Each condition creates a mask—a series of True/False values—telling pandas which rows to include.

Example: *Show all books with a rating above 4.*  
That’s like standing in front of bookshelves and pulling out only the well-reviewed ones.

**Complex filters** use multiple conditions combined with `&` (AND), `|` (OR), and `~` (NOT). Just remember:  
- Use parentheses around each condition: `(condition1) & (condition2)`
- `&` and `|` are bitwise operators, not the word `and`/`or`.

📖 **Why it matters**: Boolean indexing is the backbone of nuanced analysis. You can combine filters—like genre, price, and rating—to make precise recommendations.

---

## Query Method for Readable Filters

If boolean indexing feels crowded with parentheses, try `.query()`.  
This method lets you write conditions as a string, similar to **SQL** queries.

Example with `.query()`:  
`books.query("genre == 'Fantasy' and price < 10")`

📖 **Why it matters**: It’s easier to read and share filters when they look like natural language. In a team setting, `.query()` makes your code more approachable.

---

## Code Examples

Let’s bring this to life with our Page Turner datasets.

```python
import pandas as pd

# Load data
books = pd.read_csv("books.csv")
reviews = pd.read_csv("reviews.csv")

# 1. Selecting specific columns
just_titles_prices = books[['title', 'price']]
print(just_titles_prices.head())
# Expected output: first 5 rows showing title and price columns only

# 2. Selecting a specific cell using loc
# Let's get the price of the book with index 2
book_price = books.loc[2, 'price']
print(book_price)
# Expected output: price value from the 3rd row

# 3. Boolean indexing - Fantasy under $10 with rating > 4
# First, merge books and reviews to get rating
books_with_ratings = books.merge(reviews, on='book_id')
filtered_books = books_with_ratings[
    (books_with_ratings['genre'] == 'Fantasy') &
    (books_with_ratings['price'] < 10) &
    (books_with_ratings['rating'] > 4)
]
print(filtered_books[['title', 'genre', 'price', 'rating']])
# Expected output: all Fantasy books cheaper than $10 with ratings above 4

# 4. Using query method for cleaner syntax
filtered_books_query = books_with_ratings.query(
    "genre == 'Fantasy' and price < 10 and rating > 4"
)
print(filtered_books_query[['title', 'genre', 'price', 'rating']])
# Expected output: same as above, showing matching titles
```

---

## Common Pitfalls

1. **Forgetting Zero-Based Indexing**  
   Beginners often grab the wrong row because they think the first row is index `1`. Remember: index `0` = first row.

2. **Missing Parentheses in Boolean Indexing**  
   Without parentheses: `cond1 & cond2` can cause errors. Always wrap each condition.

3. **Column Name Typos**  
   Pandas won’t find `"Price"` if your DataFrame column is `"price"`. Double-check names with `df.columns`.

---

## Practice Checkpoint ✅

By the end of this lesson, you should be able to:

- [ ] Select specific columns and rows using `.loc` and `.iloc`.
- [ ] Filter books by genre, price, and rating with boolean indexing.
- [ ] Use `.query()` for clean, readable filtering in complex scenarios.

---
```