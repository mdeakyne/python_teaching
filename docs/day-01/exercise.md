## 📝 Day 1 – Hands‑On Exercises  
**Topic:** Environment Setup & Generating Synthetic Book Data  

---

### Task 1 – Create a Basic Synthetic Books Dataset (EASY – ~5 min)  
**Goal:** Practice creating a `DataFrame` from scratch using `pandas` to represent book catalog information.  

**Instructions:**  
1. Import `pandas`.  
2. Create a Python dictionary with keys: `book_id`, `title`, `author_name`, `genre`, `price`, `publication_year`, `pages`.  
3. Fill with at least 5 sample entries (synthetic data).  
4. Convert the dictionary to a `pandas.DataFrame`.  
5. Print the `DataFrame` and check the data types with `.dtypes`.  

**Skeleton Code:**
```python
import pandas as pd

# Step 1: Define dictionary with book data
books_data = {
    "book_id": [],
    "title": [],
    "author_name": [],
    "genre": [],
    "price": [],
    "publication_year": [],
    "pages": []
}

# Step 2: Convert to DataFrame
books_df = pd.DataFrame(books_data)

# Step 3: Output
print(books_df)
print(books_df.dtypes)
```

**Success Criteria:**  
- You see a table with your synthetic book data.  
- `.dtypes` correctly shows numeric for `book_id`, `price`, `publication_year`, `pages` and object for text columns.  

---

### Task 2 – Generate Author & Sales Data with Variation (MEDIUM – ~7 min)  
**Goal:** Create additional synthetic datasets, making sure columns align with the provided Page Turner Analytics schema.  

**Instructions:**  
1. Create a `DataFrame` for authors: `author_id`, `first_name`, `last_name`, `full_name`, `birth_year`, `country`.  
   - Generate at least 3 authors with matching IDs to books from Task 1.  
   - Ensure `full_name` is a concatenation of first and last names.  
2. Create a `DataFrame` for sales: `sale_id`, `date`, `book_id`, `quantity`, `unit_price`, `total_amount`, `customer_id`.  
   - Include at least 4 sales records that reference the `book_id` from Task 1.  
   - Calculate `total_amount` as `quantity * unit_price`.  
3. Display both DataFrames.  

**Skeleton Code:**
```python
# Authors Data
authors_data = {
    "author_id": [],
    "first_name": [],
    "last_name": [],
    "full_name": [],  # Combine first and last name strings here
    "birth_year": [],
    "country": []
}
authors_df = pd.DataFrame(authors_data)

# Sales Data
sales_data = {
    "sale_id": [],
    "date": [],
    "book_id": [],
    "quantity": [],
    "unit_price": [],
    "total_amount": [],  # Compute this from quantity and unit_price
    "customer_id": []
}
sales_df = pd.DataFrame(sales_data)

print(authors_df)
print(sales_df)
```

**Expected Output:**  
- Two tables, `authors_df` and `sales_df`, containing realistic‑looking but synthetic data.  
- `full_name` column correctly shows combined names.  
- `total_amount` values match `quantity * unit_price`.  

---

### Task 3 – Multi‑Table Synthetic Dataset (MEDIUM‑HARD – ~10 min)  
**Goal:** Integrate book, author, and sales data to prepare for analysis.  

**Instructions:**  
1. Reuse `books_df`, `authors_df`, and `sales_df` from Tasks 1 and 2.  
2. Create a synthetic `reviews` DataFrame:  
   - Columns: `review_id`, `book_id`, `customer_id`, `rating`, `review_date`, `verified_purchase`.  
   - Include at least 5 review records with ratings from 1–5.  
3. Join `books_df` with `authors_df` on matching author information (either `author_name` or `author_id`).  
4. Merge the resulting dataset with `sales_df` on `book_id`.  
5. Print the merged dataset and verify it contains columns from all three original DataFrames.  

**Skeleton Code:**
```python
# Reviews Data
reviews_data = {
    "review_id": [],
    "book_id": [],
    "customer_id": [],
    "rating": [],
    "review_date": [],
    "verified_purchase": []
}
reviews_df = pd.DataFrame(reviews_data)

# Merge books & authors
books_authors_df = pd.merge(
    books_df,
    authors_df,
    left_on="author_name",  # or "author_id" if you adjust Task 1 data
    right_on="full_name",   # or "author_id"
    how="inner"
)

# Merge with sales
merged_df = pd.merge(
    books_authors_df,
    sales_df,
    on="book_id",
    how="left"
)

print(reviews_df)
print(merged_df)
```

**Expected Output:**  
- `reviews_df` shows synthetic reviews tied to books from the earlier DataFrames.  
- `merged_df` contains columns from books, authors, and sales, with correct matches on `book_id`.  
- You can visually verify relationships between datasets (e.g., matching genres to sales quantities).  