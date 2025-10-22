```markdown
## 🛠 Exercises – Day 19: Integrating Pandas with Dash – Live Filtering

### Task 1 – Filter Sales by Selected Day of the Week (Easy – ~5 min)

**Goal:** Create a Dash dropdown to select a **day of the week** and filter sales accordingly using Pandas.

**Instructions:**
1. Load `sales.csv` into a Pandas DataFrame.
2. Add a new column `day_name` using `pd.to_datetime()` on the `date` column.
3. Create a Dash dropdown (`dcc.Dropdown`) with options for all 7 days.
4. Use a callback that:
   - Takes the selected day as input.
   - Filters the DataFrame by this day.
   - Returns the number of sales records for that day.

**Skeleton Code:**
```python
import dash
from dash import dcc, html, Input, Output
import pandas as pd

# Load data
sales_df = pd.read_csv('sales.csv')
sales_df['day_name'] = pd.to_datetime(sales_df['date']).dt.day_name()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': d, 'value': d} for d in sales_df['day_name'].unique()],
        value='Monday'
    ),
    html.Div(id='sales-count-output')
])

@app.callback(
    Output('sales-count-output', 'children'),
    Input('day-dropdown', 'value')
)
def update_sales_count(selected_day):
    # TODO: Filter sales_df by selected_day and return count
    return f"Records: {0}"

if __name__ == '__main__':
    app.run_server(debug=True)
```

**Success Criteria:**
- Selecting a day updates the displayed count of records.

**Expected Output:**
- Dropdown shows days of the week.
- Text displays: `Records: X` where X updates as the dropdown changes.


---

### Task 2 – Show Total Revenue and Top Genre for Selected Day (Medium – ~7 min)

**Goal:** Enhance filtering logic to perform aggregation and join with `books.csv` to find the **top-selling genre**.

**Instructions:**
1. Starting from Task 1 code, load `books.csv` and merge with the filtered sales data using `book_id`.
2. Compute:
   - **Total revenue** for the selected day (`sales_df['total_amount'].sum()`).
   - **Top genre** by revenue.
3. Display both in the Dash interface.

**Skeleton Code:**
```python
# Load books data
books_df = pd.read_csv('books.csv')

@app.callback(
    [Output('sales-count-output', 'children'),
     Output('top-genre-output', 'children')],
    Input('day-dropdown', 'value')
)
def update_metrics(selected_day):
    # TODO: Filter sales_df by selected day
    # TODO: Merge with books_df
    # TODO: Calculate total revenue
    # TODO: Find genre with highest revenue
    return f"Revenue: $0", f"Top Genre: N/A"

# Add a new Div to layout for top genre
app.layout = html.Div([
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': d, 'value': d} for d in sales_df['day_name'].unique()],
        value='Monday'
    ),
    html.Div(id='sales-count-output'),
    html.Div(id='top-genre-output')
])
```

**Hints:**
- Use `groupby('genre')['total_amount'].sum().idxmax()` to find top genre.
- Format revenue nicely (e.g., `f"${total_revenue:,.2f}"`).

**Expected Output:**
- Day selection updates:
  - `Revenue: $X,XXX.XX`
  - `Top Genre: GenreName`


---

### Task 3 – Live Update Multiple Charts from Filtered Data (Medium-Hard – ~10 min)

**Goal:** Integrate multiple outputs:
- **Bar chart** of top 5 genres by revenue for the selected day.
- **Revenue** and **sales count** metrics (from previous tasks).

**Instructions:**
1. Use previous setup and add a Plotly Express bar chart (`px.bar`).
2. In the same callback:
   - Filter and merge data as before.
   - Compute total revenue and sales count.
   - Group by genre, sum revenue, sort, and take top 5.
   - Return both metrics and the figure.

**Skeleton Code:**
```python
import plotly.express as px

@app.callback(
    [Output('sales-count-output', 'children'),
     Output('top-genre-output', 'children'),
     Output('genre-bar-chart', 'figure')],
    Input('day-dropdown', 'value')
)
def update_dashboard(selected_day):
    # TODO: Filter & merge
    # TODO: Calculate total revenue and sales count
    # TODO: Create bar chart of top 5 genres by revenue
    fig = px.bar()  # placeholder
    return f"Records: {0}", f"Revenue: $0", fig

app.layout = html.Div([
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': d, 'value': d} for d in sales_df['day_name'].unique()],
        value='Monday'
    ),
    html.Div(id='sales-count-output'),
    html.Div(id='top-genre-output'),
    dcc.Graph(id='genre-bar-chart')
])
```

**Hints:**
- For chart: `px.bar(df_top5, x='genre', y='total_amount', title='Top Genres')`.
- Sort values by revenue descending before taking top 5.

**Expected Output:**
- Selecting a day updates:
  - Records count.
  - Total revenue.
  - Bar chart showing top 5 genres for the chosen day.
```