```markdown
# Day 15: Dash Fundamentals – First App  
**Week 3 | Difficulty: Beginner | Duration: 3–5 minutes**

---

## Introduction  
Imagine you’re working at **Page Turner Analytics**, and you’ve just finished a set of beautiful static charts in Matplotlib and Seaborn for last quarter’s book sales and reviews. Your manager loves them—but now wants these visualizations **accessible online**, with an easy-to-navigate interface that can eventually support interactive filtering. This week we’ll bridge the gap: you’ll learn to put those insights into a simple web app using **Dash**. Building on your understanding of themes, layouts, and multi-chart reporting, today’s lesson introduces the structure of a Dash application, creating a basic layout with HTML components, and embedding static charts for a web audience.

---

## Core Content

### 1. What is a Dash App?
Dash is a Python framework for building data-driven web applications—think of it as a lightweight “web page generator” where your charts, tables, and metrics can live together. Instead of emailing PDFs or sharing Excel files, you create an interactive dashboard accessible from a browser.  
In bookstore terms: if Matplotlib is the art of drawing your charts, Dash is like setting up the **bookstore window display**, arranging your visuals so people can see them while walking by.

Key points:
- A Dash app runs locally or on a server
- You build its **layout** using Python structures that resemble HTML
- Components are reactive—later we can make them respond to user input

---

### 2. Layout and HTML Components
At the heart of a Dash app is its `layout`. You define this using Dash's `html` module (for text, headings, divs) and the `dcc` module (Dash Core Components for charts, dropdowns, sliders, etc.).  
Imagine grouping books into genre shelves (`html.Div`), putting signboards (`html.H1`) above them, and displaying featured book covers (`dcc.Graph` with plots) — each shelf is a **component**, arranged in a **layout tree**.

Common components:
- `html.H1("Title")` — Heading
- `html.Div([...], style=...)` — Container for other elements
- `dcc.Graph(figure=...)` — Place your chart inside the app

---

### 3. Displaying Static Charts
You already know how to create Matplotlib or Plotly charts offline. Dash makes displaying them simple—pass the **figure object** to `dcc.Graph`. This is perfect for first steps: showing last month’s book sales trend or top-rated authors right in the browser.  
Static charts give stakeholders immediate, visual answers without writing code or opening a Jupyter notebook.

---

## Code Examples  

### Example 1 — Basic Dash App Layout
```python
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Load sales data
sales_df = pd.read_csv("sales.csv")
books_df = pd.read_csv("books.csv")

# Merge to get book titles with sales
merged_df = sales_df.merge(books_df, on="book_id")
sales_by_book = merged_df.groupby("title")["quantity"].sum().reset_index()

# Create a static bar chart figure
fig = px.bar(sales_by_book, x="title", y="quantity",
             title="Total Sales by Book",
             labels={"quantity": "Units Sold", "title": "Book Title"})

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(children=[
    html.H1("Page Turner Analytics Dashboard"),
    html.P("A quick look at total sales for each book."),
    dcc.Graph(figure=fig)  # Embedding static chart
])

if __name__ == '__main__':
    app.run_server(debug=True)
```
**Expected output:**  
A browser view at `http://127.0.0.1:8050/` displaying:
- A header “Page Turner Analytics Dashboard”
- A subheading description
- A bar chart of book sales

---

### Example 2 — Adding Multiple Components
```python
# Adding a second chart for top genres by sales

genre_sales = merged_df.groupby("genre")["quantity"].sum().reset_index()
fig_genre = px.pie(genre_sales, names="genre", values="quantity",
                   title="Sales Distribution by Genre")

app.layout = html.Div(children=[
    html.H1("Page Turner Analytics Dashboard"),
    html.Div([
        html.H2("Sales by Book"),
        dcc.Graph(figure=fig),
    ], style={"margin-bottom": "50px"}),  # spacing between sections
    html.Div([
        html.H2("Sales by Genre"),
        dcc.Graph(figure=fig_genre),
    ])
])
```
**Expected output:**  
Two sections in the browser—first a bar chart showing units sold per book, then a genre pie chart.

---

### Example 3 — Styling for Readability
```python
app.layout = html.Div(style={"font-family": "Arial", "margin": "40px"}, children=[
    html.H1("Page Turner Analytics Dashboard", style={"color": "#2c3e50"}),
    html.P("Presenting static visuals for last quarter's performance."),
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig_genre)
])
```
**Expected output:**  
Clean, styled typography and spacing to make the dashboard pleasant and readable.

---

## Common Pitfalls
1. **Forgetting to run the server**  
   Beginners often write the layout but forget `app.run_server()`. Remember: Dash apps need a running server to show in a browser.

2. **Not importing the right modules**  
   Mixing `html` and `dcc` components without proper imports (`from dash import html, dcc`) leads to errors.

3. **Passing data instead of figures to `dcc.Graph`**  
   Always pass a prepared `figure` object—raw data won't render.

---

## Practice Checkpoint
By the end of this lesson, you should be able to:
- [ ] Set up and run a basic Dash app locally.
- [ ] Create a simple layout with headings, text, and charts.
- [ ] Embed a static chart into a Dash app using `dcc.Graph`.

---
```