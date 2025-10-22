## 📝 Day 13 Hands-On Exercises: Styling & Theming Visualizations

---

### **Task 1 — Easy (5 min)**
**Goal:** Apply a consistent color scheme to a single visualization.  
**Concept Focus:** Setting colors for a plot in Plotly.  

**Instructions:**  
Using `books.csv`, create a bar chart showing the number of books per genre. Apply a consistent color scheme of your choice (e.g., pastel tones, corporate blues).  

**Skeleton Code:**
```python
import pandas as pd
import plotly.express as px

# Load data
books_df = pd.read_csv("books.csv")

# Aggregate data
genre_counts = books_df.groupby("genre")["book_id"].count().reset_index()

# Create bar chart with consistent colors
fig = px.bar(
    genre_counts,
    x="genre",
    y="book_id",
    title="Books per Genre",
    # TODO: set a custom color sequence here
)

# Show figure
fig.show()
```

**Success Criteria:**  
You have a plot with **your chosen color palette** applied consistently to all bars.

**Expected Output:**  
A clean bar chart with each genre in the same selected color scheme, using consistent tones rather than default random colors.

---

### **Task 2 — Medium (7 min)**
**Goal:** Apply a professional template across multiple charts.  
**Concept Focus:** Using Plotly templates (`plotly_white`, `ggplot2`, etc.).  

**Instructions:**  
Using `sales.csv`, create two separate visualizations:
1. Line chart of total sales per month.
2. Bar chart of quantity sold per genre (join with `books.csv`).

Apply the same professional theme/template to both charts for a consistent visual identity.

**Skeleton Code:**
```python
# Import modules
import pandas as pd
import plotly.express as px

# Load data
sales_df = pd.read_csv("sales.csv")
books_df = pd.read_csv("books.csv")

# TODO: Aggregate sales per month for chart 1
# TODO: Aggregate quantity sold per genre for chart 2

# Create line chart
fig1 = px.line(
    ...,  # monthly sales data
    x="month",
    y="total_amount",
    title="Monthly Sales",
    template="..."  # consistent template
)

# Create bar chart
fig2 = px.bar(
    ...,  # genre sales data
    x="genre",
    y="quantity",
    title="Quantity Sold per Genre",
    template="..."  # same template as above
)

fig1.show()
fig2.show()
```

**Expected Output:**  
Two visualizations with **matching fonts, background colors, and grid styles**, demonstrating theme consistency across different chart types.

---

### **Task 3 — Medium-Hard (10 min)**
**Goal:** Prepare a mini dashboard with consistent theme, annotation, and layout.  
**Concept Focus:** Integrating styling/theme with layout in Dash.  

**Instructions:**  
Create a Dash app that shows:
- Chart 1: Monthly average review rating (from `reviews.csv`).
- Chart 2: Top 5 genres by total sales revenue (join `sales.csv` with `books.csv`).

Apply:
- **Same color scheme** for both charts.
- **Same template/theme** for both charts.
- Add a page title styled with the same branding colors.
- Arrange charts side-by-side.

**Skeleton Code:**
```python
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Load datasets
sales_df = pd.read_csv("sales.csv")
books_df = pd.read_csv("books.csv")
reviews_df = pd.read_csv("reviews.csv")

# TODO: Create monthly avg rating data
# TODO: Create top 5 genres sales revenue data

# Create charts with consistent theme + colors
color_sequence = [...]  # define your brand palette
template_style = "..."  # choose your template

fig1 = px.line(
    ...,  # monthly review avg data
    x="month",
    y="avg_rating",
    title="Monthly Average Review Rating",
    color_discrete_sequence=color_sequence,
    template=template_style
)

fig2 = px.bar(
    ...,  # top genres sales revenue data
    x="genre",
    y="total_amount",
    title="Top 5 Genres by Revenue",
    color_discrete_sequence=color_sequence,
    template=template_style
)

# Build Dash layout
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Page Turner Analytics Dashboard", style={"color": "#..."}),  # branding color
    html.Div([
        dcc.Graph(figure=fig1, style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(figure=fig2, style={"width": "48%", "display": "inline-block"}),
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
```

**Expected Output:**  
A mini dashboard with two consistently themed charts side-by-side, unified by color palette, template style, and branded title, showing both ratings and sales data in a publication-ready format.