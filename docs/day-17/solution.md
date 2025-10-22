```markdown
## ✅ Day 17 Solutions – Callbacks: Making It Interactive

---

### Task 1 – Single Input → Single Output Bar Chart

#### 1. Complete Working Code
```python
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load datasets
books = pd.read_csv("data/books.csv")
sales = pd.read_csv("data/sales.csv")

# Merge for easier filtering
book_sales = sales.merge(books, on="book_id")

# Initialize Dash app
app = dash.Dash(__name__)

# App layout: dropdown + chart
app.layout = html.Div([
    dcc.Dropdown(
        id="genre-dropdown",
        options=[{"label": g, "value": g} for g in books["genre"].unique()],
        value=books["genre"].unique()[0]
    ),
    dcc.Graph(id="sales-bar")
])

# Callback to update figure
@app.callback(
    Output("sales-bar", "figure"),
    Input("genre-dropdown", "value")
)
def update_sales_chart(selected_genre):
    # Filter by selected genre
    filtered = book_sales[book_sales["genre"] == selected_genre]
    # Group by title and sum total_amount
    genre_sales = (filtered.groupby("title", as_index=False)
                            .agg({"total_amount": "sum"})
                            .sort_values("total_amount", ascending=False))
    # Create bar chart
    fig = px.bar(genre_sales,
                 x="title",
                 y="total_amount",
                 title=f"Total Sales by Book – {selected_genre}",
                 labels={"total_amount": "Total Sales ($)", "title": "Book Title"})
    fig.update_layout(xaxis_tickangle=-45)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
```

#### 2. Explanation
We filter merged sales–books data by `selected_genre`, aggregate sales by book title, and build a responsive Plotly bar chart. Dash callbacks automatically update the chart when dropdown selection changes.

#### 3. Expected Output
When "Romance" is selected, you see bars for Romance novels ordered by total sales amount. Changing to "Science Fiction" instantly updates to relevant books.

#### 4. Key Takeaway
A single `Input` and `Output` combo in Dash lets you quickly make interactive charts driven by one control.

#### Alternative Approaches
- Use `dash.dash_table.DataTable` instead of `dcc.Graph`.
- Pre-aggregate per genre to speed up filtering.

#### Common Mistakes
1. Forgetting to sort data before plotting (results in random bar order).
2. Not matching dropdown `value` with existing genre strings.
3. Using incorrect merge keys when combining datasets.

---

### Task 2 – Multiple Inputs → Single Output

#### 1. Complete Working Code
```python
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load datasets
books = pd.read_csv("data/books.csv")
reviews = pd.read_csv("data/reviews.csv")

# Merge for easier filtering
merged_reviews = reviews.merge(books, on="book_id")

# Initialize app
app = dash.Dash(__name__)

# Layout: dropdown, slider, chart
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

# Callback for multi-input filtering
@app.callback(
    Output("rating-bar", "figure"),
    [Input("genre-dropdown", "value"),
     Input("min-rating-slider", "value")]
)
def update_rating_chart(selected_genre, min_rating):
    # Filter by genre
    filtered = merged_reviews[merged_reviews["genre"] == selected_genre]
    # Group by book and compute average rating
    avg_ratings = (filtered.groupby("title", as_index=False)
                             .agg({"rating": "mean"}))
    # Filter by minimum rating threshold
    avg_ratings = avg_ratings[avg_ratings["rating"] >= min_rating]
    # Sort for better visual
    avg_ratings = avg_ratings.sort_values("rating", ascending=False)
    # Create bar chart
    fig = px.bar(avg_ratings,
                 x="title",
                 y="rating",
                 title=f"Average Rating by Book – {selected_genre} (≥ {min_rating})",
                 labels={"rating": "Avg Rating", "title": "Book Title"},
                 range_y=[0, 5])
    fig.update_layout(xaxis_tickangle=-45)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
