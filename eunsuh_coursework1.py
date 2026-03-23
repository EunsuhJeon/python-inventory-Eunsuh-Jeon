import os

inventory = {}
product_ids = set()
next_id = 3

# sample data
sample1 = {"name": "Laptop", "brand": "Dell", "category": "Electronics", "quantity": 5, "price": 799.99}
sample2 = {"name": "Chair", "brand": "IKEA", "category": "Home", "quantity": 10, "price": 49.99}

inventory[1] = sample1
inventory[2] = sample2

# product_ids = {1, 2}
# next_id = 3

categories = ["Electronics", "Home", "Office", "Food"]
brands = ("Dell", "IKEA", "Samsung", "Other")

def add_item():
    global next_id
    name = input("Enter the product name: ").strip()
    category = input("Enter the category(Electronics, Home, Office): ").strip()
    brand = input("Enter the brand name: ").strip()
    quantity = int(input("Enter the quantity: ").strip())
    price = float(input("Enter the price: ").strip())

    perishable = input("Perishable Product? (y/n): ").strip().lower() == "y"
    if perishable:
        exp = input("Enter the expiration date (YYYY-MM-DD): ").strip()
        inventory[next_id] = PerishableProduct(
            next_id, name, brand, category, quantity, price, exp
        )
    else:
        inventory[next_id] = Product(
            next_id, name, brand, category, quantity, price
        )

    # item = {"name": name, "brand": brand, "category": category, "quantity": quantity, "price": price}
    # inventory[next_id] = item
    product_ids.add(next_id) 
    next_id += 1

    print(f"\nID {next_id} item has been added!\n")

def menu():
    while True:
        print("===========================================")
        print("1. Add Item")
        print("2. Retrieve Stock")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Exit")
        print("===========================================")
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
            print("Saving inventory to file...")
            save_inventory_to_file()
            print("Exiting system. Goodbye!")
            break
        else:
            print("Incorrect choice. Please try again..\n")

def retrieve_inventory():
    if not inventory:
        print("No Items.\n")
        return
    print("Current Inventory:\n--------------------------------")

    # for pid, item in inventory.items():
    #     print(f"ID: {pid} | Name: {item['name']} | Brand: {item['brand']} | Category: {item['category']}")
        # print(f"Quantity: {item['quantity']} | Price: ${item['price']:.2f}\n")
    for pid in sorted(inventory):
        inventory[pid].display()
        print()

def update_item():
    # pid = int(input("Enter ID to update: "))
    name = input("Enter product name to update: ").strip()
    for pid, product in inventory.items():
        if product.name.lower() == name.lower():
            new_quantity = int(input("Enter new quantity: ").strip())
            product.update_quantity(new_quantity)
            print("Stock has been updated!\n")
            return
    print("Product not found.\n")

def delete_item():
    pid = int(input("Enter ID to delete: "))
    if pid in inventory:
        del inventory[pid]
        product_ids.discard(pid)
        print("Item has been deleted!\n")
    else:
        print("The ID does not exist.\n")

def choose_category():
    print("Choose a category:")
    for i,c in enumerate(categories, start=1):
        print(f" {i}. {c}")
    while True:
        raw = input("Select category: ").strip()
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(categories):
                return categories(idx)
        except ValueError:
            pass
        print("Invalid category. Please try again.\n")

def choose_brand():
    print("Choose a brand: ")
    for i,b in enumerate(brands, start=1):
        print(f" {i}. {b}")
    while True:
        raw = input("Select brand: ").strip()
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(brands):
                return brands[idx]
        except ValueError:
            pass
        print("Invalid brand. Please try again.\n")

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
def save_inventory_to_file(path="inventory.txt"):
    with open(path, "w", encoding="utf-8") as f:
        for pid, p in inventory.items():
            if isinstance(p, PerishableProduct):
                line = f"{pid}|{p.name}|{p.brand}|{p.category}|{p.quantity}|{p.price}|P|{p.expiration_date}\n"
            else:
                line = f"{pid}|{p.name}|{p.brand}|{p.category}|{p.quantity}|{p.price}|N|\n"
            f.write(line)

# Load File
def load_inventory_from_file(path="inventory.txt"):
    global next_id
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                pid = int(parts[0])
                name, brand, category = parts[1], parts[2], parts[3]
                qty, price = int(parts[4]), float(parts[5])
                kind = parts[6] if len(parts) > 6 else "N"
                if kind == "P" and len(parts) > 7:
                    inventory[pid] = PerishableProduct(
                        pid, name, brand, category, qty, price, parts[7]
                    )
                else:
                    inventory[pid] = Product(
                        pid, name, brand, category, qty, price
                    )
                product_ids.add(pid)
                next_id = max(next_id, pid + 1)
    except FileNotFoundError:
        pass

def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())
            if value >= 0:
                return value
            print("Please enter a non-negative integer.")
        except ValueError:
            print("Invalid number. Try again.")

def read_price(prompt):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Invalid price. Try again.")

if __name__ == "__main__":
    load_inventory_from_file()
    menu()
    save_inventory_to_file()