```markdown
## Task 1 – Interactive Scatter Plot (EASY, ~5 min)

**Goal:** Create an interactive scatter plot showing **book price vs total sales quantity** using `plotly.express`.  

**Instructions:**
1. Load `books.csv` and `sales.csv`.
2. Aggregate total sales quantity per book.
3. Create a scatter plot:
   - x-axis: `price`
   - y-axis: total quantity sold
   - Hover data: `title`, `genre`
4. Make sure hovering over a point shows the title and genre.

**Skeleton Code:**
```python
import pandas as pd
import plotly.express as px

# Load datasets
books = pd.read_csv('books.csv')
sales = pd.read_csv('sales.csv')

# Aggregate total quantity per book
sales_agg = sales.groupby('book_id')['quantity'].sum().reset_index()

# Merge with books data
df = pd.merge(books, sales_agg, on='book_id')

# Create interactive scatter plot
fig = px.scatter(
    df,
    x=...,  # book price
    y=...,  # total quantity sold
    hover_data=[...]  # title, genre
)

fig.show()
```

**Success Criteria:**
- Plot renders without errors.
- Hovering shows title and genre.
- Axes correctly display price vs quantity.

**Expected Output:**  
An interactive scatter plot where each point is a book, plotted by its price vs total sales quantity, with tooltips showing title + genre when hovering.

---

## Task 2 – Hover-enabled Bar Chart (MEDIUM, ~7 min)

**Goal:** Display **top 10 genres by total revenue** as a bar chart with hover tooltips showing average book price per genre.

**Instructions:**
1. Use `books.csv` and `sales.csv`.
2. Calculate total revenue per genre.
3. Also calculate average price per genre.
4. Sort genres by total revenue (top 10).
5. Create bar chart:
   - x-axis: genre
   - y-axis: total revenue
   - Hover data: average price

**Skeleton Code:**
```python
# Group by genre for total revenue
merged = pd.merge(sales, books, on='book_id')
genre_stats = merged.groupby('genre').agg({
    'total_amount': 'sum',
    'price': 'mean'
}).reset_index()

# Sort by total revenue
top_genres = genre_stats.sort_values(by=..., ascending=False).head(10)

# Create bar chart
fig = px.bar(
    top_genres,
    x='genre',
    y=...,  # total revenue
    hover_data=[...]  # average price
)

fig.show()
```

**Expected Output:**  
Interactive bar chart showing the top 10 genres by revenue. Hovering over a bar shows the average book price for that genre.

---

## Task 3 – Interactive Time Series with Genre Filter (MEDIUM-HARD, ~10 min)

**Goal:** Plot monthly total revenue as a time series with an interactive dropdown to filter by genre.

**Instructions:**
1. Use `sales.csv` and `books.csv`.
2. Merge datasets to include genre for each sale.
3. Convert sale dates to a monthly period.
4. Group by month and genre for total revenue.
5. Create a line plot:
   - x-axis: month
   - y-axis: total revenue
   - Color by genre
   - Include a dropdown menu to select genres dynamically.

**Skeleton Code:**
```python
# Merge sales and books
merged = pd.merge(sales, books, on='book_id')

# Convert date to datetime and extract month
merged['date'] = pd.to_datetime(merged['date'])
merged['month'] = merged['date'].dt.to_period('M').dt.to_timestamp()

# Group by month + genre
monthly_genre_rev = merged.groupby(['month', 'genre'])['total_amount'].sum().reset_index()

# Create line plot with genre filter
fig = px.line(
    monthly_genre_rev,
    x='month',
    y='total_amount',
    color='genre'
    # Later: add dropdown for genre filter
)

# TODO: Add dropdown menu using fig.update_layout to filter traces

fig.show()
```

**Expected Output:**  
An interactive time series chart showing revenue trends over months for all genres, with the ability to filter to a single genre using a dropdown menu.
```