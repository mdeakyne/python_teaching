```markdown
## Task 1 – Interactive Scatter Plot (EASY, ~5 min)

### 1. Complete Working Code
```python
import pandas as pd
import plotly.express as px

# Load datasets
books = pd.read_csv('books.csv')
sales = pd.read_csv('sales.csv')

# Aggregate total quantity per book
sales_agg = sales.groupby('book_id')['quantity'].sum().reset_index()

# Merge aggregated sales with books data
df = pd.merge(books, sales_agg, on='book_id')

# Create interactive scatter plot
fig = px.scatter(
    df,
    x='price',               # book price
    y='quantity',            # total quantity sold
    hover_data=['title', 'genre']  # show title & genre when hovering
)

# Display plot
fig.show()
```

### 2. Explanation
We grouped sales by `book_id` to get the total quantity sold per book, merged that result with the `books` dataset, and plotted the price vs quantity using `plotly.express.scatter`. Hover tooltips were configured to display book titles and genres.

### 3. Expected Output
An interactive scatter plot, with each point representing a book positioned by its price and total sales quantity. Hovering reveals the title and genre.

### 4. Key Takeaway
Merging aggregated statistics with descriptive data allows interactive visualizations to provide both numeric and contextual information.

---

**Alternative Approaches**
- Use `DataFrame.join` instead of `merge` if indexes align.
- Calculate aggregates with `pivot_table`.

**Common Mistakes**
1. Forgetting to reset index after `groupby`, which can break `merge`.
2. Misnaming columns in `hover_data`, causing `KeyError`.
3. Using `sales['price']` instead of `books['price']` for x-axis, leading to mismatched values.

---

## Task 2 – Hover-enabled Bar Chart (MEDIUM, ~7 min)

### 1. Complete Working Code
```python
import pandas as pd
import plotly.express as px

# Load datasets
books = pd.read_csv('books.csv')
sales = pd.read_csv('sales.csv')

# Merge datasets to get genre and price info with each sale
merged = pd.merge(sales, books, on='book_id')

# Group by genre for total revenue and average price
genre_stats = merged.groupby('genre').agg({
    'total_amount': 'sum',  # total revenue
    'price': 'mean'         # average book price
}).reset_index()

# Sort and select top 10 genres by total revenue
top_genres = genre_stats.sort_values(by='total_amount', ascending=False).head(10)

# Create bar chart
fig = px.bar(
    top_genres,
    x='genre',
    y='total_amount',
    hover_data=['price'],  # show average price
    labels={'total_amount': 'Total Revenue', 'price': 'Avg Price'}
)

# Display plot
fig.show()
```

### 2. Explanation
We merged sales with book data, grouped by genre, and calculated total revenue and mean price. Sorting by revenue allowed us to select the top 10 genres for plotting in an interactive bar chart with hover tooltips showing average prices.

### 3. Expected Output
An interactive vertical bar chart displaying the top 10 genres ranked by total revenue, with hover tooltips revealing the average book price for that genre.

### 4. Key Takeaway
You can enrich bar chart tooltips with aggregated metadata to add valuable context for each category.

---

**Alternative Approaches**
- Use `nlargest(10, 'total_amount')` instead of sorting then head.
- Use horizontal bars (`orientation='h'`) for better readability if genre names are long.

**Common Mistakes**
1. Forgetting to aggregate before sorting, leading to incorrect rankings.
2. Using `unit_price` instead of `price` which might refer to sale-specific price rather than the list price.
3. Not resetting index after grouping, which can confuse plotting functions.

---

## Task 3 – Interactive Time Series with Genre Filter (MEDIUM-HARD, ~10 min)

### 1. Complete Working Code
```python
import pandas as pd
import plotly.express as px

# Load datasets
books = pd.read_csv('books.csv')
sales = pd.read_csv('sales.csv')

# Merge to get genre for each sale
merged = pd.merge(sales, books, on='book_id')

# Convert sale date to datetime and extract month
merged['date'] = pd.to_datetime(merged['date'])
merged['month'] = merged['date'].dt.to_period('M').dt.to_timestamp()

# Group by month and genre for total revenue
monthly_genre_rev = merged.groupby(['month', 'genre'])['total_amount'].sum().reset_index()

# Create initial line plot
fig = px.line(
    monthly_genre_rev,
    x='month',
    y='total_amount',
    color='genre',
    labels={'total_amount': 'Total Revenue', 'month': 'Month'}
)

# Create dropdown with one button per genre + "All"
genres = monthly_genre_rev['genre'].unique()
buttons = []

# Add "All" option
buttons.append(dict(
    label='All',
    method='update',
    args=[{'visible': [True] * len(fig.data)}, {'title': 'All Genres'}]
))

# Add buttons for each genre
for genre in genres:
    visibility = [trace.name == genre for trace in fig.data]
    buttons.append(dict(
        label=genre,
        method='update',
        args=[{'visible': visibility}, {'title': f'Genre: {genre}'}]
    ))

# Update layout with dropdown menu
fig.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        x=0.0,
        y=1.15,
        xanchor='left',
        yanchor='top'
    )]
)

# Display plot
fig.show()
```

### 2. Explanation
We prepared a monthly revenue dataset grouped by genre and plotted it as a multi-line chart. A dropdown menu was added that toggles visibility of lines, enabling the user to filter by genre interactively.

### 3. Expected Output
An interactive time series plot showing a separate revenue line for each genre. A dropdown at the top lets the user select a particular genre or view all genres together.

### 4. Key Takeaway
Combining Plotly's `updatemenus` with trace filtering creates powerful interactive visual controls for complex datasets.

---

**Alternative Approaches**
- Use Plotly's `facet_row` or `facet_col` instead of dropdown to show multiple small charts per genre.
- Employ a Dash app for more complex filtering and interactions.

**Common Mistakes**
1. Forgetting to match `trace.name` to the genre labels when setting visibility conditions.
2. Using `.dt.month` instead of `.dt.to_period('M')`, which causes monthly aggregation to fail over multiple years.
3. Not resetting index after grouping, leading to errors when plotting.

---
```