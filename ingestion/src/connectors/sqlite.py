import sqlite3
import os
from typing import List, Dict

class SQLiteConnector:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_all_products(self) -> List[Dict]:
        """
        Fetches all products with their categories and ingredients.
        """
        if not os.path.exists(self.db_path):
            return []

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            # 1. Fetch Products
            cursor.execute("SELECT * FROM products")
            products = [dict(row) for row in cursor.fetchall()]

            for product in products:
                p_id = product['id']
                
                # 2. Fetch Categories
                cursor.execute('''
                    SELECT c.name FROM categories c
                    JOIN product_categories pc ON c.id = pc.category_id
                    WHERE pc.product_id = ?
                ''', (p_id,))
                product['categories'] = [row['name'] for row in cursor.fetchall()]
                
                # 3. Fetch Attributes
                cursor.execute("SELECT attribute_key, attribute_value FROM product_attributes WHERE product_id = ?", (p_id,))
                product['attributes'] = {row['attribute_key']: row['attribute_value'] for row in cursor.fetchall()}
                
                # 4. Fetch Ingredients
                cursor.execute("SELECT * FROM product_ingredients WHERE product_id = ?", (p_id,))
                product['ingredients'] = [dict(row) for row in cursor.fetchall()]

            return products
        finally:
            conn.close()
