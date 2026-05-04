import json
from core.db import db
from core.expense import total_expense as get_total_expense
from utils.constants import LOW_STOCK_THRESHOLD
from datetime import datetime, timedelta

def top_selling_products(limit=5):
    query = """
    SELECT item, SUM(quantity) as total_qty, SUM(quantity * price_at_time) as revenue 
    FROM transaction_items 
    GROUP BY item 
    ORDER BY total_qty DESC 
    LIMIT ?
    """
    return db.fetchall(query, (limit,))

def daily_sales_summary():
    query = "SELECT SUM(total) FROM transactions WHERE date(timestamp) = date('now')"
    result = db.fetchone(query)
    return result[0] if result[0] else 0.0

def daily_transaction_count():
    query = "SELECT COUNT(*) FROM transactions WHERE date(timestamp) = date('now')"
    result = db.fetchone(query)
    return result[0] if result else 0

def daily_stats():
    sales = daily_sales_summary()
    expenses = get_total_expense('today')
    profit = sales - expenses
    transactions = daily_transaction_count()
    return {
        "sales": sales,
        "expenses": expenses,
        "profit": profit,
        "transactions": transactions
    }

def last_7_days_sales():
    trend = []
    for i in range(6, -1, -1):
        day = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        query = "SELECT SUM(total) FROM transactions WHERE date(timestamp) = ?"
        result = db.fetchone(query, (day,))
        trend.append((day, result[0] if result[0] else 0.0))
    return trend

def get_growth_rate():
    today = daily_sales_summary()
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    query = "SELECT SUM(total) FROM transactions WHERE date(timestamp) = ?"
    yesterday_res = db.fetchone(query, (yesterday_date,))
    yesterday = yesterday_res[0] if yesterday_res[0] else 0.0
    
    if yesterday == 0:
        return 100.0 if today > 0 else 0.0
    return ((today - yesterday) / yesterday) * 100

def low_stock_items():
    query = "SELECT item, stock FROM inventory WHERE stock <= ?"
    return db.fetchall(query, (LOW_STOCK_THRESHOLD,))

def get_actionable_insights():
    insights = []
    
    # Growth insight
    growth = get_growth_rate()
    if growth > 0:
        insights.append(f"📈 Sales up by {growth:.1f}% compared to yesterday!")
    elif growth < 0:
        insights.append(f"📉 Sales down by {abs(growth):.1f}% compared to yesterday.")

    # Low stock insight
    low_stock = low_stock_items()
    if len(low_stock) > 3:
        insights.append(f"⚠️ {len(low_stock)} items are low on stock. Restock soon!")
    
    # Top product insight
    top = top_selling_products(1)
    if top:
        insights.append(f"🌟 {top[0][0].capitalize()} is your best seller today.")
        
    if not insights:
        insights.append("Everything looks steady today.")
        
    return insights
