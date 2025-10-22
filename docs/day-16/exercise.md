## 📝 Exercise: Dash Core Components – Inputs & Controls

---

### **Task 1 – Genre Dropdown (Easy – 5 min)**

**Goal:** Create a simple dropdown to filter books by genre using `books.csv`.

**Instructions:**
1. Load `books.csv` with pandas.
2. Extract the unique genres from the dataset.
3. Create a `dcc.Dropdown` component populated with these genres.
4. Display the selected genre in a `html.Div`.

**Code Skeleton:**
```python
import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output

# Load dataset
books_df = pd.read_csv('books.csv')

# Extract unique genres
genres = books_df['genre'].unique()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': g, 'value': g} for g in genres],
        value=genres[0]  # default value
    ),
    html.Div(id='genre-output')
])

@app.callback(
    Output('genre-output', 'children'),
    Input('genre-dropdown', 'value')
)
def update_genre(selected_genre):
    # TODO: return a message showing selected genre
    pass

if __name__ == '__main__':
    app.run_server(debug=True)
```

**Expected Output:**
- A dropdown listing all genres in `books.csv`.
- Selecting a genre shows a text message, e.g., _"You selected: Mystery"_.

---

### **Task 2 – Publication Date Range Picker (Medium – 7 min)**

**Goal:** Add a date range picker to filter book sales by publication year, building on Task 1.

**Instructions:**
1. Keep the genre dropdown from Task 1.
2. Add a `dcc.RangeSlider` for selecting a publication year range.
3. Display the number of books matching the selected genre **and** year range.

**Code Skeleton:**
```python
# Continue from previous code...
min_year = books_df['publication_year'].min()
max_year = books_df['publication_year'].max()

app.layout = html.Div([
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': g, 'value': g} for g in genres],
        value=genres[0]
    ),
    dcc.RangeSlider(
        id='year-slider',
        min=min_year,
        max=max_year,
        value=[min_year, max_year],
        marks={str(y): str(y) for y in range(min_year, max_year+1, 5)}
    ),
    html.Div(id='filter-output')
])

@app.callback(
    Output('filter-output', 'children'),
    Input('genre-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_filtered_list(selected_genre, year_range):
    # TODO: Filter books_df by genre and publication year range
    # TODO: Return count of matching books
    pass
```

**Expected Output:**
- Dropdown + range slider visible.
- Adjusting genre or year shows the updated count, e.g., _"Found 12 books in Mystery between 2000 and 2010"_.

---

### **Task 3 – Price Range Filter with Sales Integration (Medium-Hard – 10 min)**

**Goal:** Combine genre, publication year, and price controls to filter books and display total sales value.

**Instructions:**
1. Continue from Task 2.
2. Add a `dcc.Slider` for selecting maximum book price.
3. Filter `books_df` using genre, year range, and selected price.
4. Join filtered books with `sales.csv` to calculate total sales amount for matching books.
5. Display the total sales in a readable format.

**Code Skeleton:**
```python
sales_df = pd.read_csv('sales.csv')

max_price = books_df['price'].max()

app.layout = html.Div([
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': g, 'value': g} for g in genres],
        value=genres[0]
    ),
    dcc.RangeSlider(
        id='year-slider',
        min=min_year,
        max=max_year,
        value=[min_year, max_year],
        marks={str(y): str(y) for y in range(min_year, max_year+1, 5)}
    ),
    dcc.Slider(
        id='price-slider',
        min=0,
        max=max_price,
        value=max_price,
        step=1,
        marks={0: '$0', int(max_price): f'${int(max_price)}'}
    ),
    html.Div(id='sales-output')
])

@app.callback(
    Output('sales-output', 'children'),
    Input('genre-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('price-slider', 'value')
)
def update_sales(selected_genre, year_range, max_selected_price):
    # TODO: Filter books_df by genre, year, price
    # TODO: Join with sales_df to filter matching book_ids
    # TODO: Sum total_amount of matching sales
    pass
```

**Expected Output:**
- Interactive controls for genre, year range, and price.
- Changing controls updates displayed total sales value, e.g., _"Total sales: $42,350 for Mystery books (2000–2010) under $20"_.