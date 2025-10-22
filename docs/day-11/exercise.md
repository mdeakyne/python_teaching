## 📊 Day 11 – Advanced Plotly: Multiple Traces & Subplots – Hands-on Exercises  

---

### Task 1 – Easy (5 min)  
**Goal:** Create a multi-line chart showing monthly sales quantity trends for **two genres**.  

**Instructions:**  
1. Load `books.csv` and `sales.csv`.  
2. Merge data so each sale has its genre information.  
3. Aggregate sales by month for two chosen genres (e.g., *Fiction* and *Non-Fiction*).  
4. Create a Plotly `go.Figure()` with **two line traces**, one per genre.  
5. Give each trace a unique color and label in the legend.

**Skeleton Code:**
```python
import pandas as pd
import plotly.graph_objects as go

# Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")

# Merge on book_id
merged = ...

# Convert 'date' to datetime and extract month-year
merged['date'] = pd.to_datetime(merged['date'])
merged['month'] = ...

# Filter for two genres
genre_list = ["Fiction", "Non-Fiction"]
filtered = ...

# Aggregate sales quantity per genre per month
agg = ...

# Create figure and add traces
fig = go.Figure()
for genre in genre_list:
    fig.add_trace(go.Scatter(
        x=...,   # months
        y=...,   # quantities
        mode='lines',
        name=genre
    ))

fig.show()
```

**Expected Output:**  
An interactive line chart with two lines—one for each selected genre—spanning month-by-month. The legend clearly differentiates the genres by color.

---

### Task 2 – Medium (7 min)  
**Goal:** Create a **subplot grid** comparing sales trends across **four genres**.  

**Instructions:**  
1. Use the merged dataset from Task 1.  
2. Choose any four genres present in the dataset.  
3. Create a 2×2 subplot layout using `plotly.subplots.make_subplots()`.  
4. Add a separate line trace to each subplot for its genre's monthly sales quantity.  
5. Include subplot titles matching each genre.  
6. Apply a consistent theme (e.g., `plotly_white`).

**Skeleton Code:**
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

genres_4 = ["Fiction", "Non-Fiction", "Fantasy", "Biography"]

fig = make_subplots(rows=2, cols=2, subplot_titles=genres_4)

# Loop through each genre and add to correct subplot
row, col = 1, 1
for idx, genre in enumerate(genres_4):
    monthly_data = ...
    fig.add_trace(
        go.Scatter(
            x=..., 
            y=..., 
            mode='lines', 
            name=genre
        ),
        row=row,
        col=col
    )
    # Update row/col counters
    col += 1
    if col > 2:
        col = 1
        row += 1

fig.update_layout(template="plotly_white")
fig.show()
```

**Expected Output:**  
A 2×2 grid of interactive subplots, each showing a single genre’s monthly sales trend. All subplots share the same style and color palette, with clear genre titles above each plot.

---

### Task 3 – Medium-Hard (10 min)  
**Goal:** Build a comprehensive dashboard-ready subplot view comparing **sales quantity and average rating** for multiple genres.  

**Instructions:**  
1. Merge the `books.csv`, `sales.csv`, and `reviews.csv` datasets so each genre has sales and review data.  
2. Select any **three genres**.  
3. For each genre, aggregate:  
   - Monthly total quantity sold (`sales.csv`).  
   - Monthly average review rating (`reviews.csv`).  
4. Create a **3-row subplot** layout:  
   - **Row 1:** Genre A – line for sales quantity & secondary line for average rating.  
   - **Row 2:** Genre B – same as above.  
   - **Row 3:** Genre C – same as above.  
5. Use different y-axes for quantity vs rating in each subplot, but keep them aligned to the same month axis.  
6. Apply layout adjustments for dashboard-style viewing (tight spacing, shared x-axis).

**Skeleton Code:**
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")
reviews = pd.read_csv("reviews.csv")

# Merge datasets appropriately
merged_sales = ...
merged_reviews = ...
merged_all = ...

genres_3 = ["Fiction", "Non-Fiction", "Fantasy"]

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
    monthly_qty = ...
    # Aggregate monthly average rating
    monthly_rating = ...

    fig.add_trace(
        go.Scatter(x=..., y=..., mode='lines', name=f"{genre} Sales"),
        row=i, col=1, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=..., y=..., mode='lines', name=f"{genre} Rating"),
        row=i, col=1, secondary_y=True
    )

fig.update_layout(height=900, template="plotly_white")
fig.show()
```

**Expected Output:**  
A vertically stacked, interactive figure where each row represents a genre, showing two aligned lines: one for monthly sales quantity and one for average rating, with separate y-axes. The layout is optimized for dashboard presentation and easy comparison.