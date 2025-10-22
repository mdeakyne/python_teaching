# Day 13: Styling & Theming Visualizations  
**Week:** 2  
**Difficulty:** Intermediate  
**Duration:** 3–5 minutes  

---

## Introduction
At Page Turner Analytics, stakeholders love beautiful charts almost as much as great books. Last week, you learned how to customize layouts, annotate points, and create compelling visual stories from sales and review data. Today, we'll take that one step further—making sure our charts share a **consistent visual identity**. Just like the bookstore keeps its signage, shelves, and flyers aligned to its brand, we'll learn to apply **color palettes, themes, and style sheets** in Python so our visualizations look polished, professional, and publication-ready.

---

## Core Content

### 1. Color Palettes
A **color palette** is a set of predefined colors you use consistently across charts. In data visualization, this ensures related charts feel part of the same "series" and that categorical distinctions are clear.  
In a bookstore analogy: imagine your *fiction* section always labeled in deep blue, *non-fiction* in green, and *children's books* in yellow. Repeat those colors everywhere—sales charts, review summaries—so viewers instantly recognize them.

Why it matters:
- Improves readability and memorability.
- Reinforces brand identity (e.g., Page Turner's logo colors).
- Avoids confusion when comparing multiple visualizations.

We’ll use built-in palettes from Plotly (`px.colors.qualitative`) or custom hex codes for brand colors.

---

### 2. Themes and Style Sheets
Themes are predefined combinations of fonts, colors, and layout settings. Plotly offers templates like `"plotly_white"`, `"ggplot2"`, and `"presentation"`.  
Style sheets are template files or Python dictionaries where you define all your visualization rules once. Then, you reuse them across your notebooks—like having a “house style” guide for your graphs.

Bookstore analogy: think of a style guide for marketing flyers—font choice, logo placement, header size—it saves time and keeps everything looking consistent.

---

### 3. Preparing Publication-Ready Visualizations
A chart is "publication-ready" when it’s visually appealing, easy to understand, and matches professional standards. That means:
- High resolution for printing or slides.
- Consistent spacing, margins, and font sizes.
- Color accessibility (consider color-blind friendly palettes).
- No unnecessary chart junk—keep it clean.

In a Page Turner sales report for investors, using well-styled plots ensures your message is clear and the presentation polished—turning data into persuasive storytelling.

---

## Code Examples

### Example 1: Applying a Consistent Color Scheme
```python
import plotly.express as px
import pandas as pd

# Load sales data
sales = pd.read_csv("sales.csv")
books = pd.read_csv("books.csv")

# Merge to get genre info
df = sales.merge(books, on="book_id")

# Aggregate sales quantity by genre
genre_sales = df.groupby("genre")["quantity"].sum().reset_index()

# Define a custom color palette for genres
genre_colors = {
    "Fiction": "#2a3eb1",   # Blue
    "Non-Fiction": "#2ca02c", # Green
    "Children": "#ff7f0e",    # Orange
    "Poetry": "#d62728"       # Red
}

fig = px.bar(
    genre_sales,
    x="genre",
    y="quantity",
    color="genre",
    color_discrete_map=genre_colors,
    title="Total Sales by Genre"
)

fig.update_layout(template="plotly_white")
fig.show()

# Expected output: A clean bar chart with each genre shown in brand-specific colors and white background.
```

---

### Example 2: Using a Plotly Theme Template
```python
# Same data prep as above
fig = px.bar(
    genre_sales,
    x="genre",
    y="quantity",
    color="genre",
    color_discrete_map=genre_colors,
    title="Total Sales by Genre (Professional Theme)"
)

# Use ggplot2-inspired theme
fig.update_layout(template="ggplot2", font=dict(family="Arial", size=14))
fig.show()

# Expected output: ggplot2-style bar chart with Arial font, ready for inclusion in a report.
```

---

### Example 3: Consistent Styling Across Multiple Charts
```python
# Define a reusable layout style
base_template = dict(
    template="plotly_white",
    font=dict(family="Arial", size=12, color="#333"),
    title=dict(font=dict(size=18))
)

# First chart: Sales
fig1 = px.line(df, x="date", y="quantity", color="genre",
               color_discrete_map=genre_colors, title="Daily Sales by Genre")
fig1.update_layout(**base_template)

# Second chart: Ratings
reviews = pd.read_csv("reviews.csv").merge(books, on="book_id")
avg_rating = reviews.groupby("genre")["rating"].mean().reset_index()
fig2 = px.bar(avg_rating, x="genre", y="rating", color="genre",
              color_discrete_map=genre_colors, title="Average Ratings by Genre")
fig2.update_layout(**base_template)

fig1.show()
fig2.show()

# Expected output: Two charts with consistent colors, fonts, and template styling.
```

---

## Common Pitfalls
1. **Inconsistent color assignments:**  
   If "Fiction" is blue in one chart and red in another, viewers get confused. Always define a color map dictionary and reuse it.

2. **Ignoring accessibility:**  
   Some color combinations are hard to distinguish for color-blind users. Use palettes like `px.colors.qualitative.Safe`.

3. **Overly busy designs:**  
   Adding too many colors, fonts, or decorations can distract from the data. Keep styles clean and focused on clarity.

---

## Practice Checkpoint
✅ I can apply the same color palette across multiple charts.  
✅ I can choose and apply a professional theme or template to my visualizations.  
✅ I can produce charts that are clean, consistent, and ready for publication.

---
**Tip:** A well-styled chart is like a well-designed book cover—inviting, engaging, and true to its story.