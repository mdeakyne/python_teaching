---
title: Data Selection & Filtering
---

# Data Selection & Filtering

```{admonition} Lesson Info
:class: note
**Duration**: 90 minutes
**Difficulty**: Beginner
**Prerequisites**: Lesson 02 completed
```

## Learning Objectives

By the end of this lesson, you will be able to:

- Use boolean indexing to filter rows
- Understand the difference between loc and iloc
- Combine multiple conditions for complex filtering
- Use the query() method for readable filters

## Introduction

Welcome back to **Page Turner Analytics**! 📚

Your manager was impressed with your data exploration work in Lesson 02. Now she has a more specific request:

> "We need to analyze only our **Fantasy books under $15 with ratings above 4.7**. Can you pull that data for me?"

In Lesson 02, you learned to load and inspect *all* the data. But in real-world data analysis, you'll often need to work with specific subsets. This lesson teaches you how to **filter** data to extract exactly what you need.

Think of filtering like using the search and filter features in an online bookstore - you want to see only books that match your specific criteria. pandas provides powerful, flexible tools to do this!

## Boolean Indexing

Boolean indexing is the foundation of filtering in pandas. It uses **True/False conditions** to select rows.

### The Concept: Boolean Masks

```{code-cell} ipython3
import pandas as pd

# Reload our book catalog
books_df = pd.read_csv('data/book_catalog.csv')

# Create a boolean condition
high_rated = books_df['rating'] > 4.5

print("Boolean mask (first 5 values):")
print(high_rated.head())
print(f"\nType: {type(high_rated)}")
print(f"True values: {high_rated.sum()} books have rating > 4.5")
```

A boolean mask is a Series of True/False values - one for each row. **True** means "include this row", **False** means "exclude this row".

### Using Boolean Masks to Filter

```{code-cell} ipython3
# Filter: Show only high-rated books (rating > 4.5)
high_rated_books = books_df[books_df['rating'] > 4.5]

print("📚 High-Rated Books (rating > 4.5):")
print(high_rated_books[['title', 'rating', 'price']])
```

**How it works**:
1. `books_df['rating'] > 4.5` creates a boolean mask
2. `books_df[mask]` returns only rows where mask is True

### Common Filtering Conditions

```{code-cell} ipython3
# Equal to
fantasy_books = books_df[books_df['genre'] == 'Fantasy']
print("Fantasy Books:")
print(fantasy_books['title'].tolist())
print()

# Not equal to
not_fiction = books_df[books_df['genre'] != 'Fiction']
print("Non-Fiction Books:")
print(not_fiction[['title', 'genre']])
print()

# Greater than / Less than
long_books = books_df[books_df['pages'] > 400]
print("Long Books (> 400 pages):")
print(long_books[['title', 'pages']])
print()

# Greater than or equal to
affordable_books = books_df[books_df['price'] <= 14.00]
print("Affordable Books (<= $14):")
print(affordable_books[['title', 'price']])
```

### String Filtering

```{code-cell} ipython3
# Books with "Python" in the title
python_books = books_df[books_df['title'].str.contains('Python', case=False)]
print("Books with 'Python' in title:")
print(python_books['title'])
print()

# Books by specific author
orwell_books = books_df[books_df['author'] == 'George Orwell']
print("Books by George Orwell:")
print(orwell_books[['title', 'year_published']])
print()

# Books starting with "The"
the_books = books_df[books_df['title'].str.startswith('The')]
print("Books starting with 'The':")
print(the_books['title'])
```

```{admonition} String Methods
:class: note
Use `.str` accessor for string operations:
- `.str.contains('text')` - Check if contains substring
- `.str.startswith('text')` - Check if starts with
- `.str.endswith('text')` - Check if ends with
- `.str.lower()` - Convert to lowercase
- Add `case=False` for case-insensitive matching
```

## loc vs iloc

pandas provides two powerful indexers: `loc` (label-based) and `iloc` (integer position-based).

### iloc: Integer-Based Selection

`iloc` selects by **integer position** (like list indexing):

