# Day 21 – Capstone: Full-Featured Book Analytics Dashboard

## Introduction

Imagine Page Turner Analytics has just signed a contract with a nationwide bookstore chain. They need a **full-featured analytics dashboard** to monitor inventory, sales trends, author performance, and customer feedback — and they need it ready by next week. Over the past 20 days, you’ve mastered responsive layouts, integrated `pandas` in callbacks, optimized performance, and deployed apps. Today, you’ll bring it all together into a **production-ready dashboard** that blends the frontend power of Dash with Python’s data manipulation capabilities.

---

## Core Content

### 1. Full-Stack Integration with Dash
By now, you know Dash lets us write **Python for the backend** and **HTML/CSS/JS-like components** for the frontend — all without manually wiring API endpoints or managing JSON communication. The Plotly integration means your book sales graphs are interactive by default, using modern web technologies under the hood. This “hidden complexity” keeps you focused on **storytelling with data**, not boilerplate.

**Bookstore analogy:** Think of Dash as a store manager who handles all the behind-the-scenes deliveries, restocking, and stock checks — you just tell them what to show customers, and they make it happen.

---

### 2. Comprehensive Dashboard Design
A good dashboard brings all relevant datasets together. For Page Turner, that means:
- **Books dataset:** Inventory & metadata
- **Authors dataset:** Background and demographics
- **Sales dataset:** Revenue over time
- **Reviews dataset:** Customer sentiment

You’ll create:
- KPI cards (e.g., total sales, average rating)
- Interactive filters (genre, author, publication year)
- Visualizations (sales trendlines, top authors, genre distribution)
- Review heatmaps (rating over time)

These features allow decision-makers to **slice and dice** data quickly, spotting trends like “romance novels surged in Q2” or “average ratings dipped after a price hike.”

---

### 3. Deployment Best Practices
Dash is built on Flask, which means you have **flexible deployment** options: from Heroku’s managed hosting to self-hosting on-premises. Before pushing live:
- Test with realistic datasets
- Enable caching for heavy queries
- Minimize component count to avoid slow rendering
- Use `app.run_server(debug=False)` in production to prevent debug info exposure

This ensures your dashboard doesn’t just work — it works reliably and securely.

---

## Code Examples

### Example 1: Interactive Sales by Genre
```python
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")

# Merge to connect sales to genres
sales_books = sales.merge(books, on="book_id")

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Sales by Genre"),
    dcc.Dropdown(
        id="genre-dropdown",
        options=[{"label": g, "value": g} for g in books["genre"].unique()],
        value=books["genre"].unique()[0]
    ),
    dcc.Graph(id="genre-sales-graph")
])

@app.callback(
    Output("genre-sales-graph", "figure"),
    Input("genre-dropdown", "value")
)
def update_graph(selected_genre):
    filtered = sales_books[sales_books["genre"] == selected_genre]
    genre_trend = filtered.groupby("date")["total_amount"].sum().reset_index()
    fig = px.line(genre_trend, x="date", y="total_amount",
                  title=f"{selected_genre} Sales Over Time")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
```
*Expected Output:* A line chart updating when you select different genres.

---

### Example 2: Author Performance KPI
```python
# Average rating per author
reviews = pd.read_csv("reviews.csv")

books_reviews = books.merge(reviews, on="book_id")
author_ratings = books_reviews.groupby("author_name")["rating"].mean().reset_index()

top_authors = author_ratings.sort_values("rating", ascending=False).head(5)
print(top_authors)
```
*Expected Output:* A table of top 5 authors with their average rating.

---

### Example 3: Cached Heavy Query
```python
from dash.dependencies import Input, Output
from flask_caching import Cache

cache = Cache(app.server, config={'CACHE_TYPE': 'SimpleCache'})

@cache.memoize(timeout=60)  # cache for 1 minute
def compute_genre_summary():
    return sales_books.groupby("genre")["total_amount"].sum().reset_index()

@app.callback(
    Output("genre-summary-graph", "figure"),
    Input("refresh-btn", "n_clicks")
)
def update_summary(n_clicks):
    df_summary = compute_genre_summary()
    return px.bar(df_summary, x="genre", y="total_amount")
```
*Expected Output:* A bar chart of total sales per genre that refreshes when the button is clicked, but avoids repeating heavy computation.

---

## Common Pitfalls

1. **Too Many Components**
   - Adding hundreds of graphs/tables can slow down rendering.
   - **Avoidance:** Use tabs, conditional rendering, or summarize data before display.

2. **Neglecting Data Integrity**
   - Inconsistent joins between datasets cause errors.
   - **Avoidance:** Always verify keys (`book_id`, `author_id`) exist in both datasets.

3. **Skipping Production Settings**
   - Running with `debug=True` in production risks exposing stack traces.
   - **Avoidance:** Switch to `debug=False` before deployment.

---

## Practice Checkpoint

✅ I can integrate multiple datasets into a single Dash application.  
✅ I can build interactive and responsive components for data filtering and visualization.  
✅ I can deploy a Dash app with caching and optimized performance for real-world use.

---