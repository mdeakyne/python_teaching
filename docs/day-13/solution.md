## 📝 Day 13 Solutions: Styling & Theming Visualizations

---

### **Task 1 — Easy (5 min)**

#### 1. Complete Working Code
```python
import pandas as pd
import plotly.express as px

# Load data from books.csv
books_df = pd.read_csv("books.csv")

# Aggregate count of books per genre
genre_counts = books_df.groupby("genre")["book_id"].count().reset_index()
genre_counts.rename(columns={"book_id": "book_count"}, inplace=True)

# Define a consistent color palette (pastel tones)
pastel_palette = ["#AEC6CF", "#FFD1DC", "#FFFACD", "#B0E0E6", "#E6E6FA", "#F5DEB3"]

# Create bar chart with consistent colors applied
fig = px.bar(
    genre_counts,
    x="genre",
    y="book_count",
    title="Books per Genre",
    color_discrete_sequence=pastel_palette
)

# Display the chart
fig.show()
```

#### 2. Explanation
We read `books.csv`, group by genre to count the books, and then choose a pastel palette to apply across all bars using `color_discrete_sequence`. This ensures a visually cohesive style instead of relying on random default colors.

#### 3. Expected Output
A bar chart where all bars share the same coordinated pastel tone sequence, with genres labeled along the X-axis and counts on the Y-axis.

#### 4. Key Takeaway
Consistent color schemes enhance readability and create a professional visual identity.

**Alternative Approaches:**
- Use built-in Plotly qualitative color scales like `px.colors.qualitative.Pastel`.
- Apply a single solid color by passing `[color_code]`.

**Common Mistakes:**
1. Forgetting to rename aggregates, causing unclear axis labels.
2. Not setting `color_discrete_sequence`, resulting in default mismatched colors.
3. Using too many colors for a small number of categories, creating visual clutter.

---

### **Task 2 — Medium (7 min)**

#### 1. Complete Working Code
```python
import pandas as pd
import plotly.express as px

# Load datasets
sales_df = pd.read_csv("sales.csv")
books_df = pd.read_csv("books.csv")

# Format date column
sales_df["date"] = pd.to_datetime(sales_df["date"])

# Chart 1: Aggregate monthly sales
sales_df["month"] = sales_df["date"].dt.to_period("M").astype(str)
monthly_sales = sales_df.groupby("month")["total_amount"].sum().reset_index()

# Chart 2: Aggregate quantity sold per genre
sales_books = sales_df.merge(books_df, on="book_id")
genre_quantity = sales_books.groupby("genre")["quantity"].sum().reset_index()

# Choose professional template
template_style = "plotly_white"

# Create line chart for monthly sales
fig1 = px.line(
    monthly_sales,
    x="month",
    y="total_amount",
    title="Monthly Sales",
    markers=True,
    template=template_style
)

# Create bar chart for quantity per genre
fig2 = px.bar(
    genre_quantity,
    x="genre",
    y="quantity",
    title="Quantity Sold per Genre",
    template=template_style
)

# Display charts
fig1.show()
fig2.show()
```

#### 2. Explanation
We extract months from sales dates, aggregate total amounts for the line chart, and group sales quantities per genre after merging with book data for the bar chart. The `plotly_white` template ensures consistent styling for both charts.

#### 3. Expected Output
Two charts with matching font, background, and grid appearance — a monthly sales line graph and a genre quantity bar chart.

#### 4. Key Takeaway
Reusing a single template across charts creates a consistent visual identity for reports.

**Alternative Approaches:**
- Try another template such as `ggplot2` or `seaborn` for predefined thematic styles.
- Customize template elements via `fig.update_layout()`.

**Common Mistakes:**
1. Not converting the date column to datetime, leading to incorrect grouping.
2. Applying different templates unintentionally, breaking visual consistency.
3. Misaligning genres due to missing join with `books.csv`.

---

### **Task 3 — Medium-Hard (10 min)**

#### 1. Complete Working Code
```python
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Load datasets
sales_df = pd.read_csv("sales.csv")
books_df = pd.read_csv("books.csv")
reviews_df = pd.read_csv("reviews.csv")

# Convert dates to datetime and extract months
sales_df["date"] = pd.to_datetime(sales_df["date"])
reviews_df["review_date"] = pd.to_datetime(reviews_df["review_date"])
sales_df["month"] = sales_df["date"].dt.to_period("M").astype(str)
reviews_df["month"] = reviews_df["review_date"].dt.to_period("M").astype(str)

# Monthly average review rating
monthly_ratings = reviews_df.groupby("month")["rating"].mean().reset_index()
monthly_ratings.rename(columns={"rating": "avg_rating"}, inplace=True)

# Top 5 genres by total sales revenue
sales_books = sales_df.merge(books_df, on="book_id")
genre_revenue = (
    sales_books.groupby("genre")["total_amount"]
    .sum()
    .reset_index()
    .sort_values("total_amount", ascending=False)
    .head(5)
)

# Define brand colors and template
color_sequence = ["#003f5c", "#58508d", "#bc5090", "#ff6361", "#ffa600"]
template_style = "plotly_white"
branding_color = "#003f5c"

# Create monthly ratings chart
fig1 = px.line(
    monthly_ratings,
    x="month",
    y="avg_rating",
    title="Monthly Average Review Rating",
    markers=True,
    color_discrete_sequence=color_sequence,
    template=template_style
)

# Create top genres revenue chart
fig2 = px.bar(
    genre_revenue,
    x="genre",
    y="total_amount",
    title="Top 5 Genres by Revenue",
    color_discrete_sequence=color_sequence,
    template=template_style
)

# Build Dash app layout
app = Dash(__name__)
app.layout = html.Div([
    html.H1(
        "Page Turner Analytics Dashboard",
        style={"color": branding_color, "textAlign": "center"}
    ),
    html.Div([
        dcc.Graph(figure=fig1, style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(figure=fig2, style={"width": "48%", "display": "inline-block"}),
    ], style={"textAlign": "center"})
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

#### 2. Explanation
We preprocess both sales and review data to get monthly aggregates, then merge sales with book genres to determine top revenue genres. Both charts use the same color palette and template, and are placed side-by-side in a Dash app with a branded title.

#### 3. Expected Output
A Dash web app showing two side-by-side charts: monthly average ratings (line chart) and top 5 genres by revenue (bar chart), both sharing the same theme and color identity.

#### 4. Key Takeaway
Consistent theming across dashboards improves brand recognition and user experience.

**Alternative Approaches:**
- Use Dash Bootstrap Components for more polished layout styling.
- Implement responsiveness with CSS Flexbox or Grid for mobile compatibility.

**Common Mistakes:**
1. Forgetting to limit to top 5 genres, resulting in clutter.
2. Using mismatched color palettes across charts.
3. Not converting dates, which breaks monthly grouping.

---