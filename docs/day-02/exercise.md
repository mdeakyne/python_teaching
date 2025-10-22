```markdown
## Task 1 (Easy – 5 min): Load and Peek at Books Data

**Goal:** Load the `books.csv` dataset and inspect the first few rows.

**Instructions:**
1. Import `pandas` as `pd`.
2. Load the `books.csv` file into a DataFrame named `books_df`.
3. Use `.head()` to display the first 5 rows.

**Skeleton Code:**
```python
import pandas as pd

# Step 1: Load CSV into DataFrame
books_df = pd.read_csv("data/books.csv")  # adjust path as needed

# Step 2: Peek at the data
# Your code here to view first rows
```

**Expected Output:**
- You should see a printed table with columns: `book_id`, `title`, `author_id`, `author_name`, `genre`, `price`, `publication_year`, `pages`.
- 5 rows displayed with sample book titles and details.

---

## Task 2 (Medium – 7 min): Inspect Authors Data with Multiple Methods

**Goal:** Load the `authors.csv` dataset and explore its structure using `.info()` and `.describe()`.

**Instructions:**
1. Load `authors.csv` into a DataFrame named `authors_df`.
2. Use `.info()` to see data types and non-null counts.
3. Use `.describe()` to summarize numeric columns.

**Skeleton Code:**
```python
import pandas as pd

# Step 1: Load Authors data
authors_df = pd.read_csv("data/authors.csv")

# Step 2: Inspect structure
# Your code here for .info()

# Step 3: Summarize numerical data
# Your code here for .describe()
```

**Expected Output:**
- `.info()` displays column names, data types (e.g., int64, object), and non-null counts.
- `.describe()` lists statistics like `count`, `mean`, `min`, `max` for numeric fields such as `birth_year`.

---

## Task 3 (Medium-Hard – 10 min): Combine and Explore Sales & Books Data

**Goal:** Load sales data, merge it with book titles, and inspect recent transactions.

**Instructions:**
1. Load `sales.csv` into `sales_df`.
2. Merge `sales_df` with `books_df` (from Task 1) on the `book_id` column to get the book title in the sales table.
3. Sort merged DataFrame by `date` in descending order.
4. Use `.head()` to view the 10 most recent sales.

**Skeleton Code:**
```python
import pandas as pd

# Step 1: Load datasets
sales_df = pd.read_csv("data/sales.csv")
books_df = pd.read_csv("data/books.csv")

# Step 2: Merge on 'book_id'
merged_df = # your merge code here

# Step 3: Sort by date descending
# your sort code here

# Step 4: View top 10 recent sales
# your head() code here
```

**Expected Output:**
- 10 rows showing recent transactions with columns: `sale_id`, `date`, `book_id`, `title`, `quantity`, `unit_price`, `total_amount`, etc.
- Sorted so the most recent sale dates appear first.
```