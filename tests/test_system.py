import unittest
from nlp.intent_parser import process_text
from core.inventory import add_item, get_stock, update_stock
from core.billing import create_bill
from utils.constants import *

class TestChotuNLP(unittest.TestCase):
    def setUp(self):
        add_item("maggi", 20, 100)
        add_item("bread", 25, 50)

    def test_intent_parsing(self):
        res = process_text("3 maggi add karo")
        self.assertEqual(res["intent"], INTENT_ADD_ITEM)
        self.assertEqual(res["item"], "maggi")
        self.assertEqual(res["quantity"], 3)

        res = process_text("bill 2 bread")
        self.assertEqual(res["intent"], INTENT_CREATE_BILL)
        self.assertEqual(res["item"], "bread")
        self.assertEqual(res["quantity"], 2)

    def test_fuzzy_matching(self):
        # Assuming 'maggi' is in inventory
        res = process_text("add 5 magy")
        self.assertEqual(res["item"], "maggi")

class TestChotuCore(unittest.TestCase):
    def setUp(self):
        add_item("test_item", 10, 100)

    def test_inventory_update(self):
        update_stock("test_item", 10)
        self.assertEqual(get_stock("test_item"), 110)
        
        # Test negative stock prevention
        res = update_stock("test_item", -200)
        self.assertFalse(res)
        self.assertEqual(get_stock("test_item"), 110)

    def test_billing(self):
        initial_stock = get_stock("test_item")
        bill = create_bill([("test_item", 5)])
        self.assertIsNotNone(bill)
        self.assertEqual(bill["total"], 50)
        self.assertEqual(get_stock("test_item"), initial_stock - 5)

if __name__ == "__main__":
    unittest.main()
