# Day 6: Merging Datasets – Authors, Books, Sales

## Introduction
Imagine you're working at **Page Turner Analytics**, helping a bookstore chain understand its business better. Yesterday, we learned how to clean, filter, and summarize data with pivot tables and aggregations. Today, we’ll take another big step: *combining data from different sources*. Just like a bookstore connects authors to their books and sales receipts to the titles sold, we’ll use **merging techniques** in Python to bring different datasets together so we can see the full picture. You'll learn how to merge authors with books, connect books to sales data, and choose the right join type to handle real-world scenarios.

---

## Core Content

### 1. What is Merging in Pandas?
In data analysis, merging is like **matching puzzle pieces**: we align rows from two DataFrames based on shared columns (keys). For example, `book_id` in the books table matches `book_id` in the sales table. Pandas’ `merge()` function lets us combine related datasets into one rich table containing all the fields we care about.

#### Why it matters:
Without merging, you only see fragments of a story. If you only look at sales data, you might know a book sold 500 copies but not which author wrote it or what genre it belongs to. By merging, we unlock deeper insights — like total sales per author or trends across genres.

---

### 2. Merge Keys and Join Types
A **merge key** is the column(s) used to match rows between DataFrames. It's typically an ID like `book_id` or `author_id`.

**Join Types**:
- **Inner Join (`how='inner'`)** – keeps only rows where the key exists in *both* DataFrames (like intersecting two lists).
- **Left Join (`how='left'`)** – keeps all rows from the left DataFrame, adding matches from the right when available.
- **Right Join (`how='right'`)** – the opposite of left join; all rows from the right DataFrame are kept.
- **Outer Join (`how='outer'`)** – keeps all rows from *both* DataFrames, filling missing data with NaN.

Think of it like matching customers to loyalty card records:
- Inner: only customers who also have loyalty cards.
- Left: all sales, even if the customer doesn’t have a loyalty card.
- Outer: every possible record, even if some info is missing.

---

### 3. Merge vs. Concat vs. Join
- **`merge()`** – powerful, flexible matching based on keys.
- **`join()`** – simpler when joining on indices.
- **`concat()`** – just stacks or appends DataFrames, without matching keys.

For our bookstore, `merge()` is ideal because we have IDs to match.

---

## Code Examples

### Example 1: Merge Authors with Books
```python
import pandas as pd

books = pd.read_csv('books.csv')
authors = pd.read_csv('authors.csv')

# Merge on the author_id key
books_authors = books.merge(authors, on='author_id', how='inner')

print(books_authors.head())
# Expected Output: Each row shows book title, price, publication year, and author details.
```

---

### Example 2: Combine Sales Data with Book Information
```python
sales = pd.read_csv('sales.csv')

# Merge books with sales
books_sales = books.merge(sales, on='book_id', how='inner')

# Example insight: total sales amount per book
total_sales_per_book = books_sales.groupby('title')['total_amount'].sum()
print(total_sales_per_book.head())
# Expected Output: Book titles with their total sales amounts.
```

---

### Example 3: Outer Join to Find Missing Sales
```python
# Outer join to include books with no sales and sales with no matching book record
books_sales_outer = books.merge(sales, on='book_id', how='outer')

print(books_sales_outer[pd.isna(books_sales_outer['quantity'])].head())
# Expected Output: Books that have never been sold (NaN in quantity).
```

---

## Common Pitfalls
1. **Wrong merge key** – Using a non-unique or incorrect column can cause duplicates or mismatched rows.  
   *Fix*: Double-check column names and uniqueness before merging.
2. **Default inner join surprises** – Forgetting to set `how` defaults to inner join, which can drop unmatched rows.  
   *Fix*: Explicitly set the `how` parameter based on your needs.
3. **Column name collisions** – When both DataFrames have the same non-key column name, pandas appends `_x` and `_y`.  
   *Fix*: Rename columns before merging or use `suffixes` parameter.

---

## Practice Checkpoint
By the end of this lesson, you should be able to:
- [ ] Merge two DataFrames using a common key.
- [ ] Choose and apply the correct join type for your use case.
- [ ] Integrate multiple datasets to create richer analytical views.

---