```{code-cell} ipython3
import pandas as pd
books_df = pd.read_csv('data/book_catalog.csv')

print("iloc: Selection by INTEGER POSITION\n")

# Single row (first row, position 0)
print("First book (iloc[0]):")
print(books_df.iloc[0])
print()

# Multiple rows by position
print("First 3 books (iloc[0:3]):")
print(books_df.iloc[0:3][['title', 'author']])
print()

# Specific rows and columns by position
# Rows 0-2, Columns 0, 4, 5 (title, rating, price)
print("Rows 0-2, specific columns:")
print(books_df.iloc[0:3, [0, 4, 5]])
print()

# Last row
print("Last book (iloc[-1]):")
print(books_df.iloc[-1][['title', 'author']])
```

### loc: Label-Based Selection

`loc` selects by **labels** (index values and column names):

```{code-cell} ipython3
print("loc: Selection by LABEL\n")

# Single row by index label
print("Book at index 0 (loc[0]):")
print(books_df.loc[0, ['title', 'rating']])
print()

# Multiple rows, specific columns
print("Books 0-2, specific columns (loc[0:2, ['title', 'price']]):")
print(books_df.loc[0:2, ['title', 'price']])
print()

# All rows, specific columns
print("All books, only title and genre:")
print(books_df.loc[:, ['title', 'genre']].head(3))
print()

# POWERFUL: Combine loc with boolean indexing
high_rated = books_df['rating'] > 4.7
print("High-rated books with loc:")
print(books_df.loc[high_rated, ['title', 'rating', 'price']])
```

### Key Differences: loc vs iloc

| Feature | `iloc` | `loc` |
|---------|--------|-------|
| Selection type | Integer position | Label/name |
| Row selection | `iloc[0]` (first row) | `loc[0]` (index label 0) |
| Column selection | `iloc[:, 0]` (first column) | `loc[:, 'title']` (column named 'title') |
| Slicing | `iloc[0:3]` (rows 0, 1, 2) | `loc[0:3]` (rows 0, 1, 2, **3**) |
| Boolean indexing | No | Yes ✅ |

```{admonition} When to Use Which?
:class: tip
- Use **iloc** when you know the exact position (e.g., "first 10 rows", "every other row")
- Use **loc** when you know labels/names (e.g., "rows where rating > 4.5", "columns 'title' and 'price'")
- **loc + boolean indexing** is the most powerful combination!
```

## Multi-Condition Filtering

Real-world queries often require multiple conditions combined together.

### AND Conditions (&)

Both conditions must be True:

```{code-cell} ipython3
import pandas as pd
books_df = pd.read_csv('data/book_catalog.csv')

# Find books that are BOTH highly rated AND affordable
high_rated_and_affordable = books_df[
    (books_df['rating'] > 4.7) & (books_df['price'] < 15.00)
]

print("📚 High-Rated AND Affordable Books:")
print(high_rated_and_affordable[['title', 'rating', 'price']])
```

**Important**: Always use **parentheses** around each condition when combining!

### OR Conditions (|)

At least one condition must be True:

```{code-cell} ipython3
# Find books that are EITHER Fantasy OR Sci-Fi
fantasy_or_scifi = books_df[
    (books_df['genre'] == 'Fantasy') | (books_df['genre'] == 'Sci-Fi')
]

print("📚 Fantasy OR Sci-Fi Books:")
print(fantasy_or_scifi[['title', 'genre', 'rating']])
```

### NOT Conditions (~)

Invert a condition (True becomes False, False becomes True):

```{code-cell} ipython3
# Find books that are NOT Fiction
not_fiction = books_df[~(books_df['genre'] == 'Fiction')]

print("📚 Not Fiction Books:")
print(not_fiction[['title', 'genre']])
```

### Complex Multi-Condition Queries

```{code-cell} ipython3
# Complex query: Fantasy books under $15 with rating > 4.7
# This is the exact query your manager requested!
manager_request = books_df[
    (books_df['genre'] == 'Fantasy') &
    (books_df['price'] < 15.00) &
    (books_df['rating'] > 4.7)
]

print("📚 Manager's Request: Fantasy, <$15, rating >4.7:")
print(manager_request[['title', 'genre', 'price', 'rating']])
print(f"\nFound {len(manager_request)} matching books!")
```

### Using isin() for Multiple Values

```{code-cell} ipython3
# Find books in multiple genres
popular_genres = ['Fantasy', 'Sci-Fi', 'Dystopian']
popular_books = books_df[books_df['genre'].isin(popular_genres)]

print(f"📚 Books in {popular_genres}:")
print(popular_books[['title', 'genre', 'rating']])
```

## The query() Method

