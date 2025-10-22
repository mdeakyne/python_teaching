```markdown
## 📝 Day 5: Aggregation & GroupBy – Hands-On Exercises

---

### **Task 1 – Total Sales by Genre**  
**Difficulty:** Easy | ⏱ ~5 min  

**Goal:**  
Load the `books.csv` and `sales.csv` datasets, merge them, and calculate **total revenue** per genre.

**Instructions:**  
1. Read `books.csv` and `sales.csv` into DataFrames.  
2. Merge them on `book_id`.  
3. Group by `genre` and calculate the sum of `total_amount`.  
4. Sort results in descending order of revenue.  

```python
import pandas as pd

# Step 1: Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")

# Step 2: Merge on book_id
merged_df = ...

# Step 3: Group by genre and sum total_amount
genre_sales = ...

# Step 4: Sort results
genre_sales_sorted = ...

print(genre_sales_sorted)
```

**Expected Output:**  
A DataFrame showing each genre and its total revenue, sorted from highest to lowest.  
_Example:_  

| genre        | total_amount |
|--------------|--------------|
| Mystery      | 12500.50     |
| Science      | 9400.75      |
| Romance      | 8650.00      |

---

### **Task 2 – Top Author per Genre by Revenue**  
**Difficulty:** Medium | ⏱ ~7 min  

**Goal:**  
Identify the **top-selling author** in each genre by total revenue.

**Instructions:**  
1. Continue from the merged DataFrame in Task 1 (ensure `author_name` is included).  
2. Group by both `genre` and `author_name`, sum `total_amount`.  
3. Sort within each genre to find the top-selling author.  
4. Output one author per genre.

```python
# Step 1: Group by genre + author_name
genre_author_sales = ...

# Step 2: Sort values appropriately
genre_author_sorted = ...

# Step 3: Select top author for each genre
top_authors_by_genre = ...

print(top_authors_by_genre)
```

**Expected Output:**  
A DataFrame showing `genre`, `author_name`, and their revenue. Only the top author per genre should be listed.  

| genre       | author_name       | total_amount |
|-------------|-------------------|--------------|
| Mystery     | Agatha Christie   | 7200.25      |
| Science     | Carl Sagan        | 5400.50      |
| Romance     | Jane Austen       | 5000.00      |

---

### **Task 3 – Genre vs Year Pivot Table: Average Revenue per Sale**  
**Difficulty:** Medium-Hard | ⏱ ~10 min  

**Goal:**  
Create a **pivot table** showing the average `total_amount` per sale, broken down by `genre` (rows) and `publication_year` (columns).

**Instructions:**  
1. Merge `books.csv` and `sales.csv` as done before.  
2. Use `pd.pivot_table()` to set:
   - `index` = genre  
   - `columns` = publication_year  
   - `values` = total_amount  
   - `aggfunc` = 'mean'  
3. Fill missing values with 0 for better display.  
4. Sort genres by their overall average revenue across years.

```python
# Step 1: Create merged DataFrame
merged_df = ...

# Step 2: Construct pivot table
pivot = pd.pivot_table(
    merged_df,
    index=...,
    columns=...,
    values=...,
    aggfunc=...
)

# Step 3: Fill NA with 0
pivot_filled = ...

# Step 4: Sort by overall average revenue
sorted_pivot = ...

print(sorted_pivot)
```

**Expected Output:**  
A pivot table showing genres as rows, publication years as columns, and average revenue per sale in each cell. Missing genre/year combos should be 0.  
_Example:_  

| genre     | 2018    | 2019    | 2020    |
|-----------|---------|---------|---------|
| Mystery   | 25.40   | 27.35   | 26.50   |
| Science   | 22.00   | 23.80   | 0.00    |
| Romance   | 18.75   | 0.00    | 20.50   |

---
```