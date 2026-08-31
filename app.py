import sys
import os
import importlib.util

# Change the working directory so Flask finds the templates/ and static/ folders
inner_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'synthesis_route_finder'))
os.chdir(inner_dir)

# Load the inner app.py dynamically to avoid circular import with the root app.py
inner_app_path = os.path.join(inner_dir, 'app.py')
spec = importlib.util.spec_from_file_location("inner_app", inner_app_path)
inner_app = importlib.util.module_from_spec(spec)
sys.modules["inner_app"] = inner_app
spec.loader.exec_module(inner_app)

# Expose the Flask app object for Gunicorn
app = inner_app.app