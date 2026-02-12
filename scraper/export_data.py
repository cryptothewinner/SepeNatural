import sqlite3
import csv
import os

DB_NAME = 'sepenatural.db'

def export_to_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']
    
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        column_names = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        csv_file = f"{table}_export.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(column_names)
            writer.writerows(rows)
        print(f"Exported {table} to {csv_file}")
    
    conn.close()

if __name__ == "__main__":
    if os.path.exists(DB_NAME):
        export_to_csv()
    else:
        print(f"Error: {DB_NAME} not found. Please wait for the scraper to finish or check the path.")
