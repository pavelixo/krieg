## Getting Started

Follow these steps to get started with the **Krieg** framework:

### Prerequisites

Make sure you have Python 3.10 or later installed. You can download it from [here](https://www.python.org/downloads/).

### Step 1: Install Krieg and Uvicorn

To install Krieg and Uvicorn, use pip:

```bash
pip install krieg uvicorn
```

### Step 2: Create a Simple API

Once you have Krieg installed, you can create a simple API. Here's an example of how to create a basic endpoint that returns a message:

1. Create a new Python file, e.g., `main.py`.
2. Add the following code to `main.py`:

```python
from krieg import Krieg

app = Krieg()

@app.get("/")
async def read_root():
    return {"message": "Hello, Krieg Framework!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### Step 3: Run the Application

To run the application, use the following command in your terminal:

```bash
python app.py
```