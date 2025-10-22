## DAY 14 – Hands-On Exercises: Mini-Project – Complete EDA Dashboard (Static)

### Task 1 (EASY – 5 min)
**Goal:** Create a single static chart showing total sales per genre.

**Instructions:**
1. Load `sales.csv` and `books.csv` into pandas DataFrames.
2. Merge them to get the genre for each sale.
3. Group by `genre` and calculate total sales revenue (`total_amount` sum).
4. Create a bar chart (Plotly static figure) displaying total revenue by genre.

**Skeleton Code:**
```python
import pandas as pd
import plotly.express as px

# Load datasets
sales_df = pd.read_csv('sales.csv')
books_df = pd.read_csv('books.csv')

# Merge to include genre
merged_df = sales_df.merge(books_df, on='book_id')

# Group and aggregate (fill in the aggregation code)
genre_sales = ...

# Create bar chart (fill in Plotly code)
fig = ...
fig.show()
```

**Success Criteria:**
- Bar chart with genres on the x-axis.
- Revenue values on the y-axis.
- Clear, static figure (no interactivity needed).

**Expected Output:**
A bar chart with 5–8 genre categories and corresponding revenue bars; highest revenue genre should be visually distinct.


---

### Task 2 (MEDIUM – 7 min)
**Goal:** Extend by adding ratings analysis to a second subplot.

**Instructions:**
1. Load and merge `reviews.csv` with `books.csv` to associate genres.
2. Group by `genre` and compute average rating.
3. Create two subplots using Plotly:
   - Left: Revenue by genre (from Task 1).
   - Right: Average rating by genre.

**Hints:**
- Use `plotly.subplots.make_subplots` for multi-panel layout.
- Use `.add_trace()` to insert each chart into the subplot.

**Skeleton Code:**
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Compute average rating per genre
reviews_df = pd.read_csv('reviews.csv')
reviews_merged = ...
avg_rating = ...

# Prepare subplot layout: 1 row, 2 columns
fig = make_subplots(rows=1, cols=2, subplot_titles=['Revenue by Genre', 'Average Rating by Genre'])

# Add Bar traces for revenue and ratings (fill in)
fig.add_trace(
    go.Bar(...),
    row=1, col=1
)
fig.add_trace(
    go.Bar(...),
    row=1, col=2
)

fig.update_layout(title_text='Sales & Ratings Overview', showlegend=False)
fig.show()
```

**Expected Output:**
A side-by-side static dashboard: left panel showing revenue per genre, right panel showing average rating per genre, aligned for easy comparison.


---

### Task 3 (MEDIUM-HARD – 10 min)
**Goal:** Build a static 3-panel dashboard combining sales trends, top authors, and ratings distribution.

**Instructions:**
1. Sales Trends:  
   - Group `sales.csv` by month (`date` column) and calculate total revenue.
   - Create a line chart showing revenue trend over time.
2. Top Authors:  
   - Merge `sales.csv` with `books.csv` and `authors.csv`.
   - Aggregate total revenue per author and select top 5.
   - Create a horizontal bar chart.
3. Ratings Distribution:  
   - Histogram of all ratings from `reviews.csv`.

4. Arrange all three charts in a single static dashboard (1 row, 3 columns) using subplot titles.

**Skeleton Code:**
```python
# 1. Sales trends
sales_df['month'] = pd.to_datetime(sales_df['date']).dt.to_period('M').astype(str)
monthly_revenue = ...

# 2. Top authors
authors_df = pd.read_csv('authors.csv')
merged_authors = ...
top_authors = ...

# 3. Ratings distribution
ratings_dist = ...

# Create 3-panel subplot
fig = make_subplots(rows=1, cols=3, subplot_titles=['Monthly Revenue', 'Top Authors by Revenue', 'Ratings Distribution'])

# Add line chart for monthly revenue
fig.add_trace(go.Scatter(...), row=1, col=1)

# Add horizontal bar chart for top authors
fig.add_trace(go.Bar(...), row=1, col=2)

# Add histogram for ratings
fig.add_trace(go.Histogram(...), row=1, col=3)

fig.update_layout(title_text='Complete EDA Dashboard – Page Turner Analytics', showlegend=False)
fig.show()
```

**Expected Output:**
A single dashboard with:
- Left panel: upward/downward monthly revenue trends line chart.
- Middle panel: top 5 authors ranked by revenue.
- Right panel: ratings histogram showing distribution peaks.
All panels clearly labeled and aligned, ready for static reporting.