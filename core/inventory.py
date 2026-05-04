from core.db import db
from utils.constants import LOW_STOCK_THRESHOLD
from utils.logger import get_logger

logger = get_logger(__name__)

def add_item(name, price, stock):
    if not name or price < 0 or stock < 0:
        logger.error(f"Invalid item details: name={name}, price={price}, stock={stock}")
        return False
    db.execute("INSERT OR REPLACE INTO inventory (item, price, stock) VALUES (?, ?, ?)", (name.lower(), price, stock))
    logger.info(f"Item '{name}' added/updated with price {price} and stock {stock}")
    return True

def update_stock(name, quantity):
    """Adds quantity to existing stock (can be negative to reduce)"""
    if not name:
        return False
        
    item = db.fetchone("SELECT stock FROM inventory WHERE item = ?", (name.lower(),))
    if item:
        current_stock = item[0]
        new_stock = current_stock + quantity
        
        # Validation: Stock cannot be negative
        if new_stock < 0:
            logger.warning(f"Insufficient stock for '{name}'. Current: {current_stock}, Requested reduction: {-quantity}")
            return False
            
        db.execute("UPDATE inventory SET stock = ? WHERE item = ?", (new_stock, name.lower()))
        logger.info(f"Updated stock for '{name}': {current_stock} -> {new_stock}")
        return True
    
    logger.warning(f"Item '{name}' not found in inventory")
    return False

def get_stock(name):
    result = db.fetchone("SELECT stock FROM inventory WHERE item = ?", (name.lower(),))
    return result[0] if result else None

def get_item_price(name):
    result = db.fetchone("SELECT price FROM inventory WHERE item = ?", (name.lower(),))
    return result[0] if result else None

def list_inventory():
    return db.fetchall("SELECT * FROM inventory")

def low_stock_alert():
    return db.fetchall("SELECT item, stock FROM inventory WHERE stock <= ?", (LOW_STOCK_THRESHOLD,))
