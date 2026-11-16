PS 51 - Inventory + Sales Management System
Language : Python 3
Concepts : CRUD, Pandas, Dictionaries, File Handling
Files:
    inventory.csv -> ID, Name, Stock, Price
    sales.csv     -> ID, Quantity, Amount
"""
import os
import pandas as pd
INVENTORY_FILE = "inventory.csv"
SALES_FILE = "sales.csv"
INVENTORY_COLS = ["ID", "Name", "Stock", "Price"]
SALES_COLS = ["ID", "Quantity", "Amount"]
FIRST_ID = 101  # first item ID is I101
# ---------------------------------------------------------------- file handling
def load_inventory():
    if os.path.exists(INVENTORY_FILE) and os.path.getsize(INVENTORY_FILE) > 0:
        return pd.read_csv(INVENTORY_FILE)
    return pd.DataFrame(columns=INVENTORY_COLS)
def load_sales():
    if os.path.exists(SALES_FILE) and os.path.getsize(SALES_FILE) > 0:
        return pd.read_csv(SALES_FILE)
    return pd.DataFrame(columns=SALES_COLS)
def save(df, filename):
    df.to_csv(filename, index=False)
def next_id(inventory):
    """Generate the next item ID: I101, I102, ..."""
    if inventory.empty:
        return f"I{FIRST_ID}"
    last = max(int(i[1:]) for i in inventory["ID"])
    return f"I{last + 1}"
def read_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        return None
def read_float(prompt):
    try:
        return float(input(prompt).strip())
    except ValueError:
        return None
def fmt(n):
    """Print 10.0 as 10, 10.5 as 10.5."""
    return int(n) if float(n).is_integer() else n
# ------------------------------------------------------------------------ CRUD
def add_item():
    inventory = load_inventory()
    name = input("Name: ").strip()
    stock = read_int("Stock: ")
    price = read_float("Price: ")
    if not name or stock is None or price is None or stock < 0 or price < 0:
        print("Invalid input. Item not added.")
        return
    new_id = next_id(inventory)
    row = pd.DataFrame([{"ID": new_id, "Name": name, "Stock": stock, "Price": price}])
    inventory = pd.concat([inventory, row], ignore_index=True)
    save(inventory, INVENTORY_FILE)
    print("Item added.")
    print(f"ID: {new_id} | {name} | Stock: {stock} | Price: {fmt(price)}")
def update_item():
    inventory = load_inventory()
    item_id = input("ID: ").strip().upper()
    if item_id not in inventory["ID"].values:
        print(f"Item ID {item_id} not found.")
        return
    idx = inventory.index[inventory["ID"] == item_id][0]
    print("Leave blank to keep the current value.")
    name = input(f"New name [{inventory.at[idx, 'Name']}]: ").strip()
    stock = input(f"New stock [{inventory.at[idx, 'Stock']}]: ").strip()
    price = input(f"New price [{fmt(inventory.at[idx, 'Price'])}]: ").strip()
    try:
        if name:
            inventory.at[idx, "Name"] = name
        if stock:
            if int(stock) < 0:
                raise ValueError
            inventory.at[idx, "Stock"] = int(stock)
        if price:
            if float(price) < 0:
                raise ValueError
            inventory.at[idx, "Price"] = float(price)
    except ValueError:
        print("Invalid input. Item not updated.")
        return
    save(inventory, INVENTORY_FILE)
    r = inventory.loc[idx]
    print("Item updated.")
    print(f"ID: {r['ID']} | {r['Name']} | Stock: {r['Stock']} | Price: {fmt(r['Price'])}")
def delete_item():
    inventory = load_inventory()
    item_id = input("ID: ").strip().upper()
    if item_id not in inventory["ID"].values:
        print(f"Item ID {item_id} not found.")
        return
    inventory = inventory[inventory["ID"] != item_id]
    save(inventory, INVENTORY_FILE)
    print(f"Item {item_id} deleted.")
def sell_item():
    inventory = load_inventory()
    sales = load_sales()
    item_id = input("ID: ").strip().upper()
    qty = read_int("Quantity: ")
    if item_id not in inventory["ID"].values:
        print(f"Item ID {item_id} not found.")
        return
    if qty is None or qty <= 0:
        print("Invalid quantity.")
        return
    idx = inventory.index[inventory["ID"] == item_id][0]
    available = int(inventory.at[idx, "Stock"])
    if qty > available:
        print(f"Not enough stock. Available: {available}")
        return
    name = inventory.at[idx, "Name"]
    amount = qty * float(inventory.at[idx, "Price"])
    # reduce stock
    inventory.at[idx, "Stock"] = available - qty
    # record sale
    row = pd.DataFrame([{"ID": item_id, "Quantity": qty, "Amount": amount}])
    sales = pd.concat([sales, row], ignore_index=True)
    save(inventory, INVENTORY_FILE)
    save(sales, SALES_FILE)
    left = available - qty
    print(f"Sale recorded: {name} x{qty} = {fmt(amount)}")
    if left == 0:
        print("Stock left: 0 | Item is now out of stock.")
    else:
        print(f"Stock left: {left}")
# ---------------------------------------------------------------------- report
def sales_report():
    inventory = load_inventory()
    sales = load_sales()
    if sales.empty:
        print("No sales recorded yet.")
        return
    # groupby: units sold and revenue per item
    report = sales.groupby("ID").agg(Units=("Quantity", "sum"),
                                     Revenue=("Amount", "sum")).reset_index()
    # map item IDs to names (dictionary lookup)
    names = dict(zip(inventory["ID"], inventory["Name"]))
    report["Name"] = report["ID"].map(names).fillna("(deleted item)")
    for _, r in report.iterrows():
        print(f"{r['Name']}: {int(r['Units'])} units | Revenue: {fmt(r['Revenue'])}")
    print(f"Total revenue: {fmt(report['Revenue'].sum())}")
    best = report.loc[report["Units"].idxmax()]
    print(f"Best seller: {best['Name']} ({int(best['Units'])} units)")
# ------------------------------------------------------------------------ menu
def main():
    # make sure both CSV files exist
    if not os.path.exists(INVENTORY_FILE):
        save(pd.DataFrame(columns=INVENTORY_COLS), INVENTORY_FILE)
    if not os.path.exists(SALES_FILE):
        save(pd.DataFrame(columns=SALES_COLS), SALES_FILE)
    actions = {
        "1": add_item,
        "2": sell_item,
        "3": update_item,
        "4": delete_item,
        "5": sales_report,
    }
    while True:
        print("\n===== Inventory + Sales Management =====")
        print("1. Add item")
        print("2. Sell")
        print("3. Update")
        print("4. Delete")
        print("5. Sales report")
        print("6. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "6":
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid option. Please choose 1-6.")
if __name__ == "__main__":
    main()
