import os

inventory = {}

# sample data
sample1 = {"name": "Laptop", "brand": "Dell", "category": "Electronics", "quantity": 5, "price": 799.99}
sample2 = {"name": "Chair", "brand": "IKEA", "category": "Home", "quantity": 10, "price": 49.99}

inventory[1] = sample1
inventory[2] = sample2

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

def menu():
    while True:
        print("1. Add Item")
        print("2. Retrieve Stock")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Exit")
        choice = input("Select Option: ").strip()

        if choice == "1":
            add_item()
        elif choice == "2":
            retrieve_inventory()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            print("Exit Program")
            break
        else:
            print("Incorrect choice. Please try again..\n")

def retrieve_inventory():
    if not inventory:
        print("No Item.\n")
        return
    for pid, item in inventory.items():
        print(f"ID: {pid} | Name: {item['name']} | Brand: {item['brand']} | Category: {item['category']}")
        print(f"Quantity: {item['quantity']} | Price: ${item['price']:.2f}\n")

def update_item():
    pid = int(input("Enter ID to update: "))
    if pid in inventory:
        new_qty = int(input("Enter new quantity: "))
        inventory[pid]['quantity'] = new_qty
        print("Stock has been updated!\n")
    else:
        print("The ID does not exist.\n")

def delete_item():
    pid = int(input("Enter ID to delete: "))
    if pid in inventory:
        del inventory[pid]
        product_ids.discard(pid)
        print("Item has been deleted!\n")
    else:
        print("The ID does not exist.\n")

# Product Class
class Product:
    def __init__(self, product_id, name, brand, category, quantity, price):
        self.id = product_id
        self.name = name
        self.brand = brand
        self.category = category
        self.quantity = quantity
        self.price = price

    def update_quantity(self, new_qty):
        self.quantity = new_qty

    def display(self):
        print(f"ID: {self.id} | {self.name} | {self.brand} | {self.category}")
        print(f"Quantity: {self.quantity} | Price: ${self.price:.2f}")

# PerishableProduct child class
class PerishableProduct(Product):
    def __init__(self, product_id, name, brand, category, quantity, price, expiration_date):
        super().__init__(product_id, name, brand, category, quantity, price)
        self.expiration_date = expiration_date

    def display(self):
        super().display()
        print(f"Expiry Date: {self.expiration_date}")

# Save File
def save_inventory_to_file():
    with open("inventory.txt", "w") as f:
        for pid, item in inventory.items():
            line = f"{pid}|{item['name']}|{item['brand']}|{item['category']}|{item['quantity']}|{item['price']}"
            f.write(line + "\n")

# Load File
def load_inventory_from_file():
    global next_id
    try:
        with open("inventory.txt", "r") as f:
            for line in f:
                parts = line.strip().split("|")
                pid = int(parts[0])
                name, brand, category = parts[1], parts[2], parts[3]
                quantity, price = int(parts[4]), float(parts[5])
                inventory[pid] = {"name": name, "brand": brand, "category": category, "quantity": quantity, "price": price}
                product_ids.add(pid)
                next_id = max(next_id, pid + 1)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    load_inventory_from_file()
    menu()
    save_inventory_to_file()