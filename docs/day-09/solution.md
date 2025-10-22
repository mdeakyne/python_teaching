```markdown
## 📝 Day 9 Solutions: Seaborn Statistical Plots - Distribution Analysis

---

### Task 1 (EASY - Histogram of Book Prices)

#### 1. Complete Working Code
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Load the dataset
books = pd.read_csv("books.csv")

# Step 2: Create histogram of book prices
sns.histplot(data=books, x="price", bins=20, kde=True, color="skyblue")

# Step 3: Add labels and title
plt.xlabel("Book Price (USD)")
plt.ylabel("Number of Books")
plt.title("Distribution of Book Prices")
plt.show()
```

#### 2. Explanation
We read the `books.csv` file into a DataFrame and use Seaborn’s `histplot` to plot the frequency distribution of book prices. Including `kde=True` overlays a Kernel Density Estimate curve, giving a smoother view of distribution trends.

#### 3. Expected Output
A histogram with bars representing the frequency of prices, overlaid with a smooth density line. If most books are inexpensive, bars will cluster toward the left.

#### 4. Key Takeaway
Histograms are effective for visualizing how a continuous numerical variable like `price` is distributed.

**Alternative Approaches:**
- Use `plt.hist()` from matplotlib for basic plotting.
- Use Seaborn’s `displot()` for more customization options.

**Common Mistakes:**
1. Forgetting to specify the column name (`x="price"`) results in an empty plot.
2. Failing to call `plt.show()` can prevent the plot from rendering.
3. Using too few bins hides meaningful distribution details; too many bins makes the plot noisy.

---

### Task 2 (MEDIUM - Box Plot of Ratings by Genre)

#### 1. Complete Working Code
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Load datasets
books = pd.read_csv("books.csv")
reviews = pd.read_csv("reviews.csv")

# Step 2: Merge on book_id
merged_df = pd.merge(books, reviews, on="book_id")

# Step 3: Create box plot of ratings by genre
sns.boxplot(data=merged_df, x="genre", y="rating", palette="Set2")

# Step 4: Rotate x-axis labels for readability
plt.xticks(rotation=45)
plt.title("Genre-wise Ratings Distribution")
plt.xlabel("Genre")
plt.ylabel("Rating")
plt.show()
```

#### 2. Explanation
We merge `books.csv` and `reviews.csv` on the common `book_id` to align ratings with genres. The box plot shows median ratings, the interquartile range, and potential outliers per genre, enabling direct comparison.

#### 3. Expected Output
A multi-category box plot showing each genre on the x-axis and ratings on the y-axis. The plot will have boxes showing spread and possibly dots representing outliers.

#### 4. Key Takeaway
Box plots are useful for comparing distributions and identifying outliers across different categories.

**Alternative Approaches:**
- Use Seaborn’s `catplot(kind="box")` for faceted layouts.
- Add `hue` for additional grouping by another variable such as `verified_purchase`.

**Common Mistakes:**
1. Not merging datasets on `book_id` causes mismatched or missing rating data.
2. Forgetting to rotate labels for long genre names makes them unreadable.
3. Passing wrong column names to `x` or `y` parameters raises `KeyError`.

---

### Task 3 (MEDIUM-HARD - Violin Plot with Average Rating Annotation)

#### 1. Complete Working Code
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1: Load datasets
books = pd.read_csv("books.csv")
reviews = pd.read_csv("reviews.csv")

# Step 2: Merge datasets on book_id
merged_df = pd.merge(books, reviews, on="book_id")

# Step 3: Calculate average rating per genre
avg_ratings = merged_df.groupby("genre")["rating"].mean()

# Step 4: Create violin plot of prices by genre
sns.violinplot(data=merged_df, x="genre", y="price", palette="Pastel1")

# Step 5: Annotate plot with average ratings
max_price = merged_df["price"].max()
for idx, genre in enumerate(avg_ratings.index):
    plt.text(
        idx,
        max_price + 1,  # position text above highest price
        f"Avg Rating: {avg_ratings[genre]:.2f}",
        ha='center',
        va='bottom',
        fontsize=9,
        color='black'
    )

plt.title("Price Distributions by Genre with Avg Ratings")
plt.xlabel("Genre")
plt.ylabel("Book Price (USD)")
plt.xticks(rotation=45)
plt.ylim(0, max_price + 5)  # add extra space for text
plt.tight_layout()
plt.show()
```

#### 2. Explanation
We combine book and review data, compute average ratings per genre, then use a violin plot to visualize price distributions for each genre. Adding text annotations above each violin indicates the genre’s average rating, integrating qualitative and quantitative insights.

#### 3. Expected Output
A violin plot per genre showing the distribution shape of book prices, with average rating values annotated above each genre's violin.

#### 4. Key Takeaway
Violin plots convey both distribution spread and density, and annotations can enrich them with summary metrics for more context.

**Alternative Approaches:**
- Use `stripplot` or `swarmplot` overlays with `violinplot` for individual price points.
- Encode average rating as color intensity using `hue` instead of text labels.

**Common Mistakes:**
1. Forgetting to add padding to y-axis limits can cause annotations to overlap with plot edges.
2. Using `groupby` without `.mean()` will return grouped objects instead of average ratings.
3. Incorrect annotation index mapping can misplace text over the wrong genre.

---
```