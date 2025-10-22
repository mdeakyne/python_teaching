## 📝 Day 12 Hands-On Exercises — Data Storytelling: Choosing the Right Chart

---

### **Task 1 — EASY (5 min)**
**Goal:** Match the right chart type to a simple analysis question.  
**Scenario:** “Show how the average ratings differ between genres.”

**Instructions:**
1. Load `books.csv` and `reviews.csv`.
2. Merge the datasets on `book_id`.
3. Group by `genre` and calculate the average rating.
4. Create a **bar chart** with Plotly Express showing `genre` vs. `average_rating`.

**Skeleton Code:**
```python
import pandas as pd
import plotly.express as px

# Step 1: Load datasets
books = pd.read_csv('data/books.csv')
reviews = pd.read_csv('data/reviews.csv')

# Step 2: Merge datasets
merged_df = # TODO: merge on 'book_id'

# Step 3: Group and aggregate
genre_avg_rating = # TODO: groupby genre and compute mean rating

# Step 4: Create bar chart
fig = # TODO: use px.bar
fig.show()
```

**Expected Output:**  
A color-coded bar chart showing each genre’s average rating, sorted by rating value.


---

### **Task 2 — MEDIUM (7 min)**
**Goal:** Explore trends over time with an appropriate chart.  
**Scenario:** “Visualize monthly sales trends for *Fiction* vs. *Non-fiction*.”

**Instructions:**
1. Load `books.csv` and `sales.csv`.
2. Merge datasets to get genre info for each sale.
3. Convert `date` to a datetime and create a `month` column.
4. Group by `month` & `genre`, summing `total_amount`.
5. Create a **line chart** with Plotly Express showing sales over months, distinguished by genre.

**Skeleton Code:**
```python
import pandas as pd
import plotly.express as px

# Step 1: Load datasets
books = pd.read_csv('data/books.csv')
sales = pd.read_csv('data/sales.csv')

# Step 2: Merge to get genre info
sales_books_df = # TODO: merge on 'book_id'

# Step 3: Convert date and extract month
sales_books_df['date'] = # TODO: pd.to_datetime
sales_books_df['month'] = # TODO: sales_books_df['date'].dt.to_period('M')

# Step 4: Aggregate monthly sales per genre
monthly_sales = # TODO: groupby month & genre, sum total_amount

# Step 5: Create line chart
fig = # TODO: use px.line
fig.show()
```

**Expected Output:**  
An interactive line chart with two lines (Fiction and Non-fiction) showing sales totals by month, allowing trend comparison.

---

### **Task 3 — MEDIUM-HARD (10 min)**
**Goal:** Combine multiple visualizations for deeper insight.  
**Scenario:** “Is there a relationship between book price and ratings, and how do sales trends vary by high vs. low-rated books?”

**Instructions:**
1. Load and merge `books.csv`, `reviews.csv`, and `sales.csv`.
2. Compute each book’s average rating & total sales over time.
3. Categorize books as **High Rated** (rating ≥ 4) or **Low Rated**.
4. Create:
   - **Scatter plot** of `price` vs. `average_rating` (color by genre).
   - **Line chart** showing monthly sales trends for High vs. Low Rated books.
5. Display both charts in a Dash app layout (two columns).

**Skeleton Code:**
```python
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Step 1: Load datasets
books = pd.read_csv('data/books.csv')
reviews = pd.read_csv('data/reviews.csv')
sales = pd.read_csv('data/sales.csv')

# Step 2: Merge & aggregate ratings
merged_ratings = # TODO: merge books & reviews, groupby book_id for avg rating

# Step 3: Merge sales data
merged_sales = # TODO: merge with sales, group and sum monthly totals

# Step 4: Categorize high vs low rated
merged_ratings['rating_category'] = # TODO: apply condition

# Step 5: Create scatter plot
scatter_fig = # TODO: px.scatter(price vs avg_rating, color=genre)

# Step 6: Create line chart
line_fig = # TODO: px.line(monthly sales, color=rating_category)

# Step 7: Dash layout
app = Dash(__name__)
app.layout = html.Div([
    html.Div([dcc.Graph(figure=scatter_fig)], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(figure=line_fig)], style={'width': '48%', 'display': 'inline-block'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

**Expected Output:**  
A Dash dashboard with:
- Left: Scatter plot showing any correlation between price and ratings, genres in different colors.
- Right: Line chart showing distinct trends in monthly sales for High vs. Low Rated books.

---