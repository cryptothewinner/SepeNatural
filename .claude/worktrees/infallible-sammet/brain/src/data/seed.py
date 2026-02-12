"""
Vector Store Seed Script
Sepenatural ürün ve hammadde verilerini PostgreSQL pgvector'e yükler.
Kullanım: docker-compose exec brain python -m src.data.seed
"""

import os
import json
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

# Sepenatural hammadde ve ürün verisi (frontend ile senkron)
RAW_MATERIALS = [
    {"id": "RM-KARA-MURVER-EKSTRE", "name": "Kara Murver Ekstresi", "unit": "KG", "priceUsd": 50.4, "category": "EKSTRE", "supplier": "Naturex GmbH", "leadTime": 14, "minOrder": 5},
    {"id": "RM-PROPOLIS-EKSTRESI", "name": "Propolis Ekstresi", "unit": "KG", "priceUsd": 45.6, "category": "EKSTRE", "supplier": "ApiPharm Ltd", "leadTime": 10, "minOrder": 3},
    {"id": "RM-TURUNC-EKSTRESI", "name": "Turunç Ekstresi", "unit": "KG", "priceUsd": 84.0, "category": "EKSTRE", "supplier": "CitrusBio Inc", "leadTime": 21, "minOrder": 2},
    {"id": "RM-MEYAN-KOKU-EKSTRES", "name": "Meyan Kökü Ekstresi", "unit": "KG", "priceUsd": 45.6, "category": "EKSTRE", "supplier": "HerbalSource", "leadTime": 7, "minOrder": 5},
    {"id": "RM-EKINEZYA-EKSTRESI", "name": "Ekinezya Ekstresi", "unit": "KG", "priceUsd": 84.0, "category": "EKSTRE", "supplier": "FloraExtract", "leadTime": 14, "minOrder": 2},
    {"id": "RM-VITAMIN-C", "name": "Vitamin C (Askorbik Asit)", "unit": "KG", "priceUsd": 18.5, "category": "VİTAMİN", "supplier": "DSM Nutritional", "leadTime": 7, "minOrder": 10},
    {"id": "RM-ZERDEÇAL-EKSTRE", "name": "Zerdeçal Ekstresi", "unit": "KG", "priceUsd": 62.0, "category": "EKSTRE", "supplier": "SpicePharm", "leadTime": 14, "minOrder": 3},
    {"id": "RM-KAPSUL-KILIF-0", "name": "Kapsül Kılıfı (Boş, Jelatin)", "unit": "ADT", "priceUsd": 0.008, "category": "AMBALAJ", "supplier": "CapsulTech", "leadTime": 5, "minOrder": 50000},
    {"id": "RM-KUTU-60", "name": "Kutu 60'lık", "unit": "ADT", "priceUsd": 0.12, "category": "AMBALAJ", "supplier": "PharmaBox", "leadTime": 3, "minOrder": 1000},
    {"id": "RM-KUTU-90", "name": "Kutu 90'lık", "unit": "ADT", "priceUsd": 0.15, "category": "AMBALAJ", "supplier": "PharmaBox", "leadTime": 3, "minOrder": 1000},
    {"id": "RM-ETIKET", "name": "Etiket (Baskılı)", "unit": "ADT", "priceUsd": 0.03, "category": "AMBALAJ", "supplier": "LabelPrint", "leadTime": 5, "minOrder": 5000},
    {"id": "RM-CHITOSAN", "name": "Chitosan Extract", "unit": "KG", "priceUsd": 72.0, "category": "EKSTRE", "supplier": "BioMarine Co", "leadTime": 21, "minOrder": 2},
    {"id": "RM-KOLAJEN", "name": "Hidrolize Kolajen", "unit": "KG", "priceUsd": 38.0, "category": "PROTEİN", "supplier": "CollagenPro", "leadTime": 10, "minOrder": 5},
    {"id": "RM-BIBERIYE-EKSTRE", "name": "Biberiye Ekstresi", "unit": "KG", "priceUsd": 55.0, "category": "EKSTRE", "supplier": "MedHerb", "leadTime": 14, "minOrder": 2},
    {"id": "RM-OMEGA3", "name": "Omega-3 Balık Yağı", "unit": "KG", "priceUsd": 28.0, "category": "YAĞ", "supplier": "NordicOils", "leadTime": 14, "minOrder": 10},
]

