## 📝 Day 5: Aggregation & GroupBy – Solutions

---

### **Task 1 – Total Sales by Genre**

#### **Complete Working Code**
```python
import pandas as pd

# Step 1: Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")

# Step 2: Merge on book_id
# We include 'genre' in the merge result
merged_df = pd.merge(sales, books, on="book_id")

# Step 3: Group by genre and sum total_amount
genre_sales = merged_df.groupby("genre", as_index=False)["total_amount"].sum()

# Step 4: Sort results in descending order of revenue
genre_sales_sorted = genre_sales.sort_values(by="total_amount", ascending=False)

# Display final DataFrame
print(genre_sales_sorted)
```

#### **Explanation**
We read the `books.csv` and `sales.csv` files into DataFrames, then merge them on the shared `book_id` column.  
Grouping by `genre` and summing `total_amount` gives total revenue per genre. Finally, we sort in descending order to see the highest grossing genres first.

#### **Expected Output**
| genre        | total_amount |
|--------------|--------------|
| Mystery      | 12500.50     |
| Science      | 9400.75      |
| Romance      | 8650.00      |

*(Values depend on actual dataset contents.)*

#### **Key Takeaway**
Merging and grouping are essential steps to combine datasets and derive aggregated insights.

#### **Alternative Approaches**
- Use `merged_df.pivot_table(index="genre", values="total_amount", aggfunc="sum").sort_values(...)`.
- Employ SQL queries via `sqlite3` or `pandasql` for more complex joins and filters.

#### **Common Mistakes**
1. Forgetting to merge datasets before grouping, resulting in missing columns.
2. Sorting before summing, which produces incorrect ordering.
3. Grouping by `book_id` instead of `genre`, leading to unnecessary detail.

---

### **Task 2 – Top Author per Genre by Revenue**

#### **Complete Working Code**
```python
import pandas as pd

# Load and merge datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")
merged_df = pd.merge(sales, books, on="book_id")

# Step 1: Group by genre + author_name and sum total_amount
genre_author_sales = (
    merged_df.groupby(["genre", "author_name"], as_index=False)["total_amount"]
    .sum()
)

# Step 2: Sort values by genre and total_amount descending
genre_author_sorted = genre_author_sales.sort_values(
    by=["genre", "total_amount"], ascending=[True, False]
)

# Step 3: Select top author for each genre
top_authors_by_genre = genre_author_sorted.groupby("genre").head(1).reset_index(drop=True)

print(top_authors_by_genre)
```

#### **Explanation**
We group by both `genre` and `author_name` to calculate revenue per author within each genre.  
Sorting ensures the highest revenue author is first for each genre, and `groupby(...).head(1)` extracts just the top performer per genre.

#### **Expected Output**
| genre       | author_name       | total_amount |
|-------------|-------------------|--------------|
| Mystery     | Agatha Christie   | 7200.25      |
| Science     | Carl Sagan        | 5400.50      |
| Romance     | Jane Austen       | 5000.00      |

#### **Key Takeaway**
Combining `groupby` and sorting allows us to rank items within categories and select top results.

#### **Alternative Approaches**
- Use `idxmax()` within `groupby` to directly select max revenue authors.
- Apply `nlargest(1, 'total_amount')` in a group-wise `apply`.

#### **Common Mistakes**
1. Using `max()` incorrectly, which loses other columns like author_name.
2. Sorting on total_amount only, ignoring genre, which can mix authors across genres.
3. Forgetting to reset_index for clean output.

---

### **Task 3 – Genre vs Year Pivot Table: Average Revenue per Sale**

#### **Complete Working Code**
```python
import pandas as pd

# Load and merge datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")
merged_df = pd.merge(sales, books, on="book_id")

# Step 2: Construct pivot table for average total_amount per sale
pivot = pd.pivot_table(
    merged_df,
    index="genre",
    columns="publication_year",
    values="total_amount",
    aggfunc="mean"
)

# Step 3: Fill NA with 0 for missing combinations
pivot_filled = pivot.fillna(0)

# Step 4: Sort by overall average revenue across years
pivot_filled["overall_avg"] = pivot_filled.mean(axis=1)
sorted_pivot = pivot_filled.sort_values(by="overall_avg", ascending=False).drop(columns="overall_avg")

print(sorted_pivot)
```

#### **Explanation**
Using `pd.pivot_table`, we reshape data to show genres as rows and publication years as columns, computing the mean revenue per sale for each combination.  
Filling NaNs with 0 improves readability, and sorting by overall average highlights the highest performing genres.

#### **Expected Output**
| genre     | 2018    | 2019    | 2020    |
|-----------|---------|---------|---------|
| Mystery   | 25.40   | 27.35   | 26.50   |
| Science   | 22.00   | 23.80   | 0.00    |
| Romance   | 18.75   | 0.00    | 20.50   |

#### **Key Takeaway**
Pivot tables in pandas are powerful for multi-dimensional aggregation and comparison.

#### **Alternative Approaches**
- Use `groupby(['genre', 'publication_year']).mean().unstack(fill_value=0)` instead of pivot_table.
- Perform manual aggregation with nested dictionaries and construct DataFrame.

#### **Common Mistakes**
1. Using `aggfunc='sum'` when average is required.
2. Not handling missing values, which leaves NaNs that complicate interpretation.
3. Forgetting to drop helper columns after sorting, resulting in cluttered output.