The `query()` method provides a more readable way to write complex filters using string expressions.

### Basic query() Usage

```{code-cell} ipython3
import pandas as pd
books_df = pd.read_csv('data/book_catalog.csv')

# Instead of: books_df[(books_df['rating'] > 4.5) & (books_df['price'] < 15)]
# Use query:
result = books_df.query('rating > 4.5 and price < 15')

print("📚 Using query(): rating > 4.5 and price < 15")
print(result[['title', 'rating', 'price']])
```

### query() with Variables

```{code-cell} ipython3
# Use @ to reference Python variables
min_rating = 4.7
max_price = 16.00

result = books_df.query('rating > @min_rating and price < @max_price')

print(f"📚 Books with rating > {min_rating} and price < ${max_price}:")
print(result[['title', 'rating', 'price']])
```

### Complex query() Examples

```{code-cell} ipython3
# Multiple conditions with OR
result = books_df.query('genre == "Fantasy" or genre == "Sci-Fi"')
print("Fantasy or Sci-Fi:")
print(result[['title', 'genre']])
print()

# Combination of AND and OR
result = books_df.query('(rating > 4.5 and price < 15) or pages < 250')
print("High-rated affordable OR short books:")
print(result[['title', 'rating', 'price', 'pages']])
print()

# Using in for multiple values
result = books_df.query('genre in ["Fantasy", "Sci-Fi", "Dystopian"]')
print("Popular genres:")
print(result[['title', 'genre']])
```

### Boolean Indexing vs query(): When to Use What?

```{code-cell} ipython3
# Boolean indexing (traditional)
bool_result = books_df[
    (books_df['rating'] > 4.5) &
    (books_df['price'] < 15) &
    (books_df['pages'] > 200)
]

# query() (more readable)
query_result = books_df.query('rating > 4.5 and price < 15 and pages > 200')

# Both produce the same result!
print("Both methods return identical results:")
print(f"Boolean indexing: {len(bool_result)} books")
print(f"query(): {len(query_result)} books")
```

**When to use each**:
- **Boolean indexing**: More flexible, better for complex logic, easier to debug
- **query()**: More readable for simple-to-moderate complexity, faster for very large datasets

## Practice Exercise

```{admonition} Exercise: Advanced Filtering Challenges
:class: tip

**Setup**: Use the book_catalog.csv file from previous lessons.

**Part 1: Single Condition Filters**
1. Find all books published before 1950
2. Find all books with exactly 4.8 rating
3. Find all books by J.K. Rowling
4. Find books with "Data" in the title (case-insensitive)

**Part 2: Multi-Condition Filters**
1. Find Fiction books published after 1950 with rating > 4.5
2. Find books that are either under 250 pages OR cost less than $13
3. Find books that are NOT Romance and NOT Historical Fiction
4. Find books with ratings between 4.0 and 4.5 (inclusive)

**Part 3: Using loc/iloc**
1. Select the first 5 books, but only show title, author, and rating columns
2. Select every other book (rows 0, 2, 4, 6, ...) using iloc
3. Use loc to filter books with rating > 4.6 and select only title and price
4. Select the last 3 books using negative indexing

**Part 4: query() Method**
1. Rewrite this filter using query(): `books_df[(books_df['pages'] > 300) & (books_df['rating'] > 4.5)]`
2. Create a query that finds books in genres ['Fantasy', 'Sci-Fi'] with price < 18
3. Use query() with variables to find books matching user-defined criteria

**Bonus Challenge**
Your manager asks: "Find all Fiction or Fantasy books published after 1960, with ratings above 4.5, priced between $12 and $18, that are not too long (under 500 pages)."

Write this filter in THREE ways:
1. Using boolean indexing
2. Using query()
3. Using loc with boolean indexing

Which method do you find most readable?
```

## Summary

Excellent work! You've mastered data filtering - one of the most essential skills in data analysis! 📚

In this lesson, you learned how to:

- ✅ **Boolean indexing**: Filter rows using True/False conditions
- ✅ **loc vs iloc**: Understand label-based vs position-based selection
- ✅ **Multi-condition filtering**: Combine conditions with `&` (and), `|` (or), `~` (not)
- ✅ **query() method**: Write readable filters using string expressions
- ✅ **String filtering**: Use `.str` methods to filter text data
- ✅ **isin()**: Filter based on multiple possible values

