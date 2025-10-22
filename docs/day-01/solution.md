```markdown
## 📝 Day 1 – Solutions for Environment Setup & Generating Synthetic Book Data

---

### Task 1 – Create a Basic Synthetic Books Dataset

#### 1. Complete Working Code
```python
import pandas as pd

# Step 1: Define dictionary with synthetic book catalog data
books_data = {
    "book_id": [1, 2, 3, 4, 5],
    "title": [
        "The Clockmaker's Secret",
        "Shadows in the Library",
        "Journey to the North",
        "Cooking with Love",
        "Data Science for Beginners"
    ],
    "author_name": [
        "Alice Thompson",
        "Bob Raymond",
        "Cynthia Lee",
        "David Foster",
        "Emily Zhang"
    ],
    "genre": ["Mystery", "Thriller", "Adventure", "Cookbook", "Technology"],
    "price": [14.99, 12.5, 19.99, 25.0, 29.99],
    "publication_year": [2018, 2020, 2015, 2019, 2021],
    "pages": [320, 275, 410, 150, 300]
}

# Step 2: Convert to DataFrame
books_df = pd.DataFrame(books_data)

# Step 3: Output DataFrame and data types
print("=== Books DataFrame ===")
print(books_df)
print("\n=== Data Types ===")
print(books_df.dtypes)
```

#### 2. Explanation
We create a Python dictionary with lists for each column, representing synthetic book data. This dictionary is converted into a `pandas.DataFrame`, which allows tabular data manipulation. `.dtypes` is used to check that numeric and string columns have appropriate data types.

#### 3. Expected Output
```
=== Books DataFrame ===
   book_id                      title    author_name      genre  price  publication_year  pages
0        1   The Clockmaker's Secret  Alice Thompson    Mystery  14.99              2018    320
1        2   Shadows in the Library    Bob Raymond   Thriller  12.50              2020    275
2        3      Journey to the North   Cynthia Lee  Adventure  19.99              2015    410
3        4         Cooking with Love   David Foster  Cookbook  25.00              2019    150
4        5  Data Science for Beginners  Emily Zhang Technology  29.99              2021    300

=== Data Types ===
book_id              int64
title               object
author_name         object
genre               object
price              float64
publication_year     int64
pages                int64
dtype: object
```

#### 4. Key Takeaway
A `pandas.DataFrame` can be easily created from a Python dictionary with list values for each column.

#### Alternative Approaches
- Create the DataFrame directly from a list of dictionaries.
- Load from CSV using `pd.read_csv()` for external datasets.

#### Common Mistakes
1. Lists of unequal lengths in the dictionary cause `ValueError`.
2. Forgetting to import `pandas` before use.
3. Mixing numeric and string types in numeric columns (e.g., `'14.99'` instead of `14.99`).

---

### Task 2 – Generate Author & Sales Data with Variation

#### 1. Complete Working Code
```python
import pandas as pd

# Authors Data
authors_data = {
    "author_id": [101, 102, 103, 104, 105],
    "first_name": ["Alice", "Bob", "Cynthia", "David", "Emily"],
    "last_name": ["Thompson", "Raymond", "Lee", "Foster", "Zhang"],
    "birth_year": [1975, 1980, 1985, 1972, 1990],
    "country": ["USA", "UK", "Canada", "Australia", "China"]
}

authors_df = pd.DataFrame(authors_data)
authors_df["full_name"] = authors_df["first_name"] + " " + authors_df["last_name"]

# Sales Data
sales_data = {
    "sale_id": [1, 2, 3, 4],
    "date": ["2024-01-05", "2024-02-10", "2024-03-15", "2024-04-21"],
    "book_id": [1, 2, 3, 5],
    "quantity": [2, 1, 3, 5],
    "unit_price": [14.99, 12.50, 19.99, 29.99],
    "customer_id": [501, 502, 503, 504]
}
sales_df = pd.DataFrame(sales_data)
sales_df["total_amount"] = sales_df["quantity"] * sales_df["unit_price"]

# Output
print("=== Authors DataFrame ===")
print(authors_df)
print("\n=== Sales DataFrame ===")
print(sales_df)
```

#### 2. Explanation
We create authors and sales datasets with realistic structure. Authors link to books by `full_name`, and sales link by `book_id`. The `total_amount` column is computed from quantity and unit price.

#### 3. Expected Output
```
=== Authors DataFrame ===
   author_id first_name last_name  birth_year   country       full_name
