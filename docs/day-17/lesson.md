```markdown
# Day 17: Callbacks – Making It Interactive
**Week:** 3  
**Difficulty:** Intermediate  
**Duration:** 3-5 minutes  

---

## 1. Introduction

At Page Turner Analytics, the team wants a dashboard where selecting a genre instantly updates daily sales charts and top-rated books for that genre. Last week, you built layouts and learned how to place dropdowns, sliders, and charts on the page. Today, we’ll connect those components so that when a user interacts with the inputs, the charts update automatically. This is where **callbacks** come in—turning a static dashboard into a live, interactive tool.

By the end of today’s lesson, you’ll know how to:
- Write callback functions that take input values and update chart data.
- Connect multiple inputs to multiple outputs.
- Chain callbacks to keep multiple parts of the dashboard in sync.

---

## 2. Core Content

### A. What Are Callbacks?
In Dash, a **callback** is a Python function that responds to user input. Think of it like a conversation between your users and your data—every time a dropdown, slider, or date picker changes, the callback says:  
*"Got it, let me prepare the updated chart for you."*

For example, if a store manager selects “Mystery” from a genre dropdown, the callback will filter your sales dataset for mystery books and redraw the sales trend chart.

**Why it matters:** Without callbacks, your dashboard is "print-only"—users can see data but not explore it. Callbacks make dashboards _explorable_, essential for finding insights fast.

---

### B. Inputs, Outputs, and State
Dash callbacks are declared with the `@app.callback` decorator, specifying:
- **Output**: Where changes appear (e.g., a chart’s `figure` property).
- **Input**: What triggers recalculation (e.g., a dropdown’s selected value).
- **State**: Values that are read but do not trigger recalculation.

Imagine a bookstore window (Output). Customers point at genres (Input) and sometimes at a date range as well (State) to see a specific sales snapshot.

---

### C. Multiple Inputs, Multiple Outputs
Real dashboards often require:
- Filtering charts **and** updating a summary table simultaneously.
- Having a single interaction change multiple components.

For instance, the marketing team might want both a sales chart and a “Top 5 Author” table to update when choosing a genre and date range.

Callback chaining can also make one callback’s output feed into another callback’s input.  
In the bookstore analogy: selecting a genre filters a list of available authors, and selecting an author updates the chart.

---

## 3. Code Examples

### Example 1: Simple Input → Output Callback
```python
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load datasets
books = pd.read_csv('books.csv')
sales = pd.read_csv('sales.csv')

# Merge sales with book info
sales_books = sales.merge(books, on='book_id')

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': g, 'value': g} for g in books['genre'].unique()],
        value='Mystery'
    ),
    dcc.Graph(id='sales-chart')
])

# Callback: change genre → update chart
@app.callback(
    Output('sales-chart', 'figure'),
    Input('genre-dropdown', 'value')
)
def update_chart(selected_genre):
    filtered = sales_books[sales_books['genre'] == selected_genre]
    fig = px.line(
        filtered.groupby('date')['quantity'].sum().reset_index(),
        x='date', y='quantity', title=f"{selected_genre} Sales Over Time"
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
```
**Expected behavior:** Selecting a genre updates the line chart to show quantities sold over time for that genre.

---

### Example 2: Multiple Inputs → Multiple Outputs
```python
app.layout = html.Div([
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': g, 'value': g} for g in books['genre'].unique()],
        value='Mystery'
    ),
    dcc.DatePickerRange(
        id='date-range',
        start_date=sales['date'].min(),
        end_date=sales['date'].max()
    ),
    dcc.Graph(id='sales-chart'),
    html.Div(id='summary-text')
])

@app.callback(
    [Output('sales-chart', 'figure'),
     Output('summary-text', 'children')],
    [Input('genre-dropdown', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_dashboard(selected_genre, start_date, end_date):
    mask = (
        (sales_books['genre'] == selected_genre) &
        (sales_books['date'] >= start_date) &
        (sales_books['date'] <= end_date)
    )
    filtered = sales_books[mask]
    fig = px.line(filtered.groupby('date')['quantity'].sum().reset_index(),
                  x='date', y='quantity',
                  title=f"{selected_genre} Sales Over Time")
    summary = f"Total units sold: {filtered['quantity'].sum()}"
    return fig, summary
```
**Expected behavior:** Both chart and summary text update when either the genre or date range is changed.

---

### Example 3: Using State
```python
from dash import State

app.layout = html.Div([
    dcc.Input(id='customer-id', type='number', value=1),
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': g, 'value': g} for g in books['genre'].unique()],
        value='Mystery'
    ),
    html.Button('Show Purchases', id='show-btn'),
    html.Div(id='output-text')
])

@app.callback(
    Output('output-text', 'children'),
    Input('show-btn', 'n_clicks'),
    State('customer-id', 'value'),
    State('genre-dropdown', 'value')
)
def show_customer_purchases(n_clicks, cust_id, genre):
    if not n_clicks:
        return ""
    cust_sales = sales_books[(sales_books['customer_id'] == cust_id) &
                             (sales_books['genre'] == genre)]
    return f"Customer {cust_id} bought {cust_sales['quantity'].sum()} {genre} books."
```
**Expected behavior:** Only when clicking the button does the output update, using both customer ID and genre from State.

---

## 4. Common Pitfalls

1. **Not Matching IDs Correctly**  
   If your `Output` or `Input` IDs do not match the component IDs in your layout, the callback won’t run.  
   *Solution:* Double-check HTML/Dash component IDs.

2. **Forgetting to Filter Data Types**  
   Passing strings instead of numbers (or vice versa) can break filters.  
   *Solution:* Validate and type-check inputs in the callback function.

3. **Too Large Dataframes in Callbacks**  
   Filtering huge datasets directly in callbacks can slow down the app.  
   *Solution:* Pre-aggregate data where possible before callback processing.

---

## 5. Practice Checkpoint

By the end of this section, you should be able to:

- [ ] Build a callback that updates a chart in response to a dropdown selection.  
- [ ] Connect two inputs to two different outputs in one callback.  
- [ ] Use State to read values without triggering updates until a button click.
```