You can now answer complex business questions like:
- "Show me all Fantasy books under $15 with ratings above 4.7"
- "Find Fiction or Dystopian books published after 1960"
- "Which highly-rated books are also affordable?"

These filtering skills will be used in **every single data analysis project** you work on!

## Quick Reference: Filtering Cheat Sheet

```python
# Single condition
df[df['column'] > value]

# Multiple conditions (AND)
df[(df['col1'] > val1) & (df['col2'] == val2)]

# Multiple conditions (OR)
df[(df['col1'] > val1) | (df['col2'] < val2)]

# NOT condition
df[~(df['column'] == value)]

# Multiple values
df[df['column'].isin(['value1', 'value2'])]

# String contains
df[df['column'].str.contains('text', case=False)]

# loc with boolean mask
df.loc[df['rating'] > 4.5, ['title', 'price']]

# iloc with positions
df.iloc[0:5, [0, 2, 4]]

# query method
df.query('column1 > @var and column2 == "value"')
```

## Common Mistakes & Solutions

### Mistake 1: Forgetting Parentheses

```python
# ❌ Wrong: This will cause an error!
df[df['rating'] > 4.5 & df['price'] < 15]

# ✅ Right: Use parentheses around each condition
df[(df['rating'] > 4.5) & (df['price'] < 15)]
```

### Mistake 2: Using 'and'/'or' Instead of &/|

```python
# ❌ Wrong: 'and' doesn't work for DataFrames
df[(df['rating'] > 4.5) and (df['price'] < 15)]

# ✅ Right: Use & for AND, | for OR
df[(df['rating'] > 4.5) & (df['price'] < 15)]
```

### Mistake 3: Confusing loc and iloc Slicing

```python
# iloc[0:3] → rows at positions 0, 1, 2 (excludes 3)
df.iloc[0:3]  # 3 rows

# loc[0:3] → rows with labels 0, 1, 2, 3 (includes 3!)
df.loc[0:3]  # 4 rows
```

## Next Steps

Great filtering work! But what happens when your data is messy? Real-world datasets often have:
- Missing values (NaN, None)
- Duplicate rows
- Inconsistent data types
- Outliers and errors

In **Lesson 04: Data Cleaning Basics**, you'll learn to:
- Detect and handle missing values
- Remove or fix duplicate records
- Convert data to the correct types
- Validate and clean your data

Your next Page Turner Analytics assignment: "Our book catalog has some missing prices and duplicate entries. Can you clean it up before we send it to the marketing team?"

Data cleaning is often 60-80% of a data scientist's work - let's master it! 🧹📊

## Additional Resources

- [pandas Boolean Indexing Guide](https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing)
- [loc and iloc Documentation](https://pandas.pydata.org/docs/user_guide/indexing.html#different-choices-for-indexing)
- [query() Method Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html)
- [10 Common pandas Mistakes](https://www.dataschool.io/common-python-mistakes-in-pandas/)

---

**Happy filtering! 📚📊**

<!--
INSTRUCTOR NOTES

Skills covered (from references/skills/data-science/):
1. accessing-dataframe-columns-by-name.md
   - Accessing DataFrame Columns by Name
   - Difficulty: beginner
2. accessing-dataframe-columns-with-special-formatting.md
   - Accessing DataFrame Columns with Special Formatting
   - Difficulty: beginner
3. calculating-binary-variable-mean-in-pandas.md
   - Calculating Binary Variable Mean in Pandas
   - Difficulty: beginner
4. calculating-column-mean-in-pandas.md
   - Calculating Column Mean in Pandas
   - Difficulty: beginner
5. calculating-correlation-matrices-in-pandas.md
   - Calculating Correlation Matrices in Pandas
   - Difficulty: beginner
6. calculating-sample-means-with-numpy.md
   - Calculating Sample Means with NumPy
   - Difficulty: beginner
7. calculating-summary-statistics-in-pandas.md
   - Calculating Summary Statistics in Pandas
   - Difficulty: beginner
8. calculating-summary-statistics-with-pandas.md
   - Calculating Summary Statistics with Pandas
   - Difficulty: beginner
9. cleaning-string-data-in-pandas-columns.md
   - Cleaning String Data in Pandas Columns
   - Difficulty: beginner
10. converting-continuous-targets-to-binary-classification-labels.md
   - Converting Continuous Targets to Binary Classification Labels
   - Difficulty: beginner
-->