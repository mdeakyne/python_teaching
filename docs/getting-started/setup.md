# Environment Setup

Configure your development environment for the best learning experience.

## Code Editor Setup

### VS Code (Recommended)

VS Code provides excellent Python support with extensions.

1. **Install VS Code** from [code.visualstudio.com](https://code.visualstudio.com/)

2. **Install Python extension**
   - Open VS Code
   - Go to Extensions (Cmd/Ctrl + Shift + X)
   - Search for "Python" by Microsoft
   - Click Install

3. **Select Python interpreter**
   - Open the project folder
   - Press Cmd/Ctrl + Shift + P
   - Type "Python: Select Interpreter"
   - Choose the `.venv` interpreter

4. **Recommended Extensions**
   - Python (Microsoft) - Core Python support
   - Pylance - Fast language server
   - Jupyter - Notebook support
   - Ruff - Fast linting and formatting

### PyCharm

PyCharm is another excellent IDE for Python.

1. Open the project folder in PyCharm
2. PyCharm will detect the virtual environment automatically
3. Configure the interpreter: Settings → Project → Python Interpreter → Select `.venv`

### Other Editors

Any text editor works! Just make sure you:
- Activate the virtual environment in your terminal
- Can run Python from the command line

## Jupyter Notebook Setup

For interactive lessons with notebooks:

```bash
# Start Jupyter Notebook
uv run jupyter notebook

# Or Jupyter Lab (more features)
uv run jupyter lab
```

Your browser will open with the Jupyter interface. Navigate to lesson notebooks to work through them interactively.

## Verifying Your Setup

Test that everything works:

```bash
# Check Python version
python --version

# Check installed packages
uv pip list

# Run a simple test
python -c "import pandas as pd; print('Setup successful!')"
```

## Building the Documentation

To build and view the Jupyter Book documentation locally:

```bash
# Build the book
uv run jupyter-book build docs/

# Open in browser
# macOS
open docs/_build/html/index.html

# Linux
xdg-open docs/_build/html/index.html

# Windows
start docs/_build/html/index.html
```

## Optional: Pre-commit Hooks

For contributors or those wanting to follow best practices:

```bash
# Install pre-commit
uv pip install pre-commit

# Set up git hooks
pre-commit install
```

This will automatically format and check your code before commits.

## Next Steps

Your environment is ready! Head to [How to Use These Materials](how-to-use) to learn how to get the most out of the training.
