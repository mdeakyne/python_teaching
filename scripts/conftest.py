"""Test configuration for scripts package.

This conftest.py adds the scripts directory to sys.path so that tests can
import the scripts package without requiring PYTHONPATH configuration.
"""

import sys
from pathlib import Path

# Add the scripts directory to sys.path
scripts_dir = Path(__file__).parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))
