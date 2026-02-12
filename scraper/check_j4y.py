import requests
from bs4 import BeautifulSoup
import re

url = "https://www.sepenatural.com.tr/urun/kara-murver-meyan-koku-turunc-ekinezya-propolis-takviye-edici-gida-90-kapsul-x900-mg"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    detail = soup.find('div', class_='product-detail')
    if detail:
        print(detail.get_text())
    else:
        print("Detail not found")
except Exception as e:
    print(f"Error: {e}")
