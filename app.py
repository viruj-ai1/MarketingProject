import sys
import os

# Add the inner directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'synthesis_route_finder')))

# Change the working directory so Flask finds the templates/ and static/ folders
os.chdir('synthesis_route_finder')

# Import the actual application
from app import app

if __name__ == "__main__":
    app.run()