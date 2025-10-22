# Day 5: Aggregation & GroupBy – Sales by Genre  
**Week 1 | Difficulty: Intermediate | Duration: 3-5 min**

---

## Introduction
At Page Turner Analytics, our marketing department wants to know which genres generate the most revenue—and which authors dominate within each genre. Building on what you’ve learned so far about selecting, filtering, and cleaning data, today we’ll explore **grouping and aggregating** sales to spot trends. We’ll calculate summary statistics per category and learn how pivot tables can help visualize complex relationships—just like transit planners use ridership data by season or time of day to plan schedules.

---

## 1. Grouping Data with `groupby`
In Python’s **pandas** library, `groupby` lets us split our dataset into groups based on unique values in one or more columns. Once grouped, we can run **aggregation functions** such as `.sum()`, `.mean()`, `.count()`, etc.

Think of it like sorting books on a shelf by **genre**, then summing up their total sales. This is similar to grouping ridership counts by season in the public transit example. The idea is:  
- **Split** data by grouping columns (e.g., `genre`)  
- **Apply** aggregation (e.g., `sum`, `mean`, `max`)  
- **Combine** results into a new summary table.

Grouping helps answer questions like:
> _"What’s the average revenue generated per genre?"_

---

## 2. Aggregation Functions
Once the data is grouped, we can call functions:
- **`sum()`** – total values per group (e.g., total revenue per author)  
- **`mean()`** – average values per group (e.g., average price of books per genre)  
- **`count()`** – number of records in each group (e.g., books sold per genre)  

We can even **aggregate multiple columns** or **multiple functions**:

```python
grouped.agg({
    'total_amount': 'sum',
    'unit_price': 'mean'
})
```

This flexibility lets us see multiple statistics side-by-side.

---

## 3. Pivot Tables for Cross-Tabulation
A pivot table reorganizes data into a grid so we can cross-tabulate categories—like rows and columns in Excel.

In the transit data example, they used a pivot table of **hour** vs **weekday** to visualize ridership using a heatmap.  
In our bookstore scenario, we might want to see **genres** as rows and **authors** as columns, showing total sales as the values.

Why it matters:
- Quickly compare across two dimensions (e.g., which author dominates each genre).
- Makes patterns visible at a glance.

---

## Code Examples

### Example 1 – Total Sales by Genre
```python
import pandas as pd

# Load datasets
books = pd.read_csv('books.csv')
sales = pd.read_csv('sales.csv')

# Merge sales with books to get genre info
sales_books = sales.merge(books, on='book_id')

# Group by genre and sum total sales
genre_sales = sales_books.groupby('genre')['total_amount'].sum().reset_index()

print(genre_sales)
# Expected output:
#       genre   total_amount
# 0    Fiction       25000.75
# 1  Non-Fiction    18000.50
# 2  Mystery        22000.00
```

---

### Example 2 – Summary Stats by Genre and Author
```python
# Group by both genre and author_name
stats = sales_books.groupby(['genre', 'author_name']).agg({
    'quantity': 'sum',      # total units sold
    'total_amount': 'sum',  # total revenue
    'unit_price': 'mean'    # average unit price
}).reset_index()

print(stats.head())
# Expected output:
#       genre    author_name    quantity   total_amount  unit_price
# 0    Fiction   Alice Moore   1200       15000.00      12.50
# 1    Fiction   Brian Scott   950        10000.00      10.53
```

---

### Example 3 – Pivot Table for Sales by Genre and Author
```python
# Pivot table: genre as index, author_name as columns
pivot_sales = pd.pivot_table(
    sales_books,
    index='genre',
    columns='author_name',
    values='total_amount',
    aggfunc='sum',
    fill_value=0  # Replace NaNs with 0
)

print(pivot_sales)
# Expected output (sample):
# author_name  Alice Moore  Brian Scott  Chloe Diaz
# genre
# Fiction         15000.0     10000.0     0.0
# Mystery         5000.0       0.0        7000.0
```

---

## Common Pitfalls
1. **Forgetting to Reset Index**  
   After grouping, pandas returns a DataFrame with grouped columns as an index. Use `.reset_index()` to make them regular columns if needed.

2. **Mismatched Column Names**  
   When merging datasets, ensure the join keys (`book_id` in this case) match exactly in name and format.

3. **NaN Issues in Pivot Tables**  
   Missing values can appear when certain combinations don’t exist. Use `fill_value=0` to make the table cleaner.

---

## Practice Checkpoint
✅ I can group data by one or more columns and apply aggregation functions.  
✅ I can calculate multiple summary statistics per group.  
✅ I can create pivot tables to compare data across two categorical dimensions.

---