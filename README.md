# Retirement Calculator

A Python-based retirement portfolio analysis tool that visualizes nominal and real portfolio growth, along with passive income projections.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

### 1. Clone or download the project

### 2. Create a virtual environment (recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```


## Running the Application

```bash
python main.py
```

Then open http://127.0.0.1:5000/

This will generate three plots showing:
1. Nominal portfolio composition
2. Real portfolio composition (adjusted for inflation)
3. Monthly passive income development

## IDE Setup

### PyCharm
1. Open the project folder in PyCharm
2. Go to **File → Settings → Project → Python Interpreter**
3. Click the gear icon → **Add**
4. Select **Existing environment** and choose the `venv` folder created above
5. Run `main.py` using the green play button

### VS Code
1. Open the project folder in VS Code
2. Install the Python extension
3. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
4. Type "Python: Select Interpreter" and choose the venv interpreter
5. Run with `F5` or the Run button

### Other IDEs
Most Python IDEs support virtual environments. Point your IDE's Python interpreter to the `venv/bin/python` (Mac/Linux) or `venv\Scripts\python.exe` (Windows) file.


###