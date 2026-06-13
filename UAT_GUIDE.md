# Panduan User Acceptance Testing (UAT) & Handover
## Implementasi ERP Odoo — Mamma Roti

Dokumen ini berfungsi sebagai panduan bagi pengguna (Mamma Roti) untuk melakukan pengujian akhir dan sebagai referensi operasional setelah sistem go-live.

---

### 1. Personas & Akses Pengguna
Berikut adalah peran yang telah dikonfigurasi dalam sistem:

| Peran | Tanggung Jawab Utama | Pengguna Terkait (Login) |
| :--- | :--- | :--- |
| **Warehouse/Gudang** | Penerimaan barang (Receipt), Internal Transfer, Cek Stok. | warehouse@mammaroti.com |
| **Production/Produksi** | Pembuatan MO, Konsumsi bahan baku, Work Order. | warehouse@mammaroti.com |
| **Purchasing** | Pembuatan RFQ, Purchase Order ke Vendor. | warehouse@mammaroti.com |
| **Finance/Accounting** | Validasi Invoice, Pembayaran, Laporan Keuangan. | finance@mammaroti.com |
| **Store Manager** | Monitor penjualan POS, Closing Session. | store.manager@mammaroti.com |
| **Cashier** | Transaksi POS harian. | cashier@mammaroti.com |

---

### 2. Skenario Pengujian (UAT Checklist)

#### Fase 1: Pengadaan Bahan Baku (Purchasing)
- [ ] Membuat RFQ ke Vendor (misal: PT Bogasari).
- [ ] Verifikasi Double Validation (PO > Rp 5.000.000 butuh persetujuan manajer).
- [ ] Menerima barang (Receipt) dan memasukkan nomor LOT serta Expiry Date.
- [ ] Verifikasi stok bahan baku bertambah di lokasi **'GUT/Stock'**.

#### Fase 2: Produksi (Manufacturing)
- [ ] Membuat Manufacturing Order (MO) untuk produk (misal: Mexican Buns Chocolate).
- [ ] Verifikasi reservasi bahan baku menggunakan strategi **FEFO** (barang paling lama kedaluwarsa diambil dulu).
- [ ] Mencatat Work Order (Mixing & Packing) untuk menangkap biaya tenaga kerja di lokasi **'CK/Produksi'**.
- [ ] Menyelesaikan MO dan memverifikasi stok produk jadi bertambah dengan nomor LOT baru.

#### Fase 3: Distribusi Internal (Logistik)
- [ ] Melakukan Internal Transfer dari Gudang Utama ke **'GUT/Stock/Cold Storage'**.
- [ ] Verifikasi stok di Cold Storage tercatat dengan akurat.

#### Fase 4: Penjualan (POS & B2B)
- [ ] **POS:** Membuka sesi kasir, melakukan transaksi, menerima pembayaran, dan menutup sesi (Closing).
- [ ] **B2B:** Membuat Sales Order (SO) untuk Mitra, melakukan pengiriman (Delivery), dan membuat Invoice.
- [ ] Verifikasi stok berkurang secara otomatis setelah transaksi/pengiriman.

#### Fase 5: Akuntansi (Finance)
- [ ] Verifikasi Jurnal Otomatis yang terbentuk dari transaksi Stok, PO, dan POS.
- [ ] Mengecek Laporan Laba Rugi (P&L) dan Neraca (Balance Sheet).
- [ ] Verifikasi perhitungan Harga Pokok Penjualan (HPP/COGS).

---

### 3. Ringkasan Master Data
- **Produk Jadi:** 16 Item (Mexican Buns & Drinks).
- **Bahan Baku:** 18 Item (Tepung, Margarin, Cokelat, dll).
- **Vendor:** 11 Supplier aktif terdaftar.
- **Lokasi:** GUT/Stock, GUT/Production, GUT/Cold Storage.

---

### 4. Rekomendasi Selanjutnya
1. **Transisi ke Average Cost (AVCO):** Saat ini sistem menggunakan Standard Price. Untuk akurasi margin yang lebih dinamis mengikuti fluktuasi harga bahan baku, disarankan beralih ke AVCO.
2. **E-Wallet Integration:** Memperluas metode pembayaran QRIS di POS Odoo.
3. **Training Karyawan Gerai:** Fokus pada adaptasi penggunaan POS Odoo di 130+ outlet lainnya.

---
**Status Sistem:** 100% Verified & Operational.
**Tanggal Handover:** 13 Juni 2026
**Tim Proyek:** Kelompok 5 (UPNVJ)
