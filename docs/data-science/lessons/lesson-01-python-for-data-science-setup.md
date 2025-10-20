---
title: Python for Data Science Setup
---

# Lesson 01: Python for Data Science Setup

```{admonition} Lesson Info
:class: note
**Duration**: 60 minutes
**Difficulty**: Beginner
**Prerequisites**: Basic computer literacy, willingness to learn
```

## Learning Objectives

By the end of this lesson, you will be able to:

- Set up a Python data science environment on your computer
- Install and configure Jupyter notebooks
- Understand the core data science packages and their purposes
- Run your first data science program and verify your installation

## Introduction

Welcome to **Page Turner Analytics**! 📚

You've just joined our team as a junior data analyst. Our company helps bookstores, libraries, and publishers make data-driven decisions about books. Throughout this course, you'll analyze book sales, reading patterns, and literary trends to answer questions like:

- Which genres are most popular this season?
- Do longer books get better ratings?
- Can we predict which books will become bestsellers?

But first, we need to set up your analyst workstation! Think of this lesson as organizing your bookshelf before you start reading - we'll install all the tools you need to analyze data effectively.

## Why These Tools?

Before we dive into installation, let's understand what we're installing and why:

**Python** is like your favorite library - it's free, welcoming to beginners, and has something for everyone. It's the most popular language for data science because of its:
- Simple, readable syntax (almost like writing in English)
- Massive ecosystem of data tools
- Active community of data scientists sharing solutions

**Key Packages We'll Use:**
- **pandas**: Your data manipulation Swiss Army knife (think: spreadsheets on steroids)
- **numpy**: Fast numerical computing (for crunching numbers efficiently)
- **matplotlib**: Basic plotting library (visualize your insights)
- **seaborn**: Beautiful statistical visualizations (make your plots publication-ready)

## Installing Python

### Option 1: Using uv (Recommended)

`uv` is a modern, fast Python package manager. It's like having a super-efficient librarian who knows exactly where every book (package) is.

```{code-cell} ipython3
# First, install uv (instructions vary by OS)
# On macOS/Linux:
# curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows:
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
!uv --version
```

### Option 2: Using Anaconda

Anaconda is like getting a complete bookstore in one package - it includes Python and hundreds of data science tools pre-installed.

Download from: https://www.anaconda.com/download

```{admonition} Which Should I Choose?
:class: tip
- **uv**: Lightweight, fast, modern (recommended for this course)
- **Anaconda**: Batteries-included, larger download, good for beginners who want everything ready
```

## Setting Up Jupyter Notebooks

Jupyter notebooks are your data science workbench - an interactive environment where you can write code, see results immediately, and document your analysis with notes and visualizations.

Think of a notebook as a lab notebook for data science: you write your experiments (code), record observations (outputs), and add commentary (markdown notes) all in one place.

### Installing Jupyter

```{code-cell} ipython3
# Using uv
!uv pip install jupyter notebook jupyterlab

# Using pip
# pip install jupyter notebook jupyterlab
```

### Starting Jupyter

```{code-cell} ipython3
# Launch Jupyter Notebook (classic interface)
# jupyter notebook

# Or launch JupyterLab (modern interface - recommended)
# jupyter lab
```

This will open Jupyter in your web browser. Don't worry - it's not actually on the internet; it's running locally on your computer!

```{admonition} Jupyter Shortcuts to Know
:class: note
- **Shift + Enter**: Run current cell and move to next
- **Ctrl/Cmd + Enter**: Run current cell and stay in it
- **Esc then A**: Insert cell above
- **Esc then B**: Insert cell below
- **Esc then D, D**: Delete current cell
```

## Installing the Data Science Stack

Now let's install the core packages we'll use throughout the course:

```{code-cell} ipython3
# Install all essential packages at once
!uv pip install pandas numpy matplotlib seaborn jupyter

# Or with regular pip:
# pip install pandas numpy matplotlib seaborn jupyter
```

Let's break down what each package does:

- **pandas**: Data manipulation (our main tool for working with book data)
- **numpy**: Numerical arrays and mathematical operations
- **matplotlib**: Basic plotting and visualization
- **seaborn**: Statistical visualizations built on matplotlib
- **jupyter**: Interactive notebook environment

## Verifying Your Installation

Time to make sure everything works! Create a new Jupyter notebook and run this verification script:

```{code-cell} ipython3
# Import all packages and display versions
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

print("📚 Page Turner Analytics - Environment Check")
print("=" * 50)
print(f"✓ pandas version: {pd.__version__}")
print(f"✓ numpy version: {np.__version__}")
print(f"✓ matplotlib version: {matplotlib.__version__}")
print(f"✓ seaborn version: {sns.__version__}")
print("=" * 50)
print("🎉 All packages loaded successfully!")
print("You're ready to start analyzing book data!")
```

**Expected Output:**
```
📚 Page Turner Analytics - Environment Check
==================================================
✓ pandas version: 2.2.0
✓ numpy version: 1.26.0
✓ matplotlib version: 3.8.0
✓ seaborn version: 0.13.0
==================================================
🎉 All packages loaded successfully!
You're ready to start analyzing book data!
```

## Your First Data Science Code

Let's create some simple book data and visualize it to confirm everything works:

