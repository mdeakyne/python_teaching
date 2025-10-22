```markdown
**DAY 5/21 – Aggregation & GroupBy: Sales by Genre 📊**

Today I explored how **`groupby`** and **aggregation functions** can turn raw sales data into actionable insights.  

🎯 **Key Takeaway:** With just a few lines of Pandas code, you can reveal your top-performing genres and star authors—crucial intel for any marketing strategy.  

💻 **What I Built:**  
I analyzed our fictional dataset from *Page Turner Analytics* to find which genres drive the highest sales, then drilled down to see which authors dominate within each genre. Using pivot tables, I transformed long-format data into a clear, visual summary for decision-makers. The result? Immediate visibility into revenue distribution, making it easier to prioritize marketing spend.  

```python
sales_by_genre = df.groupby('Genre')['Revenue'].sum().sort_values(ascending=False)
top_authors = df.groupby(['Genre', 'Author'])['Revenue'].sum()
pivot_table = df.pivot_table(values='Revenue', index='Genre', columns='Author', aggfunc='sum')
print(sales_by_genre.head())
```

📈 **Progress:** 23% through the bootcamp, and feeling more comfortable turning questions into data-driven answers.  

🚀 **Tomorrow’s Focus:** Merging datasets—connecting Authors, Books, and Sales to unlock deeper analysis.  

❓ **Question for you:** When you analyze your data, do you start with broad trends first—or dive straight into granular detail?  

#100DaysOfCode #DataScience #Python #Pandas #Dash #DataVisualization #Day5of21 #LearningJourney #Upskilling
```