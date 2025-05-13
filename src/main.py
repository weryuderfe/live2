import os
import sys

# Add the src directory to the path for imports
sys.path.insert(0, os.path.abspath("."))

# Import the main application
from app import main

if __name__ == "__main__":
    main()