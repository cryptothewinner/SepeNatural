import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import time
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Configuration & Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scraper.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SepenaturalScraper")

DB_NAME = "sepenatural.db"
BASE_URL = "https://www.sepenatural.com.tr"
PRODUCT_SITEMAP_URL = "https://www.sepenatural.com.tr/xml/sitemap_product_1.xml"

# --- DATABASE LAYER ---

def init_db():
    """Initializes the relational database schema."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Products Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE,
            barcode TEXT,
            name TEXT NOT NULL,
            url TEXT UNIQUE,
            price REAL,
            currency TEXT,
            description_html TEXT,
            usage_text TEXT,
            warnings_text TEXT,
            storage_text TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Categories Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES categories (id)
        )
    ''')

    # 3. Product-Categories mapping (Many-to-Many)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_categories (
            product_id INTEGER,
            category_id INTEGER,
            PRIMARY KEY (product_id, category_id),
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    ''')

    # 4. Product Attributes Table (Key-Value)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_attributes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            attribute_key TEXT,
            attribute_value TEXT,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        )
    ''')

    # 5. Product Ingredients Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            raw_text TEXT,
            ingredient_name TEXT,
            amount TEXT,
            unit TEXT,
            percentage TEXT,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")

# --- SCRAPING & PARSING LOGIC ---

class SepenaturalScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

    def get_product_urls(self) -> List[str]:
        """Fetches all product URLs from the sitemap."""
        logger.info(f"Fetching sitemap: {PRODUCT_SITEMAP_URL}")
        try:
            response = self.session.get(PRODUCT_SITEMAP_URL)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            # Handle XML namespaces
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = [url.find('ns:loc', namespace).text for url in root.findall('ns:url', namespace)]
            logger.info(f"Found {len(urls)} product URLs in sitemap.")
            return urls
        except Exception as e:
            logger.error(f"Failed to fetch sitemap: {e}")
            return []

    def parse_ingredients(self, raw_string: str) -> List[Dict]:
        """
        Gelişmiş içerik ayrıştırma. Yüzdelik oranları ve birimleri hassas bir şekilde yakalar.
        """
        if not raw_string:
            return []
        
        # Temizlik
        raw_string = raw_string.replace('\r', ' ').replace('\n', ' ')
        
        # Genellikle virgülle ayrılırlar
        parts = [p.strip() for p in raw_string.split(',') if p.strip()]
        
        ingredients = []
        for part in parts:
            # Örn: "Standardize Kara Mürver Ekstresi (30%) 270 mg"
            
            # Başta olabilecek işaretleri temizle
            part = re.sub(r'^[•\-\*]\s*', '', part)
            if any(x in part.lower() for x in ['beher', 'miktarı', 'tutar']):
                continue
            
            # 1. Yüzdeyi bul (Örn: %30, 30%, (30%), >=4%)
            percentage = None
            pct_match = re.search(r'\(?([<>≤≥=]?\s*\d+(?:[.,]\d+)?\s*%|%\s*\d+(?:[.,]\d+)?)\)?', part)
            if pct_match:
                percentage = pct_match.group(1).strip()
                # İsmi temizlemek için yüzde kısmını çıkar
                clean_part = part.replace(pct_match.group(0), ' ').strip()
            else:
                clean_part = part
            
            # 2. Miktar ve Birimi bul (Örn: 270 mg, 1000mg)
            amount = None
            unit = None
            amt_match = re.search(r'(\d+(?:[.,]\d+)?)\s*([a-zA-Z]{1,3}|softgel|kapsül|adet)$', clean_part, re.I)
            if amt_match:
                amount = amt_match.group(1).replace(',', '.')
                unit = amt_match.group(2).strip()
                name_part = clean_part[:amt_match.start()].strip()
            else:
                name_part = clean_part

            # 3. Kalan isimdir
            name = name_part.strip(' :;.,-')
            
            if name or amount:
                ingredients.append({
                    "raw": part,
                    "name": name if name else "Bilinmeyen",
                    "percentage": percentage,
                    "amount": amount,
                    "unit": unit
                })
        return ingredients

    def scrape_product(self, url: str) -> Optional[Dict]:
        """Scrapes a single product page with robust selection logic."""
        try:
            time.sleep(1) # Politeness
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Core Data
            name_tag = soup.find('h1', {'class': 'product-name'}) or soup.find('h1')
            name = name_tag.text.strip() if name_tag else "N/A"
            
            # Categories (Breadcrumbs)
            categories = []
            breadcrumb_tags = soup.find_all(['div', 'nav', 'ul'], class_=re.compile(r'breadcrumb|path', re.I))
            for bt in breadcrumb_tags:
                links = bt.find_all('a')
                for link in links:
                    cat_name = link.text.strip()
                    if cat_name and cat_name.lower() not in ['anasayfa', 'home']:
                        categories.append(cat_name)
                if categories: break
            
            # If no breadcrumb container, try any links in parent containers above H1
            if not categories:
                parent = name_tag.parent if name_tag else None
                while parent and not categories:
                    links = parent.find_all('a')
                    for l in links:
                        c_name = l.text.strip()
                        if c_name and c_name.lower() not in ['anasayfa', 'home'] and l.get('href', '').find('/kategori/') != -1:
                            categories.append(c_name)
                    parent = parent.parent

            # Price (Primary Selector: Schema.org meta tags)
            price_meta = soup.find('meta', {'itemprop': 'price'})
            curr_meta = soup.find('meta', {'itemprop': 'priceCurrency'})
            
            price = 0.0
            if price_meta:
                try:
                    price_val = price_meta.get('content', '0').replace(',', '.')
                    price = float(re.sub(r'[^\d.]', '', price_val))
                except ValueError: pass
            
            currency = curr_meta.get('content', 'TL') if curr_meta else "TL"
            if currency == "TRY": currency = "TL"

            # SKU & Barcode
            sku = "N/A"
            barcode = "N/A"
            sku_tag = (soup.find(None, {'itemprop': 'sku'}) or 
                       soup.find(None, {'itemprop': 'barcode'}) or
                       soup.find(class_='product-barcode'))
            
            if sku_tag:
                sku = sku_tag.text.strip()
                barcode = sku
            
            info_area = soup.find(['div', 'ul'], class_=re.compile(r'codes|attributes|info', re.I))
            if info_area:
                info_text = info_area.text
                sku_m = re.search(r'(?:SKU|Kod|Stok):\s*([a-zA-Z\d-]+)', info_text, re.I)
                bar_m = re.search(r'(?:Barkod|EAN):\s*(\d+)', info_text, re.I)
                if sku_m: sku = sku_m.group(1)
                if bar_m: barcode = bar_m.group(1)

            # --- Description Anchors ---
            def get_section(keywords):
                results = []
                # Search for all elements matching any keyword
                anchors = soup.find_all(['span', 'strong', 'h1', 'h2', 'h3', 'h4', 'b', 'div', 'p'], string=re.compile('|'.join(keywords), re.I))
                
                for anchor in anchors:
                    curr = anchor
                    for _ in range(5):
                        nxt = curr.find_next(['div', 'p', 'span', 'ul', 'li'])
                        if not nxt: break
                        txt = nxt.get_text(strip=True)
                        if len(txt) < 15: 
                            curr = nxt
                            continue
                        # Use a score based on number of ingredient-like patterns
                        matches = re.findall(r'\d+\s*(mg|g|ml|%)', txt, re.I)
                        score = len(matches)
                        if score > 0:
                            results.append((score, txt))
                        curr = nxt
                
                if results:
                    # Return the one with the most matches (the most detailed ingredient list)
                    results.sort(key=lambda x: x[0], reverse=True)
                    return results[0][1]
                return ""

            # Improved Description Extraction
            description_tag = (
                soup.find('div', id=re.compile(r'description|details|tab', re.I)) or
                soup.find('div', class_=re.compile(r'product-detail|product-feature|product-details|description', re.I)) or
                soup.find('div', id='product-details') or
                soup.find('div', class_='product-description')
            )
            
            description_html = ""
            if description_tag:
                # Clean up if it's a huge container
                description_html = str(description_tag)

            data = {
                "name": name, "sku": sku, "barcode": barcode, "price": price, 
                "currency": currency, "url": url, "categories": categories,
                "description_html": description_html,
                "usage_text": get_section(['Kullanım Önerisi', 'Nasıl Kullanılır', 'Kullanımı']),
                "warnings_text": get_section(['Uyarılar', 'Önemli Uyarılar', 'Dikkat']),
                "storage_text": get_section(['Muhafaza', 'Saklama', 'Depolama']),
                "attributes": {}, "ingredients": []
            }

            # --- Attribute Extraction (Technical Specs) ---
            # Try IdeaSoft specific list pattern first
            attr_rows = soup.find_all('div', class_='product-list-row')
            if attr_rows:
                for row in attr_rows:
                    title_tag = row.find(['div', 'span'], class_='product-list-title')
                    content_tag = row.find(['div', 'span'], class_='product-list-content')
                    if title_tag and content_tag:
                        key = title_tag.text.strip().replace(':', '')
                        val = content_tag.text.strip()
                        if key and val and len(key) < 50:
                            data["attributes"][key] = val
            
            # Fallback to general containers if nothing found
            if not data["attributes"]:
                attr_container = (soup.find('table', class_=re.compile(r'specs|attributes', re.I)) or 
                                  soup.find('ul', class_=re.compile(r'specs|features|attributes', re.I)) or
                                  soup.find('div', class_=re.compile(r'product-info', re.I)))
                
                if attr_container:
                    for row in attr_container.find_all(['tr', 'li', 'div'], recursive=False if attr_container.name != 'div' else True):
                        cols = row.find_all(['td', 'span', 'strong'], recursive=True)
                        if len(cols) >= 2:
                            key = cols[0].text.strip().replace(':', '')
                            val = cols[1].text.strip()
                            if key and val and len(key) < 50:
                                data["attributes"][key] = val
                        elif ':' in row.text:
                            parts = row.text.split(':', 1)
                            key, val = parts[0].strip(), parts[1].strip()
                            if key and val and len(key) < 50:
                                data["attributes"][key] = val

            # Ingredients Search (Broader)
            ing_marker = soup.find(['div', 'span', 'strong', 'h3', 'h4'], string=re.compile(r'İçindekiler|Beher|Bileşen|İçerik', re.I))
            if ing_marker:
                # Try finding a table or a list nearby
                ing_container = ing_marker.find_next(['table', 'ul', 'div', 'p']) or ing_marker.parent
                ing_text = ing_container.text.strip()
                # If table, handle rows specially
                if ing_container.name == 'table':
                    ing_text = " | ".join([row.text.strip().replace('\n', ' ') for row in ing_container.find_all('tr')])
                
                logger.info(f"Captured ingredient text for {sku}: {ing_text[:100]}...")
                data["ingredients"] = self.parse_ingredients(ing_text)
            else:
                # Last resort: search for keywords anywhere and take the block
                for kw in ['İçindekiler', 'Beher', 'Bileşen']:
                    found = soup.find(string=re.compile(kw, re.I))
                    if found and len(found.parent.text) > 20:
                        data["ingredients"] = self.parse_ingredients(found.parent.text)
                        break

            return data

        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None

# --- DATABASE OPERATIONS ---

def save_product(product_data: Dict):
    """Inserts or updates product data and categories."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM products WHERE sku = ? OR url = ?", (product_data['sku'], product_data['url']))
        existing = cursor.fetchone()
        
        if existing:
            product_id = existing[0]
            cursor.execute('''
                UPDATE products SET 
                sku=?, barcode=?, name=?, url=?, price=?, currency=?, 
                description_html=?, usage_text=?, warnings_text=?, storage_text=?
                WHERE id=?
            ''', (
                product_data['sku'], product_data['barcode'], product_data['name'], product_data['url'], 
                product_data['price'], product_data['currency'], product_data['description_html'],
                product_data['usage_text'], product_data['warnings_text'], product_data['storage_text'],
                product_id
            ))
        else:
            cursor.execute('''
                INSERT INTO products 
                (sku, barcode, name, url, price, currency, description_html, usage_text, warnings_text, storage_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product_data['sku'], product_data['barcode'], product_data['name'], 
                product_data['url'], product_data['price'], product_data['currency'],
                product_data['description_html'], product_data['usage_text'], 
                product_data['warnings_text'], product_data['storage_text']
            ))
            product_id = cursor.lastrowid

        # --- Categories ---
        cursor.execute("DELETE FROM product_categories WHERE product_id = ?", (product_id,))
        for cat_name in product_data.get('categories', []):
            cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat_name,))
            cursor.execute("SELECT id FROM categories WHERE name = ?", (cat_name,))
            cat_id = cursor.fetchone()[0]
            cursor.execute("INSERT OR IGNORE INTO product_categories (product_id, category_id) VALUES (?, ?)", (product_id, cat_id))

        # Clear and rebuild attributes
        cursor.execute("DELETE FROM product_attributes WHERE product_id = ?", (product_id,))
        for key, val in product_data['attributes'].items():
            cursor.execute("INSERT INTO product_attributes (product_id, attribute_key, attribute_value) VALUES (?, ?, ?)",
                           (product_id, key, val))

        # Clear and rebuild ingredients
        cursor.execute("DELETE FROM product_ingredients WHERE product_id = ?", (product_id,))
        for ing in product_data['ingredients']:
            cursor.execute('''
                INSERT INTO product_ingredients (product_id, raw_text, ingredient_name, amount, unit, percentage)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (product_id, ing['raw'], ing['name'], ing['amount'], ing['unit'], ing['percentage']))

        conn.commit()
    except Exception as e:
        logger.error(f"DB Error for SKU {product_data['sku']}: {e}")
        conn.rollback()
    finally:
        conn.close()

# --- MAIN EXECUTION ---

def main():
    logger.info("Starting Sepenatural Scraper...")
    init_db()
    
    scraper = SepenaturalScraper()
    urls = scraper.get_product_urls()
    
    if not urls:
        logger.warning("No URLs found. Exiting.")
        return

    count = 0
    for url in urls:
        logger.info(f"Processing URL {count+1}/{len(urls)}: {url}")
        product_data = scraper.scrape_product(url)
        
        if product_data:
            save_product(product_data)
            count += 1
            
    logger.info(f"Finished. Total products processed: {count}")

if __name__ == "__main__":
    main()
