```markdown
## Task 1 – EASY (5 min): Add Loading State to a Single Callback

**Objective:** Reinforce adding a loading spinner to improve user experience during data processing.

You’ll modify a callback that updates a sales table based on selected author, so users see a loading indicator while data is being filtered.

**Starter Code:**
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
        options=[{'label': name, 'value': aid} for aid, name in zip(authors['author_id'], authors['full_name'])],
        value=authors['author_id'].iloc[0]
    ),
    dcc.Loading(  # TODO: wrap table output in this component
        id="loading-sales",
        children=[
            html.Div(id='sales-table')
        ],
        type="circle"
    )
])

@app.callback(
    Output('sales-table', 'children'),
    Input('author-dropdown', 'value')
)
def update_sales_table(author_id):
    # TODO: Filter sales by books from selected author
    filtered_df = ...
    return html.Table([
        html.Tr([html.Th(col) for col in filtered_df.columns])
    ] + [
        html.Tr([html.Td(val) for val in row]) for row in filtered_df.values
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
```

**Success Criteria:**
- Selecting a different author shows a loading spinner briefly while table updates.
- Filter logic correctly displays only sales for books by selected author.

**Expected Output:**
A table of sales for the chosen author with a circular loading animation during data refresh.

---

## Task 2 – MEDIUM (7 min): Optimize Callback with `prevent_initial_call`

**Objective:** Reduce unnecessary computation by preventing callbacks until user selects data.

Now extend Task 1 by adding a second dropdown for genre, and ensure the sales table does **not** update until both filters are chosen by the user.

**Starter Code:**
```python
app.layout = html.Div([
    dcc.Dropdown(
        id='author-dropdown',
        options=[{'label': name, 'value': aid} for aid, name in zip(authors['author_id'], authors['full_name'])],
        placeholder="Select an author"
    ),
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': g, 'value': g} for g in books['genre'].unique()],
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
    prevent_initial_call=True  # TODO: Apply this setting
)
def update_sales_table(author_id, genre):
    # TODO: Filter books by author and genre, join with sales
    filtered_df = ...
    return html.Table([...])
```

**Expected Output:**
- The sales table remains empty when the app loads.
- Only when both author and genre are chosen does the table appear.
- Loading spinner is shown while results compute.

---

## Task 3 – MEDIUM-HARD (10 min): Multi-Page App with Cached Data

**Objective:** Integrate best practices: caching, loading states, multi-page structure.

Build a two-page Dash app:
- Page 1: Sales filter (author, genre) with loading spinner (from Task 2).
- Page 2: Reviews summary for selected author with average rating and total reviews.
Use `dcc.Store` or `flask_caching` to cache filtered author data so switching pages doesn’t recompute from scratch.

**Starter Code:**
```python
from flask_caching import Cache

app = Dash(__name__, suppress_callback_exceptions=True)
cache = Cache(app.server, config={'CACHE_TYPE': 'SimpleCache'})

# Layouts for each page
sales_layout = html.Div([...])  # TODO: reuse from Task 2
reviews_layout = html.Div([
    dcc.Dropdown(
        id='author-review-dropdown',
        options=[{'label': name, 'value': aid} for aid, name in zip(authors['author_id'], authors['full_name'])],
        placeholder="Select an author"
    ),
    dcc.Loading(
        children=[html.Div(id='review-summary')],
        type="dot"
    )
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/reviews':
        return reviews_layout
    else:
        return sales_layout

@cache.memoize(timeout=300)
def get_author_books(author_id):
    # TODO: Return dataframe of books for author_id
    return ...

@app.callback(
    Output('review-summary', 'children'),
    Input('author-review-dropdown', 'value')
)
def update_review_summary(author_id):
    books_df = get_author_books(author_id)
    # TODO: Join with reviews.csv and compute avg rating, total reviews
    return html.Div([...])
```

**Expected Output:**
- Users can navigate between `/` and `/reviews` without re-running expensive filters for authors already viewed.
- Page 1 shows filtered sales as before.
- Page 2 shows average rating and total reviews for selected author, with a dot-style loader.
- Fast page load after initial data retrieval due to caching.
```
