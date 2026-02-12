# CLAUDE.md — Sepenatural ERP Projesi

## Proje Özeti
Sepenatural ilaç üretim ERP'si. Çok servisli FastAPI backend + React (inline Babel) frontend. Google Gemini ile RAG destekli AI asistan içerir.

## Mimari

```
frontend/index.html       — Tek dosya React uygulaması (Tailwind, Lucide)
api/src/main.py           — FastAPI gateway, tüm servisleri orkestre eder
ingestion/src/main.py     — SAP OData mock servisi (port 8001)
semantic-layer/src/       — Veri haritalama (port 8002)
brain/src/                — Analiz + RAG motoru (port 8003)
  ├── analyzer.py         — Kural tabanlı üretim analizi
  ├── rag_engine/engine.py — Google Gemini 2.5 Flash ile RAG
  ├── vector_store/client.py — pgvector PostgreSQL client
  └── data/
      ├── mock_sap_data.py — SAP mock verisi (hammadde/üretim)
      └── seed.py         — Vector store seed scripti
docker-compose.yml        — Tüm servisler + DB + Redis
.env.example              — Gerekli env değişkenleri
```

## Geliştirme Komutları

```bash
# Tüm servisleri başlat
docker-compose up -d

# Vector store'u doldur (ilk kurulumda)
docker-compose exec brain python -m src.data.seed

# Logları izle
docker-compose logs -f brain

# Tek servis yeniden başlat
docker-compose restart api
```

## Önemli Kurallar

- **`.env` dosyasını commit etme** — `.gitignore`'da var, `.env.example` kullan
- **Hardcoded API key bırakma** — `${GOOGLE_API_KEY}` env var kullan
- **Frontend port'u**: Nginx → 3000, API Gateway → 8000
- **Tenant ID**: Tüm isteklerde `X-Tenant-ID: sepenatural` header kullan
- **CORS**: API gateway sadece `localhost:3000`'e izin veriyor

## Veri Yapısı

Frontend'deki `rawMaterials` ve `products` dizileri ile `brain/src/data/seed.py`'daki veriler **senkron tutulmalı**.

Yeni ürün/hammadde eklendiğinde:
1. `frontend/index.html` içindeki array'e ekle
2. `brain/src/data/seed.py` içindeki array'e ekle
3. Seed scriptini yeniden çalıştır

## Sprint Durumu

- **Sprint 1 (Tamamlandı)**: Mimari, mock data, frontend UI, RAG altyapısı
- **Sprint 2 (Sonraki)**: Gerçek SAP OData bağlantısı, gerçek embedding, Netsys entegrasyonu
- **Sprint 3**: ML tabanlı analiz, maliyet optimizasyon
