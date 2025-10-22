## 📊 Day 8 – Matplotlib Basics: First Charts – Complete Solutions

---

### **Task 1 – Easy: Line Chart of Monthly Sales Trends**

#### **Complete Working Code**
```python
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the data
sales = pd.read_csv("sales.csv")

# Step 2: Convert 'date' column to datetime
sales['date'] = pd.to_datetime(sales['date'])

# Step 3: Group by month and sum total_amount
# Ensure month order by using dt.to_period('M')
monthly_sales = sales.groupby(sales['date'].dt.to_period('M'))['total_amount'].sum()

# Step 4: Plot line chart
plt.figure(figsize=(8, 5))
plt.plot(monthly_sales.index.astype(str), monthly_sales.values, marker='o', linestyle='-')
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.title("Monthly Sales Trend - Page Turner Analytics")
plt.grid(True)
plt.tight_layout()
plt.show()
```

#### **Explanation**
We load the sales data, convert dates to proper datetime format, and use `dt.to_period('M')` for month-based grouping. Summing `total_amount` gives monthly totals, which we plot using Matplotlib for a clear trend visualization.

#### **Expected Output**
A clean **line chart** with 12 points representing each month of the year, showing fluctuations in total revenue, with months labeled and a grid.

#### **Key Takeaway**
Grouping by months simplifies time-series analysis and makes trends immediately visible.

#### **Alternative Approaches**
- Use `sales.resample('M', on='date')` for direct time-based aggregation.
- Format month labels with `strftime('%b')` to show short month names.

#### **Common Mistakes**
1. Forgetting to convert `date` column to datetime type.
2. Misordering months by grouping on strings instead of datetime.
3. Not calling `plt.show()` when running as a script.

---

### **Task 2 – Medium: Bar Chart Comparing Genre Revenue**

#### **Complete Working Code**
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
sales = pd.read_csv("sales.csv")
books = pd.read_csv("books.csv")

# Merge on 'book_id'
sales_books = pd.merge(sales, books, on='book_id')

# Group by genre and sum total_amount
genre_sales = sales_books.groupby('genre')['total_amount'].sum().sort_values(ascending=False)

# Plot bar chart
plt.figure(figsize=(8, 5))
colors = plt.cm.Paired(range(len(genre_sales)))  # Different color per bar
plt.bar(genre_sales.index, genre_sales.values, color=colors)
plt.xlabel("Genre")
plt.ylabel("Total Revenue")
plt.title("Revenue by Book Genre")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

#### **Explanation**
We merge `sales.csv` and `books.csv` to enrich sales data with genres. Grouping by `genre` and summing `total_amount` creates the dataset for a colorful sorted bar chart.

#### **Expected Output**
A **bar chart** with each genre on the X-axis and total revenue sorted from highest to lowest, each bar in a distinct color, labels rotated for readability.

#### **Key Takeaway**
Merging datasets before grouping enables richer insights and customized plots.

#### **Alternative Approaches**
- Use `seaborn.barplot` for automatic color handling and statistical summaries.
- Normalize revenue to percentages for proportional comparison.

#### **Common Mistakes**
1. Forgetting to sort genres by revenue for a cleaner visual.
2. Misaligned merges by using wrong keys.
3. Overcrowded labels without rotation.

---

### **Task 3 – Medium-Hard: Combined Chart – Sales Trend for Top Genre**

#### **Complete Working Code**
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
sales = pd.read_csv("sales.csv")
books = pd.read_csv("books.csv")

# Merge datasets on 'book_id'
sales_books = pd.merge(sales, books, on='book_id')

# Find top genre by revenue
genre_revenue = sales_books.groupby('genre')['total_amount'].sum()
top_genre = genre_revenue.idxmax()

# Filter for that genre
top_genre_sales = sales_books[sales_books['genre'] == top_genre]

# Convert date to datetime for both
sales_books['date'] = pd.to_datetime(sales_books['date'])
top_genre_sales['date'] = pd.to_datetime(top_genre_sales['date'])

# Group monthly revenue for top genre and all genres
monthly_top_genre = top_genre_sales.groupby(top_genre_sales['date'].dt.to_period('M'))['total_amount'].sum()
monthly_all = sales_books.groupby(sales_books['date'].dt.to_period('M'))['total_amount'].sum()

# Create combined chart
plt.figure(figsize=(9, 6))
plt.bar(monthly_all.index.astype(str), monthly_all.values, color='lightgray', label='All Genres')
plt.plot(monthly_top_genre.index.astype(str), monthly_top_genre.values, color='blue', marker='o', label=top_genre)
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.title(f"Monthly Sales: {top_genre} vs All Genres")
plt.legend()
plt.grid(True, axis='y', linestyle='--')
plt.tight_layout()
plt.show()
```

#### **Explanation**
We merge sales and book data, determine the highest-revenue genre, then prepare monthly totals for that genre and all genres. Using a combined plot with bars for all genres and a line for the top genre enables easy comparative trend analysis.

#### **Expected Output**
A **combined chart** with grey bars for total revenue across all genres each month, overlaid with a blue line chart showing the top genre’s monthly revenue, complete with legend and grid.

#### **Key Takeaway**
Layering multiple plot types in one chart enables richer context comparisons in trend analysis.

#### **Alternative Approaches**
- Use twin axes (`ax.twinx()`) for separate scales if values differ greatly.
- Normalize monthly data for percentage contribution per genre.

#### **Common Mistakes**
1. Not aligning month labels between bar and line plots.
2. Forgetting to convert dates to datetime before grouping.
3. Overlapping labels due to missing `tight_layout()` or rotation handling.