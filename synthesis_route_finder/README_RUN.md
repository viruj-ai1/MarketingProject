# How to Run the App

## The Problem
You have TWO different Python environments:
1. **Conda environment** named "venv" (shown as `(venv)` in terminal)
2. **Project venv folder** (`.\venv\`) - This is where ALL your packages are installed

## The Solution

**ALWAYS use the project's venv Python, NOT the conda Python:**

### Option 1: Use the batch file (Easiest)
```powershell
.\run_app.bat
```

### Option 2: Use venv Python directly
```powershell
.\venv\Scripts\python.exe app.py
```

### Option 3: Activate project venv first
```powershell
# Deactivate conda venv first
conda deactivate

# Activate project venv
.\venv\Scripts\activate

# Now run app
python app.py
```

## Why This Happens
- When you type `python app.py`, it uses whatever Python is first in your PATH
- Your conda environment is active, so it uses conda Python (which doesn't have packages)
- The project venv folder has all packages, so you MUST use that Python

## Quick Fix
Always use: `.\venv\Scripts\python.exe app.py` instead of `python app.py`

