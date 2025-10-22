```markdown
## 📝 Day 9 Hands-On Exercises: Seaborn Statistical Plots - Distribution Analysis

### Task 1 (EASY - 5 min)  
**Goal:** Plot a histogram of book prices using Seaborn to visualize the distribution.  

**Instructions:**  
1. Load `books.csv` into a pandas DataFrame.  
2. Use Seaborn’s `histplot()` to plot the distribution of the `price` column.  
3. Add appropriate axis labels and a title.  

**Skeleton Code:**  
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Load the dataset
books = pd.read_csv("books.csv")

# Step 2: Create histogram
sns.histplot(data=books, x=___)

# Step 3: Add labels/title
plt.xlabel("___")
plt.ylabel("___")
plt.title("___")
plt.show()
```

**Expected Output:**  
A histogram showing how book prices are distributed, with most prices observed in the lower ranges if the dataset skews inexpensive.  

---

### Task 2 (MEDIUM - 7 min)  
**Goal:** Plot a box plot of ratings by genre to compare rating spreads for different genres.  

**Instructions:**  
1. Load `books.csv` and `reviews.csv`.  
2. Merge them on `book_id`.  
3. Use Seaborn’s `boxplot()` to show `rating` on the y-axis and `genre` on the x-axis.  
4. Style the plot with rotated x-axis labels for readability.  

**Skeleton Code:**  
```python
# Step 1: Load datasets
books = pd.read_csv("books.csv")
reviews = pd.read_csv("reviews.csv")

# Step 2: Merge on book_id
merged_df = pd.merge(___, ___, on="book_id")

# Step 3: Create box plot
sns.boxplot(data=merged_df, x="___", y="___")

# Step 4: Improve readability
plt.xticks(rotation=___)
plt.title("Genre-wise Ratings Distribution")
plt.show()
```

**Expected Output:**  
A box plot where each genre shows median rating, interquartile range, and potential outliers; genres with consistently higher ratings stand out.  

---

### Task 3 (MEDIUM-HARD - 10 min)  
**Goal:** Create a violin plot comparing book prices by genre and annotate with average ratings—integrating price distribution and review data.  

**Instructions:**  
1. Load `books.csv` and `reviews.csv`.  
2. Merge them on `book_id`.  
3. Group by `genre` to calculate the average `rating`.  
4. Plot a Seaborn `violinplot()` with `genre` on the x-axis and `price` on the y-axis.  
5. Annotate each genre's violin with the calculated average rating above it.  

**Skeleton Code:**  
```python
# Step 1: Load datasets
books = pd.read_csv("books.csv")
reviews = pd.read_csv("reviews.csv")

# Step 2: Merge datasets
merged_df = pd.merge(___, ___, on="book_id")

# Step 3: Calculate average rating per genre
avg_ratings = merged_df.groupby("___")["___"].mean()

# Step 4: Create violin plot
sns.violinplot(data=merged_df, x="___", y="___")

# Step 5: Annotate plot with average ratings
for idx, genre in enumerate(avg_ratings.index):
    plt.text(idx, merged_df["price"].max() + 1, f"Avg Rating: {avg_ratings[genre]:.2f}",
             ha='center')

plt.title("Price Distributions by Genre with Avg Ratings")
plt.show()
```

**Expected Output:**  
A violin plot showing the distribution shape of book prices for each genre, with numerical average rating annotations above each genre; genres with both high average ratings and price clusters become clearly visible.
```