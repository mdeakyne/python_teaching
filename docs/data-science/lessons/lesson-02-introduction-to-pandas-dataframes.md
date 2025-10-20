---
title: Introduction to pandas DataFrames
---

# Introduction to pandas DataFrames

```{admonition} Lesson Info
:class: note
**Duration**: 90 minutes
**Difficulty**: Beginner
**Prerequisites**: Lesson 01 completed, Basic Python (lists, dictionaries)
```

## Learning Objectives

By the end of this lesson, you will be able to:

- Load data from CSV and Excel files into pandas
- Understand DataFrame structure and components
- Inspect data using head(), tail(), info(), and describe()
- Select and access DataFrame columns

## Introduction

Welcome back to **Page Turner Analytics**! 📚

In Lesson 01, you set up your data science workstation. Now it's time to start working with real data!

Your manager just handed you your first assignment: analyze the company's book catalog data. The data is stored in CSV and Excel files, and you need to load it into Python to start exploring.

Think of pandas DataFrames as **supercharged spreadsheets**. Like Excel, they have rows and columns. But unlike Excel, they can:
- Handle millions of rows efficiently
- Perform complex operations with a single line of code
- Integrate seamlessly with visualizations and statistical analysis
- Be version-controlled and reproduced exactly

By the end of this lesson, you'll be loading real datasets and inspecting them like a pro!

## Loading Data

The first step in any data analysis is loading your data. pandas makes this incredibly easy with its `read_*` functions.

### Reading CSV Files

CSV (Comma-Separated Values) is the most common data format you'll encounter:

```{code-cell} ipython3
import pandas as pd

# Let's create a sample book catalog CSV to practice with
# In real work, you'd read an existing file

# First, create sample data and save it
book_data = """title,author,year_published,pages,rating,price,genre
The Catcher in the DataFrame,J.D. Salinger,1951,234,4.2,12.99,Fiction
Moby DataFrame,Herman Melville,1851,585,4.1,15.99,Fiction
Pride and Preprocessing,Jane Austen,1813,432,4.7,11.99,Romance
The Great Gatsby Dataframe,F. Scott Fitzgerald,1925,218,4.8,13.99,Fiction
To Kill a Mockingbird Dataset,Harper Lee,1960,281,4.9,14.99,Fiction
War and Python,Leo Tolstoy,1869,1296,4.3,22.99,Historical Fiction
1984 Bytes,George Orwell,1949,328,4.6,13.49,Dystopian
The Hobbit: There and Back Again.csv,J.R.R. Tolkien,1937,310,4.8,16.99,Fantasy
Harry Potter and the Philosopher's Code,J.K. Rowling,1997,223,4.9,17.99,Fantasy
The Hitchhiker's Guide to the DataFrame,Douglas Adams,1979,193,4.7,12.49,Sci-Fi"""

# Save to a CSV file
with open('data/book_catalog.csv', 'w') as f:
    f.write(book_data)

# Now read it with pandas!
books_df = pd.read_csv('data/book_catalog.csv')
print("📚 Book Catalog Loaded Successfully!")
print(books_df)
```

**Key `read_csv()` Parameters**:
- `sep=','`: Specify delimiter (default is comma)
- `header=0`: Which row contains column names (default is first row)
- `index_col=None`: Set a column as the index
- `usecols=['title', 'rating']`: Load only specific columns
- `nrows=100`: Load only first N rows (useful for large files)

### Reading Excel Files

Many businesses store data in Excel files:

```{code-cell} ipython3
# Reading Excel files (requires openpyxl or xlrd library)
# books_excel = pd.read_excel('data/book_catalog.xlsx', sheet_name='Sheet1')

# You can also read specific sheets
# books_excel = pd.read_excel('data/book_catalog.xlsx', sheet_name='Q1_Sales')

# Or read all sheets at once
# all_sheets = pd.read_excel('data/book_catalog.xlsx', sheet_name=None)
# This returns a dictionary: {'Sheet1': df1, 'Sheet2': df2, ...}
```

```{admonition} File Path Tips
:class: tip
- Use forward slashes `/` even on Windows: `'data/books.csv'`
- Use raw strings for Windows paths: `r'C:\Users\data\books.csv'`
- Use relative paths from your notebook location: `'../data/books.csv'`
```

## DataFrame Anatomy

Let's dissect a DataFrame to understand its structure:

```{code-cell} ipython3
import pandas as pd

# Reload our book catalog
books_df = pd.read_csv('data/book_catalog.csv')

print("🔍 DataFrame Anatomy Lesson\n")
print("=" * 60)

# 1. Shape: (rows, columns)
print(f"Shape: {books_df.shape}")
print(f"  → {books_df.shape[0]} rows (books in our catalog)")
print(f"  → {books_df.shape[1]} columns (attributes per book)\n")

# 2. Columns
print(f"Columns: {books_df.columns.tolist()}")
print(f"  → These are the attributes we track for each book\n")

# 3. Index
print(f"Index: {books_df.index.tolist()}")
print(f"  → Default numeric index (0, 1, 2, ...)\n")

# 4. Data Types
print("Data Types:")
print(books_df.dtypes)
```

