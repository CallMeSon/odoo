# Panduan Inisialisasi Proyek Odoo Mamma Roti

Dokumen ini memberikan instruksi teknis untuk menyiapkan dan menjalankan lingkungan pengembangan Odoo 17 bagi proyek Mamma Roti menggunakan Docker.

## 1. Persyaratan Sistem
Pastikan perangkat Anda telah menginstal perangkat lunak berikut:
* Docker Desktop
* Docker Compose

## 2. Konfigurasi Lingkungan
Sebelum menjalankan layanan, Anda harus menyiapkan file konfigurasi lingkungan agar koneksi database dapat terbentuk dengan benar.

1. Clone repositori ini ke direktori lokal Anda.
2. Pastikan terdapat file bernama `.env` pada direktori akar proyek. Jika belum ada, buat file tersebut dan masukkan konfigurasi berikut:

```env
ODOO_HOST=db
ODOO_USER=odoo
ODOO_PASSWORD=admin123
POSTGRES_DB=postgres
POSTGRES_PASSWORD=admin123
POSTGRES_USER=odoo
```

## 3. Menjalankan Layanan
Buka terminal atau command prompt pada direktori proyek, lalu jalankan perintah berikut:

```bash
docker-compose up -d
```

Tunggu beberapa saat hingga layanan database dan aplikasi web siap diakses. Anda dapat memantau statusnya melalui Docker Desktop atau menggunakan perintah `docker-compose logs -f`.

## 4. Inisialisasi Data (Restore Database)
Untuk memastikan sistem langsung terisi dengan data master (Produk, Stok, BoM) serta konfigurasi spesifik Mamma Roti, lakukan prosedur pemulihan database berikut:

1. Dapatkan file backup database (format `.zip`) dari administrator proyek.
2. Akses halaman Database Manager melalui peramban pada alamat: `http://localhost:8069/web/database/manager`.
3. Pilih opsi **Restore Database**.
4. Masukkan parameter berikut:
   * **Master Password**: Sesuai dengan master key masing-masing.
   * **File**: Pilih file backup `.zip` yang telah Anda terima (db_Mamma_Roti.zip).
   * **Database Name**: Masukkan `mammaroti_final`.
5. Klik **Continue** dan tunggu hingga proses pemulihan selesai.

## 5. Akses dan Validasi
Setelah database berhasil dipulihkan, Anda dapat masuk ke sistem menggunakan kredensial berikut:

* **Email**: admin
* **Password**: admin

Untuk panduan pengujian alur bisnis yang meliputi Purchasing, Manufacturing, Point of Sale (POS), dan Accounting, silakan merujuk pada dokumen **[UAT_GUIDE.md](./UAT_GUIDE.md)**.

---
**Platform**: Odoo 17.0 Community
**Infrastruktur**: Docker & PostgreSQL 15
