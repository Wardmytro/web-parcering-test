import random
import sqlite3
from datetime import datetime
from config import DB_PATH, WALLETS

def init_database():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        character_name TEXT NOT NULL,
        discord TEXT NOT NULL,
        gold_amount INTEGER NOT NULL,
        price_usd REAL NOT NULL,
        selected_network TEXT NOT NULL,
        wallet_address TEXT NOT NULL,
        note TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        paid_at TIMESTAMP,
        delivered_at TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        tx_hash TEXT PRIMARY KEY,
        wallet_address TEXT NOT NULL,
        amount_received REAL NOT NULL,
        network TEXT NOT NULL,
        confirmed_at TIMESTAMP,
        order_id TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )''')

    conn.commit()
    conn.close()

def create_order(user_id, character_name, discord, gold_amount, price_usd, network, note):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    order_id = str(random.randint(100000, 999999))
    wallet = WALLETS[network]

    c.execute('''INSERT INTO orders
                 (order_id, user_id, character_name, discord, gold_amount, price_usd, selected_network, wallet_address, note)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (order_id, user_id, character_name, discord, gold_amount, price_usd, network, wallet, note))

    conn.commit()
    conn.close()
    return order_id

def get_pending_orders():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT * FROM orders WHERE status = "pending"')
    orders = c.fetchall()
    conn.close()
    return [dict(row) for row in orders]

def get_order_by_id(order_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
    order = c.fetchone()
    conn.close()
    return dict(order) if order else None

def update_order_status(order_id, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if status == 'paid':
        c.execute('UPDATE orders SET status = ?, paid_at = CURRENT_TIMESTAMP WHERE order_id = ?',
                  (status, order_id))
    elif status == 'delivered':
        c.execute('UPDATE orders SET status = ?, delivered_at = CURRENT_TIMESTAMP WHERE order_id = ?',
                  (status, order_id))
    else:
        c.execute('UPDATE orders SET status = ? WHERE order_id = ?', (status, order_id))

    conn.commit()
    conn.close()

def record_transaction(tx_hash, wallet_address, amount, network, order_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''INSERT OR IGNORE INTO transactions
                 (tx_hash, wallet_address, amount_received, network, confirmed_at, order_id)
                 VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)''',
              (tx_hash, wallet_address, amount, network, order_id))

    conn.commit()
    conn.close()

def get_all_orders():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = c.fetchall()
    conn.close()
    return [dict(row) for row in orders]

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully")
