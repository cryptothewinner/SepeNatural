import sqlite3
import os

DB_PATH = 'sepenatural.db'

def count_rows():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    tables = ['products', 'categories', 'product_categories', 'product_attributes', 'product_ingredients']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count}")
        except sqlite3.OperationalError as e:
            print(f"{table}: Table not found or error ({e})")
            
    conn.close()

if __name__ == "__main__":
    count_rows()
