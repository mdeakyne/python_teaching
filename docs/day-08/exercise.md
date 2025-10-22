```markdown
## 📊 Day 8 Hands-on Exercises – Matplotlib Basics: First Charts  

---

### **Task 1 – Easy (5 min): Line Chart of Monthly Sales Trends**  
**Goal:** Reinforce how to create a simple line chart.  

**Instructions:**  
1. Load `sales.csv` into a pandas DataFrame.  
2. Convert the `date` column to datetime format.  
3. Group data by month, summing `total_amount`.  
4. Plot a line chart showing sales trend over time.  
5. Add axis labels and a title.  

**Skeleton Code:**  
```python
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the data
sales = pd.read_csv("sales.csv")

# Step 2: Convert to datetime
sales['date'] = pd.to_datetime(sales['date'])

# Step 3: Group monthly totals
monthly_sales = ...

# Step 4: Plot line chart
plt.plot(...)
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.title("Monthly Sales Trend - Page Turner Analytics")
plt.show()
```

**Expected Output:**  
A **line chart** with 12 points, showing ups and downs of sales throughout the year, labeled with month names on the X-axis and revenue amounts on the Y-axis.  

---

### **Task 2 – Medium (7 min): Bar Chart Comparing Genre Revenue**  
**Goal:** Apply bar chart concept with merged data.  

**Instructions:**  
1. Load `sales.csv` and `books.csv`.  
2. Merge the datasets on `book_id`.  
3. Group data by `genre`, summing `total_amount`.  
4. Plot a bar chart where genres are on the X-axis and total revenue on the Y-axis.  
5. Customize the colors for each bar and rotate X-axis labels for readability.  

**Skeleton Code:**  
```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
books = pd.read_csv("books.csv")

# Merge sales with book info
sales_books = ...

# Group by genre
genre_sales = ...

# Plot bar chart
plt.bar(...)
plt.xlabel("Genre")
plt.ylabel("Total Revenue")
plt.title("Revenue by Book Genre")
plt.xticks(rotation=45)
plt.show()
```

**Expected Output:**  
A **colorful bar chart** showing each genre’s revenue side-by-side, with clear readable labels, sorted by highest revenue first.  

---

### **Task 3 – Medium-Hard (10 min): Combined Chart – Sales Trend for Top Genre**  
**Goal:** Integrate Matplotlib basics with multi-step data manipulation.  

**Instructions:**  
1. Load `sales.csv` and `books.csv`.  
2. Merge them on `book_id`.  
3. Group by `genre` to find which genre has the highest total revenue.  
4. Filter sales data for only this genre.  
5. Group by month and plot a **line chart** of monthly sales for the genre.  
6. On the same chart, plot a **bar chart** of total monthly sales for all genres (as background comparison).  
7. Add a legend, titles, and custom colors.  

**Skeleton Code:**  
```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
books = pd.read_csv("books.csv")

# Merge datasets
sales_books = ...

# Find top genre
top_genre = ...

# Filter for that genre
top_genre_sales = ...

# Group monthly genre sales and overall monthly sales
monthly_top_genre = ...
monthly_all = ...

# Create combined chart
plt.bar(..., color='lightgray', label='All Genres')
plt.plot(..., color='blue', label=top_genre)
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.title(f"Monthly Sales: {top_genre} vs All Genres")
plt.legend()
plt.show()
```

**Expected Output:**  
A **combined chart** where grey bars represent total monthly revenue for all genres, overlaid with a blue line showing the monthly trend for the top-performing genre. This allows visual comparison of the genre’s sales performance within the broader trend.  

---
```