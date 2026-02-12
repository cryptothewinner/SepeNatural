
# Mock SAP Data Mirror
# This file mirrors the data structure from frontend/index.html to serve as the RAG Knowledge Base.

material_master_data = [
    { 
        "matnr": "RM-1001", "maktx": "Çelik Levha 3mm", "mtart": "ROH", "matkl": "METAL", "meins": "KG", "werks": "1001", "lgort": "0001", "price": "15.40 TRY", "stock": 12500,
        "basic": { "gross": "3.2 kg", "net": "3.2 kg", "vol": "0.05 m3", "ean": "8690001234567" },
        "mrp": { "type": "PD", "controller": "C01", "reorder": "1000", "lot": "EX", "safety": "500", "leadTime": "3 gün" },
        "purchasing": { "group": "P01", "minOrder": "100 KG", "plifz": "2 gün", "orderUnit": "KG", "autoPO": "Evet", "sourceList": "Zorunlu" },
        "accounting": { "valClass": "3000", "priceControl": "V", "stdPrice": "15.00 TRY", "movPrice": "15.40 TRY", "totalVal": "192,500 TRY" },
        "quality": { "active": "Evet", "controlKey": "001 (Teslimatta)", "cert": "ISO 9001", "targetSystem": "QMS-01" },
        "profitability": { "cost": "12.50 TRY", "margin": "%18.8", "contribution": "2.90 TRY/Birim", "ytdProfit": "₺36,250", "trend": "up" }
    },
    { 
        "matnr": "RM-1002", "maktx": "Alüminyum Profil 40x40", "mtart": "ROH", "matkl": "METAL", "meins": "M", "werks": "1001", "lgort": "0001", "price": "45.00 TRY", "stock": 2400,
        "basic": { "gross": "1.5 kg", "net": "1.5 kg", "vol": "0.02 m3", "ean": "8690001234568" },
        "mrp": { "type": "PD", "controller": "C01", "reorder": "500", "lot": "EX", "safety": "200", "leadTime": "5 gün" },
        "purchasing": { "group": "P02", "minOrder": "50 M", "plifz": "5 gün", "orderUnit": "M", "autoPO": "Hayır", "sourceList": "İsteğe Bağlı" },
        "accounting": { "valClass": "3000", "priceControl": "V", "stdPrice": "42.00 TRY", "movPrice": "45.00 TRY", "totalVal": "108,000 TRY" },
        "quality": { "active": "Hayır", "controlKey": "-", "cert": "-", "targetSystem": "-" },
        "profitability": { "cost": "38.00 TRY", "margin": "%15.5", "contribution": "7.00 TRY/Birim", "ytdProfit": "₺16,800", "trend": "down" }
    },
    { "matnr": "sf-2001", "maktx": "Motor Gövdesi (Döküm)", "mtart": "HALB", "matkl": "MOTOR", "meins": "ADT", "werks": "1001", "lgort": "0002", "price": "250.00 TRY", "stock": 450 },
    { "matnr": "sf-2002", "maktx": "Fan Pervanesi", "mtart": "HALB", "matkl": "PLASTIK", "meins": "ADT", "werks": "1001", "lgort": "0002", "price": "45.00 TRY", "stock": 2100 },
    { "matnr": "FG-3001", "maktx": "Endüstriyel Fan M-100", "mtart": "FERT", "matkl": "MAKINE", "meins": "ADT", "werks": "1001", "lgort": "0003", "price": "1250.00 TRY", "stock": 85 },
    { "matnr": "FG-3002", "maktx": "Endüstriyel Fan L-200", "mtart": "FERT", "matkl": "MAKINE", "meins": "ADT", "werks": "1001", "lgort": "0003", "price": "1850.00 TRY", "stock": 42 },
    { "matnr": "RM-1003", "maktx": "Vida M8x40", "mtart": "ROH", "matkl": "HIRDAVAT", "meins": "ADT", "werks": "1001", "lgort": "0001", "price": "0.50 TRY", "stock": 50000 },
    { "matnr": "RM-1004", "maktx": "Conta (Kauçuk)", "mtart": "ROH", "matkl": "KIMYA", "meins": "ADT", "werks": "1001", "lgort": "0001", "price": "1.20 TRY", "stock": 15000 },
    { "matnr": "sf-2003", "maktx": "Rotor Mili", "mtart": "HALB", "matkl": "METAL", "meins": "ADT", "werks": "1001", "lgort": "0002", "price": "120.00 TRY", "stock": 300 },
    { "matnr": "FG-3003", "maktx": "Klima Ünitesi A-Class", "mtart": "FERT", "matkl": "CİHAZ", "meins": "ADT", "werks": "1001", "lgort": "0003", "price": "5400.00 TRY", "stock": 12 },
]

production_schedule = [
    { "id": 1, "machine": "CNC-01", "jobs": [
        { "id": "ORD-1001", "name": "Gövde İşleme", "start": 1, "duration": 3, "status": "completed" },
        { "id": "ORD-1004", "name": "Mil Tornalama", "start": 5, "duration": 4, "status": "running" }
    ]},
    { "id": 2, "machine": "Montaj A", "jobs": [
        { "id": "ORD-1002", "name": "Fan Montajı", "start": 2, "duration": 4, "status": "warning" }
    ]},
    { "id": 3, "machine": "Boya Hattı", "jobs": [
        { "id": "ORD-1003", "name": "Kapak Boyama", "start": 6, "duration": 2, "status": "pending" }
    ]},
    { "id": 4, "machine": "Paketleme", "jobs": [] },
    { "id": 5, "machine": "Kalite Kontrol", "jobs": [
        { "id": "ORD-1005", "name": "Son Kontrol", "start": 8, "duration": 2, "status": "pending" }
    ]}
]

# Simple Helper to simulate retrieval
def retrieve_relevant_data(query: str):
    relevant_data = {}
    
    # Simple keyword matching for demo
    if "stok" in query.lower() or "malzeme" in query.lower() or "fiyat" in query.lower() or "kar" in query.lower():
        relevant_data["materials"] = material_master_data
        
    if "üretim" in query.lower() or "makine" in query.lower() or "gecikme" in query.lower() or "iş" in query.lower():
        relevant_data["production"] = production_schedule
        
    # Default to everything if unclear (for small dataset)
    if not relevant_data:
        relevant_data = {
            "materials": material_master_data,
            "production": production_schedule
        }
        
    return relevant_data
