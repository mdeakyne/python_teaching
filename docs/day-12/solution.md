## 📝 Day 12 Solutions — Data Storytelling: Choosing the Right Chart

---

### **Task 1 — EASY (5 min)**

#### **Complete Working Code**
```python
import pandas as pd
import plotly.express as px

# Step 1: Load datasets
books = pd.read_csv('data/books.csv')
reviews = pd.read_csv('data/reviews.csv')

# Step 2: Merge datasets on 'book_id'
merged_df = pd.merge(books, reviews, on='book_id', how='inner')

# Step 3: Group by genre and compute mean rating
genre_avg_rating = (
    merged_df.groupby('genre', as_index=False)['rating']
             .mean()
             .rename(columns={'rating': 'average_rating'})
)

# Sort by average rating for better visual clarity
genre_avg_rating = genre_avg_rating.sort_values(by='average_rating', ascending=False)

# Step 4: Create bar chart
fig = px.bar(
    genre_avg_rating,
    x='genre',
    y='average_rating',
    color='average_rating',
    title='Average Ratings by Genre',
    labels={'average_rating': 'Average Rating', 'genre': 'Genre'},
    color_continuous_scale='Blues'
)
fig.show()
```

#### **Explanation**
We join `books.csv` and `reviews.csv` by `book_id` to pair each book with its ratings. Then, we group by `genre` to compute average ratings per genre and create a bar chart to visualize the differences in a clear and sorted manner.

#### **Expected Output**
A vertical bar chart where each bar represents a genre, with height equal to the average rating, and colored by rating value.

#### **Key Takeaway**
Bar charts are ideal for comparing averages across categorical groups like genres.

#### **Alternative Approaches**
- Use **seaborn** or **matplotlib** instead of Plotly for static charts.
- Incorporate number of reviews to weigh averages.

#### **Common Mistakes**
1. Forgetting to convert ratings to numeric types before averaging.
2. Not renaming aggregated columns, causing confusion in Plotly.
3. Not sorting results, making interpretation harder.

---

### **Task 2 — MEDIUM (7 min)**

#### **Complete Working Code**
```python
import pandas as pd
import plotly.express as px

# Step 1: Load datasets
books = pd.read_csv('data/books.csv')
sales = pd.read_csv('data/sales.csv')

# Step 2: Merge to get genre info
sales_books_df = pd.merge(sales, books, on='book_id', how='inner')

# Step 3: Convert date to datetime and extract month period
sales_books_df['date'] = pd.to_datetime(sales_books_df['date'])
sales_books_df['month'] = sales_books_df['date'].dt.to_period('M').dt.to_timestamp()

# Step 4: Aggregate monthly sales per genre
monthly_sales = (
    sales_books_df.groupby(['month', 'genre'], as_index=False)['total_amount']
                  .sum()
)

# Step 5: Create line chart
fig = px.line(
    monthly_sales,
    x='month',
    y='total_amount',
    color='genre',
    title='Monthly Sales Trends: Fiction vs. Non-fiction',
    labels={'total_amount': 'Total Sales Amount', 'month': 'Month'}
)
fig.show()
```

#### **Explanation**
We merge sales with book metadata to attach genres and convert the raw `date` into a monthly period. Summed sales per genre per month are then plotted using a line chart to compare trends.

#### **Expected Output**
Interactive line chart with two colored lines (Fiction and Non-fiction) showing total sales amounts over time.

#### **Key Takeaway**
Line charts effectively reveal trends over time and make genre comparisons clear.

#### **Alternative Approaches**
- Plot stacked area charts to see cumulative sales contribution.
- Use a rolling average to smooth fluctuations.

#### **Common Mistakes**
1. Not converting date strings to datetime objects before extracting months.
2. Forgetting to aggregate sales before plotting, resulting in noisy charts.
3. Using `groupby` incorrectly and losing column names.

---

### **Task 3 — MEDIUM-HARD (10 min)**

#### **Complete Working Code**
```python
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Step 1: Load datasets
books = pd.read_csv('data/books.csv')
reviews = pd.read_csv('data/reviews.csv')
sales = pd.read_csv('data/sales.csv')

# Step 2: Merge books & reviews, compute average rating per book
books_reviews = pd.merge(books, reviews, on='book_id', how='inner')
avg_ratings = (
    books_reviews.groupby(['book_id', 'title', 'genre', 'price'], as_index=False)['rating']
                 .mean()
                 .rename(columns={'rating': 'average_rating'})
)

# Step 3: Merge sales data and process month
sales_data = pd.merge(sales, avg_ratings, on='book_id', how='inner')
sales_data['date'] = pd.to_datetime(sales_data['date'])
sales_data['month'] = sales_data['date'].dt.to_period('M').dt.to_timestamp()

# Step 4: Categorize books (High Rated vs Low Rated)
sales_data['rating_category'] = sales_data['average_rating'].apply(
    lambda x: 'High Rated' if x >= 4 else 'Low Rated'
)

# Step 5: Create scatter plot (Price vs Avg Rating, colored by Genre)
scatter_fig = px.scatter(
    avg_ratings,
    x='price',
    y='average_rating',
    color='genre',
    title='Book Price vs. Average Rating',
    labels={'price': 'Price (USD)', 'average_rating': 'Average Rating'},
    hover_data=['title']
)

# Step 6: Create monthly sales data aggregated by rating category
monthly_sales_category = (
    sales_data.groupby(['month', 'rating_category'], as_index=False)['total_amount']
              .sum()
)

line_fig = px.line(
    monthly_sales_category,
    x='month',
    y='total_amount',
    color='rating_category',
    title='Monthly Sales Trends: High vs Low Rated Books',
    labels={'total_amount': 'Total Sales Amount', 'month': 'Month'}
)

# Step 7: Dash layout with two-column display
app = Dash(__name__)
app.layout = html.Div([
    html.Div([dcc.Graph(figure=scatter_fig)], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(figure=line_fig)], style={'width': '48%', 'display': 'inline-block'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

#### **Explanation**
We calculate per-book average ratings and merge them with sales data, categorizing books into “High Rated” and “Low Rated”. We then create two visuals: a scatter plot to explore the relationship between price and rating, and a line chart to observe monthly sales trends between the two categories, integrated into a simple Dash dashboard.

#### **Expected Output**
A web app with:
- **Left:** Scatter plot with price vs rating, colored by genre.
- **Right:** Line chart showing monthly sales trends for high vs low-rated books.

#### **Key Takeaway**
Combining multiple charts in a dashboard enables both correlation analysis and trend monitoring in context.

#### **Alternative Approaches**
- Use Plotly’s `make_subplots` for a single figure layout without Dash.
- Add filters in the Dash app using callbacks for interactive genre selection.

#### **Common Mistakes**
1. Not grouping ratings before merging with sales, leading to duplicate rows.
2. Failing to convert `date` before extracting month results in grouping errors.
3. In Dash, forgetting to serve the app via `app.run_server()` when testing locally.

---