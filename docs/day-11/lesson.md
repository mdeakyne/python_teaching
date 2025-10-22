# Day 11: Advanced Plotly – Multiple Traces & Subplots  
**Week**: 2  
**Difficulty**: Intermediate  
**Duration**: 3–5 minutes  

---

## Introduction  
Imagine you’re working for **Page Turner Analytics**, and a manager asks:  
*"Can we see sales trends for multiple genres over time—side by side—so we can compare them quickly?"*  

Up until now, you’ve created interactive charts, histograms, and single scatter plots with Plotly Express. But in real-world analysis, executives often need **multiple views at once**—different lines for each genre or several plots in a grid layout that tell a richer story.  

Today, you’ll learn how to:
- Draw multi-line charts using separate traces for each genre
- Build subplot grids to compare different metrics (e.g., sales vs. ratings)
- Customize layouts and themes for clarity

---

## Core Content  

### 1. Plotly Graph Objects: Going Beyond Plotly Express  
Plotly Express is fantastic for quick, simple charts—but when you need **multiple traces** on the same figure or complex subplot layouts, you’ll use `plotly.graph_objects` (often abbreviated as `go`).

Think of Plotly Express as ordering a pre-packaged "combo meal"—fast and easy.  
Graph Objects is like à la carte dining—full control over each dish, its seasoning, and arrangement.

Instead of auto-creating a figure, you’ll explicitly build it, add traces, and tweak layouts step-by-step.

---

### 2. Multiple Traces – Multi-Line Sales Trends  
A "trace" is essentially one dataset's visual representation (like a single genre’s sales trend line). Multiple traces mean multiple genres in the same chart—each trace can have its own styling, color, and legend entry.

**Why it matters**:  
This is like showing the sales history of Mystery, Romance, and Sci-Fi in one chart, so you can instantly detect which genre is growing fastest.

---

### 3. Subplots – Organizing Complex Views  
When one chart isn’t enough, you can create subplot grids using `make_subplots`. Each subplot can display a different metric entirely.  
Example: Top-left shows total sales per genre, top-right shows average rating per genre. Just as a bookstore manager’s dashboard might have a sales panel and a reviews panel side by side.

From our Matplotlib reference (source material, page 41), we know there’s a concept of a **figure** (container) holding multiple **axes** (plots). Plotly follows the same principle—you define the container (`Figure`) and then define multiple "axes areas" with traces assigned to each.

---

### 4. Layout and Theme Customization  
Once you have multiple elements in a figure, layout customization makes sure labels, titles, and colors are clear—not overwhelming.  
Themes help make visual consistency across multiple reports—your "brand identity" for charts.

---

## Code Examples  

### Example 1 – Multi-Line Chart: Sales Quantity Over Time by Genre
```python
import pandas as pd
import plotly.graph_objects as go

# Load datasets
books = pd.read_csv('books.csv')
sales = pd.read_csv('sales.csv')

# Merge to get genres with sales data
sales_with_genre = sales.merge(books, on='book_id')

# Group data by date and genre
genre_sales_trends = sales_with_genre.groupby(['date', 'genre'])['quantity'].sum().reset_index()

# Create figure
fig = go.Figure()

# Add a trace for each genre
for genre in genre_sales_trends['genre'].unique():
    genre_data = genre_sales_trends[genre_sales_trends['genre'] == genre]
    fig.add_trace(go.Scatter(
        x=genre_data['date'], 
        y=genre_data['quantity'],
        mode='lines',
        name=genre  # Legend label
    ))

fig.update_layout(
    title="Sales Trends by Genre",
    xaxis_title="Date",
    yaxis_title="Quantity Sold",
    template="plotly_dark"  # Dark theme for clarity
)

fig.show()

# Expected: Interactive multi-line chart showing separate lines for each genre over time.
```

---

### Example 2 – Two Subplots: Sales Trends & Average Ratings
```python
from plotly.subplots import make_subplots

reviews = pd.read_csv('reviews.csv')

# Compute trends
genre_sales_avg = genre_sales_trends.groupby('genre')['quantity'].mean().reset_index()
genre_ratings_avg = reviews.merge(books, on='book_id').groupby('genre')['rating'].mean().reset_index()

# Create subplot grid: 1 row, 2 columns
fig = make_subplots(rows=1, cols=2, subplot_titles=("Average Sales per Genre", "Average Ratings per Genre"))

# Left plot: Bar Chart for Sales
fig.add_trace(
    go.Bar(x=genre_sales_avg['genre'], y=genre_sales_avg['quantity'], name="Avg Sales"),
    row=1, col=1
)

# Right plot: Bar Chart for Ratings
fig.add_trace(
    go.Bar(x=genre_ratings_avg['genre'], y=genre_ratings_avg['rating'], name="Avg Rating", marker_color='orange'),
    row=1, col=2
)

fig.update_layout(title="Genre Performance Overview", template="ggplot2")
fig.show()

# Expected: Two side-by-side bar charts with clear subplot titles.
```

---

### Example 3 – Mixed Chart Types in Subplots
```python
# Using subplots: line chart + bar chart
fig = make_subplots(rows=2, cols=1, subplot_titles=("Sci-Fi Sales Trend", "Top-Mystery Authors"))

# Sci-Fi trend
sci_fi_data = genre_sales_trends[genre_sales_trends['genre'] == 'Sci-Fi']
fig.add_trace(go.Scatter(
    x=sci_fi_data['date'],
    y=sci_fi_data['quantity'],
    mode='lines',
    name='Sci-Fi'
), row=1, col=1)

# Mystery authors: bar chart of total pages published
mystery_authors = books[books['genre'] == 'Mystery'].groupby('author_name')['pages'].sum().reset_index()
fig.add_trace(go.Bar(
    x=mystery_authors['author_name'],
    y=mystery_authors['pages'],
    name='Pages Published'
), row=2, col=1)

fig.update_layout(height=600, title="Sci-Fi vs Mystery Insights", template="plotly_white")
fig.show()
```

---

## Common Pitfalls  

1. **Forgetting to specify subplot positions**  
   - When adding traces in `make_subplots`, always set `row` and `col`—otherwise, Plotly may place your data incorrectly.  

2. **Mismatched Data Types in Dates**  
   - Ensure date columns are parsed as `datetime` objects before plotting; otherwise, lines may display incorrectly or sort as strings.  

3. **Overcrowded Legends**  
   - Limit the number of genres or traces in one chart. Too many lines make interpretation harder—consider filtering for top genres.

---

## Practice Checkpoint  

By the end of today, you should be able to:  

- [ ] Create a chart with **multiple traces** showing trends for different genres.  
- [ ] Build **subplot grids** combining different chart types and metrics.  
- [ ] Customize layouts and themes for clarity and brand consistency.  