```markdown
## 📊 Day 11 – Advanced Plotly: Multiple Traces & Subplots – Solutions

---

### Task 1 – Easy  
**Goal:** Multi-line chart showing monthly sales quantity trends for two genres.

---

#### 1. Complete Working Code
```python
import pandas as pd
import plotly.graph_objects as go

# Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")

# Merge on book_id to get genre for each sale
merged = pd.merge(sales, books, on="book_id", how="left")

# Ensure date is datetime and create month-year label
merged['date'] = pd.to_datetime(merged['date'])
merged['month'] = merged['date'].dt.to_period('M').astype(str)

# Filter for desired genres
genre_list = ["Fiction", "Non-Fiction"]
filtered = merged[merged['genre'].isin(genre_list)]

# Aggregate sales quantity by genre and month
agg = (
    filtered.groupby(['month', 'genre'])['quantity']
    .sum()
    .reset_index()
)

# Create figure and add line traces per genre
fig = go.Figure()
for genre in genre_list:
    genre_data = agg[agg['genre'] == genre]
    fig.add_trace(
        go.Scatter(
            x=genre_data['month'],
            y=genre_data['quantity'],
            mode='lines',
            name=genre
        )
    )

fig.update_layout(
    title="Monthly Sales Quantity – Fiction vs Non-Fiction",
    xaxis_title="Month",
    yaxis_title="Total Quantity Sold",
    template="plotly_white"
)

fig.show()
```

---

#### 2. Explanation
We join the sales data to the books data using `book_id` to bring in genre information. Dates are normalized to month-year strings, then filtered down to the target genres. The grouped aggregate computes monthly quantities for each genre, and we plot them as separate traces.

---

#### 3. Expected Output
An interactive Plotly chart with two lines — one showing Fiction monthly quantities, the other Non-Fiction — against the month axis with separate legend entries.

---

#### 4. Key Takeaway
Merging datasets on IDs and grouping by time periods enables multi-trace comparisons between categories.

---

**Alternative Approaches:**
- Use `pd.Grouper(freq='M')` for direct monthly aggregation without converting to string first.
- Pivot the aggregated DataFrame to wide format and directly pass columns to `go.Figure`.

**Common Mistakes:**
1. Forgetting to convert the `date` column to `datetime` before extracting month/year.
2. Filtering genres after aggregation, which may include unnecessary data in calculations.
3. Not resetting index after `.groupby()`, leading to mismatched plotting axes.

---

### Task 2 – Medium  
**Goal:** Subplot grid comparing monthly sales trends for four genres.

---

#### 1. Complete Working Code
```python
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")

# Merge to include genre
merged = pd.merge(sales, books, on="book_id", how="left")
merged['date'] = pd.to_datetime(merged['date'])
merged['month'] = merged['date'].dt.to_period('M').astype(str)

# Define genres
genres_4 = ["Fiction", "Non-Fiction", "Fantasy", "Biography"]

# Create subplot layout
fig = make_subplots(rows=2, cols=2, subplot_titles=genres_4)

# Add traces to subplots
row, col = 1, 1
for genre in genres_4:
    monthly_data = (
        merged[merged['genre'] == genre]
        .groupby('month')['quantity'].sum()
        .reset_index()
    )
    fig.add_trace(
        go.Scatter(
            x=monthly_data['month'],
            y=monthly_data['quantity'],
            mode='lines',
            name=genre
        ),
        row=row,
        col=col
    )
    col += 1
    if col > 2:
        col = 1
        row += 1

fig.update_layout(
    template="plotly_white",
    title="Monthly Sales Trends by Genre (4 Genres)",
    height=700
)

