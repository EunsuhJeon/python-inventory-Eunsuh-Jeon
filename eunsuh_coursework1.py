import os

inventory = {}
product_ids = set()
next_id = 4

categories = ["Electronics", "Home", "Office", "Food"]
brands = ("Dell", "IKEA", "Samsung", "Other")

def initialize_sample_items(inventory_dict, product_ids_set, start_id):
    sample_items = [
        {"name": "Laptop", "brand": "Dell", "category": "Electronics", "quantity": 5, "price": 799.99},
        {"name": "Chair", "brand": "IKEA", "category": "Home", "quantity": 10, "price": 49.99},
    ]
    current_id = start_id
    for item in sample_items:
        inventory_dict[current_id] = Product(
            current_id,
            item["name"],
            item["brand"],
            item["category"],
            item["quantity"],
            item["price"],
        )
        product_ids_set.add(current_id)
        current_id += 1
    return current_id

def add_item(inventory_dict, product_ids_set, current_next_id):
    name = input("Enter the product name: ").strip()
    category = choose_category()
    brand = choose_brand()
    quantity = read_positive_int("Enter the quantity: ")
    price = read_price("Enter the price: ")

    perishable = input("Perishable Product? (y/n): ").strip().lower() == "y"
    if perishable:
        exp = input("Enter the expiration date (YYYY-MM-DD): ").strip()
        product = PerishableProduct(
            current_next_id, name, brand, category, quantity, price, exp
        )
    else:
        product = Product(
            current_next_id, name, brand, category, quantity, price
        )

    inventory_dict[current_next_id] = product
    product_ids_set.add(current_next_id)
    added_id = current_next_id
    current_next_id += 1

    print(f"\nID {added_id} item has been added!\n")
    return current_next_id

def menu(inventory_dict, product_ids_set, current_next_id):
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
            current_next_id = add_item(inventory_dict, product_ids_set, current_next_id)
        elif choice == "2":
            retrieve_inventory(inventory_dict)
        elif choice == "3":
            update_item(inventory_dict)
        elif choice == "4":
            delete_item(inventory_dict, product_ids_set)
        elif choice == "5":
            print("Saving inventory to file...")
            save_inventory_to_file(inventory_dict)
            print("Exiting system. Goodbye!")
            break
        else:
            print("Incorrect choice. Please try again..\n")
    return current_next_id

def retrieve_inventory(inventory_dict):
    if not inventory_dict:
        print("No Items.\n")
        return
    print("Current Inventory:\n--------------------------------")
    for pid in sorted(inventory_dict):
        inventory_dict[pid].display()
        print()

def update_item(inventory_dict):
    name = input("Enter product name to update: ").strip()
    for _, product in inventory_dict.items():
        if product.name.lower() == name.lower():
            new_quantity = read_positive_int("Enter new quantity: ")
            product.update_quantity(new_quantity)
            print("Stock has been updated!\n")
            return True
    print("Product not found.\n")
    return False

def delete_item(inventory_dict, product_ids_set):
    pid = read_positive_int("Enter ID to delete: ")
    if pid in inventory_dict:
        del inventory_dict[pid]
        product_ids_set.discard(pid)
        print("Item has been deleted!\n")
        return True
    else:
        print("The ID does not exist.\n")
        return False

def choose_category():
    print("Choose a category:")
    for i,c in enumerate(categories, start=1):
        print(f" {i}. {c}")
    while True:
        raw = input("Select category: ").strip()
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(categories):
                return categories[idx]
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
def save_inventory_to_file(inventory_dict, path="inventory.txt"):
    with open(path, "w", encoding="utf-8") as f:
        for pid, p in inventory_dict.items():
            if isinstance(p, PerishableProduct):
                line = f"{pid}|{p.name}|{p.brand}|{p.category}|{p.quantity}|{p.price}|P|{p.expiration_date}\n"
            else:
                line = f"{pid}|{p.name}|{p.brand}|{p.category}|{p.quantity}|{p.price}|N|\n"
            f.write(line)

# Load File
def load_inventory_from_file(inventory_dict, product_ids_set, current_next_id, path="inventory.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            inventory_dict.clear()
            product_ids_set.clear()
            loaded_count = 0
            for line in f:
                parts = line.strip().split("|")
                pid = int(parts[0])
                name, brand, category = parts[1], parts[2], parts[3]
                qty, price = int(parts[4]), float(parts[5])
                kind = parts[6] if len(parts) > 6 else "N"
                if kind == "P" and len(parts) > 7:
                    inventory_dict[pid] = PerishableProduct(
                        pid, name, brand, category, qty, price, parts[7]
                    )
                else:
                    inventory_dict[pid] = Product(
                        pid, name, brand, category, qty, price
                    )
                product_ids_set.add(pid)
                current_next_id = max(current_next_id, pid + 1)
                loaded_count += 1
            return current_next_id, loaded_count
    except FileNotFoundError:
        return current_next_id, 0

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
    next_id, loaded_count = load_inventory_from_file(inventory, product_ids, next_id)
    if loaded_count == 0:
        next_id = initialize_sample_items(inventory, product_ids, next_id)
    next_id = menu(inventory, product_ids, next_id)