```{code-cell} ipython3
import pandas as pd
import matplotlib.pyplot as plt

# Create a small sample of book data
books = pd.DataFrame({
    'title': ['Pride and Preprocessing', 'The Great Gatsby Dataframe',
              'To Kill a Mockingbird Dataset', 'War and Python'],
    'pages': [324, 218, 281, 1296],
    'rating': [4.5, 4.8, 4.9, 4.3],
    'price': [12.99, 14.99, 11.99, 19.99]
})

# Display the data
print("📖 Sample Book Catalog:")
print(books)

# Create a simple visualization
plt.figure(figsize=(10, 6))
plt.bar(books['title'], books['rating'], color='skyblue', edgecolor='navy')
plt.xlabel('Book Title', fontsize=12)
plt.ylabel('Average Rating', fontsize=12)
plt.title('Book Ratings at Page Turner Analytics', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 5)
plt.tight_layout()
plt.show()
```

If you see a DataFrame printed and a bar chart displayed, congratulations! Your data science environment is fully functional. 🎉

## Understanding Jupyter Notebook Structure

A Jupyter notebook consists of **cells**. There are two main types:

### Code Cells

These contain Python code that you can run:

```{code-cell} ipython3
# This is a code cell
favorite_book = "The Hitchhiker's Guide to the DataFrame"
print(f"My favorite book is: {favorite_book}")
```

### Markdown Cells

These contain formatted text, like this explanation you're reading now! You can use markdown to:

- Create lists
- **Bold** and *italic* text
- Add [links](https://pandas.pydata.org)
- Include `code snippets`

## Organizing Your Project

Create a folder structure for this course:

```
data-science-course/
├── data/              # Where we'll store book datasets
├── notebooks/         # Your Jupyter notebooks
├── outputs/           # Saved plots and results
└── notes/            # Additional notes and references
```

```{code-cell} ipython3
# Create these folders from Python
import os

folders = ['data', 'notebooks', 'outputs', 'notes']
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✓ Created: {folder}/")
```

## Practice Exercise

```{admonition} Exercise: Verify and Customize
:class: tip

**Part 1: Environment Check**
1. Open a new Jupyter notebook
2. Import pandas, numpy, matplotlib, and seaborn
3. Print the version of each package
4. If any imports fail, reinstall that package

**Part 2: Create Your First Analysis**
1. Create a DataFrame with 5 of your favorite books
2. Include columns: title, author, pages, your_rating
3. Display the DataFrame
4. Calculate and print the average number of pages
5. BONUS: Create a bar chart of your ratings

**Part 3: Document Your Work**
1. Add markdown cells explaining what each code cell does
2. Save your notebook as "lesson-01-setup.ipynb"
3. Close and reopen it to make sure it saved correctly
```

## Common Installation Issues

### Issue: "Command not found" errors

**Solution**: You may need to add Python to your PATH.
- On Mac/Linux: Add to `.bashrc` or `.zshrc`
- On Windows: Check "Add Python to PATH" during installation

### Issue: Package import fails

**Solution**: Make sure you're running the notebook in the same environment where you installed packages:

```{code-cell} ipython3
# Check which Python you're using
import sys
print(f"Python location: {sys.executable}")
```

### Issue: Jupyter won't start

**Solution**: Try reinstalling Jupyter:
```bash
uv pip install --force-reinstall jupyter
```

## Summary

In this lesson, you:

- ✅ Installed Python and essential data science packages
- ✅ Set up Jupyter notebooks for interactive analysis
- ✅ Verified your installation with test code
- ✅ Ran your first data science program with book data
- ✅ Learned basic Jupyter notebook usage

You now have a fully functional data science environment! Your analyst workstation at Page Turner Analytics is ready.

## Next Steps

In **Lesson 02: Introduction to pandas DataFrames**, you'll start working with real book data! We'll load a catalog of books from a CSV file and learn how to inspect and explore the data.

Get ready to dive into DataFrames - pandas' powerful data structure that will become your best friend in data analysis.

## Additional Resources

- [Jupyter Notebook Documentation](https://jupyter-notebook.readthedocs.io/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Python for Data Analysis Book](https://wesmckinney.com/book/) by Wes McKinney
- [Real Python Tutorials](https://realpython.com/)

---

**Happy analyzing! 📚📊**

<!--
INSTRUCTOR NOTES

Skills covered (from references/skills/data-science/):
1. creating-basic-plots-with-matplotlib.md
   - Creating Basic Plots with Matplotlib
   - Difficulty: beginner
2. downloading-and-loading-spacy-statistical-models.md
   - Downloading and Loading spaCy Statistical Models
   - Difficulty: beginner
3. ignoring-files-in-git.md
   - Ignoring Files in Git
   - Difficulty: beginner
4. installing-and-importing-pandas-in-python.md
   - Installing and Importing pandas in Python
   - Difficulty: beginner
5. installing-and-setting-up-cython-for-python-projects.md
   - Installing and Setting Up Cython for Python Projects
   - Difficulty: beginner
6. installing-and-setting-up-dash-environment.md
   - Installing and Setting Up Dash Environment
   - Difficulty: beginner
7. installing-and-upgrading-spacy-in-python.md
   - Installing and Upgrading spaCy in Python
   - Difficulty: beginner
8. installing-and-using-numpy-and-pyaudio-on-raspberry-pi.md
   - Installing and Using numpy and pyaudio on Raspberry Pi
   - Difficulty: beginner
9. installing-and-using-the-pillow-library.md
   - Installing and Using the Pillow Library
   - Difficulty: beginner
10. installing-python-modules-on-raspberry-pi.md
   - Installing Python Modules on Raspberry Pi
   - Difficulty: beginner
-->