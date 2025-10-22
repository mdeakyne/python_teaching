**DAY 6/21: Merging Datasets – Authors, Books, Sales 📚**

Today I discovered how powerful dataset merges can be for unlocking business insights. By combining different sources of information — authors, books, and sales data — I learned how to create a single, cohesive view of the bookstore’s performance.

🎯 **Key Takeaway:** The right merge keys and join types can make or break your analysis — choosing wisely ensures you keep the data you need without introducing errors.

💻 **What I Built:** I simulated working at *Page Turner Analytics*, where each table told part of the story: author details from one dataset, book inventory from another, and daily sales logs from a third. Using `merge`, `join`, and `concat` in Pandas, I brought them together seamlessly, experimenting with inner, left, and outer joins to see how the shape of the data changed. This exercise really clarified how different join types impact the completeness and scope of the final analysis.

```python
authors_books = pd.merge(authors, books, on="author_id", how="inner")
full_data = pd.merge(authors_books, sales, on="book_id", how="left")
summary = full_data.groupby("author_name")["sales_amount"].sum()
```

📈 **Progress:** 28% complete — over a quarter of the way through the bootcamp!  

🚀 **Tomorrow:** Time Series Basics — exploring daily book sales trends and patterns over time.  

❓ **Question for you:** When combining datasets in your projects, do you prefer starting with an inner join for precision or a left join for completeness?  

#100DaysOfCode #DataScience #Python #Pandas #Dash #DataVisualization #Day6of21