import shutil
import os
from utils.constants import DB_PATH, BACKUP_PATH

def backup_db():
    try:
        shutil.copy2(DB_PATH, BACKUP_PATH)
        return True
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

def format_currency(amount):
    return f"₹{amount:.2f}"