```

#### 2. Explanation
Two inputs — a dropdown for genre and a slider for minimum rating — drive filtering logic. We compute average ratings per book, apply the rating threshold, and render sorted bars.

#### 3. Expected Output
For "Mystery" and min rating 4, only Mystery books with average ratings ≥ 4 are shown in descending order.

#### 4. Key Takeaway
Dash callbacks can accept multiple inputs, enabling compound filtering logic for a single visualization.

#### Alternative Approaches
- Dynamically update slider range based on selected genre's ratings.
- Use horizontal bars (`orientation='h'`) for better readability.

#### Common Mistakes
1. Forgetting to merge reviews with book info before filtering.
2. Applying threshold before averaging (distorts calculations).
3. Not converting ratings to numeric type before filtering.

---

### Task 3 – Multiple Inputs → Multiple Outputs

#### 1. Complete Working Code
```python
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load datasets
books = pd.read_csv("data/books.csv")
sales = pd.read_csv("data/sales.csv")
reviews = pd.read_csv("data/reviews.csv")

# Prepare data
sales["date"] = pd.to_datetime(sales["date"])
merged_sales = sales.merge(books, on="book_id")
merged_reviews = reviews.merge(books, on="book_id")

# App initialization
app = dash.Dash(__name__)

# Layout: dropdowns + two graphs
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
        dcc.Graph(id="top-books-table")
    ])
])

@app.callback(
    [Output("daily-sales-chart", "figure"),
     Output("top-books-table", "figure")],
    [Input("genre-dropdown", "value"),
     Input("year-dropdown", "value")]
)
def update_dashboard(selected_genre, selected_year):
    # Filter sales by genre & year
    filtered_sales = merged_sales[
        (merged_sales["genre"] == selected_genre) &
        (merged_sales["publication_year"] == selected_year)
    ]
    # Daily Sales Time Series
    daily_sales = (filtered_sales.groupby("date", as_index=False)
                                .agg({"total_amount": "sum"}))
    sales_fig = px.line(daily_sales,
                        x="date",
                        y="total_amount",
                        title=f"Daily Sales – {selected_genre} ({selected_year})",
                        labels={"total_amount": "Total Sales ($)", "date": "Date"})
    
    # Filter reviews for same genre/year
    filtered_reviews = merged_reviews[
        (merged_reviews["genre"] == selected_genre) &
        (merged_reviews["publication_year"] == selected_year)
    ]
    # Top 5 books by average rating
    top_books = (filtered_reviews.groupby("title", as_index=False)
                                .agg({"rating": "mean"})
                                .sort_values("rating", ascending=False)
                                .head(5))
    top_books_fig = px.bar(top_books,
                           x="title",
                           y="rating",
                           title=f"Top 5 Books by Avg Rating – {selected_genre} ({selected_year})",
                           labels={"rating": "Avg Rating", "title": "Book Title"},
                           range_y=[0, 5])
    top_books_fig.update_layout(xaxis_tickangle=-30)
    
    return sales_fig, top_books_fig

if __name__ == "__main__":
    app.run_server(debug=True)
```

#### 2. Explanation
Both graphs share the same two inputs. The first chart aggregates daily sales over the filtered dataset, and the second finds top 5 books by average rating for the same filters. Returning a tuple of figures updates both outputs simultaneously.

#### 3. Expected Output
For "Fantasy" in year 2022, the left plot shows a time series with peaks; the right bar chart lists the top 5 Fantasy books published in 2022 sorted by rating.

#### 4. Key Takeaway
Dash supports multiple outputs in a single callback, allowing you to coordinate updates across multiple visual components.

#### Alternative Approaches
- Use `dash_table.DataTable` for the top books instead of a bar chart.
- Cache filtered results to optimize performance.

#### Common Mistakes
1. Forgetting to filter **both** sales and reviews datasets by genre & year.
2. Not converting `date` columns to `datetime` before grouping.
3. Returning figures in wrong order — must match Output list order.

---
```