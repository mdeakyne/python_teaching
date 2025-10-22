Day 10/21: Plotly Express – Interactive Basics 📊  

Today I explored **Plotly Express** and learned how easy it is to create interactive charts directly from a pandas DataFrame. The magic lies in how quickly you can transform raw data into visuals where hovering, zooming, and filtering give deeper insights without writing complex code.  

🎯 **Key Takeaway:** Interactive data visualizations help teams uncover patterns faster and make better decisions with minimal effort.  

💻 **What I Built:** I created a scatter plot showing book genres vs. sales volume, enriched with hover data for author names and average ratings. This allowed the fictional **Page Turner Analytics** sales team to instantly see which genres outperform in terms of both quantity and reader satisfaction—all in a browser-ready interactive chart.  

```python
import plotly.express as px  
fig = px.scatter(df, x="sales", y="genre", size="avg_rating", hover_name="author")  
fig.show()
```

📈 **Progress:** 47% through the bootcamp!  

🚀 **Tomorrow:** Advanced Plotly – Multiple Traces & Subplots, diving deeper into custom layouts and combining different chart types for storytelling.  

❓ **Question for you:** If you could make one dataset in your work fully interactive, which would it be—and how would it change your analysis?  

#100DaysOfCode #DataScience #Python #Pandas #Dash #DataVisualization #Day10of21