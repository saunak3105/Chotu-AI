import os

# Database Path
DB_PATH = "chotu.db"
BACKUP_PATH = "chotu_backup.db"

# PIN for authentication
SECURITY_PIN = "1234"

# Inventory constants
LOW_STOCK_THRESHOLD = 10

# Speech Config
VOSK_MODEL_PATH = "model/vosk-model-small-en-us-0.15" # Corrected path

# Intents
INTENT_ADD_ITEM = "ADD_ITEM"
INTENT_REMOVE_ITEM = "REMOVE_ITEM"
INTENT_QUERY_STOCK = "QUERY_STOCK"
INTENT_CREATE_BILL = "CREATE_BILL"
INTENT_ADD_EXPENSE = "ADD_EXPENSE"
INTENT_SHOW_SALES = "SHOW_SALES"
INTENT_UNKNOWN = "UNKNOWN"
