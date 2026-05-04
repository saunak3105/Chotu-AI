from core.db import db
from datetime import datetime

def add_expense(amount, category):
    db.execute("INSERT INTO expenses (amount, category) VALUES (?, ?)", (amount, category))

def get_expenses(start_date=None, end_date=None):
    if start_date and end_date:
        return db.fetchall("SELECT * FROM expenses WHERE timestamp BETWEEN ? AND ?", (start_date, end_date))
    return db.fetchall("SELECT * FROM expenses")

def total_expense(date_filter=None):
    """
    date_filter: 'today' or None
    """
    if date_filter == 'today':
        query = "SELECT SUM(amount) FROM expenses WHERE date(timestamp) = date('now')"
    else:
        query = "SELECT SUM(amount) FROM expenses"
    
    result = db.fetchone(query)
    return result[0] if result[0] else 0.0
