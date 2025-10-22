```markdown
## Task 1 – Parsing and Setting Datetime Index (Easy – ~5 min)

**Goal:** Load `sales.csv`, parse the `date` column as a datetime, and set it as the DataFrame index.

**Instructions:**
1. Import pandas and load the `sales.csv` dataset.
2. Convert the `date` column to a pandas datetime dtype.
3. Set the `date` column as the DataFrame index.
4. Sort the index in ascending order.

**Skeleton Code:**
```python
import pandas as pd

# 1. Load the dataset
sales_df = pd.read_csv("sales.csv")

# 2. Convert date column to datetime
# sales_df['date'] = ...

# 3. Set date as index
# sales_df = ...

# 4. Sort index
# sales_df = ...
```

**Expected Output:**
- `sales_df.index` should be a `DatetimeIndex`.
- The first few rows show sorted dates, e.g. `2023-01-01`, `2023-01-02`, ...

---

## Task 2 – Weekly Resampling of Total Sales (Medium – ~7 min)

**Goal:** Using the indexed sales DataFrame, calculate the total book sales amount per calendar week.

**Instructions:**
1. Resample the data to weekly frequency (`'W'`), summing `total_amount`.
2. Reset the index for easier viewing.
3. Rename columns appropriately.

**Skeleton Code:**
```python
# 1. Resample to weekly frequency
# weekly_sales = sales_df.resample( ... )['total_amount'].sum()

# 2. Reset index
# weekly_sales = ...

# 3. Rename columns
# weekly_sales.columns = [...]
```

**Expected Output:**
- A DataFrame where each row represents a week.
- Columns: `date` (week ending date), `total_amount`.
- Values show aggregated sales per week (e.g., Week ending `2023-01-08` → 1250.50).

---

## Task 3 – Monthly Genre Trends with Rolling Average (Medium-Hard – ~10 min)

**Goal:** Combine sales and books data to see monthly trends by genre, with a rolling average to smooth fluctuations.

**Instructions:**
1. Merge `sales_df` (indexed by date) with `books.csv` on `book_id`.
2. Group by `genre` and resample monthly (`'M'`), summing `total_amount`.
3. For each genre, compute a 3-month rolling average of monthly totals.
4. Return a DataFrame suitable for plotting trends in Dash:
    - Column names: `genre`, `date`, `monthly_total`, `monthly_rolling_mean`.

**Skeleton Code:**
```python
# 1. Load books.csv
books_df = pd.read_csv("books.csv")

# 2. Merge sales_df with books_df
# merged_df = ...

# 3. Group by genre and resample monthly
# monthly_genre_sales = merged_df.groupby('genre').resample( ... )['total_amount'].sum().reset_index()

# 4. Compute rolling average per genre
# monthly_genre_sales['monthly_rolling_mean'] = monthly_genre_sales.groupby('genre')['total_amount'].transform( ... )

# 5. Rename columns as needed
# monthly_genre_sales.columns = [...]
```

**Expected Output:**
- A DataFrame where each genre has a time series of monthly sales totals.
- Rolling average column shows smoothed sales trends.
- Ready to feed into a Dash line chart to compare genres over time.
```