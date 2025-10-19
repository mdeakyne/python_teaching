# Installation

Detailed instructions for setting up your Python development environment.

## Python Installation

### macOS

```bash
# Using Homebrew
brew install python@3.11

# Verify installation
python3 --version
```

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Fedora
sudo dnf install python3.11

# Verify installation
python3 --version
```

### Windows

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify in Command Prompt:
   ```cmd
   python --version
   ```

## Installing uv

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver, used for managing dependencies in this project.

### macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Verify uv Installation

```bash
uv --version
```

## Setting Up the Project

1. **Clone the repository**
   ```bash
   git clone https://github.com/mdeakyne/python_teaching.git
   cd python_teaching
   ```

2. **Install all dependencies**
   ```bash
   uv sync
   ```

   This will:
   - Create a virtual environment in `.venv/`
   - Install all project dependencies
   - Set up Jupyter Book and all learning track packages

3. **Activate the virtual environment**
   ```bash
   # macOS/Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

   You should see `(.venv)` in your terminal prompt.

## Troubleshooting

### Python version issues

If you have multiple Python versions:
```bash
# Specify Python version for uv
uv sync --python 3.11
```

### Permission errors (macOS/Linux)

```bash
# Don't use sudo with uv
# If you get permission errors, check directory ownership
ls -la
```

### Windows PATH issues

If `python` or `uv` commands aren't found, add them to your PATH:
1. Search "Environment Variables" in Windows
2. Edit PATH variable
3. Add Python and uv installation directories

## Next Steps

Once installation is complete, proceed to [Environment Setup](setup) to configure your editor and tools.
