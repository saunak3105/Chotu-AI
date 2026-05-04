import re
import difflib
from utils.logger import get_logger

logger = get_logger(__name__)

# Basic mapping for Hindi numbers
HINDI_NUMBERS = {
    "ek": 1, "do": 2, "teen": 3, "char": 4, "chaar": 4, "paanch": 5, "panch": 5,
    "chhay": 6, "che": 6, "saat": 7, "aath": 8, "nau": 9, "das": 10,
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
}

def extract_quantity(text):
    # Try numeric first
    nums = re.findall(r'\d+', text)
    if nums:
        return int(nums[0])
    
    # Try word mapping
    words = text.lower().split()
    for word in words:
        if word in HINDI_NUMBERS:
            return HINDI_NUMBERS[word]
    
    return 1 # Default to 1 if not specified

def extract_item(text, inventory_items):
    """
    inventory_items: list of valid item names in lowercase
    """
    if not inventory_items:
        return None
        
    text = text.lower()
    words = text.split()
    
    # 1. Exact match in words
    for word in words:
        if word in inventory_items:
            return word
    
    # 2. Substring match
    for item in inventory_items:
        if item in text:
            return item
            
    # 3. Fuzzy matching using difflib
    # We look for the best match among all words in text against inventory
    best_match = None
    highest_ratio = 0.0
    
    for word in words:
        matches = difflib.get_close_matches(word, inventory_items, n=1, cutoff=0.6)
        if matches:
            ratio = difflib.SequenceMatcher(None, word, matches[0]).ratio()
            if ratio > highest_ratio:
                highest_ratio = ratio
                best_match = matches[0]
                
    if best_match:
        logger.info(f"Fuzzy matched '{text}' to item '{best_match}' (ratio: {highest_ratio})")
    
    return best_match

def extract_amount(text):
    nums = re.findall(r'\d+', text)
    if nums:
        return float(nums[0])
    return 0.0
