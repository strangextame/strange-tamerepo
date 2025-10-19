# Code Style Guide

The MTG Card Finder codebase follows the **Google Python Style Guide** with a few project‑specific conventions.

## General Python Guidelines

- **Indentation**: 4 spaces, no tabs.  
- **Line Length**: Maximum 100 characters.  
- **Imports**: Standard library imports first, then third‑party, then local imports, each group separated by a blank line.  
- **Naming**:
  - Variables & functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

## Docstrings

All public functions, classes, and modules must include a **Google‑style** docstring.

### Module‑level Docstring (example)

```python
"""
MTG Card Finder Flask Application
Provides a simple web interface to search Magic: The Gathering cards via the Scryfall API.
"""
```

### Function Docstring (example)

```python
def search():
    """Handle card search requests.

    Retrieves the card name from the submitted form, queries the Scryfall API,
    and renders either the results page or an error page.

    Returns:
        flask.Response: Rendered ``results.html`` with card data or
        ``error.html`` with an error message.
    """
```

## Commenting

- Use inline comments sparingly to explain *why* something is done, not *what* the code does.
- Block comments should start with a capital letter and end with a period.

## Linting

- Run `flake8` and `pylint` to ensure compliance.
- Use `black` for automatic code formatting.

Adhering to these guidelines helps maintain readability and consistency across the project.