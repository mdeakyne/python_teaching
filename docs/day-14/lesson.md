# DAY 14: Mini-Project – Complete EDA Dashboard (Static)

## Introduction
Imagine you’re a data analyst for **Page Turner Analytics**, tasked with helping the management understand **sales performance, popular genres, and customer ratings trends**. In previous lessons, you learned how to create individual charts, customize layouts, and tell visual stories with annotations and themes. Today, you’ll combine those skills to perform a **complete, end-to-end exploratory data analysis (EDA)**—creating a **multi-panel static dashboard** that consolidates book store insights into one clear visual report.

By the end of this session, you’ll know how to:
- Perform a full EDA workflow
- Create multiple charts in one static dashboard layout
- Generate actionable insights for sales decisions

---

## Core Content

### 1. EDA Workflow in Context
**Exploratory Data Analysis (EDA)** is like walking through your bookstore with a notepad, jotting down where customers spend the most time, which shelves are bare, and what genres fly off the racks. The steps:
1. **Data loading** – Bring datasets into Python (our “book inventory”).
2. **Cleaning & transformation** – Fix typos, handle missing pages (missing values), unify formats.
3. **Exploration** – Ask questions through aggregated views, groupings, and visualizations.
4. **Insight generation** – Turn charts into decisions—e.g., “Increase fantasy stock in Q4.”

From *Tuckfield’s Dive Into Data Science*: EDA gives you the foundational understanding before forecasting demand or optimizing marketing campaigns. Without it, more advanced analytics miss context.

---

### 2. Multi-Chart Layout Concepts
In a single dashboard, **multiple panels** allow different angles on the same story:
- **Sales by Genre** reveals which categories are top performers.
- **Monthly Revenue Trend** shows seasonal patterns.
- **Average Ratings by Genre** gives customer satisfaction context.

In bookstore terms, think of it as giving the manager one sheet showing:
- 📊 What sells
- 📈 When it sells
- ⭐ How customers feel about it

We use **subplots** and **grid layouts** to organize visuals. This keeps information compact and easy to digest—especially for decision-makers with limited time.

---

### 3. Insight Generation & Reporting
Data without interpretation is just noise. The power of an EDA dashboard lies in **turning visual cues into business levers**:
- A spike in December revenue? Plan a holiday-themed campaign.
- Low ratings for a high-selling genre? Improve quality or curate offerings.
- Growth in new authors? Support them with marketing to increase retention.

This is where you connect the dots and make the “So what?” explicit in your report. In our project, we’ll output key observations alongside the visual dashboard.

---

## Code Examples

### Example 1 – Load & Prep Data
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
books = pd.read_csv("books.csv")
sales = pd.read_csv("sales.csv")
reviews = pd.read_csv("reviews.csv")

# Merge sales with books for genre and price info
sales_books = sales.merge(books, on='book_id', how='left')

# Add month column for time-based analysis
sales_books['date'] = pd.to_datetime(sales_books['date'])
sales_books['month'] = sales_books['date'].dt.to_period('M').astype(str)

print(sales_books.head())
# Expected: Each sale row now has genre, price, and month info
```

---

### Example 2 – Multi-Panel Dashboard
```python
# Aggregate data
genre_sales = sales_books.groupby('genre')['total_amount'].sum().sort_values()
monthly_sales = sales_books.groupby('month')['total_amount'].sum()
genre_ratings = reviews.merge(books, on='book_id').groupby('genre')['rating'].mean()

# Create multi-panel layout
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Panel 1: Sales by Genre
genre_sales.plot(kind='barh', ax=axes[0], color='skyblue')
axes[0].set_title("Sales by Genre")
axes[0].set_xlabel("Total Sales ($)")

# Panel 2: Monthly Revenue Trend
monthly_sales.plot(kind='line', marker='o', ax=axes[1], color='green')
axes[1].set_title("Monthly Revenue Trend")
axes[1].set_ylabel("Total Sales ($)")

# Panel 3: Average Ratings by Genre
genre_ratings.plot(kind='bar', ax=axes[2], color='orange')
axes[2].set_title("Average Ratings by Genre")
axes[2].set_ylabel("Rating (out of 5)")

plt.tight_layout()
plt.show()
```

**Expected Output**:
- **Left chart**: Horizontal bars showing genres sorted by total sales.
- **Middle chart**: Line chart with seasonal sales fluctuations.
- **Right chart**: Bar chart of average ratings per genre.

---

### Example 3 – Generating a Quick Report
```python
# Example quick insights
top_genre = genre_sales.idxmax()
best_month = monthly_sales.idxmax()
lowest_rated_genre = genre_ratings.idxmin()

print(f"Top performing genre: {top_genre}")
print(f"Best sales month: {best_month}")
print(f"Lowest rated genre: {lowest_rated_genre}")
```
**Expected Output**:
```
Top performing genre: Fiction
Best sales month: 2023-12
Lowest rated genre: Mystery
```

---

## Common Pitfalls
1. **Misaligned Merges** – Forgetting the correct join key (e.g., merging on `author_id` instead of `book_id`) can produce misleading charts.  
   *Fix:* Always check `head()` after merges.
2. **Ignoring Scale Differences** – Comparing sales in dollars to ratings on a 1–5 scale in the same axis can mislead.  
   *Fix:* Use separate panels for metrics with different units.
3. **Overcrowding Dashboards** – Too many charts in one view makes it hard to focus.  
   *Fix:* Limit static dashboards to 3–4 panels with clear titles.

---

## Practice Checkpoint
By the end of today, you should be able to:
- ✅ Load multiple datasets and merge them for richer EDA
- ✅ Build a multi-panel static dashboard showing different sales metrics
- ✅ Summarize and report meaningful business insights from visual data

---