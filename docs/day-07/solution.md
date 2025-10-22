## Task 1 – Parsing and Setting Datetime Index

### 1. Complete Working Code
```python
import pandas as pd

# 1. Load the dataset
sales_df = pd.read_csv("sales.csv")

# 2. Convert 'date' column to datetime format
sales_df['date'] = pd.to_datetime(sales_df['date'], format='%Y-%m-%d', errors='coerce')

# 3. Set 'date' column as the DataFrame index
sales_df.set_index('date', inplace=True)

# 4. Sort index in ascending order
sales_df.sort_index(inplace=True)

# Check result
print(sales_df.index)
print(sales_df.head())
```

### 2. Explanation
We load the CSV into a pandas DataFrame, then use `pd.to_datetime` to reliably convert string dates into `datetime64` objects. Setting the datetime column as the index enables powerful time-series operations like resampling and rolling averages, and sorting ensures chronological order.

### 3. Expected Output
```
DatetimeIndex(['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02', '2023-01-03'],
              dtype='datetime64[ns]', name='date', freq=None)
            sale_id  book_id  quantity  unit_price  total_amount  customer_id
date                                                                          
2023-01-01        1     101        2       15.00         30.00         501
2023-01-01        2     102        1       20.50         20.50         502
2023-01-02        3     103        1       12.00         12.00         503
...
```

### 4. Key Takeaway
Setting a `DatetimeIndex` is the foundation for time-series analysis in pandas.

**Alternative Approaches:**
- Combine parsing and loading using `pd.read_csv("sales.csv", parse_dates=['date'], index_col='date')`.
- Use `infer_datetime_format=True` for faster parsing if dates are standard.

**Common Mistakes:**
1. Forgetting to sort the index, which can cause inaccurate resampling.
2. Not handling invalid date formats → use `errors='coerce'` to turn them into NaT.
3. Setting the index before parsing to datetime leads to incorrect index type.

---

## Task 2 – Weekly Resampling of Total Sales

### 1. Complete Working Code
```python
# 1. Resample to weekly frequency, summing total_amount
weekly_sales = sales_df.resample('W')['total_amount'].sum()

# 2. Reset index for easier viewing
weekly_sales = weekly_sales.reset_index()

# 3. Rename columns appropriately
weekly_sales.columns = ['date', 'total_amount']

print(weekly_sales.head())
```

### 2. Explanation
We leverage `resample('W')` to group by calendar week using the datetime index. Summing `total_amount` aggregates sales for that week. Resetting the index makes it easier to inspect and use in reporting tools.

### 3. Expected Output
```
        date  total_amount
0 2023-01-08       1250.50
1 2023-01-15       1400.75
2 2023-01-22       1320.00
...
```

### 4. Key Takeaway
Weekly resampling is an efficient way to spot broader sales trends beyond daily fluctuations.

**Alternative Approaches:**
- Use `sales_df.groupby(pd.Grouper(freq='W'))['total_amount'].sum().reset_index()` for a single-step process.
- Choose `'W-MON'` or `'W-SUN'` for custom week ending days.

**Common Mistakes:**
1. Resampling without first ensuring a proper `DatetimeIndex`.
2. Forgetting to aggregate after resampling (will result in empty data if not specified).
3. Misinterpreting week end date — by default `'W'` ends on Sunday.

---

## Task 3 – Monthly Genre Trends with Rolling Average

### 1. Complete Working Code
```python
# 1. Load books.csv
books_df = pd.read_csv("books.csv")

# 2. Merge sales_df with books_df on book_id
merged_df = sales_df.reset_index().merge(books_df, on='book_id', how='left')

# 3. Set date back as index for resampling
merged_df['date'] = pd.to_datetime(merged_df['date'])
merged_df.set_index('date', inplace=True)

# 4. Group by genre and resample monthly
monthly_genre_sales = (
    merged_df
    .groupby('genre')
    .resample('M')['total_amount']
    .sum()
    .reset_index()
)

# 5. Compute 3-month rolling average per genre
monthly_genre_sales['monthly_rolling_mean'] = (
    monthly_genre_sales
    .groupby('genre')['total_amount']
    .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
)

# 6. Rename columns for plotting
monthly_genre_sales.columns = ['genre', 'date', 'monthly_total', 'monthly_rolling_mean']

print(monthly_genre_sales.head(10))
```

### 2. Explanation
We combine sales and book metadata to link each sale to its genre. Resampling by month within each genre aggregates monthly totals, and the rolling mean smooths short-term volatility to reveal longer-term trends. This output is ideal for visualization tools.

### 3. Expected Output
```
      genre       date  monthly_total  monthly_rolling_mean
0    Fiction 2023-01-31         520.00               520.00
1    Fiction 2023-02-28         610.00               565.00
2    Fiction 2023-03-31         580.00               570.00
3  Non-Fiction 2023-01-31         430.00               430.00
...
```

### 4. Key Takeaway
Combining metadata with sales and using rolling averages provides clearer insights into genre-specific performance over time.

**Alternative Approaches:**
- Pivot table: `pd.pivot_table(..., index='date', columns='genre', values='total_amount', aggfunc='sum')` then rolling average per column.
- Use `GroupBy.rolling()` directly on a multi-index for more compact code.

**Common Mistakes:**
1. Forgetting to reset the index after resampling before computing grouped rolling averages.
2. Not specifying `min_periods=1` in rolling, which leads to NaN for first months.
3. Merging on wrong key (`sale_id` instead of `book_id`) → incorrect joins.

---