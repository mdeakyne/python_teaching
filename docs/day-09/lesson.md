# Day 9: Seaborn Statistical Plots - Distribution Analysis  
**Week:** 2  
**Difficulty:** Beginner  
**Duration:** 3-5 minutes  

## Introduction  
At Page Turner Analytics, our team wants to understand patterns in book prices, ratings, and genres so we can make better buying and promotional decisions. In previous lessons, we’ve used Matplotlib to make line charts and bar charts for time series and sales data. Today, we’ll build on those skills using **Seaborn’s statistical plots**—a library built on Matplotlib that gives us prettier, more powerful visualizations for analyzing **distributions**. By the end of this lesson, you’ll be able to create histograms, box plots, and violin plots to dig deeper into our bookstore’s data.

---

## Core Content  

### 1. Visualizing Distributions with Histograms  
A **histogram** lets us see how values are spread across a range—for example, the distribution of book prices in our store. In Seaborn, the `histplot()` function quickly creates a histogram and can also overlay a density curve. If we imagine lining up all books by price like shelves ordered from cheapest to most expensive, the histogram is like counting how many books are in each "price shelf."

**Why this matters:** It helps us identify patterns—Do most books cost between \$10 and \$15? Are expensive books rare or common?

---

### 2. Comparing Ratings with Box Plots  
A **box plot** summarizes data using quartiles and highlights any outliers. Think of it as looking inside a “ratings box”—where most ratings fall in the middle, and a few stand far apart. In Seaborn, `boxplot()` lets us compare across categories easily—such as ratings grouped by genre.

**Why this matters:** A box plot tells us if romance novels consistently get high ratings or if they have a wide spread of opinions. It’s perfect for spotting variability and extremes.

*(From the source material: Like the `sns.boxplot()` example, this is ideal for visualizing counts or distributions across subgroups—similar to how we compared registered users by hour.)*

---

### 3. Multi-Genre Comparisons with Violin Plots  
A **violin plot** combines a box plot with a mirrored density plot, giving more detail about the shape of the data distribution. Imagine the outline of a violin: the wider parts show where data points are dense. In Seaborn, `violinplot()` can compare multiple genres side-by-side.

**Why this matters:** For genres like sci-fi or mystery, violin plots reveal not just the range of ratings but how they cluster—are most ratings packed near 5 stars, or spread evenly from 1 to 5?

---

## Code Examples  

### Example 1 – Histogram of Book Prices  
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the books dataset
books = pd.read_csv("books.csv")

# Create histogram of prices
plt.figure(figsize=(8, 5))
sns.histplot(data=books, x="price", bins=10, kde=True)  # kde=True adds a smooth density curve
plt.title("Distribution of Book Prices")
plt.xlabel("Price ($)")
plt.ylabel("Number of Books")
plt.show()

# Expected output: A histogram showing most books grouped within mid-range prices, with a smooth curve
```

---

### Example 2 – Box Plot of Ratings by Genre  
```python
reviews = pd.read_csv("reviews.csv")

# Merge reviews with books to bring in genre
reviews_books = reviews.merge(books, on="book_id")

plt.figure(figsize=(10, 6))
sns.boxplot(data=reviews_books, x="genre", y="rating")
plt.title("Book Ratings by Genre")
plt.xlabel("Genre")
plt.ylabel("Rating (Stars)")
plt.xticks(rotation=45)  # Rotate genre names for readability
plt.show()

# Expected output: Each genre has a box showing median rating, spread, and outliers
```

---

### Example 3 – Violin Plot Comparing Genres  
```python
plt.figure(figsize=(10, 6))
sns.violinplot(data=reviews_books, x="genre", y="rating", inner="quartile")
plt.title("Distribution of Ratings by Genre")
plt.xlabel("Genre")
plt.ylabel("Rating (Stars)")
plt.xticks(rotation=45)
plt.show()

# Expected output: Smooth violin shapes revealing dense clusters of ratings per genre
```

---

## Common Pitfalls  

1. **Not merging datasets before plotting**  
   - If `genre` is in `books.csv` but not in `reviews.csv`, you must merge the two or your plot will fail.  
   - *Tip:* Always check column names with `df.columns` before plotting.

2. **Forgetting to adjust plot size or labels**  
   - Default plot settings can make category names overlap or be unreadable.  
   - *Tip:* Use `figsize` and `rotation` for clarity.

3. **Too many categories at once**  
   - Adding 50 genres to a single plot makes it messy and hard to read.  
   - *Tip:* Focus on top 5-10 categories or filter your dataset first.

---

## Practice Checkpoint  

By the end of this lesson, you should be able to:  
✅ Create a histogram using Seaborn to visualize book price distribution.  
✅ Use box plots to compare review ratings across different genres.  
✅ Build violin plots to analyze the shape and spread of ratings for multiple genres.

---