0        101      Alice  Thompson        1975       USA  Alice Thompson
1        102        Bob   Raymond        1980        UK    Bob Raymond
2        103    Cynthia       Lee        1985    Canada   Cynthia Lee
3        104      David    Foster        1972 Australia   David Foster
4        105      Emily     Zhang        1990     China   Emily Zhang

=== Sales DataFrame ===
   sale_id        date  book_id  quantity  unit_price  customer_id  total_amount
0        1  2024-01-05        1         2       14.99         501        29.98
1        2  2024-02-10        2         1       12.50         502        12.50
2        3  2024-03-15        3         3       19.99         503        59.97
3        4  2024-04-21        5         5       29.99         504       149.95
```

#### 4. Key Takeaway
We can create multiple synthetic datasets that link on shared identifiers to simulate realistic data relationships.

#### Alternative Approaches
- Generate synthetic data using libraries like `Faker`.
- Calculate `full_name` during DataFrame creation.

#### Common Mistakes
1. Mismatch between `book_id` in sales and books_df entries.
2. Forgetting to calculate `total_amount` correctly.
3. Incorrect string concatenation (e.g., missing space between names).

---

### Task 3 – Multi‑Table Synthetic Dataset

#### 1. Complete Working Code
```python
import pandas as pd

# ---- Reuse previous books_df, authors_df, sales_df ----
# Creating Reviews DataFrame
reviews_data = {
    "review_id": [201, 202, 203, 204, 205],
    "book_id": [1, 2, 3, 1, 5],
    "customer_id": [501, 502, 503, 505, 504],
    "rating": [5, 4, 3, 5, 4],
    "review_date": ["2024-01-06", "2024-02-12", "2024-03-18", "2024-01-07", "2024-04-25"],
    "verified_purchase": [True, True, False, True, True]
}
reviews_df = pd.DataFrame(reviews_data)

# Merge books & authors
books_authors_df = pd.merge(
    books_df,
    authors_df,
    left_on="author_name",
    right_on="full_name",
    how="inner"
)

# Merge with sales
merged_df = pd.merge(
    books_authors_df,
    sales_df,
    on="book_id",
    how="left"
)

# Output
print("=== Reviews DataFrame ===")
print(reviews_df)
print("\n=== Merged Books-Authors-Sales DataFrame ===")
print(merged_df)
```

#### 2. Explanation
We add a synthetic reviews dataset with links to books and customers. We merge books with authors on matching names, then merge the result with sales data using `book_id`. This produces a dataset containing combined information from all tables.

#### 3. Expected Output
```
=== Reviews DataFrame ===
   review_id  book_id  customer_id  rating review_date  verified_purchase
0        201        1         501       5  2024-01-06               True
1        202        2         502       4  2024-02-12               True
2        203        3         503       3  2024-03-18              False
3        204        1         505       5  2024-01-07               True
4        205        5         504       4  2024-04-25               True

=== Merged Books-Authors-Sales DataFrame ===
   book_id                      title    author_name      genre  price  publication_year  pages  author_id first_name last_name  birth_year   country       full_name  sale_id        date  quantity  unit_price  customer_id  total_amount
0        1   The Clockmaker's Secret  Alice Thompson    Mystery  14.99              2018    320       101      Alice  Thompson        1975       USA  Alice Thompson        1  2024-01-05         2       14.99         501        29.98
1        2   Shadows in the Library    Bob Raymond     Thriller  12.50              2020    275       102        Bob   Raymond        1980        UK    Bob Raymond        2  2024-02-10         1       12.50         502        12.50
2        3      Journey to the North   Cynthia Lee   Adventure  19.99              2015    410       103    Cynthia       Lee        1985    Canada   Cynthia Lee        3  2024-03-15         3       19.99         503        59.97
3        4         Cooking with Love   David Foster   Cookbook  25.00              2019    150       104      David    Foster        1972 Australia   David Foster      NaN         NaN       NaN         NaN         NaN           NaN
4        5  Data Science for Beginners  Emily Zhang  Technology  29.99              2021    300       105      Emily     Zhang        1990     China   Emily Zhang        4  2024-04-21         5       29.99         504       149.95
```

#### 4. Key Takeaway
Merging datasets on common keys allows combining related information into a unified table for analysis.

#### Alternative Approaches
- Merge on `author_id` instead of names for more reliable matching.
- Use `pd.concat()` for stacking similar datasets vertically.

#### Common Mistakes
1. Merging on mismatched columns (data contents or types).
2. Forgetting `how='left'` or `how='inner'` depending on desired preservation of rows.
3. Not handling NaN values when some entries have no matching sales.

---
```