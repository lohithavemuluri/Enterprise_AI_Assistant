import sqlite3


# Create database
connection = sqlite3.connect("enterprise.db")

cursor = connection.cursor()


# ==========================================
# EMPLOYEES TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary REAL
)
""")


# ==========================================
# PRODUCTS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
)
""")


# ==========================================
# SALES TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    employee_id INTEGER,
    quantity INTEGER,
    sale_amount REAL,
    sale_date TEXT,
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(employee_id) REFERENCES employees(id)
)
""")


# ==========================================
# INSERT EMPLOYEES
# ==========================================

employees = [
    (1, "Ananya", "Sales", 45000),
    (2, "Rahul", "Marketing", 50000),
    (3, "Priya", "Sales", 48000),
    (4, "Arjun", "IT", 65000),
    (5, "Sneha", "Finance", 60000)
]

cursor.executemany("""
INSERT OR IGNORE INTO employees
VALUES (?, ?, ?, ?)
""", employees)


# ==========================================
# INSERT PRODUCTS
# ==========================================

products = [
    (1, "Laptop", "Electronics", 75000),
    (2, "Smartphone", "Electronics", 30000),
    (3, "Tablet", "Electronics", 25000),
    (4, "Monitor", "Accessories", 15000),
    (5, "Keyboard", "Accessories", 3000)
]

cursor.executemany("""
INSERT OR IGNORE INTO products
VALUES (?, ?, ?, ?)
""", products)


# ==========================================
# INSERT SALES
# ==========================================

sales = [
    (1, 1, 1, 2, 150000, "2026-01-10"),
    (2, 2, 1, 5, 150000, "2026-01-15"),
    (3, 3, 3, 3, 75000, "2026-02-05"),
    (4, 1, 3, 1, 75000, "2026-02-12"),
    (5, 4, 2, 4, 60000, "2026-02-20"),
    (6, 5, 1, 10, 30000, "2026-03-01"),
    (7, 2, 3, 4, 120000, "2026-03-10"),
    (8, 1, 1, 1, 75000, "2026-03-15")
]

cursor.executemany("""
INSERT OR IGNORE INTO sales
VALUES (?, ?, ?, ?, ?, ?)
""", sales)


# Save database
connection.commit()

connection.close()

print("Enterprise database created successfully!")