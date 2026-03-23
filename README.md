# Inventory Management System

A simple command-line inventory management program that lets you add, view, update, and remove products while demonstrating Python data structures, functions, and OOP.

## How to run

From the project directory, run:

```bash
python3 eunsuh_coursework1.py
```

## Features implemented

- Basic setup using an `inventory` dictionary (stores `Product` / `PerishableProduct` objects by ID)
- Sample item data loaded from `inventory.txt` when the program starts
- Add items using `input()` and store fields like name (string), quantity (int), and price (float)
- Neatly formatted inventory display (shows ID, name, brand, category, quantity, price; and expiration date for perishable items)
- Categories stored in a list; user selects a category from the list
- Brands stored in a tuple; user selects a brand from the list
- Unique product IDs tracked using a `set`
- Menu-driven loop with conditional statements:
  - Add Item
  - Retrieve Stock
  - Update Item
  - Delete Item
  - Exit (saves to file)
- Separate functions for adding, retrieving, updating, and deleting items
- OOP:
  - `Product` class with attributes and methods (`update_quantity`, `display`)
  - `PerishableProduct` subclass that adds `expiration_date` and overrides `display`
- File handling:
  - `load_inventory_from_file()` loads from `inventory.txt` at startup
  - `save_inventory_to_file()` saves back to `inventory.txt` when exiting
- Basic input validation using `try/except` for numeric inputs (quantity, price, and menu/category/brand selection)

## Limitations / Known issues

- `Update Item` searches by product **name** (case-insensitive), not by ID.
- The `inventory.txt` file format is a simple pipe-delimited string; if the file contains malformed lines, parsing may fail.
- Perishable expiration date is stored as a string; there is no strict date format validation beyond reading input.