PRODUCTS = [
    {
        "id": "P-JFY-001", "stockNo": "000632-A", "name": "Just 4 You Kompleks",
        "form": "Kapsül", "barcode": "8680462001153", "cpPerBox": 90, "mgPerCapsule": 900,
        "description": "Bağışıklık destek kompleksi", "category": "TAKVİYE", "status": "active",
        "bom": [
            {"rmId": "RM-KARA-MURVER-EKSTRE", "seq": 10, "qtyMgPerCapsule": 270},
            {"rmId": "RM-PROPOLIS-EKSTRESI", "seq": 20, "qtyMgPerCapsule": 125},
            {"rmId": "RM-TURUNC-EKSTRESI", "seq": 30, "qtyMgPerCapsule": 125},
            {"rmId": "RM-MEYAN-KOKU-EKSTRES", "seq": 40, "qtyMgPerCapsule": 125},
            {"rmId": "RM-EKINEZYA-EKSTRESI", "seq": 50, "qtyMgPerCapsule": 125},
        ]
    },
    {
        "id": "P-CHI-001", "stockNo": "000014-A", "name": "Chitosan Kitosan Extract",
        "form": "Kapsül", "barcode": "8680462000156", "cpPerBox": 90, "mgPerCapsule": 330,
        "description": "Kilo kontrol desteği", "category": "TAKVİYE", "status": "active",
        "bom": [{"rmId": "RM-CHITOSAN", "seq": 10, "qtyMgPerCapsule": 330}]
    },
    {
        "id": "P-VIT-001", "stockNo": "000045-A", "name": "Vitamin C Plus",
        "form": "Kapsül", "barcode": "8680462001160", "cpPerBox": 60, "mgPerCapsule": 500,
        "description": "Güçlendirilmiş C vitamini", "category": "VİTAMİN", "status": "active",
        "bom": [
            {"rmId": "RM-VITAMIN-C", "seq": 10, "qtyMgPerCapsule": 400},
            {"rmId": "RM-ZERDEÇAL-EKSTRE", "seq": 20, "qtyMgPerCapsule": 50},
            {"rmId": "RM-BIBERIYE-EKSTRE", "seq": 30, "qtyMgPerCapsule": 50},
        ]
    },
    {
        "id": "P-KOL-001", "stockNo": "000078-A", "name": "Kolajen Beauty Complex",
        "form": "Kapsül", "barcode": "8680462001177", "cpPerBox": 90, "mgPerCapsule": 750,
        "description": "Cilt, saç, tırnak desteği", "category": "GÜZELLİK", "status": "active",
        "bom": [
            {"rmId": "RM-KOLAJEN", "seq": 10, "qtyMgPerCapsule": 500},
            {"rmId": "RM-VITAMIN-C", "seq": 20, "qtyMgPerCapsule": 150},
            {"rmId": "RM-BIBERIYE-EKSTRE", "seq": 30, "qtyMgPerCapsule": 100},
        ]
    },
    {
        "id": "P-OMG-001", "stockNo": "000091-A", "name": "Omega-3 Premium",
        "form": "Kapsül", "barcode": "8680462001184", "cpPerBox": 60, "mgPerCapsule": 1000,
        "description": "Yüksek EPA/DHA omega-3", "category": "TAKVİYE", "status": "draft",
        "bom": [{"rmId": "RM-OMEGA3", "seq": 10, "qtyMgPerCapsule": 1000}]
    },
]

BATCH_RECORDS = [
    {"id": "B-2025-001", "productId": "P-JFY-001", "qty": 5000, "date": "2025-01-15", "expiry": "2027-01-15", "status": "released", "qcStatus": "passed"},
    {"id": "B-2025-002", "productId": "P-JFY-001", "qty": 3000, "date": "2025-02-01", "expiry": "2027-02-01", "status": "in_production", "qcStatus": "pending"},
    {"id": "B-2025-003", "productId": "P-CHI-001", "qty": 2000, "date": "2025-01-20", "expiry": "2027-01-20", "status": "released", "qcStatus": "passed"},
    {"id": "B-2025-004", "productId": "P-VIT-001", "qty": 4000, "date": "2025-02-05", "expiry": "2027-02-05", "status": "quarantine", "qcStatus": "testing"},
    {"id": "B-2025-005", "productId": "P-KOL-001", "qty": 1500, "date": "2025-02-10", "expiry": "2027-02-10", "status": "released", "qcStatus": "passed"},
]


