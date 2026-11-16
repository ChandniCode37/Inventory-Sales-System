# PS 51 – Inventory + Sales Management System

## Project Information
- **Project Title:** Inventory + Sales Management System
- **Programming Language:** Python 3
- **Libraries Used:** Pandas, OS
- **Concepts:** CRUD Operations, Dictionaries, File Handling

## Project Description
The Inventory + Sales Management System is a Python-based application designed to manage product inventory and sales records.

It allows users to add, update, delete and sell products. It also maintains stock details and generates sales reports.

## Features
1. Add new inventory items.
2. Sell products and automatically update stock.
3. Update existing item details.
4. Delete inventory items.
5. Generate sales reports.
6. Calculate total revenue.
7. Identify the best-selling product.
8. Store inventory and sales records in CSV files.

## Technologies Used
- Python 3
- Pandas Library
- Dictionaries
- CSV File Handling

## Project Files

**inventory.py** – Main Python program.

**inventory.csv** – Stores product ID, Name, Stock and Price.

**sales.csv** – Stores product ID, Quantity and Amount sold.

Both CSV files are automatically created when the program runs for the first time.

## Installation

Install the Pandas library using:

```bash
pip install pandas
```

## How to Run

1. Download or clone the repository.
2. Install Python 3.
3. Install the Pandas library.
4. Open the project folder.
5. Run the following command:

```bash
python inventory.py
```

## Main Menu

```text
===== Inventory + Sales Management =====

1. Add item
2. Sell
3. Update
4. Delete
5. Sales report
6. Exit
```

## Expected Output

```text
Item added.
ID: I101 | Apple | Stock: 10 | Price: 5

Sale recorded: Apple x3 = 15
Stock left: 7
```

## Conclusion

This project demonstrates the practical use of Python programming, CRUD operations, Pandas, dictionaries and file handling to manage inventory and sales records efficiently.
