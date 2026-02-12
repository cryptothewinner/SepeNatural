# Sepenatural — İlaç Üretim & Maliyet Yönetim Sistemi

Sepenatural için geliştirilmiş, çok servisli (microservice) üretim planlama ve maliyet yönetimi platformu. RAG (Retrieval-Augmented Generation) destekli AI asistan içerir.

## Mimari

```
frontend (port 3000)  →  api-gateway (port 8000)
                              ├── ingestion   (port 8001)  SAP OData bağlantısı
                              ├── semantic-layer (port 8002)  Veri haritalama
                              └── brain       (port 8003)  Analiz + RAG (Gemini)
                                   └── PostgreSQL pgvector (port 5432)
                                   └── Redis (port 6379)
```

## Hızlı Başlangıç

### 1. Ortam değişkenlerini ayarla

```bash
cp .env.example .env
# .env dosyasını düzenle: GOOGLE_API_KEY değerini gir
```

### 2. Servisleri başlat

```bash
docker-compose up -d
```

### 3. Vector store'u seed et (ilk çalıştırmada)

```bash
docker-compose exec brain python -m src.data.seed
```

### Erişim

| Servis | URL |
|--------|-----|
| Frontend | http://localhost:3000 |
| API Gateway | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

## Özellikler

- **Ürün & BOM Yönetimi** — Reçete bazlı hammadde takibi
- **Maliyet Motoru** — USD kuruna göre dinamik maliyet hesaplama
- **Maliyet Tablosu** — Tüm ürünlerin karşılaştırmalı analizi
- **Parti Yönetimi** — Üretim partisi ve QC takibi
- **Fiyat Listeleri** — Kanal bazlı fiyatlandırma (perakende, toptan, eczane, ihracat)
- **AI Asistan** — Google Gemini destekli RAG ile üretim verisi analizi
- **Netsys Entegrasyon** — ERP senkronizasyonu (geliştirme aşamasında)

## Servisler

### API Gateway (`/api`)
Ana giriş noktası. Tüm servisleri orkestre eder.

- `GET /health`
- `GET /analyze/full/{order_id}` — Tam pipeline analizi
- `POST /brain/rag/analyze` — AI analiz proxy
- `GET /ingestion/production-orders` — Üretim emirleri

### Brain Service (`/brain`)
Analiz motoru ve RAG.

- `POST /brain/analyze/order` — Kural tabanlı order analizi
- `POST /brain/rag/analyze` — Gemini ile AI analiz

### Ingestion Service (`/ingestion`)
SAP OData bağlantısı (Sprint 1: mock).

- `GET /ingest/production-orders`

### Semantic Layer (`/semantic-layer`)
Veri haritalama servisi.

- `POST /semantic/map/order`

## Geliştirme Notları

- Tüm servisler `X-Tenant-ID` header desteğiyle çok kiracılı yapıda çalışır
- RAG motoru Google Gemini 2.5 Flash kullanır; `GOOGLE_API_KEY` gereklidir
- Frontend API erişilemezseyerel veri fallback devreye girer
- Vector store seed scripti: `docker-compose exec brain python -m src.data.seed`
