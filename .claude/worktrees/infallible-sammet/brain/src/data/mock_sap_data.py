
# Mock SAP Data Mirror — Sepenatural İlaç Üretim Verileri
# Frontend index.html ile senkron tutulmalıdır.

material_master_data = [
    {
        "matnr": "RM-KARA-MURVER-EKSTRE", "maktx": "Kara Murver Ekstresi", "mtart": "ROH",
        "matkl": "EKSTRE", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "50.40 USD", "stock": 18, "reorderPoint": 10, "minOrder": 5,
        "mrp": {"type": "PD", "leadTime": "14 gün", "safety": "5"},
        "purchasing": {"supplier": "Naturex GmbH", "minOrder": "5 KG", "autoPO": "Evet"},
        "accounting": {"valClass": "3100", "priceControl": "V", "movPrice": "50.40 USD"},
        "quality": {"active": "Evet", "cert": "GMP, ISO 9001"},
        "profitability": {"cost": "50.40 USD/kg", "trend": "stable"}
    },
    {
        "matnr": "RM-PROPOLIS-EKSTRESI", "maktx": "Propolis Ekstresi", "mtart": "ROH",
        "matkl": "EKSTRE", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "45.60 USD", "stock": 12, "reorderPoint": 8, "minOrder": 3,
        "mrp": {"type": "PD", "leadTime": "10 gün", "safety": "3"},
        "purchasing": {"supplier": "ApiPharm Ltd", "minOrder": "3 KG", "autoPO": "Evet"},
        "accounting": {"valClass": "3100", "priceControl": "V", "movPrice": "45.60 USD"},
        "quality": {"active": "Evet", "cert": "GMP"},
        "profitability": {"cost": "45.60 USD/kg", "trend": "up"}
    },
    {
        "matnr": "RM-TURUNC-EKSTRESI", "maktx": "Turunç Ekstresi", "mtart": "ROH",
        "matkl": "EKSTRE", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "84.00 USD", "stock": 4, "reorderPoint": 5, "minOrder": 2,
        "mrp": {"type": "PD", "leadTime": "21 gün", "safety": "2"},
        "purchasing": {"supplier": "CitrusBio Inc", "minOrder": "2 KG", "autoPO": "Hayır"},
        "accounting": {"valClass": "3100", "priceControl": "V", "movPrice": "84.00 USD"},
        "quality": {"active": "Evet", "cert": "GMP, Organic"},
        "profitability": {"cost": "84.00 USD/kg", "trend": "up"}
    },
    {
        "matnr": "RM-MEYAN-KOKU-EKSTRES", "maktx": "Meyan Kökü Ekstresi", "mtart": "ROH",
        "matkl": "EKSTRE", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "45.60 USD", "stock": 25, "reorderPoint": 10, "minOrder": 5,
        "mrp": {"type": "PD", "leadTime": "7 gün", "safety": "5"},
        "purchasing": {"supplier": "HerbalSource", "minOrder": "5 KG", "autoPO": "Evet"},
        "accounting": {"valClass": "3100", "priceControl": "V", "movPrice": "45.60 USD"},
        "quality": {"active": "Evet", "cert": "GMP"},
        "profitability": {"cost": "45.60 USD/kg", "trend": "stable"}
    },
    {
        "matnr": "RM-EKINEZYA-EKSTRESI", "maktx": "Ekinezya Ekstresi", "mtart": "ROH",
        "matkl": "EKSTRE", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "84.00 USD", "stock": 7, "reorderPoint": 6, "minOrder": 2,
        "mrp": {"type": "PD", "leadTime": "14 gün", "safety": "2"},
        "purchasing": {"supplier": "FloraExtract", "minOrder": "2 KG", "autoPO": "Hayır"},
        "accounting": {"valClass": "3100", "priceControl": "V", "movPrice": "84.00 USD"},
        "quality": {"active": "Evet", "cert": "GMP"},
        "profitability": {"cost": "84.00 USD/kg", "trend": "stable"}
    },
    {
        "matnr": "RM-VITAMIN-C", "maktx": "Vitamin C (Askorbik Asit)", "mtart": "ROH",
        "matkl": "VİTAMİN", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "18.50 USD", "stock": 45, "reorderPoint": 15, "minOrder": 10,
        "mrp": {"type": "PD", "leadTime": "7 gün", "safety": "10"},
        "purchasing": {"supplier": "DSM Nutritional", "minOrder": "10 KG", "autoPO": "Evet"},
        "accounting": {"valClass": "3100", "priceControl": "V", "movPrice": "18.50 USD"},
        "quality": {"active": "Evet", "cert": "GMP, USP"},
        "profitability": {"cost": "18.50 USD/kg", "trend": "down"}
    },
    {
        "matnr": "RM-ZERDEÇAL-EKSTRE", "maktx": "Zerdeçal Ekstresi", "mtart": "ROH",
        "matkl": "EKSTRE", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "62.00 USD", "stock": 9, "reorderPoint": 6, "minOrder": 3,
        "mrp": {"type": "PD", "leadTime": "14 gün", "safety": "3"},
        "purchasing": {"supplier": "SpicePharm", "minOrder": "3 KG", "autoPO": "Evet"},
        "accounting": {"valClass": "3100", "priceControl": "V", "movPrice": "62.00 USD"},
        "quality": {"active": "Evet", "cert": "GMP"},
        "profitability": {"cost": "62.00 USD/kg", "trend": "stable"}
    },
    {
        "matnr": "RM-KAPSUL-KILIF-0", "maktx": "Kapsül Kılıfı (Boş, Jelatin)", "mtart": "ROH",
        "matkl": "AMBALAJ", "meins": "ADT", "werks": "SEPE01", "lgort": "0002",
        "price": "0.008 USD", "stock": 250000, "reorderPoint": 100000, "minOrder": 50000,
        "mrp": {"type": "PD", "leadTime": "5 gün", "safety": "50000"},
        "purchasing": {"supplier": "CapsulTech", "minOrder": "50000 ADT", "autoPO": "Evet"},
        "quality": {"active": "Evet", "cert": "GMP"},
        "profitability": {"cost": "0.008 USD/adet", "trend": "stable"}
    },
    {
        "matnr": "RM-KUTU-60", "maktx": "Kutu 60'lık", "mtart": "ROH",
        "matkl": "AMBALAJ", "meins": "ADT", "werks": "SEPE01", "lgort": "0002",
        "price": "0.12 USD", "stock": 8000, "reorderPoint": 3000, "minOrder": 1000,
        "mrp": {"type": "PD", "leadTime": "3 gün", "safety": "1000"},
        "purchasing": {"supplier": "PharmaBox", "minOrder": "1000 ADT", "autoPO": "Evet"},
        "quality": {"active": "Hayır", "cert": "-"},
        "profitability": {"cost": "0.12 USD/adet", "trend": "stable"}
    },
    {
        "matnr": "RM-KUTU-90", "maktx": "Kutu 90'lık", "mtart": "ROH",
        "matkl": "AMBALAJ", "meins": "ADT", "werks": "SEPE01", "lgort": "0002",
        "price": "0.15 USD", "stock": 12000, "reorderPoint": 4000, "minOrder": 1000,
        "mrp": {"type": "PD", "leadTime": "3 gün", "safety": "1000"},
        "purchasing": {"supplier": "PharmaBox", "minOrder": "1000 ADT", "autoPO": "Evet"},
        "quality": {"active": "Hayır", "cert": "-"},
        "profitability": {"cost": "0.15 USD/adet", "trend": "stable"}
    },
    {
        "matnr": "RM-CHITOSAN", "maktx": "Chitosan Extract", "mtart": "ROH",
        "matkl": "EKSTRE", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "72.00 USD", "stock": 3, "reorderPoint": 4, "minOrder": 2,
        "mrp": {"type": "PD", "leadTime": "21 gün", "safety": "2"},
        "purchasing": {"supplier": "BioMarine Co", "minOrder": "2 KG", "autoPO": "Hayır"},
        "quality": {"active": "Evet", "cert": "GMP, Marine"},
        "profitability": {"cost": "72.00 USD/kg", "trend": "up"}
    },
    {
        "matnr": "RM-KOLAJEN", "maktx": "Hidrolize Kolajen", "mtart": "ROH",
        "matkl": "PROTEİN", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "38.00 USD", "stock": 20, "reorderPoint": 8, "minOrder": 5,
        "mrp": {"type": "PD", "leadTime": "10 gün", "safety": "5"},
        "purchasing": {"supplier": "CollagenPro", "minOrder": "5 KG", "autoPO": "Evet"},
        "quality": {"active": "Evet", "cert": "GMP, Halal"},
        "profitability": {"cost": "38.00 USD/kg", "trend": "stable"}
    },
    {
        "matnr": "RM-BIBERIYE-EKSTRE", "maktx": "Biberiye Ekstresi", "mtart": "ROH",
        "matkl": "EKSTRE", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "55.00 USD", "stock": 6, "reorderPoint": 5, "minOrder": 2,
        "mrp": {"type": "PD", "leadTime": "14 gün", "safety": "2"},
        "purchasing": {"supplier": "MedHerb", "minOrder": "2 KG", "autoPO": "Hayır"},
        "quality": {"active": "Evet", "cert": "GMP"},
        "profitability": {"cost": "55.00 USD/kg", "trend": "stable"}
    },
    {
        "matnr": "RM-OMEGA3", "maktx": "Omega-3 Balık Yağı", "mtart": "ROH",
        "matkl": "YAĞ", "meins": "KG", "werks": "SEPE01", "lgort": "0001",
        "price": "28.00 USD", "stock": 30, "reorderPoint": 12, "minOrder": 10,
        "mrp": {"type": "PD", "leadTime": "14 gün", "safety": "10"},
        "purchasing": {"supplier": "NordicOils", "minOrder": "10 KG", "autoPO": "Evet"},
        "quality": {"active": "Evet", "cert": "GMP, IFOS"},
        "profitability": {"cost": "28.00 USD/kg", "trend": "stable"}
    },
]