**Understanding Data Types**:
- `int64`: Integer numbers (pages, year)
- `float64`: Decimal numbers (rating, price)
- `object`: Text/strings (title, author, genre)
- `bool`: True/False values
- `datetime64`: Dates and times

**Visual Representation**:
```
         Index  │  Column Names
                │  title    author    pages   rating   price
        ─────────┼────────────────────────────────────────────
Row 0   →    0  │  "Book"  "Author"   234     4.2     12.99
Row 1   →    1  │  "Book"  "Author"   585     4.1     15.99
Row 2   →    2  │  "Book"  "Author"   432     4.7     11.99
                     ↑        ↑         ↑       ↑        ↑
                  Series   Series   Series  Series   Series
```

Each column is a **Series** (pandas' 1-dimensional data structure). A DataFrame is a collection of Series!

## Basic Data Inspection

pandas provides powerful methods to quickly understand your data:

### Quick Peek: head() and tail()

```{code-cell} ipython3
import pandas as pd
books_df = pd.read_csv('data/book_catalog.csv')

print("📖 First 5 Books (head):")
print(books_df.head())
print("\n" + "=" * 60 + "\n")

print("📖 Last 3 Books (tail):")
print(books_df.tail(3))
```

### Information Summary: info()

```{code-cell} ipython3
print("ℹ️  DataFrame Info:")
books_df.info()
```

**What `info()` tells you**:
- Number of rows and columns
- Column names and their data types
- Non-null counts (helps identify missing data!)
- Memory usage

### Statistical Summary: describe()

```{code-cell} ipython3
print("📊 Statistical Summary:")
print(books_df.describe())
```

**What `describe()` shows for numeric columns**:
- `count`: Number of non-null values
- `mean`: Average value
- `std`: Standard deviation (spread of data)
- `min`: Minimum value
- `25%`, `50%`, `75%`: Percentiles (quartiles)
- `max`: Maximum value

```{admonition} Pro Tip: describe() for Text
:class: tip
Use `books_df.describe(include='object')` to get statistics on text columns:
- count, unique values, most frequent value (top), frequency of top value
```

### Other Useful Inspection Methods

```{code-cell} ipython3
# Get column names as a list
print("Column names:", books_df.columns.tolist())

# Get unique values in a column
print("\nUnique genres:", books_df['genre'].unique())
print(f"Number of unique genres: {books_df['genre'].nunique()}")

# Value counts: how many books in each genre?
print("\nBooks per genre:")
print(books_df['genre'].value_counts())

# Check for missing data
print("\nMissing values per column:")
print(books_df.isnull().sum())
```

## Selecting Columns

There are multiple ways to access columns in a DataFrame:

### Single Column Selection

```{code-cell} ipython3
import pandas as pd
books_df = pd.read_csv('data/book_catalog.csv')

# Method 1: Bracket notation (always works)
titles = books_df['title']
print("Method 1 - Bracket notation:")
print(titles.head(3))
print(f"Type: {type(titles)}")  # pandas.Series
print()

# Method 2: Dot notation (only works if column name is valid Python identifier)
titles_dot = books_df.title
print("Method 2 - Dot notation:")
print(titles_dot.head(3))
```

**Bracket vs Dot Notation**:
- ✅ `books_df['title']` - Always works
- ✅ `books_df.title` - Clean, but only if column name has no spaces/special chars
- ❌ `books_df.year published` - Won't work (space in name)
- ✅ `books_df['year_published']` - Works!

### Multiple Column Selection

```{code-cell} ipython3
# Select multiple columns: pass a LIST of column names
subset = books_df[['title', 'author', 'rating']]
print("📚 Book Ratings Subset:")
print(subset.head())
print(f"\nType: {type(subset)}")  # pandas.DataFrame
```

**Key Difference**:
- `books_df['title']` → Returns a **Series** (1-dimensional)
- `books_df[['title']]` → Returns a **DataFrame** (2-dimensional with 1 column)
- `books_df[['title', 'rating']]` → Returns a **DataFrame** (2-dimensional with 2 columns)

### Creating New Columns from Existing Ones

```{code-cell} ipython3
# Calculate price per page
books_df['price_per_page'] = books_df['price'] / books_df['pages']

# Add a column based on conditions
books_df['long_book'] = books_df['pages'] > 400

# Display results
print("📖 Books with New Calculated Columns:")
print(books_df[['title', 'pages', 'price', 'price_per_page', 'long_book']].head())
```

## Practice Exercise

```{admonition} Exercise: Explore the Book Catalog
:class: tip

**Part 1: Load and Inspect**
1. Load the `book_catalog.csv` file you created
2. Display the first 5 rows
3. Use `info()` to check data types and missing values
4. Use `describe()` to get summary statistics

**Part 2: Answer These Questions**
1. How many books are in the catalog?
2. What is the average book rating?
3. What is the most expensive book?
4. How many unique authors are there?
5. Which genre has the most books?

**Part 3: Column Operations**
1. Select only the 'title', 'rating', and 'price' columns
2. Create a new column called 'price_category':
   - 'Budget' if price < 13
   - 'Standard' if 13 ≤ price < 17
   - 'Premium' if price ≥ 17
3. Display the 5 highest-rated books with their price categories

**Bonus Challenge**
1. Find all books published before 1950
2. Calculate the average pages for Fiction vs non-Fiction books
3. Identify books where the rating is above 4.5 AND price is below $15
```

## Summary

Congratulations! You've completed your first real data analysis assignment at Page Turner Analytics! 📚

In this lesson, you learned how to:

- ✅ **Load data** from CSV files (and Excel files) using `pd.read_csv()`
- ✅ **Understand DataFrame structure**: rows, columns, index, data types
- ✅ **Inspect data** using `head()`, `tail()`, `info()`, and `describe()`
- ✅ **Select columns** using bracket and dot notation
- ✅ **Create new columns** from existing data
- ✅ **Explore data** with `unique()`, `nunique()`, and `value_counts()`

You now have the fundamental skills to load any dataset and perform initial exploration - a critical first step in every data science project!

## Common Issues & Solutions

### Issue: "FileNotFoundError: book_catalog.csv"

**Problem**: Python can't find your CSV file.

**Solution**:
```{code-cell} ipython3
import os
print("Current directory:", os.getcwd())
print("Files in data folder:", os.listdir('data'))

# Make sure the data folder exists
os.makedirs('data', exist_ok=True)
```

### Issue: "ParserError: Error tokenizing data"

**Problem**: CSV file has formatting issues (inconsistent delimiters, quotes).

**Solution**:
```{code-cell} ipython3
# Try specifying encoding
books_df = pd.read_csv('data/book_catalog.csv', encoding='utf-8')

# Or try different delimiter
books_df = pd.read_csv('data/book_catalog.csv', sep=';')

# Or skip bad lines (use with caution!)
books_df = pd.read_csv('data/book_catalog.csv', on_bad_lines='skip')
```

### Issue: "KeyError: 'column_name'"

**Problem**: Column name doesn't exist or has typo.

**Solution**:
```{code-cell} ipython3
# Check actual column names
print(books_df.columns.tolist())

# Use exact column name (case-sensitive!)
# Wrong: books_df['Title']
# Right: books_df['title']
```

## Next Steps

Great job! You can now load and inspect data like a pro. But what if you only want to analyze *some* of the books - like all Fiction books published after 1950, or books with ratings above 4.5?

In **Lesson 03: Data Selection & Filtering**, you'll learn powerful techniques to:
- Filter rows using boolean conditions
- Master `loc` and `iloc` for precise selection
- Combine multiple conditions with AND/OR logic
- Use the `query()` method for readable complex filters

Your manager already has your next assignment ready: "Find all Fantasy books under $15 with ratings above 4.7" 📊

## Additional Resources

- [pandas Official Tutorial](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)
- [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [Real Python: pandas DataFrames](https://realpython.com/pandas-dataframe/)

---

**Happy analyzing! 📚📊**

<!--
INSTRUCTOR NOTES

Skills covered (from references/skills/data-science/):
1. accessing-dataframe-columns-by-name.md
   - Accessing DataFrame Columns by Name
   - Difficulty: beginner
2. accessing-dataframe-columns-with-special-formatting.md
   - Accessing DataFrame Columns with Special Formatting
   - Difficulty: beginner
3. adding-predicted-values-to-a-pandas-dataframe.md
   - Adding Predicted Values to a Pandas DataFrame
   - Difficulty: beginner
4. adjusting-pandas-display-options.md
   - Adjusting Pandas Display Options
   - Difficulty: beginner
5. avoiding-modification-of-global-variables-in-dash-apps.md
   - Avoiding Modification of Global Variables in Dash Apps
   - Difficulty: beginner
6. calculating-binary-variable-mean-in-pandas.md
   - Calculating Binary Variable Mean in Pandas
   - Difficulty: beginner
7. calculating-column-mean-in-pandas.md
   - Calculating Column Mean in Pandas
   - Difficulty: beginner
8. calculating-correlation-matrices-in-pandas.md
   - Calculating Correlation Matrices in Pandas
   - Difficulty: beginner
9. calculating-pearson-correlation-coefficient-in-pandas.md
   - Calculating Pearson Correlation Coefficient in Pandas
   - Difficulty: beginner
10. calculating-pearson-correlation-coefficient-with-pandas.md
   - Calculating Pearson Correlation Coefficient with pandas
   - Difficulty: beginner
-->