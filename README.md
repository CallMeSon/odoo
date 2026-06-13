# Implementasi ERP Odoo — Mamma Roti

[![Odoo Version](https://img.shields.io/badge/Odoo-17.0-714B67.svg)](https://www.odoo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Repositori ini berisi konfigurasi, data master, dan skrip otomasi untuk implementasi ERP Odoo 17 pada **Mamma Roti**. Proyek ini mencakup seluruh rantai pasok mulai dari pengadaan bahan baku, produksi (CK), distribusi, hingga penjualan di gerai (POS).

## 🚀 Fitur Utama

- **📦 Inventory & Supply Chain:**
  - Strategi pengambilan barang **FEFO (First Expiry First Out)**.
  - Tracking nomor LOT dan tanggal kedaluwarsa untuk bahan baku.
  - Manajemen lokasi multi-gudang (Gudang Utama, Cold Storage, Mitra Demo).
- **🏭 Manufacturing (MRP):**
  - Manajemen Recipe (Bill of Materials) untuk roti dan minuman.
  - Perhitungan Biaya Tenaga Kerja melalui Work Center (Mixing & Packing).
  - Integrasi otomatis konsumsi stok saat produksi.
- **🏪 Point of Sale (POS):**
  - Konfigurasi khusus untuk outlet mitra.
  - Sinkronisasi stok real-time antara outlet dan pusat.
- **🧾 Accounting & Finance:**
  - Inventarisasi otomatis (Automated Valuation).
  - Laporan Laba Rugi dan Neraca yang terintegrasi.
  - Chart of Accounts (CoA) yang telah disesuaikan.

## 🛠️ Tech Stack

- **Platform:** Odoo 17.0 (Community/Enterprise)
- **Database:** PostgreSQL 15
- **Infrastructure:** Docker & Docker Compose
- **Automation:** Python Scripts (OdooRPC/XML-RPC)

## 📂 Struktur Repositori

```text
C:\odoo\
├── custom_addons/          # Modul kustom dan skrip otomasi
│   ├── data_import/        # Skrip inisialisasi data (Python)
│   └── ...                 # Modul Odoo tambahan (MIS Builder, Report XLSX, dll)
├── PRODUCT_*.csv           # Master data produk dan kategori
├── RAW_MATERIAL.csv        # Master data bahan baku
├── VENDOR.csv              # Master data supplier
├── BRD.md                  # Business Requirements Document
├── UAT_GUIDE.md            # Panduan pengujian pengguna (UAT)
└── docker-compose.yaml     # Konfigurasi containerisasi
```

## ⚙️ Cara Instalasi

### 1. Prasyarat
Pastikan Anda sudah menginstal:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 2. Setup Lingkungan
Salin file `.env.example` menjadi `.env` dan sesuaikan kredensial database Anda.
```bash
cp .env.example .env
```

### 3. Menjalankan Odoo
Jalankan perintah berikut di root direktori:
```bash
docker-compose up -d
```
Akses Odoo melalui browser di `http://localhost:8069`.

### 4. Inisialisasi Data (Opsional)
Gunakan skrip di folder `custom_addons/data_import/` untuk mengimpor data secara otomatis:
```bash
# Contoh menjalankan skrip import
python custom_addons/data_import/import_data.py
```

## 🧪 Pengujian (UAT)
Untuk memverifikasi sistem, silakan ikuti langkah-langkah yang ada di [UAT_GUIDE.md](./UAT_GUIDE.md). Panduan tersebut mencakup skenario dari Purchasing hingga Accounting.

## 👥 Tim Proyek
Implementasi ini dilakukan oleh **Kelompok 5 - Sistem ERP (UPNVJ)**:
- Fokus: Optimasi Supply Chain & Manufacturing Mamma Roti.

---
