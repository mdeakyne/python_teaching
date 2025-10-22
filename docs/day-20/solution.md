```markdown
## Task 1 – EASY: Add Loading State to a Single Callback

### 1. Complete Working Code
```python
import dash
from dash import Dash, html, dcc, Output, Input
import pandas as pd

# Load datasets
sales = pd.read_csv("sales.csv")
books = pd.read_csv("books.csv")
authors = pd.read_csv("authors.csv")

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='author-dropdown',
        options=[
            {'label': name, 'value': aid} 
            for aid, name in zip(authors['author_id'], authors['full_name'])
        ],
        value=authors['author_id'].iloc[0]
    ),
    # Wrap the output div in dcc.Loading for spinner
    dcc.Loading(
        id="loading-sales",
        children=[html.Div(id='sales-table')],
        type="circle"
    )
])

@app.callback(
    Output('sales-table', 'children'),
    Input('author-dropdown', 'value')
)
def update_sales_table(author_id):
    # Filter books by selected author
    author_books = books[books['author_id'] == author_id]
    # Filter sales for those books
    filtered_sales = sales[sales['book_id'].isin(author_books['book_id'])]
    if filtered_sales.empty:
        return html.Div("No sales found for this author.")
    
    # Build HTML table
    table_header = [html.Tr([html.Th(col) for col in filtered_sales.columns])]
    table_rows = [
        html.Tr([html.Td(val) for val in row]) 
        for row in filtered_sales.values
    ]
    return html.Table(table_header + table_rows)

if __name__ == '__main__':
    app.run_server(debug=True)
```

### 2. Explanation
We wrap the sales display in `dcc.Loading` so Dash displays a spinner while the callback fetches and filters data. The callback filters sales by matching book IDs from the chosen author and constructs an HTML table for display.

### 3. Expected Output
- Initially displays sales for the first author.
- When user selects a different author from dropdown, a circular spinner briefly appears before the updated table renders.

### 4. Key Takeaway
Loading states greatly improve perceived performance by signaling work in progress.

**Alternative Approaches:**
- Use `dash_table.DataTable` instead of HTML tables for more functionality.
- Apply server-side prefiltering for large datasets to reduce callback time.

**Common Mistakes:**
1. Forgetting to wrap the output `html.Div` in `dcc.Loading`.
2. Not handling the case of empty filtered data.
3. Using `iloc[0]` without checking if dataset is non-empty.


---

## Task 2 – MEDIUM: Optimize Callback with `prevent_initial_call`

### 1. Complete Working Code
```python
import dash
from dash import Dash, html, dcc, Output, Input
import pandas as pd

# Data load
sales = pd.read_csv("sales.csv")
books = pd.read_csv("books.csv")
authors = pd.read_csv("authors.csv")

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='author-dropdown',
        options=[
            {'label': name, 'value': aid} 
            for aid, name in zip(authors['author_id'], authors['full_name'])
        ],
        placeholder="Select an author"
    ),
    dcc.Dropdown(
        id='genre-dropdown',
        options=[
            {'label': g, 'value': g} 
            for g in books['genre'].unique()
        ],
        placeholder="Select a genre"
    ),
    dcc.Loading(
        id="loading-sales",
        children=[html.Div(id='sales-table')],
        type="circle"
    )
])

@app.callback(
    Output('sales-table', 'children'),
    Input('author-dropdown', 'value'),
    Input('genre-dropdown', 'value'),
    prevent_initial_call=True
)
def update_sales_table(author_id, genre):
    if not author_id or not genre:
        return html.Div("Please select both author and genre.")
    
    # Filter books by author AND genre
    filtered_books = books[
        (books['author_id'] == author_id) & (books['genre'] == genre)
    ]
    filtered_sales = sales[sales['book_id'].isin(filtered_books['book_id'])]
    if filtered_sales.empty:
        return html.Div("No data for these filters.")
    
    table_header = [html.Tr([html.Th(col) for col in filtered_sales.columns])]
    table_rows = [
        html.Tr([html.Td(val) for val in row]) for row in filtered_sales.values
    ]
    return html.Table(table_header + table_rows)

if __name__ == '__main__':
    app.run_server(debug=True)
```

### 2. Explanation
We add a genre dropdown and use `prevent_initial_call=True` to stop the callback from running until both filters are selected. The callback applies both filters to produce the filtered sales table.

### 3. Expected Output
- On page load, table remains empty.
- After selecting both an author and a genre, a spinner shows briefly, then filtered sales table appears.

### 4. Key Takeaway
`prevent_initial_call` prevents wasted computation until all necessary inputs are provided.

**Alternative Approaches:**
- Use `State` instead of multiple `Input`s to trigger on explicit user action (e.g., button click).
- Chain callbacks to populate genres only after author selection.

**Common Mistakes:**
1. Forgetting to check `None` values for dropdowns.
2. Using `prevent_initial_call` incorrectly (must set on `@app.callback`).
3. Not matching column names exactly when filtering.


---

## Task 3 – MEDIUM-HARD: Multi-Page App with Cached Data

### 1. Complete Working Code
```python
import dash
from dash import Dash, html, dcc, Output, Input
import pandas as pd
from flask_caching import Cache

