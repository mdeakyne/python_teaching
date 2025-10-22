Today I explored **chart selection** as part of my data storytelling journey — learning how the right visual can make insights crystal clear. Picking the wrong chart can hide trends or confuse the audience, while the right one turns numbers into a narrative anyone can understand.  

🎯 **Key Takeaway:** Every dataset has a “best-fit” visual — choose with purpose, not habit.  

💻 **What I Built:** I simulated book sales data by genre and experimented with line charts, bar charts, and stacked area charts to find the clearest way to compare trends. I then added simple annotations to highlight peak sales months and sudden shifts, turning raw output into a story my audience could act on.  

```python
import pandas as pd
import matplotlib.pyplot as plt

df = sales_df.groupby("Month")["Fiction", "Non-Fiction"].sum()
df.plot(kind="line", marker="o")
plt.annotate("Holiday boost", xy=("Dec", df.loc["Dec","Fiction"]))
plt.show()
```

📈 **Progress:** 57% through the bootcamp — and starting to think visually first when tackling data problems.  

🚀 **Tomorrow:** Styling & Theming Visualizations — moving from clear charts to beautiful ones.  

How do *you* decide which chart type to use when telling a data story? Share your go-to approach!  

#100DaysOfCode #DataScience #Python #Pandas #Dash #DataVisualization #Day12of21