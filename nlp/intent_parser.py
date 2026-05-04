from utils.constants import *
from nlp.entity_extractor import extract_quantity, extract_item, extract_amount
from core.inventory import list_inventory
from utils.logger import get_logger

logger = get_logger(__name__)

# Priority-based intent mapping
INTENT_KEYWORDS = {
    INTENT_ADD_EXPENSE: ["expense", "kharcha", "bill pay", "kharch"],
    INTENT_SHOW_SALES: ["sales", "kamai", "summary", "report", "hisaab", "hisab"],
    INTENT_CREATE_BILL: ["bill", "becha", "sell", "billing", "bech"],
    INTENT_QUERY_STOCK: ["stock", "kitna", "check", "baki", "balance", "inventory", "dikhao"],
    INTENT_ADD_ITEM: ["add", "daalo", "rakho", "bhardo", "le aaya", "plus"],
    INTENT_REMOVE_ITEM: ["remove", "hatao", "nikalo", "minus", "kam karo"]
}

def parse_intent(text):
    text = text.lower()
    
    # Priority-based parsing
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return intent

    return INTENT_UNKNOWN

def process_text(text):
    logger.info(f"Processing input: {text}")
    intent = parse_intent(text)
    
    # Get current inventory for matching
    inventory = [item[0] for item in list_inventory()]
    
    data = {
        "intent": intent, 
        "original_text": text,
        "item": None,
        "quantity": 1,
        "amount": 0.0,
        "category": "general"
    }
    
    if intent in [INTENT_ADD_ITEM, INTENT_REMOVE_ITEM, INTENT_CREATE_BILL, INTENT_QUERY_STOCK]:
        data["item"] = extract_item(text, inventory)
        data["quantity"] = extract_quantity(text)
    
    if intent == INTENT_ADD_EXPENSE:
        data["amount"] = extract_amount(text)
        words = text.split()
        # Find a word that is not the amount as category
        for word in reversed(words):
            if not word.isdigit() and word not in INTENT_KEYWORDS[INTENT_ADD_EXPENSE]:
                data["category"] = word
                break

    logger.info(f"Parsed data: {data}")
    return data
