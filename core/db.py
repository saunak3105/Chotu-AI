import sqlite3
import json
from datetime import datetime
from utils.constants import DB_PATH

class Database:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Inventory Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                item TEXT PRIMARY KEY,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        ''')

        # Transactions Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                items TEXT, -- Keep for legacy/summary if needed, or remove later
                total REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Normalized Transaction Items Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaction_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER,
                item TEXT,
                quantity INTEGER,
                price_at_time REAL,
                FOREIGN KEY (transaction_id) REFERENCES transactions (id)
            )
        ''')

        # Expenses Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            return None

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

# Singleton instance
db = Database()
