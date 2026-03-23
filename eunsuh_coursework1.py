import os

inventory = {}

# sample data
sample1 = {"name": "Laptop", "brand": "Dell", "category": "Electronics", "quantity": 5, "price": 799.99}
sample2 = {"name": "Chair", "brand": "IKEA", "category": "Home", "quantity": 10, "price": 49.99}

inventory[1] = sample_product_1
inventory[2] = sample_product_2

product_ids = {1, 2}
next_id = 3

categories = ["Electronics", "Home", "Office", "Food"]
brands = ("Dell", "IKEA", "Samsung")

def add_item():
    global next_id
    name = input("Enter the product name: ").strip()
    category = input("Enter the category(Electronics, Home, Office): ").strip()
    brand = input("Enter the brand name: ").strip()
    quantity = int(input("Enter the quantity: ").strip())
    price = float(input("Enter the price: ").strip())

    item = {"name": name, "brand": brand, "category": category, "quantity": quantity, "price": price}
    inventory[next_id] = item
    product_ids.add(next_id)
    print(f"\nID {next_id} item has been added!\n")
    next_id += 1

