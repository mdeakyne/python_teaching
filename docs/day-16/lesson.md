```markdown
# Day 16: Dash Core Components – Inputs & Controls

## Introduction
Imagine you’re building **Page Turner Analytics**’ interactive dashboard for a bookstore chain. Last week, you learned how to style layouts, arrange charts, and tell a data story. But now, our users want **control** — the ability to filter books by genre, narrow results by publication dates, and adjust price ranges directly in the browser. Today, we'll explore Dash **core input components** like dropdowns, date pickers, and sliders so end-users can explore exactly the slice of data they care about, without touching code.

---

## Core Content

### 1. dcc.Dropdown – Genre Selection
A dropdown lets readers choose a category — just like picking a shelf in a physical bookstore (“Fiction,” “Non-fiction,” “Mystery,” etc.).  
In Dash, `dcc.Dropdown` creates a selection menu. You can supply options from your dataset and bind them to callbacks for filtering data.

*Why it matters:* Filtering by genre quickly narrows down analysis to relevant books, making visualizations more focused and meaningful.

Using the **className** prop (from our source material) allows us to control layout: grouping dropdowns in a row with columns that define width.

---

### 2. dcc.DatePickerRange – Time Filtering
Sometimes you want to see sales only for last quarter or book releases in 2020. `dcc.DatePickerRange` offers start and end dates in one component.

*Store analogy:* Think of a calendar on the store manager’s desk used to check seasonal sales — we bring that calendar into our app.

Date range filters are especially important for time-series analysis, ensuring our visuals respond only to the selected period.

---

### 3. dcc.Slider – Price Range Control
Sliders create instant numerical filters — perfect for setting **minimum and maximum book prices**.  
Instead of scanning a table for values, the user can swipe to adjust thresholds in real time.

*Why it matters:* Pricing analysis benefits from sliceable ranges — whether analyzing premium hardcovers or budget-friendly paperbacks.

---

## Code Examples

### Example 1 – Genre Dropdown
```python
import dash
from dash import html, dcc
import pandas as pd

books_df = pd.read_csv("books.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='genre-dropdown',
            options=[{'label': g, 'value': g} for g in books_df['genre'].unique()],
            value='Fiction',  # default selection
            clearable=False
        )
    ], className="four columns")
], className="row")

# Expected behavior: Dropdown lists unique genres from books.csv.
# Selecting a genre will later filter charts/tables in callbacks.
if __name__ == '__main__':
    app.run_server(debug=True)
```

---

### Example 2 – Date Range Picker
```python
app.layout = html.Div([
    html.Div([
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=books_df['publication_year'].min(),
            max_date_allowed=books_df['publication_year'].max(),
            start_date=2015,
            end_date=2020
        )
    ], className="six columns")
], className="row")

# Expected behavior: Users select publication year ranges to filter books released in that period.
```

---

### Example 3 – Price Slider
```python
app.layout = html.Div([
    html.Div([
        dcc.Slider(
            id='price-slider',
            min=books_df['price'].min(),
            max=books_df['price'].max(),
            step=0.50,
            value=20.00,  # default value
            marks={int(p): f"${int(p)}" for p in range(int(books_df['price'].min()), int(books_df['price'].max())+1, 5)}
        )
    ], className="six columns")
], className="row")

# Expected behavior: Dragging the slider changes the price filter for charts/tables.
```

These components will later tie into **callbacks** so that updating a control instantly updates data visualizations.

---

## Common Pitfalls

1. **Missing `value` or `start_date` defaults**  
   If you don’t set sensible defaults, your app may start blank or error out. Begin with commonly used or safe ranges.

2. **Incorrect column widths**  
   Forgetting to wrap inputs inside rows and properly sized columns can make the layout look broken. Follow the `row` + `{n} columns` pattern from the source material.

3. **Improper option formatting**  
   For dropdowns, ensure each option is a `{label: ..., value: ...}` dict; otherwise, Dash will throw a type error.

---

## Practice Checkpoint

✅ I can create a **dropdown** that dynamically loads options from `books.csv`.  
✅ I can build a **date picker** that filters by publication year or sales date.  
✅ I can implement a **slider** to filter books by price range.

Next session, we’ll connect these inputs to callbacks so the dashboard reacts in real-time to user selections.
```