# Load datasets once
sales = pd.read_csv("sales.csv")
books = pd.read_csv("books.csv")
authors = pd.read_csv("authors.csv")
reviews = pd.read_csv("reviews.csv")

# Initialize app with multi-page support
app = Dash(__name__, suppress_callback_exceptions=True)
cache = Cache(app.server, config={'CACHE_TYPE': 'SimpleCache'})

# Page 1 layout: Sales filter
sales_layout = html.Div([
    html.H3("Sales Filter"),
    dcc.Dropdown(
        id='author-dropdown',
        options=[
            {'label': name, 'value': aid} 
            for aid, name in zip(authors['author_id'], authors['full_name'])
        ],
        placeholder="Select an author"
    ),
    dcc.Dropdown(
        id='genre-dropdown',
        options=[
            {'label': g, 'value': g} 
            for g in books['genre'].unique()
        ],
        placeholder="Select a genre"
    ),
    dcc.Loading(
        children=[html.Div(id='sales-table')],
        type="circle"
    ),
    html.Br(),
    dcc.Link('Go to Reviews Page', href='/reviews')
])

# Page 2 layout: Reviews summary
reviews_layout = html.Div([
    html.H3("Reviews Summary"),
    dcc.Dropdown(
        id='author-review-dropdown',
        options=[
            {'label': name, 'value': aid} 
            for aid, name in zip(authors['author_id'], authors['full_name'])
        ],
        placeholder="Select an author"
    ),
    dcc.Loading(
        children=[html.Div(id='review-summary')],
        type="dot"
    ),
    html.Br(),
    dcc.Link('Go to Sales Page', href='/')
])

# App container layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Router callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/reviews':
        return reviews_layout
    else:
        return sales_layout

# Cache helper for books by author
@cache.memoize(timeout=300)
def get_author_books(author_id):
    return books[books['author_id'] == author_id]

# Callback for Page 1 sales filter
@app.callback(
    Output('sales-table', 'children'),
    Input('author-dropdown', 'value'),
    Input('genre-dropdown', 'value'),
    prevent_initial_call=True
)
def update_sales_table(author_id, genre):
    if not author_id or not genre:
        return html.Div("Please select both filters.")
    filtered_books = get_author_books(author_id)
    filtered_books = filtered_books[filtered_books['genre'] == genre]
    filtered_sales = sales[sales['book_id'].isin(filtered_books['book_id'])]
    if filtered_sales.empty:
        return html.Div("No sales found for these filters.")
    header = [html.Tr([html.Th(c) for c in filtered_sales.columns])]
    rows = [html.Tr([html.Td(v) for v in row]) for row in filtered_sales.values]
    return html.Table(header + rows)

# Callback for Page 2 reviews summary
@app.callback(
    Output('review-summary', 'children'),
    Input('author-review-dropdown', 'value')
)
def update_review_summary(author_id):
    if not author_id:
        return html.Div("Please select an author.")
    books_df = get_author_books(author_id)
    reviews_df = reviews[reviews['book_id'].isin(books_df['book_id'])]
    if reviews_df.empty:
        return html.Div("No reviews for this author.")
    avg_rating = reviews_df['rating'].mean()
    total_reviews = len(reviews_df)
    return html.Div([
        html.P(f"Average Rating: {avg_rating:.2f}"),
        html.P(f"Total Reviews: {total_reviews}")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
```

### 2. Explanation
We implement a multi-page structure with `dcc.Location` and a router callback, separating layouts for sales filtering and reviews summary. Caching via `flask_caching` stores filtered books per author to avoid recomputation when navigating between pages.

### 3. Expected Output
- `/` shows author + genre filters and sales table with circular loading spinner.
- `/reviews` shows author dropdown and computed average rating and review count with dot-style loader.
- Switching between pages is instant for previously loaded authors due to caching.

### 4. Key Takeaway
Combining multi-page routing, caching, and loading states yields responsive, user-friendly dashboards.

**Alternative Approaches:**
- Use `dcc.Store` for client-side caching instead of server cache.
- Organize pages into separate Python modules for maintainability.

**Common Mistakes:**
1. Forgetting `suppress_callback_exceptions=True` in multi-page apps.
2. Not memoizing expensive data filters before page switching.
3. Leaving out navigation links, making switching pages difficult.
```