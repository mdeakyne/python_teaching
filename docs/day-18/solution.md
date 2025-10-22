```markdown
## Day 18: Advanced Layouts – Multi-page Dashboard  

---

### Task 1 – EASY: Create a Basic Multi-Tab Structure  

#### 1. Complete Working Code
```python
import dash
from dash import dcc, html
import pandas as pd

# Load datasets
sales_df = pd.read_csv("sales.csv")
books_df = pd.read_csv("books.csv")

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with basic two tabs and placeholder text
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="Sales Trends", children=[
            html.Div("Placeholder for Sales Trends", style={"padding": "20px"})
        ]),
        dcc.Tab(label="Inventory Reports", children=[
            html.Div("Placeholder for Inventory Reports", style={"padding": "20px"})
        ])
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

#### 2. Explanation
We load the CSVs into Pandas DataFrames but only display placeholders for now. Using `dcc.Tabs` and `dcc.Tab`, we create two sections for later chart insertion. Clicking on each tab changes visible content without page reload.

#### 3. Expected Output
A webpage with two tabs:  
- "Sales Trends" → `"Placeholder for Sales Trends"`  
- "Inventory Reports" → `"Placeholder for Inventory Reports"`

#### 4. Key Takeaway
`dcc.Tabs` provides an easy way to organize multiple sections in a single-page Dash app.

**Alternative Approaches:**  
- Use `dcc.RadioItems` and dynamic callbacks to swap content.  
- Use separate routes (`dcc.Location`) for more control.

**Common Mistakes:**  
- Not importing `dash` submodules correctly (`dcc`, `html`).  
- Forgetting to wrap tabs inside a container like `html.Div`.  
- Mismatched dataset paths.

---

### Task 2 – MEDIUM: Populate Tabs with Actual Visualizations  

#### 1. Complete Working Code
```python
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load datasets
sales_df = pd.read_csv("sales.csv", parse_dates=["date"])
books_df = pd.read_csv("books.csv")

# Sales Trends Figure
sales_trend_data = (
    sales_df.groupby("date")["total_amount"]
    .sum()
    .reset_index()
    .sort_values("date")
)
sales_trend_fig = px.line(
    sales_trend_data,
    x="date",
    y="total_amount",
    title="Total Sales Over Time"
)

# Inventory Reports Figure
inventory_data = (
    books_df.groupby("genre")["book_id"]
    .count()
    .reset_index()
    .rename(columns={"book_id": "book_count"})
)
inventory_fig = px.bar(
    inventory_data,
    x="genre",
    y="book_count",
    title="Books per Genre"
)

# Initialize app
app = dash.Dash(__name__)

# Layout
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

if __name__ == "__main__":
    app.run_server(debug=True)
```

#### 2. Explanation
We process the datasets to get aggregated values for charts. The line chart visualizes sales totals over time, and the bar chart shows how many books per genre exist. We replace text placeholders with real Plotly Express visualizations.

#### 3. Expected Output
- **Sales Trends**: Line chart with date vs. sales total.  
- **Inventory Reports**: Bar chart showing genres vs. book counts.

#### 4. Key Takeaway
Pre-processing data before plotting ensures charts correctly reflect aggregated metrics.

**Alternative Approaches:**  
- Use `plotly.graph_objects` for more styling control.  
- Add hover templates for richer tooltips.

**Common Mistakes:**  
- Not parsing dates with `parse_dates` in `read_csv`.  
- Forgetting to `reset_index()` after groupby.  
- Using raw data without sorting, causing jagged lines.

---

### Task 3 – MEDIUM-HARD: URL-based Multi-page Dashboard with Shared Components  

#### 1. Complete Working Code
```python
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load datasets
sales_df = pd.read_csv("sales.csv", parse_dates=["date"])
books_df = pd.read_csv("books.csv")
reviews_df = pd.read_csv("reviews.csv")

# Prepare figures
sales_trend_data = (
    sales_df.groupby("date")["total_amount"]
    .sum()
    .reset_index()
    .sort_values("date")
)
sales_trend_fig = px.line(
    sales_trend_data,
    x="date",
    y="total_amount",
    title="Total Sales Over Time"
)

inventory_data = (
    books_df.groupby("genre")["book_id"]
    .count()
    .reset_index()
    .rename(columns={"book_id": "book_count"})
)
inventory_fig = px.bar(
    inventory_data,
    x="genre",
    y="book_count",
    title="Books per Genre"
)

reviews_fig = px.histogram(
    reviews_df,
    x="rating",
    nbins=5,
    title="Distribution of Ratings"
)

# Shared summary component
shared_summary = html.Div(
    [
        html.H4(f"Total Books: {books_df['book_id'].nunique()}")
    ],
    style={"backgroundColor": "#f0f0f0", "padding": "10px", "marginBottom": "20px"}
)

# Page layouts
sales_layout = html.Div([
    shared_summary,
    dcc.Graph(figure=sales_trend_fig)
])

inventory_layout = html.Div([
    shared_summary,
    dcc.Graph(figure=inventory_fig)
])

reviews_layout = html.Div([
    shared_summary,
    dcc.Graph(figure=reviews_fig)
])

# Initialize app
app = dash.Dash(__name__)
server = app.server

# App layout with router
app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div([
        dcc.Link("Sales Trends", href="/sales", style={"marginRight": "15px"}),
        dcc.Link("Inventory Reports", href="/inventory", style={"marginRight": "15px"}),
        dcc.Link("Customer Reviews", href="/reviews")
    ], style={"padding": "10px", "backgroundColor": "#e0e0e0"}),
    html.Hr(),
    html.Div(id="page-content")
])

# Callback to handle routing
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/sales":
        return sales_layout
    elif pathname == "/inventory":
        return inventory_layout
    elif pathname == "/reviews":
        return reviews_layout
    else:
        # Default route
        return sales_layout

if __name__ == "__main__":
    app.run_server(debug=True)
```

#### 2. Explanation
We create three separate layouts for three pages and use `dcc.Location` plus a callback to control which layout appears based on the URL path. A shared summary component appears at the top of all pages, maintaining consistency and giving key context everywhere.

#### 3. Expected Output
- `/sales`: Sales Trends line chart with “Total Books” summary.  
- `/inventory`: Inventory bar chart with “Total Books” summary.  
- `/reviews`: Ratings histogram with “Total Books” summary.  
Navigation links let users move between pages without reloading the app.

#### 4. Key Takeaway
URL-based navigation allows a Dash app to scale to multiple pages with unique content while sharing global components.

**Alternative Approaches:**  
- Use `dash_pages` plugin (in newer versions) for automatic page registration.  
- Tab navigation for smaller multi-section apps instead of URL routing.

**Common Mistakes:**  
- Forgetting to include `dcc.Location` to capture URL changes.  
- Mismatched paths in `dcc.Link` and routing callback causing blank output.  
- Not defining a default layout for unexpected paths.
```
