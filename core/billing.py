import json
from datetime import datetime
from core.db import db
from core.inventory import update_stock, get_item_price
from utils.logger import get_logger

logger = get_logger(__name__)

def calculate_total(items):
    """items is a list of (item_name, quantity)"""
    total = 0
    for name, qty in items:
        price = get_item_price(name)
        if price:
            total += price * qty
    return total

def create_bill(items):
    """
    items: list of tuples (item_name, quantity)
    """
    if not items:
        logger.warning("Attempted to create bill with no items")
        return None

    total = calculate_total(items)
    if total == 0:
        logger.warning(f"Total calculated as 0 for items: {items}")
        return None
    
    try:
        # 1. Reduce inventory and collect prices
        processed_items = []
        for name, qty in items:
            price = get_item_price(name)
            if price is not None:
                if update_stock(name, -qty):
                    processed_items.append((name, qty, price))
                else:
                    logger.error(f"Failed to update stock for {name}")
            else:
                logger.error(f"Item {name} not found in inventory during billing")

        if not processed_items:
            return None

        # 2. Store transaction summary
        items_json = json.dumps([(n, q) for n, q, p in processed_items])
        cursor = db.execute("INSERT INTO transactions (items, total) VALUES (?, ?)", (items_json, total))
        transaction_id = cursor.lastrowid

        # 3. Store normalized transaction items
        for name, qty, price in processed_items:
            db.execute(
                "INSERT INTO transaction_items (transaction_id, item, quantity, price_at_time) VALUES (?, ?, ?, ?)",
                (transaction_id, name, qty, price)
            )
        
        db.commit()
        logger.info(f"Transaction {transaction_id} completed. Total: {total}")
        
        return {
            "id": transaction_id,
            "items": processed_items,
            "total": total,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        logger.error(f"Error during billing: {e}")
        return None
