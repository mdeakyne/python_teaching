```markdown
## 🛠 Day 19: Integrating Pandas with Dash – Live Filtering

---

### **Task 1 – Filter Sales by Selected Day of the Week**

#### 1. Complete Working Code
```python
import dash
from dash import dcc, html, Input, Output
import pandas as pd

# Load sales data
sales_df = pd.read_csv('sales.csv')

# Add day_name column from date
sales_df['day_name'] = pd.to_datetime(sales_df['date']).dt.day_name()

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with dropdown and output div
app.layout = html.Div([
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': day, 'value': day} for day in sales_df['day_name'].unique()],
        value='Monday',
        clearable=False
    ),
    html.Div(id='sales-count-output')
])

# Callback for live filtering
@app.callback(
    Output('sales-count-output', 'children'),
    Input('day-dropdown', 'value')
)
def update_sales_count(selected_day):
    # Filter DataFrame by day_name
    filtered_df = sales_df[sales_df['day_name'] == selected_day]
    record_count = filtered_df.shape[0]
    return f"Records: {record_count}"

if __name__ == '__main__':
    app.run_server(debug=True)
```

#### 2. Explanation
We load the sales dataset, extract the weekday name from the date, and populate a dropdown with unique days. On selection, the callback filters the DataFrame and returns the record count for that day.

#### 3. Expected Output
- **Dropdown:** Displays Monday, Tuesday, etc.
- **Text Output:** Changes to `Records: X` depending on current selection.

#### 4. Key Takeaway
Day-based filtering with Pandas can be easily integrated into Dash callbacks for live metrics.

#### Alternative Approaches
- Generate dropdown options from `calendar.day_name` to ensure all days are always shown.
- Pre-sort days in a standard Monday–Sunday order.

#### Common Mistakes
1. Forgetting to parse `date` as datetime before extracting day names.
2. Using `.count()` on `DataFrame` without selecting the correct axis, leading to unexpected results.
3. Not handling case sensitivity for day names.

---

### **Task 2 – Show Total Revenue and Top Genre for Selected Day**

#### 1. Complete Working Code
```python
import dash
from dash import dcc, html, Input, Output
import pandas as pd

# Load datasets
sales_df = pd.read_csv('sales.csv')
books_df = pd.read_csv('books.csv')

# Add day_name column
sales_df['day_name'] = pd.to_datetime(sales_df['date']).dt.day_name()

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with dropdown and output components
app.layout = html.Div([
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': day, 'value': day} for day in sales_df['day_name'].unique()],
        value='Monday',
        clearable=False
    ),
    html.Div(id='sales-count-output'),
    html.Div(id='top-genre-output')
])

# Callback to show revenue and top genre
@app.callback(
    [Output('sales-count-output', 'children'),
     Output('top-genre-output', 'children')],
    Input('day-dropdown', 'value')
)
def update_metrics(selected_day):
    # Filter sales by selected day
    filtered_sales = sales_df[sales_df['day_name'] == selected_day]
    # Merge with books_df to get genre info
    merged_df = filtered_sales.merge(books_df, on='book_id', how='left')
    total_revenue = merged_df['total_amount'].sum()
    # Find top genre by revenue
    genre_revenue = merged_df.groupby('genre')['total_amount'].sum()
    top_genre = genre_revenue.idxmax() if not genre_revenue.empty else 'N/A'
    return (f"Revenue: ${total_revenue:,.2f}",
            f"Top Genre: {top_genre}")

if __name__ == '__main__':
    app.run_server(debug=True)
```

#### 2. Explanation
We extend Task 1 to merge the filtered sales data with books metadata, allowing genre identification and revenue aggregation. The total revenue and highest earning genre for that day are computed and displayed.

#### 3. Expected Output
- Dropdown selection updates:
  - `Revenue: $X,XXX.XX`
  - `Top Genre: Fiction` (example)

#### 4. Key Takeaway
Merging related datasets allows richer metrics beyond simple counts.

#### Alternative Approaches
- Use `pd.merge` with `validate='m:1'` to ensure join correctness.
- Precompute per-day genre aggregates for faster callback execution.

#### Common Mistakes
1. Forgetting to merge on the correct key (`book_id`).
2. Not handling empty filtered sets, causing `.idxmax()` errors.
3. Summing `quantity * unit_price` incorrectly instead of using `total_amount`.

---

### **Task 3 – Live Update Multiple Charts from Filtered Data**

#### 1. Complete Working Code
```python
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load datasets
sales_df = pd.read_csv('sales.csv')
books_df = pd.read_csv('books.csv')

# Add day_name column
sales_df['day_name'] = pd.to_datetime(sales_df['date']).dt.day_name()

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with dropdown, outputs, and chart
app.layout = html.Div([
    dcc.Dropdown(
        id='day-dropdown',
        options=[{'label': day, 'value': day} for day in sales_df['day_name'].unique()],
        value='Monday',
        clearable=False
    ),
    html.Div(id='sales-count-output'),
    html.Div(id='top-genre-output'),
    dcc.Graph(id='genre-bar-chart')
])

# Callback
@app.callback(
    [Output('sales-count-output', 'children'),
     Output('top-genre-output', 'children'),
     Output('genre-bar-chart', 'figure')],
    Input('day-dropdown', 'value')
)
def update_dashboard(selected_day):
    # Filter and merge datasets
    filtered_sales = sales_df[sales_df['day_name'] == selected_day]
    merged_df = filtered_sales.merge(books_df, on='book_id', how='left')

    # Metrics calculation
    total_revenue = merged_df['total_amount'].sum()
    sales_count = merged_df.shape[0]
    genre_revenue_df = (merged_df.groupby('genre', as_index=False)['total_amount']
                        .sum()
                        .sort_values(by='total_amount', ascending=False))

    # Top genre
    top_genre = genre_revenue_df.iloc[0]['genre'] if not genre_revenue_df.empty else 'N/A'

    # Bar chart for top 5 genres
    df_top5 = genre_revenue_df.head(5)
    fig = px.bar(df_top5,
                 x='genre',
                 y='total_amount',
                 title=f"Top 5 Genres by Revenue ({selected_day})",
                 labels={'genre': 'Genre', 'total_amount': 'Revenue'},
                 text_auto=True)

    return (f"Records: {sales_count}",
            f"Revenue: ${total_revenue:,.2f} | Top Genre: {top_genre}",
            fig)

if __name__ == '__main__':
    app.run_server(debug=True)
```

#### 2. Explanation
We combine statistics and visualization by filtering, merging, and grouping the data in one callback, then returning multiple outputs—a record count, total revenue/top genre text, and a bar chart for the top 5 genres.

#### 3. Expected Output
- Dropdown selection updates:
  - `Records: 120`
  - `Revenue: $5,324.50 | Top Genre: Mystery`
  - Bar chart showing top 5 genres with revenue values.

#### 4. Key Takeaway
Dash callbacks can return multiple UI components, enabling synchronized data updates across text and charts.

#### Alternative Approaches
- Use separate callbacks for metrics and chart if performance or reusability is a priority.
- Pre-calculate aggregates for each day to minimize runtime filtering.

#### Common Mistakes
1. Not sorting before slicing top 5 genres.
2. Forgetting to merge sales with books, resulting in missing genre data.
3. Passing empty DataFrames to Plotly without handling, causing blank charts.

---
```