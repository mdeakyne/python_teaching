## 📝 Solutions: Dash Core Components – Inputs & Controls

---

### **Task 1 – Genre Dropdown**

#### **Complete Working Code**
```python
import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output

# Load dataset
books_df = pd.read_csv('books.csv')

# Extract unique genres
genres = books_df['genre'].unique()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Book Genre Filter"

# Layout
app.layout = html.Div([
    html.H2("📚 Book Genre Dropdown"),
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': g, 'value': g} for g in genres],
        value=genres[0],  # default selection
        clearable=False
    ),
    html.Br(),
    html.Div(id='genre-output', style={'fontSize': 18, 'color': '#333'})
])

# Callback
@app.callback(
    Output('genre-output', 'children'),
    Input('genre-dropdown', 'value')
)
def update_genre(selected_genre):
    """Display the selected genre as text output."""
    return f"You selected: {selected_genre}"

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
```

#### **Explanation**
We load the `books.csv` file, extract unique genres, and feed them into a Dash `dcc.Dropdown`. The callback listens to the dropdown's value and updates a `html.Div` to display the choice.

#### **Expected Output**
- Dropdown listing genres: *Mystery*, *Romance*, *Science Fiction*, etc.
- Selected genre displayed: `"You selected: Mystery"`

#### **Key Takeaway**
Dash callbacks allow reactive updates to UI elements based on user control inputs.

#### **Alternative Approaches**
- Use `options=books_df['genre'].drop_duplicates().sort_values()` to ensure alphabetical order.
- Populate dropdown dynamically from an API rather than static CSV.

#### **Common Mistakes**
1. Forgetting to set a default value; leads to empty output initially.  
2. Using `.unique()` without converting to list when needed for compatibility.  
3. Providing duplicate options if not deduplicated.

---

### **Task 2 – Publication Date Range Picker**

#### **Complete Working Code**
```python
import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output

# Load dataset
books_df = pd.read_csv('books.csv')
genres = books_df['genre'].unique()

# Year range
min_year = books_df['publication_year'].min()
max_year = books_df['publication_year'].max()

# Initialize app
app = dash.Dash(__name__)
app.title = "Book Filter by Genre & Publication Year"

# Layout
app.layout = html.Div([
    html.H2("📚 Filter Books by Genre & Year"),
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': g, 'value': g} for g in genres],
        value=genres[0],
        clearable=False
    ),
    html.Br(),
    dcc.RangeSlider(
        id='year-slider',
        min=min_year,
        max=max_year,
        value=[min_year, max_year],
        marks={str(y): str(y) for y in range(min_year, max_year + 1, 5)},
        step=1
    ),
    html.Br(),
    html.Div(id='filter-output', style={'fontSize': 18, 'color': '#333'})
])

# Callback
@app.callback(
    Output('filter-output', 'children'),
    Input('genre-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_filtered_list(selected_genre, year_range):
    """Filter books by selected genre and year range, return count."""
    start_year, end_year = year_range
    filtered = books_df[
        (books_df['genre'] == selected_genre) &
        (books_df['publication_year'] >= start_year) &
        (books_df['publication_year'] <= end_year)
    ]
    count = filtered.shape[0]
    return f"Found {count} books in {selected_genre} between {start_year} and {end_year}."

if __name__ == '__main__':
    app.run_server(debug=True)
```

#### **Explanation**
We keep Task 1’s genre dropdown and add a `RangeSlider` for years. The callback filters the DataFrame based on both selections and returns the count.

#### **Expected Output**
- Dropdown + RangeSlider visible.
- When selecting *Mystery* and years 2000–2010: `"Found 12 books in Mystery between 2000 and 2010."`

#### **Key Takeaway**
Dash can combine multiple inputs to dynamically filter and summarize datasets.

#### **Alternative Approaches**
- Use a `DatePickerRange` component if publication years are stored as full dates.
- Add histogram visualization instead of just a count.

#### **Common Mistakes**
1. Forgetting to unpack the `year_range` list into start/end variables.  
2. Using incorrect comparison operators (e.g., `>` instead of `>=`).  
3. Not updating slider marks when dataset changes.

---

### **Task 3 – Price Range Filter with Sales Integration**

#### **Complete Working Code**
```python
import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output

# Load datasets
books_df = pd.read_csv('books.csv')
sales_df = pd.read_csv('sales.csv')

# Prepare controls data
genres = books_df['genre'].unique()
min_year = books_df['publication_year'].min()
max_year = books_df['publication_year'].max()
max_price = books_df['price'].max()

# Initialize app
app = dash.Dash(__name__)
app.title = "Book Sales Filter"

# Layout
app.layout = html.Div([
    html.H2("📊 Filter Books by Genre, Year & Price to See Sales"),
    
    # Genre selector
    dcc.Dropdown(
        id='genre-dropdown',
        options=[{'label': g, 'value': g} for g in genres],
        value=genres[0],
        clearable=False
    ),
    html.Br(),
    
    # Year range slider
    dcc.RangeSlider(
        id='year-slider',
        min=min_year,
        max=max_year,
        value=[min_year, max_year],
        marks={str(y): str(y) for y in range(min_year, max_year + 1, 5)},
        step=1
    ),
    html.Br(),
    
    # Price slider
    dcc.Slider(
        id='price-slider',
        min=0,
        max=max_price,
        value=max_price,
        step=1,
        marks={0: '$0', int(max_price): f'${int(max_price)}'}
    ),
    html.Br(),
    
    # Output
    html.Div(id='sales-output', style={'fontSize': 18, 'color': '#333'})
])

# Callback
@app.callback(
    Output('sales-output', 'children'),
    Input('genre-dropdown', 'value'),
    Input('year-slider', 'value'),
    Input('price-slider', 'value')
)
def update_sales(selected_genre, year_range, max_selected_price):
    """Filter books by genre, year range, and max price; join with sales and sum total_amount."""
    start_year, end_year = year_range
    
    # Filter books
    filtered_books = books_df[
        (books_df['genre'] == selected_genre) &
        (books_df['publication_year'] >= start_year) &
        (books_df['publication_year'] <= end_year) &
        (books_df['price'] <= max_selected_price)
    ]
    
    # Join with sales
    filtered_sales = sales_df[sales_df['book_id'].isin(filtered_books['book_id'])]
    total_sales = filtered_sales['total_amount'].sum()
    
    return (f"Total sales: ${total_sales:,.2f} for {selected_genre} books "
            f"({start_year}–{end_year}) under ${max_selected_price:.2f}")

if __name__ == '__main__':
    app.run_server(debug=True)
```

#### **Explanation**
We add a `dcc.Slider` for limiting maximum price and filter `books_df` against genre, year, and price. Matching books are joined with `sales_df` on `book_id`, and we sum their `total_amount`.

#### **Expected Output**
- Selecting *Mystery*, 2000–2010, price ≤ $20:
  `"Total sales: $42,350.00 for Mystery books (2000–2010) under $20"`

#### **Key Takeaway**
Combining multiple filters and joining datasets within a callback enables rich, cross-data analytics in Dash apps.

#### **Alternative Approaches**
- Use `merge` instead of `isin` for better performance on large datasets.
- Display sales breakdown in a bar chart rather than text.

#### **Common Mistakes**
1. Forgetting to filter the joined dataset by all control values.  
2. Performing joins on mismatched key column names without renaming.  
3. Treating price as string rather than numeric type, breaking comparisons.