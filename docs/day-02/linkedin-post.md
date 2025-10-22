```markdown
**DAY 2/21: DataFrame Basics – Creating & Inspecting Data**

Today I discovered the essential skill of reading CSV files into Pandas DataFrames and exploring them to quickly understand the shape and structure of the data.  

🎯 **Key Takeaway:** Being able to inspect data efficiently is the first step toward uncovering meaningful patterns and insights.  

💻 **What I Built:** I loaded bookstore sales data into a Pandas DataFrame and explored it using key inspection methods. I checked column names, data types, and summarized statistics to get a clearer picture of the dataset. This process helped me spot potential data quality issues early — something critical before deeper analysis begins.  

```python
import pandas as pd

df = pd.read_csv("bookstore_sales.csv")
print(df.head())
print(df.info())
print(df.describe())
```

📈 **Progress:** 9% through the bootcamp  

🚀 **Tomorrow:** Data Selection & Filtering – Finding the Right Books  

💬 **Question for you:** When you start a new dataset, what’s the very first thing you check to understand its structure?  

#100DaysOfCode #DataScience #Python #Pandas #Dash #DataVisualization #Day2of21
```