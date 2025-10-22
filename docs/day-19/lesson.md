```markdown
# Day 19: Integrating Pandas with Dash – Live Filtering

## Introduction
Imagine Page Turner Analytics wants a dashboard that lets managers select a specific day of the week and instantly see **filtered book sales, top genres, and total revenue**, all updating live. In previous lessons, we worked with sliders, inputs, and callbacks to control charts interactively. Today, we’ll take it up a notch: you’ll learn to connect **Pandas DataFrame filtering and aggregation** directly inside **Dash callbacks**, and drive **multiple charts** at once from a single user selection.

---

## Core Content

### 1. Pandas in Callbacks
Dash apps run Python callbacks whenever a user interacts with UI components. Inside these callbacks, we can filter DataFrames using user inputs. Think of a DataFrame as our “digital bookstore ledger.” Filtering lets us pull out just the rows that matter—like all sales on Mondays.

In Pandas, filtering is done with boolean masks:
```python
filtered_df = df[df['column_name'] == value]
```
In practice, this means if a manager selects `'Mon'` from a dropdown, we’re instantly slicing our **sales.csv** DataFrame to only Monday transactions.

---

### 2. Dynamic Aggregation
Filtering is half the story; aggregation is where insights appear. Aggregation means **grouping data and summarizing it**—for example, “total sales per genre.” Once filtered to Mondays, you can use `.groupby()` and `.sum()` to produce condensed results. Imagine going from thousands of rows to a clear summary: *Fiction – $1,200, Non-Fiction – $900, Mystery – $450*.

Dynamic aggregation inside callbacks ensures that your charts always reflect **current selections**, without precomputing every scenario.

---

### 3. Updating Multiple Charts
Callbacks can return multiple outputs. A single dropdown selection can drive:
- A revenue trend line for the day
- A bar chart of genres sold
- A numeric KPI card showing total transactions

This is efficient because you apply your Pandas filtering once, then reuse the result to feed multiple charts. It’s like scanning the sales ledger once and producing **several reports simultaneously**.

---

## Code Examples

### Example 1: Filtering Sales by Day of Week
```python
import pandas as pd
import dash
from dash import dcc, html, Input, Output

# Load datasets
sales = pd.read_csv('sales.csv', parse_dates=['date'])
books = pd.read_csv('books.csv')

# Add day of week column
sales['day_of_week'] = sales['date'].dt.strftime('%a')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3("Sales Dashboard – Filter by Day"),
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': day, 'value': day} for day in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']],
        value='Mon'
    ),
    html.Div(id='total-sales-output')
])

@app.callback(
    Output('total-sales-output', 'children'),
    Input('day-dropdown', 'value')
)
def update_sales(selected_day):
    # Filter DataFrame
    filtered_sales = sales[sales['day_of_week'] == selected_day]
    total_amount = filtered_sales['total_amount'].sum()
    return f"Total sales on {selected_day}: ${total_amount:,.2f}"

if __name__ == '__main__':
    app.run_server(debug=True)
```
**Expected Output:** Selecting “Tue” will update the text to show total Tuesday sales.

---

### Example 2: Multi-Output Aggregation
```python
import plotly.express as px

app.layout = html.Div([
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': day, 'value': day} for day in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']],
        value='Mon'
    ),
    dcc.Graph(id='genre-bar'),
    dcc.Graph(id='revenue-trend')
])

@app.callback(
    [Output('genre-bar', 'figure'),
     Output('revenue-trend', 'figure')],
    Input('day-dropdown', 'value')
)
def update_charts(selected_day):
    filtered_sales = sales[sales['day_of_week'] == selected_day]
    merged = filtered_sales.merge(books, on='book_id')
    
    # Genre aggregation
    genre_totals = merged.groupby('genre')['total_amount'].sum().reset_index()
    genre_fig = px.bar(genre_totals, x='genre', y='total_amount', title=f"Sales by Genre on {selected_day}")

    # Revenue trend (hourly or as per dataset granularity)
    revenue_trend = filtered_sales.groupby(filtered_sales['date'].dt.hour)['total_amount'].sum().reset_index()
    trend_fig = px.line(revenue_trend, x='date', y='total_amount', title=f"Revenue Trend on {selected_day}")

    return genre_fig, trend_fig
```
**Expected:** Both charts update when the day changes—bar chart shows genres, line chart shows sales trend.

---

## Common Pitfalls
1. **Filtering Before Parsing Dates**
   - If you don’t parse `sales['date']` as a datetime, extracting days of week will fail.
   - **Fix:** Use `parse_dates=['date']` in `read_csv` or `pd.to_datetime()`.

2. **Multiple Filters**
   - Beginners often re-read the CSV for every filter, slowing down the app.
   - **Fix:** Load once, filter in memory inside callbacks.

3. **Mismatched Keys in Merge**
   - Always ensure columns used in `.merge()` match in dtype and naming.

---

## Practice Checkpoint
✅ I can filter a Pandas DataFrame inside a Dash callback based on dropdown input.  
✅ I can perform live aggregations (`groupby` + `sum`) after filtering.  
✅ I can update multiple charts from one filtered DataFrame without reloading data.

---
```