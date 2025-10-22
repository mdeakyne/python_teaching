```markdown
## 🧩 Hands-on Exercises – Day 18: Advanced Layouts – Multi-page Dashboard

---

### Task 1 – EASY (5 min): Create a Basic Multi-Tab Structure  
**Goal:** Build a simple Dash app with tabs for "Sales Trends" and "Inventory Reports" using `dcc.Tabs`.  

**Instructions:**  
1. Load datasets `sales.csv` and `books.csv` using pandas.  
2. Create a Dash layout with two tabs (`dcc.Tab`).  
3. In each tab, display a placeholder `html.Div` with a title for that section.  

**Skeleton Code:**
```python
import dash
from dash import dcc, html
import pandas as pd

# Load data
sales_df = pd.read_csv("sales.csv")
books_df = pd.read_csv("books.csv")

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="Sales Trends", children=[
            html.Div("Placeholder for Sales Trends")
        ]),
        dcc.Tab(label="Inventory Reports", children=[
            html.Div("Placeholder for Inventory Reports")
        ])
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

**Success Criteria:**  
- The app runs without errors.  
- Clicking each tab changes the visible content.  

**Expected Output:**  
Two tabs in the browser: "Sales Trends" shows text `"Placeholder for Sales Trends"`, and "Inventory Reports" shows `"Placeholder for Inventory Reports"`.

---

### Task 2 – MEDIUM (7 min): Populate Tabs with Actual Visualizations  
**Goal:** Replace placeholders with basic charts in each tab using `plotly.express`.  

**Instructions:**  
1. For "Sales Trends": Show a line chart of total sales amount over time.  
2. For "Inventory Reports": Show a bar chart of book counts by genre from `books.csv`.  
3. Keep the same tab structure from Task 1.  

**Skeleton Code:**
```python
import plotly.express as px

# Create Sales Trends figure
sales_trend_fig = px.line(
    sales_df.groupby("date")["total_amount"].sum().reset_index(),
    x="date", y="total_amount", title="Total Sales Over Time"
)

# Create Inventory Reports figure
inventory_fig = px.bar(
    books_df.groupby("genre")["book_id"].count().reset_index(),
    x="genre", y="book_id", title="Books per Genre"
)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="Sales Trends", children=[
            dcc.Graph(figure=sales_trend_fig)
        ]),
        dcc.Tab(label="Inventory Reports", children=[
            dcc.Graph(figure=inventory_fig)
        ])
    ])
])
```

**Expected Output:**  
- "Sales Trends" tab: Line chart with date on x-axis and total sales amount on y-axis.  
- "Inventory Reports" tab: Bar chart showing each genre and the number of books in that genre.

---

### Task 3 – MEDIUM-HARD (10 min): Add a Third Page with Shared Components  
**Goal:** Create a multi-page dashboard with navigation, where "Customer Reviews" shares a summary chart with other pages.  

**Instructions:**  
1. Implement URL-based navigation using `dcc.Location` and multiple layouts.  
2. Create three page layouts:
    - **Sales Trends:** Line chart from Task 2.  
    - **Inventory Reports:** Bar chart from Task 2.  
    - **Customer Reviews:** Histogram of review ratings from `reviews.csv`.  
3. Add a shared summary component (e.g., `html.Div` showing total number of books) visible on all pages.  

**Skeleton Code:**
```python
from dash.dependencies import Input, Output

reviews_df = pd.read_csv("reviews.csv")

# Shared summary component
shared_summary = html.Div([
    html.H4(f"Total Books: {books_df['book_id'].nunique()}")
], style={"backgroundColor": "#f0f0f0", "padding": "10px"})

# Page layouts
sales_layout = html.Div([shared_summary,
    dcc.Graph(figure=sales_trend_fig)
])

inventory_layout = html.Div([shared_summary,
    dcc.Graph(figure=inventory_fig)
])

reviews_fig = px.histogram(
    reviews_df, x="rating", nbins=5, title="Distribution of Ratings"
)

reviews_layout = html.Div([shared_summary,
    dcc.Graph(figure=reviews_fig)
])

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="page-content")
])

@app.callback(Output("page-content", "children"),
              Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/sales":
        return sales_layout
    elif pathname == "/inventory":
        return inventory_layout
    elif pathname == "/reviews":
        return reviews_layout
    else:
        return sales_layout  # default

```

**Expected Output:**  
- Navigating to `/sales`, `/inventory`, and `/reviews` shows respective charts.  
- The shared "Total Books" summary appears at the top of all three pages.  
```

Would you like me to also include **bonus challenge prompts** so learners can extend this dashboard with dropdown filters and responsive grids? This could make Task 3 more hands-on.