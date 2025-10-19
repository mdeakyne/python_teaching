# Getting Started

Welcome to the Python Training Materials! This guide will help you get set up and ready to learn.

## What You'll Need

Before diving into the training materials, make sure you have:

- **Python 3.11 or higher** installed on your system
- **Basic command-line familiarity** (running commands, navigating directories)
- **A code editor or IDE** (VS Code, PyCharm, or your preference)
- **Git** for cloning the repository (optional but recommended)

## Installation Options

You have two main ways to use these materials:

### Option 1: View Online (Easiest)

If the documentation is deployed, you can simply browse it online without any installation.

### Option 2: Local Setup (Recommended for Hands-On Learning)

For the full experience with code execution and experimentation:

1. **Clone the repository**
   ```bash
   git clone https://github.com/mdeakyne/python_teaching.git
   cd python_teaching
   ```

2. **Install uv** (if not already installed)
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```

You're now ready to work through the tutorials and run the code examples!

## Next Steps

- [Installation Details](installation) - Detailed installation instructions
- [Environment Setup](setup) - Configure your development environment
- [How to Use These Materials](how-to-use) - Tips for getting the most out of this course

## Learning Paths

Not sure where to start? Here are some suggested learning paths:

**New to Python?**
Start with the basics in each track, beginning with Automation & Scripting for fundamental concepts.

**Data-focused?**
Jump into the Data Science & Analysis track to work with pandas and numpy.

**Building web apps?**
Head to Web Development to learn FastAPI and HTTP.

**Want to write better code?**
Check out Testing & Quality to learn professional development practices.

Choose your track from the sidebar and let's get started!
