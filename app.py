from flask import Flask, request, session
import os
import sqlite3 

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
def get_db():
    conn = sqlite3.connect("saibank.db")
    conn.row_factory = sqlite3.Row
    return conn

APP_VERSION = os.getenv("APP_VERSION", "Development")
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        )
    """)

    conn.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_transactions_unique
    ON transactions(customer_id, description, amount)
""")
    
    conn.execute(
        "INSERT OR IGNORE INTO customers (id, name, balance) VALUES (?, ?, ?)",
        (101, "Ravi", 50000)
    )

    conn.execute(
        "INSERT OR IGNORE INTO customers (id, name, balance) VALUES (?, ?, ?)",
        (102, "Sai", 25000)
    )

    conn.execute(
        "INSERT OR IGNORE INTO customers (id, name, balance) VALUES (?, ?, ?)",
        (103, "Ram", 80000)
    )
    conn.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL
        )
    """)
    conn.execute(
        "INSERT OR IGNORE INTO transactions (customer_id, description, amount) VALUES (?, ?, ?)",
        (101, "Grocery", 2000)
    )

    conn.execute(
        "INSERT OR IGNORE INTO transactions (customer_id, description, amount) VALUES (?, ?, ?)",
        (101, "Salary", 5000)
    )

    conn.execute(
        "INSERT OR IGNORE INTO transactions (customer_id, description, amount) VALUES (?, ?, ?)",
        (102, "Petrol", 1500)
    )

    conn.execute(
        "INSERT OR IGNORE INTO transactions (customer_id, description, amount) VALUES (?, ?, ?)",
        (103, "Shopping", 3000)
    )
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return f"Welcome to SaiBank - {APP_VERSION}!"

@app.route("/login/<int:customer_id>")
def login(customer_id):
    conn = get_db()

    customer = conn.execute(
        "SELECT id, name FROM customers WHERE id = ?",
        (customer_id,)
    ).fetchone()

    conn.close()

    if customer:
        session["customer_id"] = customer["id"]
        return f"Welcome {customer['name']}"

    return "Customer not found"

@app.route("/balance")
def balance():
    conn = get_db()

    customer = conn.execute(
        "SELECT name, balance FROM customers WHERE id = ?",
        (session["customer_id"],)
    ).fetchone()

    conn.close()

    if customer:
        return f"{customer['name']}'s balance: ₹{customer['balance']:.2f}"

    return "Customer not found"


@app.route("/balance/<int:customer_id>")
def customer_balance(customer_id):
    conn = get_db()

    customer = conn.execute(
        "SELECT name, balance FROM customers WHERE id = ?",
        (customer_id,)
    ).fetchone()

    conn.close()

    if customer:
        return f"{customer['name']}'s balance: ₹{customer['balance']:.2f}"

    return "Customer not found"

@app.route("/transactions")
def customer_transactions():
    conn = get_db()

    transactions = conn.execute(
        "SELECT description, amount FROM transactions WHERE customer_id = ?",
        (session["customer_id"],)
    ).fetchall()

    conn.close()

    if transactions:
        result = "<br>".join(
            f"{transaction['description']}: ₹{transaction['amount']:.2f}"
            for transaction in transactions
        )
        return result

    return "No transactions found"


@app.route("/secret-status")
def secret_status():
    return "Secret configured ✅" if os.getenv("APP_SECRET") else "Secret missing ❌"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)