production_schedule = [
    {"id": 1, "machine": "Kapsülleme Hattı-1", "jobs": [
        {"id": "B-2025-001", "name": "Just 4 You Kompleks", "start": 1, "duration": 3, "status": "completed", "qty": 5000},
        {"id": "B-2025-002", "name": "Just 4 You Kompleks", "start": 6, "duration": 2, "status": "running", "qty": 3000},
    ]},
    {"id": 2, "machine": "Kapsülleme Hattı-2", "jobs": [
        {"id": "B-2025-003", "name": "Chitosan Extract", "start": 2, "duration": 2, "status": "completed", "qty": 2000},
        {"id": "B-2025-005", "name": "Kolajen Beauty Complex", "start": 5, "duration": 2, "status": "completed", "qty": 1500},
    ]},
    {"id": 3, "machine": "QC Kontrol", "jobs": [
        {"id": "B-2025-004", "name": "Vitamin C Plus — Karantina", "start": 4, "duration": 3, "status": "warning", "qty": 4000},
    ]},
    {"id": 4, "machine": "Paketleme", "jobs": [
        {"id": "B-2025-001P", "name": "Just 4 You Paketleme", "start": 5, "duration": 1, "status": "completed", "qty": 5000},
    ]},
    {"id": 5, "machine": "Depo / Sevkiyat", "jobs": [
        {"id": "B-2025-003S", "name": "Chitosan Sevkiyat", "start": 5, "duration": 1, "status": "pending", "qty": 2000},
    ]},
]


