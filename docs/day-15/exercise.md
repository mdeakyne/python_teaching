## Task 1 – Easy: Your First Dash App Layout  
**Goal:** Build a basic Dash app that displays a static heading and one image of a chart (use any existing PNG chart from your earlier Matplotlib work).  

**Skeleton Code:**  
```python
import dash
from dash import html
import dash_bootstrap_components as dbc

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container([
    html.H1("Page Turner Analytics – Sales Overview"),
    html.Img(src="assets/sales_chart.png", style={"width": "60%"})
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

**Instructions:**  
1. Save one of your Matplotlib-generated charts into an `assets` folder (e.g., `sales_chart.png`).  
2. Replace the heading text with something relevant.  
3. Run the app and verify it loads in the browser.  

**Success Criteria:**  
- Web page shows a heading and your chart image.  
- No interactive elements yet—just static content.  

**Expected Output:**  
A simple web page with a large heading at the top and a centered chart image below it.  


---

## Task 2 – Medium: Display Static Chart with Dataset Context  
**Goal:** Extend your app to include a short data summary from `books.csv` and display another static chart below it.  

**Skeleton Code:**  
```python
import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

# Load dataset
books = pd.read_csv("data/books.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Prepare summary info
unique_authors = books['author_name'].nunique()
total_books = books.shape[0]

app.layout = dbc.Container([
    html.H1("Page Turner Analytics – Catalog Overview"),
    html.P(f"Total Books: {total_books} | Total Authors: {unique_authors}"),
    html.Img(src="assets/genre_distribution.png", style={"width": "50%"})
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

**Instructions:**  
1. Compute at least two summary metrics (e.g., number of books, average price, unique genres).  
2. Replace the image with a genre distribution chart from earlier work.  
3. Arrange text above the chart neatly.  

**Expected Output:**  
Heading, a small paragraph summarizing dataset stats, and a static chart showing the distribution of books by genre. Text and chart are vertically stacked.  


---

## Task 3 – Medium-Hard: Multi-Section Layout with Sales & Reviews  
**Goal:** Build a multi-section layout that displays:  
- Sales summary using `sales.csv`  
- Reviews summary using `reviews.csv`  
- Two static charts (sales trend and average ratings per genre)  

**Skeleton Code:**  
```python
import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

# Load datasets
sales = pd.read_csv("data/sales.csv", parse_dates=["date"])
reviews = pd.read_csv("data/reviews.csv")

# Prepare summaries
total_sales_amount = sales['total_amount'].sum()
total_units_sold = sales['quantity'].sum()
avg_rating = reviews['rating'].mean()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Page Turner Analytics – Quarterly Report"),
    
    dbc.Row([
        dbc.Col([
            html.H3("Sales Summary"),
            html.P(f"Total Revenue: ${total_sales_amount:,.2f}"),
            html.P(f"Total Units Sold: {total_units_sold}")
        ], width=6),
        
        dbc.Col([
            html.H3("Reviews Summary"),
            html.P(f"Average Rating: {avg_rating:.2f} / 5")
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col(html.Img(src="assets/sales_trend.png", style={"width": "100%"}), width=6),
        dbc.Col(html.Img(src="assets/avg_ratings_genre.png", style={"width": "100%"}), width=6)
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

**Instructions:**  
1. Calculate and display at least three relevant KPIs from sales and reviews datasets.  
2. Ensure each chart’s image file is placed in the `assets` directory.  
3. Use `dbc.Row`/`dbc.Col` to arrange the two charts side-by-side below the summaries.  

**Expected Output:**  
Responsive web layout: top section contains two summaries (Sales, Reviews) side-by-side; bottom section contains two static charts side-by-side. Metrics update based on actual CSV contents.  