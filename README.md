<div align="center">
    <img src="https://imgur.com/PHVUbTR.png" alt="Krieg logo" width="150" />
</div>

# Krieg framework
The **Krieg** is a minimal, lightweight asynchronous web framework built with Python, focusing on simplicity and performance. Built on **aiohttp**, it efficiently handles concurrent requests in a non-blocking manner, offering high performance for scalable web applications.

## Installation

To install the Krieg, simply use pip:

```bash
pip install krieg
```

## Quick Start

Here's a example of how to create a simple API with Krieg:

```python
from krieg import Krieg

app = Krieg()

@app.get("/")
async def read_root():
    return {"message": "Hello, Krieg Framework!"}
```
## Documentation

The **Krieg** framework provides a set of simple and efficient features for asynchronous web development. You can find detailed documentation [here](docs/README.md).

## License

Krieg is open-source and released under the MIT License. See the [LICENSE](https://chatgpt.com/c/LICENSE) file for more information.
