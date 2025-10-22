# Day 18 – Advanced Layouts: Multi-page Dashboard

## Introduction

Imagine you’re building a **Page Turner Analytics** dashboard for a bookstore chain. Until now, we’ve displayed our sales graphs, dropdown filters, and date pickers all on one screen. But what if our manager wants separate tabs for **Sales Trends**, **Inventory Reports**, and **Customer Reviews**—each with its own layout, but sharing some common components like summary charts?  
Today, we’ll move beyond single-page designs and learn how to create **multi-tab, multi-page dashboards** with **responsive layouts** that adapt to mobile or desktop. We’ll build on the callback and layout skills from previous lessons, and you’ll see how navigation between pages can make large apps easier to use.

---

## Core Content

### 1. Multi-page & Tab Layouts

In Dash, large apps often benefit from **logical separation of content**. Like walking through sections of a bookstore—Fiction, Non-fiction, and Children’s Books—you guide your users to the right information without overwhelming them.  

Tabs (`dcc.Tabs`) or multi-page setups let us:
- Keep the interface clean by hiding unrelated controls
- Make interactions faster by updating only the relevant section
- Maintain persistent content across sections (e.g., a sales graph on the right column that doesn’t change when switching tabs)

From the source material: in the **investment portfolio** example, the first column changes per tab, but the second column with graphs stays constant. We’ll replicate that structure for our bookstore data.

---

### 2. Responsive Grid Layouts with `dbc.Row` and `dbc.Col`

A responsive layout adapts to different screen sizes—important when your regional manager views the dashboard on her tablet. Using Dash Bootstrap Components (`dbc.Row` / `dbc.Col`), we can define column widths for different screen sizes:
- `width`: default width for small devices  
- `lg`: width for large screens  

For example:
```python
dbc.Col("Column 1", width=12, lg=5)
dbc.Col("Column 2", width=12, lg=7)
```
This ensures stacked content on mobile (12-width each), but side-by-side columns on desktop.

Setting `fluid=True` in our `dbc.Container` makes it **span the full viewport width**, a key part of responsive design.

---

### 3. Navigation Between Pages

Navigation can be:
- **Tabs**: Switching content panes within the same URL
- **Multi-page routing**: Navigating different URLs within the same app

For our use case, tabs are efficient because we want to switch between related views. Navigation matters for analysis because your users don’t want to scroll endlessly—they want **quick, organized access** to relevant data.

---

## Code Examples

### Example 1 – Basic Multi-tab Dashboard
```python
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

# Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Common summary graph (right column)
summary_graph = dcc.Graph(
    figure={
        "data": [{"x": books['genre'], "y": books['price'], "type": "bar"}],
        "layout": {"title": "Average Price by Genre"}
    }
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Tabs(id="tabs", value="sales", children=[
                dcc.Tab(label="Sales Trends", value="sales"),
                dcc.Tab(label="Inventory Reports", value="inventory"),
                dcc.Tab(label="Customer Reviews", value="reviews")
            ]),
            html.Div(id="tab-content")
        ], width=12, lg=5),
        dbc.Col(summary_graph, width=12, lg=7)
    ])
], fluid=True)

@app.callback(
    dash.Output("tab-content", "children"),
    dash.Input("tabs", "value")
)
def update_tab(tab_name):
    if tab_name == "sales":
        return dcc.Markdown("### Monthly Sales Report\nHere we show sales trends.")
    elif tab_name == "inventory":
        return dcc.Markdown("### Inventory Levels\nReport on current stock.")
    elif tab_name == "reviews":
        return dcc.Markdown("### Customer Ratings\nVisualize reviews.")
    return "Select a tab."

if __name__ == "__main__":
    app.run_server(debug=True)
```
**Expected Output:**  
Tabs on the left, switching text content per tab. Right column shows a static bar chart.

---

### Example 2 – Responsive Design in Action
```python
# Adding more layout components inside a tab
inventory_table = dbc.Table.from_dataframe(
    books[['title', 'genre', 'pages']], striped=True, bordered=True, hover=True
)

@app.callback(
    dash.Output("tab-content", "children"),
    dash.Input("tabs", "value")
)
def update_tab(tab_name):
    if tab_name == "inventory":
        return html.Div([
            html.H4("Top 5 Longest Books"),
            inventory_table
        ])
    # ... other tabs remain the same
```
On mobile devices, columns stack vertically; on desktop, they remain side-by-side.

---

### Example 3 – Page-wide Footer
```python
footer = dbc.Container([
    html.Hr(),
    html.P("Page Turner Analytics © 2024 | Contact: info@pageturner.com")
], fluid=True)

app.layout = html.Div([
    # main container...
    footer
])
```
Consistent footer across all pages/tabs builds a cohesive user experience.

---

## Common Pitfalls

1. **Putting all components in one column** – This defeats the purpose of responsive layouts. Use `dbc.Row` and `dbc.Col` with appropriate `lg` values.
2. **Forgetting persistent elements** – If you want a chart or summary always visible, place it outside tab-specific callbacks.
3. **Not testing on different devices** – A layout may look fine on desktop but break on mobile. Always resize your browser to check alignment.

---

## Practice Checkpoint

You can now:
- [ ] Create a dashboard with multiple tabs that show different data views
- [ ] Build responsive layouts using `dbc.Row` and `dbc.Col`
- [ ] Implement navigation that keeps common components persistent across tabs

---