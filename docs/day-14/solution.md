## DAY 14 – Mini-Project: Complete EDA Dashboard (Static) – Solutions

---

### Task 1 – Total Sales per Genre

#### 1. Complete Working Code
```python
import pandas as pd
import plotly.express as px

# Load datasets
sales_df = pd.read_csv('sales.csv')
books_df = pd.read_csv('books.csv')

# Merge sales with book details to include genre
merged_df = sales_df.merge(books_df, on='book_id')

# Group by genre and sum total_amount to get total revenue per genre
genre_sales = merged_df.groupby('genre', as_index=False)['total_amount'].sum()

# Create static bar chart showing revenue by genre
fig = px.bar(
    genre_sales,
    x='genre',
    y='total_amount',
    title='Total Revenue by Genre',
    labels={'total_amount': 'Revenue', 'genre': 'Genre'},
    color='genre'  # for clear category distinction
)

# Display the chart
fig.show()
```

#### 2. Explanation
We merge sales and books to connect each purchase to its genre. Grouping by genre and summing `total_amount` gives revenue totals per category, which we visualize in a bar chart to show which genres sell best.

#### 3. Expected Output
A static bar chart with genre labels along the x-axis and revenue values on the y-axis. Bars are colored per genre, with the highest revenue genre clearly standing out.

#### 4. Key Takeaway
Merging datasets and grouping by categorical variables allows quick summarization of sales performance.

**Alternative Approaches**
- Use `plotly.graph_objects` for finer control of styling and layout.
- Sort genres by revenue before plotting for better visual interpretation.

**Common Mistakes**
1. Forgetting to merge before grouping, leading to missing genre information.
2. Summing `quantity` instead of `total_amount` when the task requires revenue.
3. Using `interactive` figures or dashboards when a static chart is requested.

---

### Task 2 – Revenue & Ratings Side-by-Side

#### 1. Complete Working Code
```python
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load datasets
sales_df = pd.read_csv('sales.csv')
books_df = pd.read_csv('books.csv')
reviews_df = pd.read_csv('reviews.csv')

# Revenue by genre
sales_merged = sales_df.merge(books_df, on='book_id')
genre_revenue = sales_merged.groupby('genre', as_index=False)['total_amount'].sum()

# Average rating by genre
reviews_merged = reviews_df.merge(books_df, on='book_id')
avg_rating = reviews_merged.groupby('genre', as_index=False)['rating'].mean()

# Create subplot layout: 1 row, 2 columns
fig = make_subplots(rows=1, cols=2, subplot_titles=['Revenue by Genre', 'Average Rating by Genre'])

# Add revenue bar chart
fig.add_trace(
    go.Bar(x=genre_revenue['genre'], y=genre_revenue['total_amount'], marker_color='skyblue'),
    row=1, col=1
)

# Add average rating bar chart
fig.add_trace(
    go.Bar(x=avg_rating['genre'], y=avg_rating['rating'], marker_color='orange'),
    row=1, col=2
)

# Update layout
fig.update_layout(
    title_text='Sales & Ratings Overview',
    showlegend=False,
    xaxis_title='Genre',
    yaxis_title='Revenue'
)

fig.show()
```

#### 2. Explanation
We compute two metrics—total revenue and average rating—both grouped by genre. Then we arrange them as two static panels using `make_subplots`, enabling visual comparison between financial performance and customer sentiment.

#### 3. Expected Output
A dashboard with two vertical bar charts: left shows revenue per genre, right shows average ratings. Genres align between charts for side-by-side analysis.

#### 4. Key Takeaway
Subplots help combine related metrics into a single visual, enabling direct comparisons.

**Alternative Approaches**
- Use `px.bar` twice and concatenate images for static reporting.
- Normalize scales if revenue and ratings variation differs greatly.

**Common Mistakes**
1. Failing to use the same genre order in both charts, making comparison harder.
2. Averaging ratings without ensuring they're numeric (e.g., converting strings to floats).
3. Creating subplots but forgetting to specify the correct `row` and `col` parameters in `.add_trace()`.

---

### Task 3 – Complete 3-Panel Static Dashboard

#### 1. Complete Working Code
```python
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load datasets
sales_df = pd.read_csv('sales.csv')
books_df = pd.read_csv('books.csv')
authors_df = pd.read_csv('authors.csv')
reviews_df = pd.read_csv('reviews.csv')

# 1. Sales Trends (monthly revenue)
sales_df['month'] = pd.to_datetime(sales_df['date']).dt.to_period('M').astype(str)
monthly_revenue = sales_df.groupby('month', as_index=False)['total_amount'].sum().sort_values('month')

# 2. Top Authors by Revenue
merged_authors = sales_df.merge(books_df, on='book_id').merge(authors_df, on='author_id')
author_revenue = merged_authors.groupby('full_name', as_index=False)['total_amount'].sum()
top_authors = author_revenue.sort_values('total_amount', ascending=False).head(5)

# 3. Ratings Distribution
ratings = reviews_df['rating']

# Create 3-panel subplot
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=['Monthly Revenue', 'Top Authors by Revenue', 'Ratings Distribution']
)

# Add line chart for monthly revenue
fig.add_trace(
    go.Scatter(x=monthly_revenue['month'], y=monthly_revenue['total_amount'],
               mode='lines+markers', marker_color='green'),
    row=1, col=1
)

# Add horizontal bar chart for top authors
fig.add_trace(
    go.Bar(
        x=top_authors['total_amount'],
        y=top_authors['full_name'],
        orientation='h',
        marker_color='purple'
    ),
    row=1, col=2
)

# Add histogram for ratings
fig.add_trace(
    go.Histogram(x=ratings, nbinsx=5, marker_color='gold'),
    row=1, col=3
)

# Layout settings
fig.update_layout(
    title_text='Complete EDA Dashboard – Page Turner Analytics',
    showlegend=False,
    height=500,
    width=1400
)

fig.show()
```

#### 2. Explanation
We separately prepare each panel’s data: monthly revenue for trends, top authors’ revenues, and ratings distribution. `make_subplots` arranges them in one row with three columns, creating a concise, static view of sales dynamics, bestselling authors, and customer ratings.

#### 3. Expected Output
A single wide dashboard:  
- **Left panel:** Line chart showing monthly revenue trends.  
- **Middle panel:** Horizontal bars of top 5 authors by revenue.  
- **Right panel:** Histogram showing ratings distribution peaks.

#### 4. Key Takeaway
Complex dashboards can be built in Plotly by preparing separate data summaries and combining them into multi-panel layouts for holistic reporting.

**Alternative Approaches**
- Use `matplotlib` with `plt.subplots()` for static PNG outputs.
- Build in Dash for interactive dashboarding if interactivity is required later.

**Common Mistakes**
1. Not converting dates to a monthly period before grouping, causing overly granular data.
2. Forgetting to sort top authors before selecting the top 5.
3. Using too many bins in the ratings histogram, making patterns harder to see.

---