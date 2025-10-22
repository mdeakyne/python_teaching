**DAY 11/21: Advanced Plotly – Multiple Traces & Subplots**  

Today I discovered how to harness **Plotly graph objects** to create powerful visualizations with **multiple traces** and **subplots**—unlocking the ability to tell richer, more nuanced data stories.  

🎯 **Key Takeaway:** Combining multiple traces in a single figure allows you to compare different data sets side-by-side while maintaining clarity and visual appeal.  

💻 **What I Built:**  
I simulated a request from a fictional company, **Page Turner Analytics**, to visualize sales trends for multiple book genres over time. Using Plotly’s `make_subplots` and `go.Scatter`, I created a dashboard-style figure where each subplot displayed a genre’s sales trend, and custom layouts ensured a clean, aligned presentation. This approach improves interpretability for stakeholders by keeping related insights together while offering individual detail for each category.  

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=1, cols=2, subplot_titles=("Fiction", "Non-Fiction"))
fig.add_trace(go.Scatter(x=dates, y=fiction_sales, name="Fiction"), row=1, col=1)
fig.add_trace(go.Scatter(x=dates, y=nonfiction_sales, name="Non-Fiction"), row=1, col=2)
fig.update_layout(title="Sales Trends by Genre")
fig.show()
```

📈 **Progress:** 52% through the bootcamp!  

🚀 **Tomorrow:** Diving into **Data Storytelling – Choosing the Right Chart** to make insights resonate even more.  

💬 **Question for you:** How do you decide when to use subplots versus layering multiple traces in one chart for your audience?  

#100DaysOfCode #DataScience #Python #Pandas #Dash #DataVisualization #Day11of21