def retrieve_relevant_data(query: str):
    """Sorguya göre ilgili Sepenatural verilerini döndür."""
    relevant_data = {}
    q = query.lower()

    if any(k in q for k in ["stok", "malzeme", "hammadde", "fiyat", "tedarik", "supplier", "price", "stock"]):
        relevant_data["materials"] = material_master_data

    if any(k in q for k in ["üretim", "makine", "batch", "parti", "kapsül", "schedule", "production"]):
        relevant_data["production"] = production_schedule

    if any(k in q for k in ["just 4 you", "chitosan", "vitamin c", "kolajen", "omega", "ürün", "reçete", "bom"]):
        relevant_data["products_summary"] = [
            {"id": "P-JFY-001", "name": "Just 4 You Kompleks", "cpPerBox": 90, "mg": 900, "bom_count": 5, "status": "active"},
            {"id": "P-CHI-001", "name": "Chitosan Kitosan Extract", "cpPerBox": 90, "mg": 330, "bom_count": 1, "status": "active"},
            {"id": "P-VIT-001", "name": "Vitamin C Plus", "cpPerBox": 60, "mg": 500, "bom_count": 3, "status": "active"},
            {"id": "P-KOL-001", "name": "Kolajen Beauty Complex", "cpPerBox": 90, "mg": 750, "bom_count": 3, "status": "active"},
            {"id": "P-OMG-001", "name": "Omega-3 Premium", "cpPerBox": 60, "mg": 1000, "bom_count": 1, "status": "draft"},
        ]

    if any(k in q for k in ["maliyet", "kar", "fiyat", "cost", "profitability", "margin"]):
        relevant_data["cost_note"] = (
            "Maliyet hesaplama: 1 kutu maliyet = BOM'daki her hammaddenin (mg/kutu * fiyat_usd/kg) toplamı. "
            "USD/TRY kuru 44 varsayılan. Genel gider %10. Kâr çarpanı x2.0 (perakende)."
        )
        relevant_data["materials"] = material_master_data

    if not relevant_data:
        relevant_data = {
            "materials": material_master_data[:5],
            "production": production_schedule,
            "company": "Sepenatural — Doğal takviye ürünleri üreticisi. GMP sertifikalı kapsül üretimi."
        }

    return relevant_data
