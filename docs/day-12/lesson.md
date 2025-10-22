```markdown
# Day 12: Data Storytelling – Choosing the Right Chart
**Week:** 2  
**Difficulty:** Intermediate  
**Duration:** 3-5 minutes  

---

## 1. Introduction
Imagine you’re working at Page Turner Analytics and your manager asks: *“Can you show me how our sales trends compare between genres over time, and whether higher-priced books get better ratings?”*  
In our previous sessions, we explored violin plots, interactive charts with Plotly Express, and even built multi-trace subplots. Today, we’ll take that knowledge and focus on **chart selection**—picking the right visualization for the question you’re answering. You’ll learn how to create compelling visual narratives, use annotations for emphasis, and combine multiple charts into one cohesive story.

---

## 2. Core Content

### 2.1 Chart Selection – Matching Visualization to Question
Different questions call for different chart types:
- **Comparisons:** Bar charts or grouped bar charts are ideal for comparing categories (e.g., sales by genre).
- **Trends over time:** Line charts show changes clearly (e.g., monthly sales totals).
- **Distributions:** Violin plots, box plots, and histograms reveal how data is spread (e.g., ratings spread for each genre).
- **Relationships:** Scatter plots and bubble charts visualize correlations (e.g., price vs. rating).

**Bookstore analogy:** Think of chart types like shelves in a bookstore. Fiction belongs in one place; nonfiction elsewhere. Misplacing a chart is like filing a cookbook in the romance section—it confuses the reader.

---

### 2.2 Visual Storytelling – Turning Data into a Narrative
Raw charts show numbers; **visual stories** explain why they matter.  
Storytelling steps:
1. **Hook:** Start with a question or observation (e.g., “Do higher-rated books sell more copies?”).
2. **Evidence:** Present charts that answer the question directly.
3. **Flow:** Arrange charts so each builds on the last—like chapters in a book.
4. **Highlight:** Use color, annotations, and emphasis markers to draw the eye to key data points.

When done well, visual storytelling transforms analytics from *interesting* to *actionable*.

---

### 2.3 Combining Multiple Visualizations for Insights
Sometimes one chart isn't enough. For instance, you might use:
- A line chart for monthly sales trends  
**plus**  
- A bar chart for genre performance in the same time frame

Plotly subplots and multiple traces let you present these together. This aligns with our earlier lessons on subplots and layout customization—allowing you to put related insights side-by-side.

---

## 3. Code Examples

### Example 1: Genre Sales Over Time
```python
import pandas as pd
import plotly.express as px

# Load datasets
sales = pd.read_csv('sales.csv')
books = pd.read_csv('books.csv')

# Merge to get genre info for each sale
sales_books = sales.merge(books, on='book_id')

# Aggregate monthly sales by genre
sales_books['month'] = pd.to_datetime(sales_books['date']).dt.to_period('M')
monthly_genre_sales = sales_books.groupby(['month', 'genre'])['total_amount'].sum().reset_index()

# Line chart: monthly sales per genre
fig = px.line(
    monthly_genre_sales,
    x='month', y='total_amount',
    color='genre',
    title="Monthly Sales by Genre"
)
fig.show()

# Expected Output: Interactive line chart showing genre trends over months.
```

---

### Example 2: Price vs Rating – Annotating Key Outliers
```python
reviews = pd.read_csv('reviews.csv')
price_rating = books.merge(reviews, on='book_id')

# Average rating per book
avg_ratings = price_rating.groupby(['book_id', 'title', 'price'])['rating'].mean().reset_index()

# Scatter plot for price vs rating
fig = px.scatter(
    avg_ratings,
    x='price', y='rating',
    hover_data=['title'],
    title="Price vs Average Rating"
)

# Annotate highest-rated expensive book
max_point = avg_ratings.loc[avg_ratings['rating'].idxmax()]
fig.add_annotation(
    x=max_point['price'], y=max_point['rating'],
    text=f"Top-rated: {max_point['title']}",
    showarrow=True, arrowhead=2
)
fig.show()

# Expected Output: Scatter plot with one annotated point highlighting a standout performer.
```

---

### Example 3: Combining Multiple Views with Subplots
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Bar chart: sales by genre
genre_sales = sales_books.groupby('genre')['total_amount'].sum().reset_index()
bar_trace = go.Bar(x=genre_sales['genre'], y=genre_sales['total_amount'], name='Total Sales')

# Histogram: ratings distribution
rating_counts = reviews['rating'].value_counts().sort_index()
hist_trace = go.Bar(x=rating_counts.index, y=rating_counts.values, name='Rating Counts')

# Create subplot figure
fig = make_subplots(rows=1, cols=2, subplot_titles=("Sales by Genre", "Rating Distribution"))
fig.add_trace(bar_trace, row=1, col=1)
fig.add_trace(hist_trace, row=1, col=2)

fig.update_layout(title="Sales and Ratings Overview")
fig.show()

# Expected Output: Two charts side-by-side: genre sales and rating distribution.
```

---

## 4. Common Pitfalls
1. **Choosing the wrong chart type** – Avoid using line charts for categorical comparisons; instead, use bar charts.
2. **Overloading the chart** – Too many categories or colors can confuse viewers. Limit to key genres or time periods.
3. **Ignoring context** – Sales spikes may be seasonal; without annotation, viewers might misinterpret them.

---

## 5. Practice Checkpoint
✅ I can choose a chart type that fits the analysis question.  
✅ I can enhance a chart with annotations to highlight important data points.  
✅ I can combine multiple charts into a cohesive visual story.

---
```