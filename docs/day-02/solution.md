```markdown
## Task 1 (Easy – 5 min): Load and Peek at Books Data

### Complete Working Code
```python
import pandas as pd

# Step 1: Load CSV into DataFrame
# Assuming the CSV file is in a 'data' directory
books_df = pd.read_csv("data/books.csv")

# Step 2: Peek at the data - first 5 rows
print(books_df.head())
```

### Explanation
We import pandas, load the dataset from the provided path using `pd.read_csv()`, and store it in a DataFrame named `books_df`. We then call `.head()` to view the first five rows for a quick understanding of the data's structure.

### Expected Output
```
   book_id                      title  author_id        author_name     genre  price  publication_year  pages
0        1       The Winds of Winter         101      George R. R. Martin  Fantasy   29.99              2023    1024
1        2       Pride and Prejudice         102      Jane Austen          Romance   15.50              1813     432
2        3       A Brief History of Time      103      Stephen Hawking     Science   18.75              1988     256
3        4       The Great Gatsby           104      F. Scott Fitzgerald Fiction   12.99              1925     180
4        5       Moby-Dick                 105      Herman Melville     Adventure   14.95              1851     720
```

### Key Takeaway
`pd.read_csv()` combined with `.head()` is the quickest way to load and inspect the top rows of a dataset.

### Alternative Approaches
- Use `books_df.sample(5)` to view random rows for varied snapshot.
- Use `.head(n)` where `n` is any integer to view more/less rows.

### Common Mistakes
1. Providing an incorrect file path, causing a `FileNotFoundError`.
2. Forgetting to include `import pandas as pd`.
3. Overlooking that `.head()` defaults to 5 rows, causing confusion when expecting a different number.


---

## Task 2 (Medium – 7 min): Inspect Authors Data with Multiple Methods

### Complete Working Code
```python
import pandas as pd

# Step 1: Load Authors data
authors_df = pd.read_csv("data/authors.csv")

# Step 2: Inspect structure
print("\n--- Authors Data Info ---")
authors_df.info()

# Step 3: Summarize numerical data
print("\n--- Authors Data Summary ---")
print(authors_df.describe())
```

### Explanation
After reading the authors dataset into `authors_df`, we call `.info()` to display the DataFrame's column names, data types, and counts of non-null values. `.describe()` computes summary statistics for numeric columns, giving an overview of distributions.

### Expected Output
```
--- Authors Data Info ---
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 150 entries, 0 to 149
Data columns (total 6 columns):
 #   Column      Non-Null Count  Dtype 
---  ------      --------------  ----- 
 0   author_id   150 non-null    int64 
 1   first_name  150 non-null    object
 2   last_name   150 non-null    object
 3   full_name   150 non-null    object
 4   birth_year  148 non-null    float64
 5   country     150 non-null    object
dtypes: float64(1), int64(1), object(4)

--- Authors Data Summary ---
       author_id    birth_year
count  150.000000   148.000000
mean   175.240000  1965.540541
std     12.520000    15.245672
min    101.000000  1920.000000
max    200.000000  1999.000000
```

### Key Takeaway
`.info()` is ideal for understanding structure and completeness, while `.describe()` provides quick statistical insights into numeric data.

### Alternative Approaches
- Use `authors_df.dtypes` to see data types directly.
- Use `authors_df.describe(include="all")` to summarize both numeric and categorical data.

### Common Mistakes
1. Forgetting parentheses on `.info()` which will print a method object instead.
2. Using `.describe()` without considering non-numeric columns.
3. Assuming `.describe()` shows all columns—by default it only shows numeric ones unless `include` is specified.


---

## Task 3 (Medium-Hard – 10 min): Combine and Explore Sales & Books Data

### Complete Working Code
```python
import pandas as pd

# Step 1: Load datasets
sales_df = pd.read_csv("data/sales.csv")
books_df = pd.read_csv("data/books.csv")

# Step 2: Merge on 'book_id' to bring book titles into sales data
merged_df = pd.merge(sales_df, books_df[['book_id', 'title']], on='book_id', how='left')

# Step 3: Sort by date descending
merged_df['date'] = pd.to_datetime(merged_df['date'], errors='coerce')  # ensure proper date type
merged_df_sorted = merged_df.sort_values(by='date', ascending=False)

# Step 4: View top 10 recent sales
print(merged_df_sorted.head(10))
```

### Explanation
We first load both the sales and books datasets. By merging them on `book_id` and selecting only essential fields from `books_df`, we combine sales transaction data with book titles. Converting the date column to `datetime` ensures proper sorting by date, and `.head(10)` lets us inspect the most recent sales quickly.

### Expected Output
```
   sale_id       date  book_id  quantity  unit_price  total_amount customer_id                         title
89     450 2023-12-30       12         1       22.99         22.99       C100   The Name of the Wind
32     300 2023-12-29        5         2       14.95         29.90       C045   Moby-Dick
...
```

*(10 rows total, most recent first)*

### Key Takeaway
Merging DataFrames on a common key allows you to enrich datasets, and sorting gives control over the order in which you view the data.

### Alternative Approaches
- Use `.merge()` with `how='inner'` to exclude non-matching records.
- Use `DataFrame.join()` if indexes are aligned instead of columns.
- Chain operations (`pd.merge(...).sort_values(...)`) for concise code.

### Common Mistakes
1. Forgetting to convert string dates to `datetime` before sorting.
2. Not selecting relevant columns from the second DataFrame, leading to unnecessarily large merged datasets.
3. Using the wrong join type and unexpectedly dropping rows in the merge.
```
