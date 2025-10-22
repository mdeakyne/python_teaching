```markdown
## 📝 Hands-On Exercises – Day 17: Callbacks – Making It Interactive

---

### Task 1 (EASY – 5 min)  
**Goal:** Write a Dash callback to update a single chart based on one dropdown input.

**Scenario:** Display a bar chart of **total sales by book** for a selected genre.

**Skeleton Code:**
```python
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load datasets
books = pd.read_csv("data/books.csv")
sales = pd.read_csv("data/sales.csv")

# Merge for easier filtering
book_sales = sales.merge(books, on="book_id")

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="genre-dropdown",
        options=[{"label": g, "value": g} for g in books["genre"].unique()],
        value=books["genre"].unique()[0]
    ),
    dcc.Graph(id="sales-bar")
])

@app.callback(
    Output("sales-bar", "figure"),
    Input("genre-dropdown", "value")
)
def update_sales_chart(selected_genre):
    # TODO: Filter `book_sales` by genre
    # TODO: Group by book title and sum total_amount
    # TODO: Create a bar chart figure
    pass

if __name__ == "__main__":
    app.run_server(debug=True)
```

**Success Criteria:**
- Changing the genre in the dropdown updates the bar chart without page refresh.
- Bar chart shows book titles (x-axis) and total sales amount (y-axis) for that genre.

**Expected Output:**  
A responsive bar chart where selecting "Science Fiction" shows its books sorted by sales amount; selecting "Romance" updates instantly to display that genre's books.

---

### Task 2 (MEDIUM – 7 min)  
**Goal:** Add a second input to control the displayed chart — introduce multiple inputs in a callback.

**Scenario:** Update the chart to show **average rating by book**, filtered by selected genre and minimum rating.

**Skeleton Code:**
```python
reviews = pd.read_csv("data/reviews.csv")
books = pd.read_csv("data/books.csv")
merged_reviews = reviews.merge(books, on="book_id")

app.layout = html.Div([
    dcc.Dropdown(
        id="genre-dropdown",
        options=[{"label": g, "value": g} for g in books["genre"].unique()],
        value=books["genre"].unique()[0]
    ),
    dcc.Slider(
        id="min-rating-slider",
        min=1, max=5, step=0.5,
        value=3,
        marks={i: str(i) for i in range(1, 6)}
    ),
    dcc.Graph(id="rating-bar")
])

@app.callback(
    Output("rating-bar", "figure"),
    [Input("genre-dropdown", "value"),
     Input("min-rating-slider", "value")]
)
def update_rating_chart(selected_genre, min_rating):
    # TODO: Filter by genre
    # TODO: Group by book title and compute average rating
    # TODO: Filter out books below min_rating
    # TODO: Create bar chart figure
    pass
```

**Success Criteria:**
- Selecting a new genre **and/or** adjusting minimum rating updates chart immediately.
- Chart excludes books that have an average rating below chosen threshold.

**Expected Output:**  
If genre is "Mystery" and min rating is set to 4.0, only Mystery books with average rating ≥ 4.0 appear as bars.

---

### Task 3 (MEDIUM-HARD – 10 min)  
**Goal:** Handle multiple outputs using combined inputs — connect two different graphs that update together.

**Scenario:** A dashboard with:
1. **Daily sales time series chart** filtered by genre and year.
2. **Top 5 books table** (by average rating) for same genre and year.

**Skeleton Code:**
```python
books = pd.read_csv("data/books.csv")
sales = pd.read_csv("data/sales.csv")
reviews = pd.read_csv("data/reviews.csv")

sales["date"] = pd.to_datetime(sales["date"])
merged_sales = sales.merge(books, on="book_id")
merged_reviews = reviews.merge(books, on="book_id")

app.layout = html.Div([
    dcc.Dropdown(
        id="genre-dropdown",
        options=[{"label": g, "value": g} for g in books["genre"].unique()],
        value=books["genre"].unique()[0]
    ),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": y, "value": y} for y in sorted(books["publication_year"].unique())],
        value=books["publication_year"].min()
    ),
    html.Div([
        dcc.Graph(id="daily-sales-chart"),
        dcc.Graph(id="top-books-table")  # Can use DataTable or bar chart
    ])
])

@app.callback(
    [Output("daily-sales-chart", "figure"),
     Output("top-books-table", "figure")],
    [Input("genre-dropdown", "value"),
     Input("year-dropdown", "value")]
)
def update_dashboard(selected_genre, selected_year):
    # TODO: Filter sales + reviews by genre & year
    # TODO: Prepare daily sales time series
    # TODO: Prepare top 5 books by avg rating
    # TODO: Return two figures
    pass
```

**Success Criteria:**
- Changing genre or year updates **both** charts instantly.
- Time series shows sales trend over the selected year for the selected genre.
- The second chart displays top-rated books for same filters, limited to 5 entries.

**Expected Output:**  
For genre "Fantasy" in year 2022: the daily sales chart shows spikes on key dates; the top 5 books table lists Fantasy books published in 2022 with highest average ratings.

---
```