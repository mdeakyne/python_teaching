```markdown
# Day 8: Matplotlib Basics – First Charts  
**Week:** 2  
**Difficulty:** Beginner  
**Duration:** 3–5 minutes  

---

## Introduction
Imagine you’re working for **Page Turner Analytics**, and the marketing team wants to understand how sales trends have shifted over the past year and which genres bring in the most revenue. You already know how to clean, merge, and shape your data from previous lessons—now it’s time to **visualize** it. Today we’ll use Matplotlib, Python’s most widely-used plotting library, to create **line charts for trends** and **bar charts for comparisons**, adding clear colors, labels, and titles so our insights speak for themselves.

---

## Core Content

### 1. Matplotlib and `pyplot`
Matplotlib is the "grandparent" of Python plotting tools. We'll use its `pyplot` module, typically imported as `plt`, to create quick charts. Think of `pyplot` like the display window in a bookstore—it's where you put the books in an attractive layout for customers to notice trends and patterns.

**Why it matters:**  
Numbers in a table can be difficult to interpret. Charts reveal patterns at a glance—whether sales are climbing, which genres dominate revenue, or seasonal spikes.

---

### 2. Line Charts for Trends
A **line chart** connects data points over time and highlights up–or–down movement. In our bookstore analogy, picture sales receipts stacked month by month; connecting them shows which months were strong and which were slow.

**When to use it:**  
- Time series data (e.g., monthly sales)
- Forecasting and seasonality analysis
- Showing continuous data trends

---

### 3. Bar Charts for Comparisons
A **bar chart** compares discrete categories—like genres, countries, or authors. Imagine the store has a shelf for each genre; the taller the shelf’s pile of books sold, the more popular that genre.

**When to use it:**  
- Comparing totals across categories
- Ranking most popular items
- Summarizing categorical distribution

---

### 4. Basic Customization
Labels and titles tell the reader **what** they're looking at, and colors can differentiate datasets or simply make charts more appealing.

Matplotlib lets you:
- Add `plt.title()` for a chart headline
- Use `plt.xlabel()`, `plt.ylabel()` for describing axes
- Change colors (`color='skyblue'`, etc.) to improve clarity

---

## Code Examples

### Example 1: Line Chart of Monthly Sales Trends
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load sales dataset
sales = pd.read_csv('sales.csv', parse_dates=['date'])

# Aggregate monthly total sales
monthly_sales = sales.resample('M', on='date')['total_amount'].sum()

# Plot line chart
plt.figure(figsize=(8, 4))  # set chart size
plt.plot(monthly_sales.index, monthly_sales.values, color='green', marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.grid(True)  # adds grid lines for readability
plt.show()

# Expected output: A green line chart with sales amounts rising/falling over months
```

---

### Example 2: Bar Chart Comparing Genre Revenues
```python
# Load books and sales data
books = pd.read_csv('books.csv')
sales = pd.read_csv('sales.csv')

# Merge to get genres alongside sales
sales_books = sales.merge(books, on='book_id')

# Aggregate total revenue by genre
genre_revenue = sales_books.groupby('genre')['total_amount'].sum()

# Sort genres by revenue
genre_revenue = genre_revenue.sort_values(ascending=False)

# Plot bar chart
plt.figure(figsize=(8, 4))
plt.bar(genre_revenue.index, genre_revenue.values, color='skyblue')
plt.title('Revenue by Genre')
plt.xlabel('Genre')
plt.ylabel('Total Revenue ($)')
plt.xticks(rotation=45)  # angle labels for readability
plt.show()

# Expected output: Sky-blue bars showing each genre's total revenue, ranked.
```

---

### Example 3: Combining Trends and Comparisons
```python
# Compare monthly sales for top genre
top_genre = genre_revenue.idxmax()
top_genre_sales = sales_books[sales_books['genre'] == top_genre]
monthly_top = top_genre_sales.resample('M', on='date')['total_amount'].sum()

plt.figure(figsize=(8, 4))
plt.plot(monthly_sales.index, monthly_sales.values, label='All Genres', color='gray')
plt.plot(monthly_top.index, monthly_top.values, label=f'{top_genre}', color='orange')
plt.title(f'Monthly Sales Trend: All vs {top_genre}')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.legend()
plt.show()

# Expected output: Gray line for all genres, orange line for top genre, for visual comparison.
```

---

## Common Pitfalls
1. **Forgetting `plt.show()`**  
   Without calling `plt.show()`, your chart may not display. Always end plotting code with this function in scripts (not always necessary in Jupyter).
2. **Mixing datetime formats**  
   Ensure dates are parsed (`parse_dates`) before plotting time series; otherwise, your x-axis may be unreadable or misaligned.
3. **Overcrowded labels**  
   Use `rotation` on tick labels to avoid overlapping text and make charts easier to read.

---

## Practice Checkpoint
By the end of today’s lesson, you should be able to:
- [ ] Create a line chart showing book sales trends over time.
- [ ] Build a bar chart comparing genres using aggregated revenue.
- [ ] Customize colors, labels, and titles to clearly communicate insights.

---
```