def build_documents():
    """Tüm verileri düz metin dokümanlara dönüştürür (embedding için)."""
    docs = []

    # Her hammaddeyi bir doküman olarak ekle
    for rm in RAW_MATERIALS:
        content = (
            f"Hammadde: {rm['name']} (ID: {rm['id']})\n"
            f"Kategori: {rm['category']}, Birim: {rm['unit']}\n"
            f"Fiyat: ${rm['priceUsd']}/kg, Tedarikçi: {rm['supplier']}\n"
            f"Teslim Süresi: {rm['leadTime']} gün, Min. Sipariş: {rm['minOrder']} {rm['unit']}"
        )
        docs.append({"content": content, "metadata": json.dumps({"type": "raw_material", "id": rm["id"]})})

    # Her ürünü ve BOM'unu bir doküman olarak ekle
    rm_map = {rm["id"]: rm for rm in RAW_MATERIALS}
    for p in PRODUCTS:
        bom_lines = []
        for item in p["bom"]:
            rm = rm_map.get(item["rmId"])
            if rm:
                bom_lines.append(f"  - {rm['name']}: {item['qtyMgPerCapsule']}mg/kapsül (${rm['priceUsd']}/kg)")
        bom_text = "\n".join(bom_lines)
        content = (
            f"Ürün: {p['name']} (Stok No: {p['stockNo']}, ID: {p['id']})\n"
            f"Form: {p['form']}, {p['cpPerBox']} kapsül x {p['mgPerCapsule']}mg\n"
            f"Kategori: {p['category']}, Durum: {p['status']}\n"
            f"Açıklama: {p['description']}\n"
            f"Barkod: {p['barcode']}\n"
            f"BOM (Reçete):\n{bom_text}"
        )
        docs.append({"content": content, "metadata": json.dumps({"type": "product", "id": p["id"]})})

    # Parti kayıtlarını ekle
    p_map = {p["id"]: p for p in PRODUCTS}
    for b in BATCH_RECORDS:
        prod = p_map.get(b["productId"])
        content = (
            f"Parti: {b['id']}\n"
            f"Ürün: {prod['name'] if prod else b['productId']}\n"
            f"Miktar: {b['qty']} adet, Üretim: {b['date']}, SKT: {b['expiry']}\n"
            f"Durum: {b['status']}, QC: {b['qcStatus']}"
        )
        docs.append({"content": content, "metadata": json.dumps({"type": "batch", "id": b["id"]})})

    return docs


def run_seed():
    db_url = os.getenv("DATABASE_URL", "postgresql://antigravity:antigravity_secret@db:5432/sap_pp_core")
    logger.info(f"Connecting to DB: {db_url}")

    try:
        from .client import VectorStoreClient
    except ImportError:
        from brain.src.vector_store.client import VectorStoreClient

    try:
        store = VectorStoreClient(db_url)
    except Exception as e:
        logger.error(f"DB bağlantı hatası: {e}")
        sys.exit(1)

    docs = build_documents()
    logger.info(f"{len(docs)} doküman hazırlandı, vector store'a ekleniyor...")

    # Embedding olmadan içerik olarak ekle (zero-vector ile)
    # Gerçek embedding için Google Gemini embedding API kullanılabilir
    docs_with_embedding = []
    for doc in docs:
        docs_with_embedding.append({
            "content": doc["content"],
            "metadata": doc["metadata"],
            "embedding": [0.0] * 1536  # Placeholder — gerçek embedding için güncelle
        })

    store.add_documents(docs_with_embedding, tenant_id="sepenatural")
    logger.info(f"Seed tamamlandı. {len(docs_with_embedding)} doküman eklendi.")


if __name__ == "__main__":
    run_seed()
