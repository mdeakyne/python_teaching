```markdown
## Task 1 – Easy: Your First Dash App Layout

### 1. Complete Working Code
```python
import dash
from dash import html
import dash_bootstrap_components as dbc

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout: Heading and static chart image from assets directory
app.layout = dbc.Container(
    [
        html.H1("Page Turner Analytics – Sales Overview", className="mt-4"),
        html.Img(
            src="assets/sales_chart.png",
            style={"width": "60%", "display": "block", "margin": "auto"}
        )
    ],
    fluid=True
)

if __name__ == "__main__":
    # Run the app locally with debugging enabled
    app.run_server(debug=True)
```

### 2. Explanation
This app uses Dash with Bootstrap styling to render a static HTML layout containing a heading and an image stored in the `assets` folder. Dash automatically serves static files from `assets`, so placing the chart PNG there ensures it is accessible via a relative path.

### 3. Expected Output
A web page with:
- A large centered heading: *Page Turner Analytics – Sales Overview*
- Below the heading, a centered chart image (`sales_chart.png`), scaled to 60% width.

### 4. Key Takeaway
A fundamental Dash app can display static content easily when assets are placed in the appropriate folder.

---

**Alternative Approaches**  
- Use `dcc.Image` with a `base64` encoded image embedded directly in the layout.  
- Generate the chart on the fly and save into `assets` at runtime.

**Common Mistakes**  
1. Placing the image outside of the `assets` directory—Dash won't find it.  
2. Using the wrong path (`/assets/...`) instead of just `assets/...`.  
3. Forgetting to run the server with `app.run_server()`.

---

## Task 2 – Medium: Display Static Chart with Dataset Context

### 1. Complete Working Code
```python
import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

# Load the books dataset
books_df = pd.read_csv("data/books.csv")

# Compute summary metrics
total_books = books_df.shape[0]
unique_authors_count = books_df['author_name'].nunique()
average_price = books_df['price'].mean()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout: Heading, paragraph summary, and static chart
app.layout = dbc.Container(
    [
        html.H1("Page Turner Analytics – Catalog Overview", className="mt-4"),
        html.P(
            f"Total Books: {total_books} | Total Authors: {unique_authors_count} | "
            f"Average Price: ${average_price:,.2f}",
            className="lead"
        ),
        html.Img(
            src="assets/genre_distribution.png",
            style={"width": "50%", "display": "block", "margin": "auto"}
        )
    ],
    fluid=True
)

if __name__ == "__main__":
    app.run_server(debug=True)
```

### 2. Explanation
We extend the previous app by reading `books.csv` into a Pandas DataFrame, computing summary statistics, and adding them to the layout above a static genre distribution chart. This gives users immediate context about the dataset alongside a visual.

### 3. Expected Output
A page with:
- Heading: *Page Turner Analytics – Catalog Overview*
- A short paragraph: *Total Books: X | Total Authors: Y | Average Price: $Z*
- Genre distribution chart image centered at 50% width.

### 4. Key Takeaway
Combining textual KPIs with visual charts improves data communication and provides more insights at a glance.

---

**Alternative Approaches**  
- Display the summary metrics in Bootstrap cards for enhanced styling.  
- Load charts from Plotly as interactive components instead of static images.

**Common Mistakes**  
1. Forgetting to parse numeric columns correctly, resulting in string data types.  
2. Not formatting numeric outputs (e.g., average price) to two decimal places.  
3. Using incorrect column names—always check CSV headers.

---

## Task 3 – Medium-Hard: Multi-Section Layout with Sales & Reviews

### 1. Complete Working Code
```python
import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

# Load datasets
sales_df = pd.read_csv("data/sales.csv", parse_dates=["date"])
reviews_df = pd.read_csv("data/reviews.csv")

# KPI calculations for Sales
total_revenue = sales_df['total_amount'].sum()
total_units = sales_df['quantity'].sum()
average_unit_price = sales_df['unit_price'].mean()

# KPI calculations for Reviews
average_rating = reviews_df['rating'].mean()
total_reviews = reviews_df.shape[0]
verified_purchase_pct = (reviews_df['verified_purchase'].sum() / total_reviews) * 100

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout: Top summary section, bottom charts section
app.layout = dbc.Container(
    [
        html.H1("Page Turner Analytics – Quarterly Report", className="mt-4"),

        # KPI summaries in two columns
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Sales Summary"),
                        html.P(f"Total Revenue: ${total_revenue:,.2f}"),
                        html.P(f"Total Units Sold: {total_units}"),
                        html.P(f"Average Unit Price: ${average_unit_price:,.2f}")
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        html.H3("Reviews Summary"),
                        html.P(f"Average Rating: {average_rating:.2f} / 5"),
                        html.P(f"Total Reviews: {total_reviews}"),
                        html.P(f"Verified Purchases: {verified_purchase_pct:.1f}%")
                    ],
                    width=6
                ),
            ],
            className="mb-4"
        ),

        # Charts arranged side-by-side
        dbc.Row(
            [
                dbc.Col(
                    html.Img(src="assets/sales_trend.png",
                             style={"width": "100%", "border": "1px solid #ccc"}),
                    width=6
                ),
                dbc.Col(
                    html.Img(src="assets/avg_ratings_genre.png",
                             style={"width": "100%", "border": "1px solid #ccc"}),
                    width=6
                ),
            ]
        )
    ],
    fluid=True
)

if __name__ == "__main__":
    app.run_server(debug=True)
```

### 2. Explanation
We read two datasets (`sales.csv` and `reviews.csv`) and compute multiple KPIs for each. Using Dash Bootstrap Components, summaries are displayed in a responsive two-column layout, and beneath them, two static charts are positioned side-by-side to visually supplement the data.

### 3. Expected Output
A responsive dashboard:
- Top: 
  - Left column: *Total Revenue, Units Sold, Average Unit Price*
  - Right column: *Average Rating, Total Reviews, Verified Purchase %*
- Bottom:
  - Left chart: Sales trend (`sales_trend.png`)
  - Right chart: Average ratings per genre (`avg_ratings_genre.png`)

### 4. Key Takeaway
Organizing related metrics and visuals in structured multi-section layouts improves readability and makes dashboards more professional.

---

**Alternative Approaches**  
- Replace static images with interactive Plotly graphs using `dcc.Graph`.  
- Store KPIs in Bootstrap cards or badge components for visual emphasis.

**Common Mistakes**  
1. Forgetting to parse dates when working with time-series sales data.  
2. Division by zero errors when calculating percentages (check total count > 0).  
3. Large images not resized properly—can break layout responsiveness.

---
```