from core.db import db

def seed_inventory():
    items = [
        ("maggi", 20, 100),
        ("bread", 25, 50),
        ("biscuit", 10, 120),
        ("milk", 35, 80),
        ("butter", 45, 40),
        ("cheese", 60, 35),
        ("rice", 60, 200),
        ("wheat", 50, 180),
        ("sugar", 45, 150),
        ("salt", 20, 140),
        ("turmeric", 35, 60),
        ("chilli_powder", 40, 70),
        ("coriander_powder", 35, 65),
        ("cooking_oil", 120, 90),
        ("tea", 150, 75),
        ("coffee", 180, 60),
        ("toothpaste", 55, 50),
        ("toothbrush", 30, 60),
        ("soap", 35, 90),
        ("shampoo", 120, 70),
        ("detergent", 95, 85),
        ("dishwash", 75, 80),
        ("cola", 40, 100),
        ("juice", 50, 90),
        ("water_bottle", 20, 120),
        ("chips", 20, 110),
        ("namkeen", 30, 95),
        ("chocolate", 25, 100),
        ("icecream", 60, 40),
        ("paneer", 80, 50),
        ("curd", 35, 60),
        ("egg_tray", 180, 45),
        ("banana", 5, 200),
        ("apple", 10, 180),
        ("onion", 30, 150),
        ("potato", 25, 170),
        ("garlic", 60, 90),
        ("ginger", 50, 85),
        ("tomato", 20, 160),
        ("green_chilli", 15, 140),
        ("bread_buns", 30, 70),
        ("instant_noodles", 25, 90),
        ("cornflakes", 150, 40),
        ("oats", 120, 45),
        ("energy_drink", 110, 50)
    ]

    for item, price, stock in items:
        db.execute(
            "INSERT OR IGNORE INTO inventory VALUES (?,?,?)",
            (item, price, stock)
        )

    db.commit()
    print("✔ Sample kirana inventory seeded successfully")