fig.show()
```

---

#### 2. Explanation
We reuse the merged dataset approach, focusing on four target genres. Each genre’s monthly quantity trend is added to its own subplot cell in a 2×2 layout to enable visual comparison while keeping consistent styling.

---

#### 3. Expected Output
Four separate subplots, arranged in a grid, each showing a line chart for one genre’s monthly sales quantity.

---

#### 4. Key Takeaway
Subplots allow simultaneous visualization of multiple similar metrics across categories without overlapping lines.

---

**Alternative Approaches:**
- Create a panel chart using facetting in Plotly Express (`px.line` with `facet_col`/`facet_row`).
- Use color grouping inside a single shared chart for comparison.

**Common Mistakes:**
1. Misaligning subplot positions without incrementing row/col counters properly.
2. Grouping without filtering genre first, resulting in multi-genre aggregated lines.
3. Forgetting to set `subplot_titles` leading to unclear labeling in the dashboard.

---

### Task 3 – Medium-Hard  
**Goal:** Dashboard-ready subplot comparing sales quantity and average rating.

---

#### 1. Complete Working Code
```python
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")
reviews = pd.read_csv("reviews.csv")

# Prepare merged datasets
# Merge sales with books to add genre
merged_sales = pd.merge(sales, books, on="book_id", how="left")
merged_sales['date'] = pd.to_datetime(merged_sales['date'])
merged_sales['month'] = merged_sales['date'].dt.to_period('M').astype(str)

# Merge reviews with books to add genre
merged_reviews = pd.merge(reviews, books, on="book_id", how="left")
merged_reviews['review_date'] = pd.to_datetime(merged_reviews['review_date'])
merged_reviews['month'] = merged_reviews['review_date'].dt.to_period('M').astype(str)

# Select genres
genres_3 = ["Fiction", "Non-Fiction", "Fantasy"]

# Create subplot layout with secondary y-axis for ratings
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    subplot_titles=genres_3,
    specs=[[{"secondary_y": True}],
           [{"secondary_y": True}],
           [{"secondary_y": True}]]
)

for i, genre in enumerate(genres_3, start=1):
    # Aggregate monthly quantity
    monthly_qty = (
        merged_sales[merged_sales['genre'] == genre]
        .groupby('month')['quantity'].sum()
        .reset_index()
    )
    # Aggregate monthly average rating
    monthly_rating = (
        merged_reviews[merged_reviews['genre'] == genre]
        .groupby('month')['rating'].mean()
        .reset_index()
    )

    fig.add_trace(
        go.Scatter(
            x=monthly_qty['month'],
            y=monthly_qty['quantity'],
            mode='lines',
            name=f"{genre} Sales"
        ),
        row=i, col=1, secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=monthly_rating['month'],
            y=monthly_rating['rating'],
            mode='lines',
            name=f"{genre} Rating",
            line=dict(dash='dot')
        ),
        row=i, col=1, secondary_y=True
    )

# Layout adjustments
fig.update_yaxes(title_text="Quantity Sold", secondary_y=False)
fig.update_yaxes(title_text="Avg Rating", secondary_y=True, range=[0, 5])

fig.update_layout(
    height=900,
    template="plotly_white",
    title="Monthly Sales & Avg Rating by Genre – Dashboard View",
    legend=dict(orientation="h", yanchor="bottom", y=-0.1)
)

fig.show()
```

---

#### 2. Explanation
We separately aggregate monthly sales quantities and monthly average ratings for each genre. Using Plotly’s secondary y-axis feature enables plotting metrics with different scales in the same subplot per genre, stacked vertically for clear comparative viewing.

---

#### 3. Expected Output
A vertical dashboard with 3 stacked subplots — each subplot showing two lines: solid line for quantity sold (left y-axis) and dotted line for average rating (right y-axis), all sharing the month x-axis.

---

#### 4. Key Takeaway
Secondary y-axes let you overlay metrics of different units/scales in the same chart for richer comparisons.

---

**Alternative Approaches:**
- Normalize ratings and quantities to a common scale to plot them on a single y-axis.
- Use separate color-coded bars and lines for mixed metrics in each subplot.

**Common Mistakes:**
1. Not aligning month formats between sales and reviews datasets, causing mismatched traces.
2. Forgetting `secondary_y=True` for rating traces, leading to wrong scaling.
3. Using default y-axis range for ratings, which may misrepresent values if not locked to 0–5.

---
```