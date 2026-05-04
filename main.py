import sys
import getpass
from core.db import db
from core.seed import seed_inventory
from core.inventory import list_inventory
from ui.app import ChotuApp
from utils.constants import SECURITY_PIN
from utils.logger import get_logger

logger = get_logger("Main")

def authenticate():
    print("=== Chotu AI: Vernacular Assistant for Kirana Stores ===")
    # For GUI, we might want a GUI login, but for now, simple CLI check is fine
    # Or just skip for the demo if requested. Let's keep it simple.
    pin = getpass.getpass("Enter Security PIN to start: ")
    if pin == SECURITY_PIN:
        return True
    else:
        print("Invalid PIN. Access Denied.")
        return False

def main():
    logger.info("Starting Chotu AI Upgraded System")
    
    # Initialize/Seed DB if empty
    try:
        inventory = list_inventory()
        if not inventory:
            logger.info("Initializing database with sample items...")
            seed_inventory()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)

    # Launch GUI
    try:
        logger.info("Launching Desktop GUI...")
        app = ChotuApp()
        app.mainloop()
    except Exception as e:
        logger.error(f"GUI failed to start: {e}")
        print("Error: Could not start GUI. Check logs/chotu.log")

if __name__ == "__main__":
    main()
