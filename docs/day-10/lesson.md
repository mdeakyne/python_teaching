```markdown
# Day 10: Plotly Express – Interactive Basics  
**Week:** 2  
**Difficulty:** Intermediate  
**Duration:** 3-5 minutes  

---

## 1. Introduction

Imagine you’re working for **Page Turner Analytics** and your job today is to help the sales team quickly explore which book genres generate the most revenue, how prices relate to sales volume, and spot seasonal trends.  
Up until now, we’ve used **Matplotlib** and **Seaborn** to make static charts. Those are great for reports, but what if your stakeholders want to hover over a bar to see *exactly* which book it represents, or zoom in on a specific time frame? Today, we’ll step into **Plotly Express** — a tool for creating interactive charts with minimal code. You’ll learn to make scatter plots, hover-enabled bar charts, and time series visualizations that let you *explore* rather than just *look*.

---

## 2. Core Content

### 2.1 What is Plotly Express?
**Plotly Express** is a high-level interface to Plotly, designed for quick, concise interactive visualizations. Think of it as “Seaborn for interactivity”: one function call can create a fully interactive chart with zoom, pan, and hover tooltips.  

Why it matters:
- Your charts are *automatically interactive* — no extra code for zoom or tooltips.
- Hover data lets decision-makers identify specific records without cross-referencing tables.
- Perfect for dashboards or exploratory analysis.

---

### 2.2 Interactive Scatter Plots
In bookstore terms, a scatter plot might show **price** on the x-axis and **sales quantity** on the y-axis. This lets you see if cheaper books sell more copies.  
With Plotly Express, one function creates the plot, and you can hover to see *title*, *genre*, and *sales figures* for individual points.

Key features:
- `hover_data` adds fields you want in tooltips
- Automatic zoom/pan
- Switch between linear/log scales interactively

---

### 2.3 Hover-Enabled Bar Charts
Bar charts are common for comparing totals, like total revenue by genre.  
Plotly Express enhances these by showing exact values when hovering, which is invaluable for quick decision-making.  
For example: A static chart might show “Romance” has the tallest bar, but with hover tooltips, you can see it made **$27,845** exactly without pulling up a calculator.

---

### 2.4 Interactive Time Series
Time series plots show trends over months or years, such as daily total sales.  
Plotly Express lets you:
- Hover to see precise date and value
- Zoom into specific time periods
- Save or download charts to embed in presentations

This is especially useful for spotting seasonal sales trends, like increased romance book sales every February, without manually filtering datasets.

---

## 3. Code Examples

### Example 1 – Price vs Sales Quantity Scatter Plot
```python
import pandas as pd
import plotly.express as px

# Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")

# Merge sales and books
sales_books = sales.merge(books, on="book_id")

# Aggregate quantity sold per book
qty_by_book = sales_books.groupby(
    ["book_id", "title", "genre", "price"], as_index=False
).agg({"quantity": "sum"})

# Interactive scatter plot
fig = px.scatter(
    qty_by_book,
    x="price",
    y="quantity",
    hover_data=["title", "genre", "quantity", "price"],
    title="Price vs Quantity Sold"
)
fig.show()
# Expected: A scatter plot with each point representing a book,
# hover shows Title, Genre, Quantity, and Price
```

---

### Example 2 – Revenue by Genre Bar Chart
```python
# Calculate total revenue per genre
sales_books["revenue"] = sales_books["total_amount"]
revenue_by_genre = sales_books.groupby("genre", as_index=False)["revenue"].sum()

fig = px.bar(
    revenue_by_genre,
    x="genre",
    y="revenue",
    hover_data=["revenue"],
    title="Total Revenue by Genre"
)
fig.show()
# Expected: Interactive bar chart, hovering shows exact revenue value
```

---

### Example 3 – Daily Sales Time Series
```python
# Aggregate by date
daily_sales = sales.groupby("date", as_index=False)["total_amount"].sum()

fig = px.line(
    daily_sales,
    x="date",
    y="total_amount",
    title="Daily Total Sales",
    hover_data=["total_amount"]
)
fig.show()
# Expected: Interactive line chart where you can zoom in on specific dates
```

---

## 4. Common Pitfalls

1. **Not converting dates to datetime**  
   - Plotly expects proper datetime objects for time series.  
   - **Fix:** `pd.to_datetime(df['date'])` before plotting.

2. **Large datasets causing slow rendering**  
   - Interactivity can be sluggish with massive data.  
   - **Fix:** Aggregate or sample data before plotting.

3. **Overloading hover tooltips**  
   - Too much hover data can clutter the popup and slow interaction.  
   - **Fix:** Include only relevant fields.

---

## 5. Practice Checkpoint

By the end of this lesson, you should be able to:
- [ ] Create an interactive scatter plot for book price vs sales with meaningful hover tooltips.
- [ ] Build hover-enabled bar charts for aggregated sales data.
- [ ] Generate interactive time series plots to explore seasonal trends.

---
```