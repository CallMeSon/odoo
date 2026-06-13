# 

# **Business Requirements Document (BRD)** {#business-requirements-document-(brd)}

![][image1]

| Field  | Detail  |  |
| :---- | :---- | ----- |
| Nama Proyek  | Implementasi ERP Odoo — Mamma Roti  |  |
| Versi | 1.0 |  |
| Tanggal | 12/05/2026 |  |

### Table of Contents {#table-of-contents}

[**Business Requirements Document (BRD)	1**](#business-requirements-document-\(brd\))

[Table of Contents	2](#table-of-contents)

[1\. Introduction	3](#1.-introduction)

[1.1 Latar Belakang & Konteks Bisnis	3](#1.1-latar-belakang-&-konteks-bisnis)

[1.2 Purpose of the Document	3](#1.2-purpose-of-the-document)

[1.3 Scope of the Project	4](#1.3-scope-of-the-project)

[2\. Business Objectives	6](#2.-business-objectives)

[2.1 Business Goals	6](#2.1-business-goals)

[2.2 Project Objectives	6](#2.2-project-objectives)

[2.3 Success Criteria	7](#2.3-success-criteria)

[3\. Current Business Environment	8](#3.-current-business-environment)

[3.1 Current Processes	8](#3.1-current-processes)

[3.2 Challenges and Issues	8](#3.2-challenges-and-issues)

[4\. Proposed Solution	9](#4.-proposed-solution)

[4.1 Description of the Solution	9](#4.1-description-of-the-solution)

[4.2 Functional Requirements	9](#4.2-functional-requirements)

[4.3 Non-Functional Requirements	10](#4.3-non-functional-requirements)

[5\. Stakeholders	11](#5.-stakeholders)

[5.1 List of Stakeholders	11](#5.1-list-of-stakeholders)

[5.2 Roles and Responsibilities	11](#5.2-roles-and-responsibilities)

[6\. Constraints	12](#6.-constraints)

[6.1 Budgetary Constraints	12](#6.1-budgetary-constraints)

[6.2 Timeline Constraints	12](#6.2-timeline-constraints)

[6.3 Regulatory Constraints	12](#6.3-regulatory-constraints)

[7\. Assumptions	13](#7.-assumptions)

[7.1 List of Assumptions	13](#7.1-list-of-assumptions)

[8\. Risks	14](#8.-risks)

[8.1 List of Risks	14](#8.1-list-of-risks)

[8.2 Risk Mitigation Strategies	14](#8.2-risk-mitigation-strategies)

[9\. Dependencies	15](#9.-dependencies)

[9.1 List of Dependencies	15](#9.1-list-of-dependencies)

[10\. Approval	16](#10.-approval)

[10.1 Sign-off	16](#10.1-sign-off)

### **1\. Introduction** {#1.-introduction}

#### **1.1 Latar Belakang & Konteks Bisnis** {#1.1-latar-belakang-&-konteks-bisnis}

Mamma Roti didirikan pada tahun 2022 dengan 5 outlet di Bandung, Bekasi, dan Jakarta Timur. Dalam waktu singkat, perusahaan berkembang menjadi lebih dari 130 outlet di seluruh Indonesia dengan produk utama roti dan minuman.

Saat ini, operasional mengandalkan Moka POS untuk penjualan dan Accurate untuk akuntansi. Kedua sistem berjalan terpisah, sementara sebagian besar proses lain masih manual melalui spreadsheet dan WhatsApp. Kondisi ini menyebabkan data terfragmentasi, sulitnya akses informasi real-time, dan terhambatnya pengambilan keputusan.

Setelah evaluasi, Mamma Roti memilih Odoo sebagai ERP utama karena sifatnya open-source, fleksibel, dan modular. Implementasi ini difokuskan pada Central Kitchen dan Gudang Utama sebagai fondasi sistem terintegrasi yang mendukung ekspansi ke depan.

#### **1.2 Purpose of the Document** {#1.2-purpose-of-the-document}

Dokumen Business Requirements Document (BRD) ini disusun untuk mendefinisikan secara jelas dan komprehensif kebutuhan bisnis, tujuan, ruang lingkup, serta persyaratan teknis dan fungsional untuk implementasi ERP Odoo di Mamma Roti. Dokumen ini berfungsi sebagai acuan utama bagi seluruh pihak yang terlibat dalam proyek, termasuk tim manajemen Mamma Roti, tim proyek implementasi, vendor/partner Odoo, serta stakeholder terkait lainnya.  
BRD ini bertujuan untuk memastikan pemahaman yang seragam terhadap visi proyek, mengurangi risiko kesalahpahaman selama implementasi, dan menyediakan dasar yang jelas untuk pengembangan, pengujian, serta evaluasi keberhasilan sistem yang akan dibangun.

#### **1.3 Scope of the Project** {#1.3-scope-of-the-project}

Implementasi ERP Odoo di Mamma Roti mencakup modul-modul utama yang mendukung operasional bisnis, meliputi namun tidak terbatas pada:

| Modul | Tujuan |
| :---- | :---- |
| Point of Sale (POS) | Menggantikan dan mengintegrasikan fungsi penjualan untuk transaksi di seluruh outlet |
| Inventory/Stock Management | Manajemen stok bahan baku dan produk jadi secara real-time di seluruh outlet  |
| Purchase/Purchasing | Otomatisasi proses pemesanan bahan baku (pengganti pemesanan via WhatsApp manual)  |
| Accounting & Finance | Integrasi laporan keuangan yang menggantikan/mengintegrasikan Accurate  |
| Sales Management | Monitoring penjualan outlet secara real-time dan konsolidasi data  |
| Manufacturing/Production | Manajemen proses produksi roti di level pusat/komisariat  |
| Human Resources (HR)  | Manajemen data karyawan, absensi, dan penggajian (Payroll) di seluruh outlet  |
| Dashboard & Reporting  | Visualisasi data real-time dan laporan analitik untuk manajemen pusat  |

Implementasi pada tahap ini mencakup operasional Central Kitchen dan Gudang Utama sebagai pilot project, dengan potensi perluasan ke gerai-gerai lainnya pada tahap selanjutnya.

Out-of-Scope:

* Integrasi langsung dengan seluruh gerai/outlet (130+ outlet) akan menjadi tahapan ekspansi setelah pilot project berhasil   
* Modul eCommerce/Website untuk penjualan online langsung ke konsumen  
* Pengembangan aplikasi mobile native terpisah dari Odoo  
* Migrasi data historis dari Moka POS dan Accurate yang melebihi periode yang akan ditentukan  
* Perubahan infrastruktur hardware (jika tidak termasuk dalam kesepakatan implementasi)

### **2\. Business Objectives** {#2.-business-objectives}

#### **2.1 Business Goals** {#2.1-business-goals}

Implementasi ERP Odoo di Mamma Roti bertujuan untuk mencapai efisiensi operasional yang signifikan serta mempersiapkan fondasi sistem yang kuat dalam menghadapi ekspansi bisnis ke depan. Tujuan bisnis utama yang ingin dicapai meliputi: 

1. Meningkatkan Efisiensi Operasional   
   Mengurangi downtime operasional bisnis yang disebabkan oleh proses manual, data yang terfragmentasi, dan ketergantungan pada komunikasi informal (WhatsApp) untuk pemesanan bahan baku.   
2. Mempercepat Pengambilan Keputusan   
   Menyediakan akses data operasional dan keuangan yang akurat serta real-time bagi manajemen, sehingga keputusan strategis dapat diambil lebih cepat dan berbasis fakta.   
3. Mengotomasi Laporan   
   Menggantikan proses penyusunan laporan manual menggunakan spreadsheet dengan sistem yang menghasilkan laporan keuangan, stok, dan operasional secara otomatis dan terintegrasi.   
4. Menciptakan Single Source of Truth   
   Menyatukan seluruh data bisnis Mamma Roti ke dalam satu sistem ERP Odoo yang terpusat, mulai dari pengadaan bahan baku, produksi, stok, penjualan, hingga sumber daya manusia. 

#### **2.2 Project Objectives** {#2.2-project-objectives}

Untuk mendukung tujuan bisnis di atas, proyek implementasi ERP Odoo ini memiliki objektif teknis dan operasional yang spesifik sebagai berikut: 

| No | Project Objective  | Deskripsi  |
| :---- | :---- | :---- |
| 1 | Pelacakan Stok Bahan Baku Real-Time | Memungkinkan tim Central Kitchen dan Gudang Utama untuk memantau ketersediaan stok bahan baku secara langsung dan akurat dalam sistem Odoo.  |
| 2  | Sistem FEFO (First Expired First Out) | Mengimplementasikan manajemen persediaan berbasis tanggal kedaluwarsa (expiry date) untuk memastikan bahan baku digunakan sesuai prioritas kedaluwarsa, mengurangi waste, dan menjaga kualitas produk.  |
| 3 | Pencatatan Bill of Materials (BoM) | Mendokumentasikan resep/formula produksi (BoM) untuk setiap jenis produk roti di Central Kitchen, sehingga biaya produksi per unit dapat dikalkulasi dengan tepat. |
| 4 | Integrasi Data Transaksi .  | Mengalirkan data transaksi penjualan ke sistem pusat Odoo untuk konsolidasi laporan penjualan.  |
| 5 | Laporan Keuangan Terintegrasi  | Menyatukan data keuangan dari berbagai unit operasional sehingga laporan keuangan dapat disusun secara terintegrasi dan terstandarisasi.  |
| 6 | Manajemen Sumber Daya Manusia (HR)  | Mengelola data karyawan, absensi, dan penggajian (payroll) di Central Kitchen dan Gudang Utama secara terstruktur dalam satu sistem.  |
| 7 | Pemantauan Pengiriman Produk ke Gerai  | Mencatat dan memantau proses distribusi produk dari Central Kitchen/Gudang Utama ke gerai-gerai Mamma Roti untuk memastikan visibilitas rantai pasok.  |

#### **2.3 Success Criteria** {#2.3-success-criteria}

Keberhasilan proyek implementasi ERP Odoo akan diukur berdasarkan kriteria berikut: 

| No | Success Criteria | Indikator  |
| :---- | ----- | :---- |
| 1 | Pengurangan Waktu Penyusunan Laporan Keuangan  | Waktu yang dibutuhkan untuk menyusun laporan keuangan berkurang secara signifikan dibandingkan dengan proses manual sebelumnya.  |
| 2 | Peningkatan Akurasi Stok  | Tingkat akurasi data stok bahan baku dan produk jadi meningkat secara substansial melalui pencatatan real-time di sistem Odoo.  |
| 3 | Kompetensi Pengguna Sistem  | Seluruh karyawan terkait di Central Kitchen dan Gudang Utama lulus training dan mampu mengoperasikan modul-modul Odoo yang relevan dengan pekerjaannya secara mandiri.  |
| 4 | Go-Live yang Stabil  | Sistem berhasil di-*go-live*\-kan tanpa mengalami downtime kritis yang berkepanjangan, sehingga operasional bisnis tidak terganggu secara material.  |

### **3\. Current Business Environment** {#3.-current-business-environment}

#### **3.1 Current Processes** {#3.1-current-processes}

Berdasarkan hasil observasi, wawancara dengan manajemen, dan survei internal yang telah dilakukan, berikut adalah gambaran umum proses bisnis yang berjalan saat ini di Mamma Roti, difokuskan pada operasional Central Kitchen dan Gudang Utama

Operasional Mamma Roti mengadopsi model make-to-order, di mana proses produksi baru dimulai setelah adanya pesanan dan pembayaran dari mitra (franchise). Alur rantai pasok berjalan sebagai berikut:

| Tahap | Identifikasi |  |
| :---- | :---- | ----- |
| Pemesanan | Proses: Mitra melakukan pemesanan bahan baku atau produk jadi melalui grup WhatsApp khusus per outlet. Tim admin mengkonfirmasi pesanan dan tim finance menerbitkan invoice. Pembayaran dilakukan di muka (upfront).  |  |
|  | Pelaku: Mitra, Admin, Finance |  |
|  | Media/Tools: WhatsApp Group per Outlet |  |
| Pengadaan Bahan Baku | Proses:Tim gudang mengidentifikasi stok penyangga (buffer stock). Jika menipis, tim purchasing memesan bahan baku dari supplier (misal: Bogasari untuk tepung, supplier impor untuk coklat). Lead time pemesanan ke vendor memerlukan waktu 2 hari setelah pembayaran.  |  |
|  | Pelaku: Gudang, Purchasing  |  |
|  | Media/Tools: WhatsApp, Telepon, Invoice Manual  |  |
| Produksi  | Proses: Setelah pembayaran diterima, admin meneruskan detail pesanan ke divisi produksi. Kepala gudang bahan baku mengeluarkan bahan mentah ke tim produksi. Adonan diolah dan disimpan di cold storage untuk mencapai titik beku maksimal, lalu dipindahkan ke chest freezer di gudang produk jadi.  |  |
|  | Pelaku: Produksi, Kepala Gudang |  |
|  | Media/Tools: SOP Internal, Pencatatan Manual |  |
| Quality Control  | Proses: Pengiriman diperkuat dengan sistem 2-checker, satu orang menyiapkan bahan baku/produk dan satu orang lagi melakukan cross-check pesanan sebelum dikirim. |  |
|  | Pelaku: Checker Gudang |  |
|  | Media/Tools: Nota Manual, Foto |  |
| Distribusi  | Proses: Tim gudang produk jadi menginformasikan admin bahwa pesanan siap. Mitra melakukan pick-up langsung. Untuk Jabodetabek digunakan jasa ekspedisi seperti Lalamove atau Deliveree (maksimal 2 jam). Untuk luar kota/pulau digunakan vendor ekspedisi khusus dengan armada frozen untuk menjaga suhu \-20°C. |  |
|  | Pelaku: Gudang, Pengiriman, Mitra |  |
|  | Media/Tools: WhatsApp, Surat Jalan, Logistik Third Party |  |
| Penerimaan di Mitra  | Proses: Mitra melakukan pengecekan produk saat diterima. Batas waktu komplain adalah 1x24 jam. Jika tidak ada komplain, pesanan dianggap clear. |  |
|  | Pelaku: Mitra |  |
|  | Media/Tools: Nota, Foto, WhatsApp |  |
| Penjualan di Gerai  | Proses: Transaksi penjualan di gerai dicatat menggunakan Moka POS. Data transaksi dari Moka POS belum terhubung secara otomatis ke sistem pusat. |  |
|  | Pelaku: Karyawan Gerai |  |
|  | Media/Tools: Moka POS |  |
| Pencatatan Keuangan | Proses: Laporan keuangan disusun menggunakan software Accurate. Input data dilakukan secara manual berdasarkan rekap dari berbagai sumber. |  |
|  | Pelaku: Finance |  |
|  | Media/Tools: Accurate, Spreadsheet Rekap |  |
| HR & Payroll  | Proses: Data karyawan, absensi, dan perhitungan gaji dikelola secara manual atau menggunakan tools terpisah. Absensi menggunakan fingerprint. |  |
|  | Pelaku: HR  |  |
|  | Media/Tools: Spreadsheet, Fingerprint |  |

#### **3.2 Challenges and Issues** {#3.2-challenges-and-issues}

Berdasarkan kondisi operasional saat ini, Mamma Roti menghadapi sejumlah tantangan dan permasalahan yang menjadi pemicu utama kebutuhan implementasi ERP Odoo, yaitu: 

* Data Terfragmentasi & Proses Manual  
  Data bisnis tersebar di Moka POS, Accurate, WhatsApp, dan spreadsheet. Pemesanan bahan baku masih via WhatsApp manual.  
* Kontrol Inventori & FEFO Lemah  
  Tidak ada sistem alert reorder point. Manajemen expiry date bahan baku belum terstruktur. Pencatatan stok manual sering selisih.  
* Tindak Lanjut & Keputusan Lambat  
  Persetujuan lintas divisi sering tertunda karena menunggu atasan. Keputusan lapangan diambil mendadak karena tidak ada panduan tertulis.  
* Kesiapan Darurat & Risiko Infrastruktur  
  Tim ragu menjalankan langkah darurat saat cold storage rusak atau gangguan produksi. Pendekatan manajemen risiko masih reaktif.  
* Sistem Tidak Mampu Menskalakan  
  Sistem operasional yang ada dirancang untuk skala kecil. Struktur manajemen masih dengan jabatan yang dirangkap.

### **4\. Proposed Solution** {#4.-proposed-solution}

#### **4.1 Description of the Solution** {#4.1-description-of-the-solution}

Implementasi ERP Odoo di Mamma Roti bertujuan untuk mengintegrasikan seluruh data operasional Central Kitchen dan Gudang Utama ke dalam satu platform terpusat. Solusi ini akan menggantikan proses manual yang saat ini tersebar di WhatsApp, spreadsheet, Moka POS, dan Accurate, menjadi sistem yang terstruktur, terotomatisasi, dan terukur.

Odoo dipilih karena sifatnya yang open-source, modular, dan dapat dikustomisasi sesuai kebutuhan spesifik bisnis Mamma Roti. Dengan satu database terpusat, seluruh divisi  mulai dari purchasing, produksi, gudang, hingga finance dapat mengakses data real-time dalam satu sistem.

#### **4.2 Functional Requirements** {#4.2-functional-requirements}

* Inventory Management (Stok)

| Fitur  | Keterangan Implementasi |
| :---- | :---- |
| Multi-location tracking (CK & Gudang Utama) | Menggunakan fitur Multi-Warehouse standar Odoo. Dibuat 2 gudang: Central Kitchen dan Gudang Utama. |
| FEFO tracking untuk bahan baku dengan expiry date | Menggunakan fitur Lots & Serial Numbers dengan removal strategy di-set ke FEFO. |
| Reorder point alert (notifikasi stok minimum) | Menggunakan fitur Reordering Rules standar. Ketika stok di bawah minimum, Odoo otomatis membuat RFQ/PO. |
| Pencatatan stok real-time (masuk, keluar, internal transfer) | Setiap receipt, delivery, dan internal transfer tercatat otomatis di sistem. |
| Stock move history | Riwayat pergerakan stok tersedia secara otomatis untuk audit trail. |

* Purchase (Pengadaan Bahan Baku)

| Fitur  | Keterangan Implementasi |
| :---- | :---- |
| Vendor management | Master vendor, alamat, dan kontak dikelola di modul Purchase. |
| Request for Quotation (RFQ) & Purchase Order (PO) | Pemesanan ke vendor dibuat via RFQ → PO secara digital. |
| Reordering rules otomatis | Ketika stok mencapai minimum, Odoo otomatis generate RFQ berdasarkan vendor dan lead time yang telah dikonfigurasi. |
| Lead time vendor | Dikonfigurasi di level vendor/produk (2 hari) sehingga sistem dapat memperhitungkan kapan stok sampai. |
| Approval workflow PO | Menggunakan fitur Approval bawaan Purchase untuk PO di atas nilai tertentu (dapat dikonfigurasi tanpa coding). |
| Riwayat pemesanan | Semua RFQ, PO, dan status penerimaan terekam otomatis di sistem. |

* Manufacturing (Produksi)

| Fitur  | Keterangan Implementasi |
| :---- | :---- |
| Bill of Materials (BoM) per produk roti | Dibuat di modul Manufacturing untuk setiap jenis roti (Butter, Vanilla, Cheese, Choco, dll.). |
| Work Orders | Alur produksi dicatat sebagai work order dengan routing sederhana. |
| Material consumption | Penggunaan bahan baku tercatat otomatis saat work order selesai. |
| Perhitungan biaya produksi | Odoo menghitung COGS produk berdasarkan BoM dan biaya operasi yang dikonfigurasi. |

* Point of Sale (POS)

| Fitur  | Keterangan Implementasi |
| :---- | :---- |
| POS untuk transaksi di Central Kitchen | Menggunakan modul POS standar Odoo untuk transaksi langsung di lokasi CK (jika ada penjualan retail ke mitra/walk-in). |
| Konsolidasi data penjualan | Jika menggunakan Odoo POS, data penjualan otomatis masuk ke Accounting dan Inventory. |
| Pricelist dan promo | Dapat dikonfigurasi di POS untuk harga promo. |

* Accounting & Finance

| Fitur  | Keterangan Implementasi |
| :---- | :---- |
| Jurnal otomatis | Setiap transaksi di Inventory, Purchase, Sales, dan Manufacturing otomatis generate jurnal ke Accounting. |
| Chart of Accounts | Dibuat sesuai standar akuntansi Indonesia (dapat diimpor template). |
| Invoice dan Payment | Vendor bill dan customer invoice dikelola di satu sistem. |
| Laporan keuangan | P\&L, Balance Sheet, Cash Flow tersedia secara standar. |
| Multi-currency | Jika ada pembelian bahan baku impor, dapat dikonfigurasi. |

* Human Resources (HR)

| Fitur  | Keterangan Implementasi |
| :---- | :---- |
| Master data karyawan | Data karyawan CK & Gudang Utama dicatat di modul Employees. |
| Absensi (Attendance) | Karyawan check-in/check-out via Odoo (web/mobile) sebagai pengganti/pendamping fingerprint. |
| Leave management | Pengajuan cuti dan izin dikelola via modul Leave. |
| Department dan job positions | Struktur organisasi divisidibuat di Odoo untuk memudahkan tracking. |

* Sales & Distribution

| Fitur  | Keterangan Implementasi |
| :---- | :---- |
| Sales Order (SO) dari mitra | Pesanan dari mitra dicatat sebagai Sales Order di Odoo. |
| Delivery Order (DO) | Pengiriman produk ke mitra dicatat sebagai Delivery Order dengan surat jalan digital. |
| Tracking status pengiriman | Status draft → ready → delivered tercatat di sistem. |
| Invoice otomatis | Setelah pengiriman, invoice dapat digenerate otomatis ke mitra. |

* Dashboard & Reporting

| Fitur  | Keterangan Implementasi |
| :---- | :---- |
| Dashboard stok real-time | Menggunakan Odoo dashboard standar untuk melihat stok per lokasi. |
| Laporan penjualan dan pembelian | Tersedia di masing-masing modul secara native. |
| Laporan produksi | Manufacturing reports untuk melihat biaya dan efisiensi produksi. |
| Custom report sederhana | Menggunakan Odoo Studio (jika tersedia) atau filter/group by di list view untuk kebutuhan reporting dasar. |

#### **4.3 Non-Functional Requirements** {#4.3-non-functional-requirements}

| Fitur  | Keterangan Implementasi |
| :---- | :---- |
| Performance | Sistem mampu menangani operasional Central Kitchen dan Gudang Utama dengan 20–30 user concurrent. |
| Availability | Sistem berjalan pada jam operasional (08.00–17.00) dengan maintenance di luar jam kerja. |
| Security | Role-based access control (RBAC) dikonfigurasi per divisi menggunakan grup standar Odoo. |
| Scalability | Arsitektur database dirancang agar dapat dikembangkan ke gerai lain di masa depan. |
| Integration | Tidak ada integrasi API eksternal pada tahap implementasi ini. Seluruh modul berjalan secara native dalam satu database Odoo. Fungsi kasir outlet yang saat ini menggunakan Moka POS akan dimigrasi ke modul POS Odoo pada fase berikutnya. |

### **5\. Stakeholders** {#5.-stakeholders}

#### **5.1 List of Stakeholders** {#5.1-list-of-stakeholders}

| Jabatan / Peran | Organisasi | Kategori |
| :---- | :---- | :---- |
| Founder & CEO | Mamma Roti | Internal |
| Manajer Operasional | Mamma Roti | Internal |
| Kepala Produksi | Mamma Roti | Internal |
| Kepala Gudang | Mamma Roti | Internal |
| Tim Purchasing | Mamma Roti | Internal |
| Tim Finance | Mamma Roti | Internal |
| Tim HR | Mamma Roti | Internal |
| Tim Operasional | Mamma Roti | Internal |
| Dosen Pengampu | UPN "Veteran" Jakarta | Akademik |
| Ketua Tim Proyek | Kelompok 5 | Tim Proyek |
| Anggota Tim Proyek | Kelompok 5 | Tim Proyek |
| Anggota Tim Proyek | Kelompok 5 | Tim Proyek |
| Anggota Tim Proyek | Kelompok 5 | Tim Proyek |

#### **5.2 Roles and Responsibilities** {#5.2-roles-and-responsibilities}

* Stakeholder Internal (Mamma Roti)

| Stakeholder | Tanggung Jawab dalam Proyek |
| :---- | :---- |
| Founder & CEO | Menyetujui arah strategis proyek dan BRD, menyediakan akses data dan wawancara. |
| Manajer Operasional | Mengoordinasikan antar divisi, memastikan operasional tidak terganggu selama implementasi. |
| Kepala Produksi | Memberikan input kebutuhan modul Manufacturing dan workflow produksi. |
| Kepala Gudang | Memberikan input kebutuhan modul Inventory, FEFO, dan tracking stok. |
| Tim Purchasing | Menguji modul Purchase dan memberikan feedback workflow pemesanan. |
| Tim Finance | Menguji modul Accounting dan memastikan laporan keuangan sesuai kebutuhan. |
| Tim HR | Menguji modul HR dan memastikan data karyawan tercatat dengan benar. |
| Tim Operasional | Menguji modul Sales & Distribution serta alur pengiriman ke gerai. |

* Stakeholder Akademik

| Stakeholder | Tanggung Jawab dalam Proyek |
| ----- | ----- |
| Dosen Pengampu | Memberikan arahan metodologi dan meninjau kelengkapan dokumen proyek. |

* Tim Proyek (Kelompok 5\)

| Stakeholder | Tanggung Jawab dalam Proyek |
| ----- | ----- |
| Ketua Tim Proyek | Mengoordinasikan aktivitas proyek dan menjadi penghubung dengan pihak Mamma Roti. |
| Anggota Tim Proyek | Menganalisis kebutuhan, mengkonfigurasi sistem Odoo, melakukan testing, dan menyusun dokumentasi. |

### **6\. Constraints** {#6.-constraints}

#### **6.1 Budgetary Constraints** {#6.1-budgetary-constraints}

Implementasi Odoo ERP di Mamma Roti harus dijalankan dalam koridor keuangan yang ketat namun tetap realistis terhadap kondisi pertumbuhan bisnis yang sedang agresif. Saat ini Mamma Roti memanfaatkan fasilitas kredit perbankan sebagai instrumen utama untuk menjaga stabilitas arus kas (cash flow) sekaligus membiayai rencana ekspansi menuju 500 cabang. Kondisi ini secara langsung membatasi ruang alokasi anggaran untuk kebutuhan teknologi informasi.  
Kebijakan internal perusahaan mewajibkan penyisihan dana darurat sebesar 10 hingga 15 persen dari omzet bulanan. Dana ini bersifat eksklusif dan hanya boleh digunakan untuk mengatasi krisis operasional di lapangan, sehingga tidak dapat dialihkan untuk keperluan pengembangan sistem. Implikasinya adalah seluruh biaya implementasi Odoo, termasuk lisensi, infrastruktur server, dan biaya pengembangan customization, harus bersumber dari anggaran operasional reguler dan tidak boleh menyentuh modal kerja utama maupun cadangan darurat tersebut.  
Batasan anggaran ini paling terasa pada komponen customization teknis, khususnya pengembangan integrasi API antara Odoo dan Moka POS. Pengembangan custom harus dirancang seminimal mungkin dengan memanfaatkan fitur konfigurasi standar Odoo secara maksimal terlebih dahulu, dan customization baru dilakukan apabila konfigurasi standar benar-benar tidak mampu mengakomodasi kebutuhan bisnis yang ada. Pendekatan ini dikenal sebagai strategi "configuration-first, customization-last" dan menjadi prinsip utama dalam pengambilan keputusan teknis pada proyek ini.  
Untuk memastikan pengendalian biaya, setiap keputusan pengembangan tambahan di luar lingkup yang telah disepakati wajib melalui persetujuan manajemen puncak dan dievaluasi dalam forum Weekly Meeting setiap hari Senin.

#### **6.2 Timeline Constraints** {#6.2-timeline-constraints}

Proyek implementasi ini dibatasi oleh ritme operasional Central Kitchen yang sangat padat. Berdasarkan data yang diperoleh dari wawancara, tim produksi menjalankan 7 hingga 10 batch adonan setiap harinya tanpa jeda operasional yang signifikan. Kondisi ini menjadikan proses migrasi sistem (cut-over) sebagai aktivitas berisiko tinggi yang membutuhkan perencanaan sangat cermat.

Proses perpindahan dari sistem pencatatan manual berbasis Excel dan WhatsApp ke Odoo tidak boleh menyebabkan downtime yang menghentikan lini produksi, menunda pengiriman produk setengah jadi ke mitra, maupun menginterupsi alur penerimaan pesanan dari lebih dari 90 hingga 130 outlet. Oleh karena itu, strategi cut-over yang dipilih adalah pendekatan paralel terbatas (parallel run), di mana sistem lama dan sistem baru dioperasikan secara bersamaan selama periode transisi tertentu sebelum sistem lama sepenuhnya dihentikan. Target keseluruhan implementasi ditetapkan dalam rentang 12 hingga 14 minggu, dengan pembagian fase sebagai berikut:

* **Fase 1 (Minggu 1 sampai 4): Requirement Analysis dan Setup Lingkungan**   
  Pada fase ini dilakukan finalisasi Business Requirements Document, konfigurasi awal server Odoo, pembuatan akun dan struktur organisasi dalam sistem, serta pelatihan awal bagi tim inti (key users) dari divisi gudang, produksi, dan akuntansi.  
* **Fase 2 (Minggu 5 sampai 10): Konfigurasi Modul dan Pengembangan Customization**   
  Konfigurasi modul Inventory dengan aturan FEFO dan multi-warehouse, modul Manufacturing dengan Bill of Materials (BoM) dan penjadwalan MRP, modul Sales dan Accounting dilakukan secara bertahap. Secara paralel, konfigurasi modul Point of Sale Odoo dimulai dan diuji di lingkungan staging sebagai persiapan transisi dari Moka POS.   
* **Fase 3 (Minggu 11 sampai 14): User Acceptance Testing (UAT), Migrasi Data, dan Go-Live**   
  Pengujian menyeluruh oleh pengguna akhir, migrasi data historis dari Excel ke Odoo, pelatihan seluruh staf operasional, dan cut-over ke sistem baru dilakukan di akhir fase ini.  
  Progres implementasi wajib dilaporkan setiap hari Senin dalam forum Weekly Meeting bersama Top Level Management untuk memastikan setiap hambatan dapat direspons dengan cepat dan keputusan eskalasi dapat diambil tanpa penundaan.

#### **6.3 Regulatory Constraints** {#6.3-regulatory-constraints}

Mamma Roti beroperasi dalam industri pangan sehingga tunduk pada regulasi keamanan dan standar kualitas produk yang berlaku. Berbeda dengan produk pangan kemasan yang dipasarkan secara ritel, produk Mamma Roti tidak mensyaratkan izin edar dari BPOM maupun sertifikasi SNI. Namun demikian, perusahaan wajib mempertahankan dan memperbarui sertifikasi Halal dari Kementerian Agama Republik Indonesia (Kemenag) secara berkala. Kewajiban sertifikasi Halal ini memiliki implikasi langsung terhadap desain sistem Odoo, terutama pada modul Inventory dan Quality Control. Sistem harus mampu memenuhi persyaratan berikut:

1) Pertama, sistem harus dapat memisahkan alur barang masuk dan barang jadi secara tegas di dalam sistem agar tidak terjadi kontaminasi silang, baik secara fisik maupun pada level pencatatan data. Pemisahan ini mencakup jalur penerimaan bahan baku, proses produksi di Central Kitchen, hingga pengiriman produk ke mitra.  
2) Kedua, sistem harus mampu melacak asal-usul setiap batch bahan baku yang digunakan dalam produksi (lot traceability). Bahan-bahan yang rentan terhadap pelanggaran standar Halal, seperti ragi, margarine, dan bahan tambahan pangan lainnya, harus memiliki rekam jejak lengkap mulai dari nomor lot penerimaan dari supplier hingga batch produksi yang menggunakannya.  
3) Ketiga, pencatatan kebersihan fasilitas produksi dan hasil pemeriksaan QC harus terdokumentasi di dalam sistem dan dapat diakses sewaktu-waktu apabila dibutuhkan untuk keperluan audit Halal. Fitur chatter dan log aktivitas pada Odoo dapat dimanfaatkan untuk keperluan ini.

Selain regulasi Halal, sistem juga harus mengakomodasi praktik pencatatan keuangan yang sesuai dengan standar akuntansi berlaku di Indonesia mengingat perusahaan menggunakan Software Accurate untuk akuntansi pusat dan akan bermigrasi sebagian fungsinya ke modul Accounting Odoo.

### **7\. Assumptions** {#7.-assumptions}

#### **7.1 List of Assumptions** {#7.1-list-of-assumptions}

Perencanaan implementasi ERP ini dibangun di atas sejumlah asumsi dasar yang ditetapkan berdasarkan hasil wawancara dengan Pak Reza dan kondisi operasional Mamma Roti yang telah dipahami tim. Asumsi-asumsi ini perlu diverifikasi ulang sebelum implementasi dimulai dan selama implementasi berlangsung. Jika ada asumsi yang terbukti tidak valid, tim implementasi wajib melakukan penilaian ulang terhadap lingkup dan jadwal proyek.

* **A1: Kesiapan dan Kooperasi Mitra Waralaba**   
  Seluruh mitra waralaba yang tersebar di lebih dari 90 hingga 130 outlet bersedia meninggalkan pola komunikasi pemesanan tradisional yang selama ini dilakukan hanya melalui WhatsApp Group, dan beralih menggunakan mekanisme pencatatan yang terintegrasi dengan Odoo. Asumsi ini bersifat kritikal karena seluruh alur pemesanan produk dari mitra ke pusat saat ini bergantung sepenuhnya pada WhatsApp Group per outlet.  
* **A2: Kestabilan Infrastruktur Jaringan di Luar Jawa**   
  Infrastruktur internet di gerai-gerai yang berlokasi di luar Pulau Jawa, termasuk Kalimantan, Sulawesi, dan Kepulauan Bangka, dianggap cukup stabil untuk mendukung sinkronisasi data transaksi harian secara real-time atau minimal End-of-Day (EoD). Apabila asumsi ini tidak terpenuhi, mekanisme sinkronisasi offline dengan queue system perlu dipertimbangkan sebagai fallback.  
* **A3: Kesiapan Mitra untuk Bertransisi ke Odoo POS**   
  Seluruh outlet mitra dianggap memiliki kesiapan dasar untuk bertransisi secara bertahap dari Moka POS ke modul Point of Sale Odoo sesuai jadwal yang akan ditetapkan. Pada fase awal implementasi, Moka POS masih digunakan sebagai sistem kasir di outlet, namun asumsi ini menegaskan bahwa tidak ada hambatan teknis atau kontraktual dari pihak mitra yang dapat menghalangi proses migrasi ke Odoo POS di fase berikutnya.   
* **A4: Ketersediaan Data Historis** **yang Memadai**   
  Data stok, transaksi penjualan, dan data Bill of Materials yang selama ini dikelola dalam format Excel dan Accurate tersedia dalam kondisi yang cukup bersih dan terstruktur untuk dapat dimigrasikan ke Odoo. Tim implementasi mengasumsikan tidak ada kebutuhan pembersihan data (data cleansing) berskala masif yang dapat memperlambat jadwal migrasi.  
* **A5: Komitmen dan Partisipasi Key Users** **dari Setiap Divisi**   
  Personel yang ditunjuk sebagai key users dari masing-masing divisi, yaitu tim gudang, tim produksi, dan tim administrasi keuangan, memiliki kapasitas waktu dan komitmen yang cukup untuk mengikuti seluruh sesi pelatihan, proses UAT, dan fase parallel run tanpa gangguan dari beban kerja operasional harian.  
* **A6: Kewenangan Pengambilan Keputusan** **Tersedia Selama Proyek**   
  Pak Reza selaku Owner dan CEO Mamma Roti, atau delegasinya yang telah diberikan mandat penuh, tersedia dan dapat dihubungi untuk pengambilan keputusan yang memerlukan persetujuan manajemen puncak dalam tenggat waktu yang wajar sehingga tidak terjadi bottleneck keputusan yang menghambat progres implementasi.  
* **A7: Komposisi dan Jumlah Bahan Baku (BoM) Bersifat Relatif Stabil**   
  Formula atau resep produksi untuk setiap jenis roti (terdiri dari 8 bahan baku per produk) dianggap sudah final dan stabil untuk dikonfigurasi sebagai Bill of Materials di Odoo. Perubahan komposisi yang terjadi di tengah implementasi akan diperlakukan sebagai change request dan dikelola secara terpisah dari lingkup implementasi awal.

### **8\. Risks** {#8.-risks}

#### **8.1 List of Risks** {#8.1-list-of-risks}

Identifikasi risiko berikut disusun berdasarkan kerangka kerja ISO 31000, dengan mempertimbangkan konteks internal dan eksternal operasional Mamma Roti. Setiap risiko diklasifikasikan berdasarkan kategori, potensi dampak, dan probabilitas kejadiannya.

1) **R1: Risiko Kegagalan Cold Storage (Kategori: Operasional, Dampak: Sangat Tinggi, Probabilitas: Sedang)**  
   Kerusakan mesin cold storage di Central Kitchen merupakan risiko yang paling dikategorikan mengkhawatirkan oleh manajemen Mamma Roti. Gangguan pada cold storage dapat melumpuhkan kapasitas produksi harian yang mencapai 10.000 roti dan menghentikan seluruh proses distribusi ke mitra. Dalam konteks implementasi ERP, kegagalan cold storage yang terjadi bersamaan dengan periode cut-over sistem akan menciptakan krisis berlapis yang sangat sulit dikelola.  
2) **R2: Risiko Kerusakan atau Penurunan Kualitas Adonan Selama Distribusi (Kategori: Logistik, Dampak: Tinggi, Probabilitas: Sedang)**  
   Adonan yang rusak, mencair, atau melembek selama proses distribusi ke luar pulau akibat gangguan mesin pendingin pada armada logistik atau kondisi cuaca ekstrem (force majeure) dapat menyebabkan kerugian produksi sekaligus komplain mitra. Risiko ini berdampak langsung pada reputasi Mamma Roti di mata mitra waralaba.  
3) **R3: Risiko Resistensi dan Lambatnya Adaptasi Pengguna (Kategori: Sumber Daya Manusia, Dampak: Tinggi, Probabilitas: Tinggi)**  
   Berdasarkan pengakuan langsung dari Pak Reza, karyawan gerai membutuhkan waktu adaptasi lebih lama dalam mempelajari sistem digital baru. Risiko ini mencakup kemungkinan terjadinya input data yang tidak konsisten, penggunaan sistem yang tidak optimal, atau bahkan penolakan terhadap perubahan prosedur kerja. Dalam konteks implementasi ERP, rendahnya adopsi sistem oleh pengguna akhir adalah salah satu penyebab utama kegagalan proyek ERP secara global.  
4) **R4: Risiko Selisih dan Ketidakakuratan Data Stok (Kategori: Sistem dan Data, Dampak: Tinggi, Probabilitas: Tinggi)**  
   Sistem pencatatan stok 2-checker yang ada saat ini rentan terhadap keterlambatan input data. Selisih stok yang terus berulang akan merusak keandalan laporan MRP dan memicu kesalahan perencanaan produksi. Apabila data stok di Odoo tidak mencerminkan kondisi fisik gudang secara akurat, seluruh proses perencanaan otomatis di Odoo menjadi tidak dapat diandalkan.  
5) **R5: Risiko Kehilangan Jejak Informasi Kritis (Kategori: Sistem dan Data, Dampak: Sedang, Probabilitas: Tinggi)**  
   Keputusan manajerial, komplain mitra, dan informasi operasional penting yang selama ini tersimpan secara tidak terstruktur di grup WhatsApp dan file Excel berpotensi hilang atau tidak terdokumentasi ketika proses migrasi ke Odoo berlangsung. Informasi historis yang hilang akan menyulitkan proses audit dan analisis tren di kemudian hari.  
6) **R6: Risiko Reputasi Akibat Keterlambatan Penanganan Komplain Pelanggan (Kategori: Reputasi, Dampak: Tinggi, Probabilitas: Sedang)**  
   Ulasan negatif di platform digital seperti Google Review, GoFood, dan Instagram yang tidak ditangani dalam batas waktu yang wajar dapat memicu efek domino yang merusak citra merek Mamma Roti secara nasional. Dengan jaringan outlet yang tersebar di seluruh Indonesia, sebuah isu reputasi yang tidak terkelola dengan baik berpotensi memengaruhi keputusan calon mitra baru untuk bergabung.  
7) **R7: Risiko Ketergantungan Jangka Panjang pada Moka POS dan Fragmentasi Data (Kategori: Teknis dan Strategis, Dampak: Tinggi, Probabilitas: Tinggi)**   
   Saat ini seluruh transaksi penjualan di outlet mitra dicatat melalui Moka POS secara real-time, sementara data keuangan pusat dikelola terpisah di Software Accurate. Kondisi ini menciptakan fragmentasi data antara sistem kasir outlet dan sistem back-office pusat yang tidak terhubung secara langsung. Ketergantungan pada dua sistem terpisah dalam jangka panjang meningkatkan risiko inkonsistensi laporan, duplikasi kerja administrasi, serta keterbatasan visibilitas manajemen terhadap performa penjualan secara konsolidasi. Seiring rencana ekspansi menuju 500 cabang, kompleksitas pengelolaan data yang tersebar di banyak sistem akan semakin sulit dikendalikan dan berpotensi menghambat pengambilan keputusan berbasis data yang cepat dan akurat.   
8) **R8: Risiko Ketergantungan pada Supplier Tunggal untuk Bahan Baku Utama (Kategori: Rantai Pasok, Dampak: Tinggi, Probabilitas: Rendah)**  
   Ketergantungan pada Bogasari sebagai pemasok tepung utama dan sumber impor tunggal untuk cokelat dari Singapura menciptakan risiko rantai pasok yang signifikan. Gangguan pengiriman atau lonjakan harga dari supplier kunci ini dapat secara langsung menghentikan operasi produksi Central Kitchen.

#### **8.2 Risk Mitigation Strategies** {#8.2-risk-mitigation-strategies}

Strategi mitigasi berikut dirancang menggunakan pendekatan ISO 31000 yang membedakan antara perlakuan risiko berupa "mitigasi (reduce)", "transfer", "penerimaan (accept)", dan "penghindaran (avoid)". Implementasi mitigasi ini sebagian dapat diakomodasi langsung melalui konfigurasi sistem Odoo, dan sebagian lainnya bersifat prosedural atau organisasional di luar sistem.

1) **Mitigasi R1: Cold Storage Bermasalah**   
   Perlakuan risiko: Mitigasi dan Contingency Planning. Mamma Roti telah memiliki Business Continuity Plan (BCP) berupa pemindahan darurat adonan ke chest freezer cadangan jika cold storage utama mengalami gangguan. Dalam sistem Odoo, mitigasi ini didukung dengan konfigurasi multi-warehouse yang memungkinkan pencatatan perpindahan lokasi stok secara cepat tanpa kehilangan traceability. Selain itu, notifikasi otomatis pada Odoo dapat dikonfigurasi untuk memantau suhu penyimpanan apabila perangkat sensor terintegrasi di masa mendatang.   
     
2) **Mitigasi R2: Kerusakan Adonan Selama Distribusi**   
   Perlakuan risiko: Transfer dan Mitigasi. Regulasi komplain ditetapkan dengan batas waktu maksimal 1 kali 24 jam bagi mitra untuk melaporkan adonan rusak disertai bukti foto. Jika terjadi force majeure logistik laut, manajemen mengambil langkah darurat pengiriman melalui jalur udara untuk mempertahankan ketersediaan stok di gerai. Di dalam Odoo, modul Inventory dikonfigurasi untuk mencatat status pengiriman dan dokumentasi klaim kerusakan pada setiap transfer order, sehingga seluruh riwayat komplain logistik tersimpan dalam sistem dan dapat dianalisis untuk evaluasi vendor ekspedisi.   
     
3) **Mitigasi R3: Resistensi dan Lambatnya Adaptasi Pengguna**  
   Perlakuan risiko: Mitigasi. Strategi utama adalah pelatihan bertahap berbasis peran (role-based training) dengan materi yang disesuaikan dengan kebutuhan setiap divisi. Panduan visual singkat (SOP mini) per skenario operasional utama akan dibuat dalam format yang mudah dipahami oleh staf lapangan. Periode parallel run direncanakan minimal dua minggu untuk memberikan waktu adaptasi yang memadai sebelum sistem lama sepenuhnya dihentikan. Key users yang terlatih akan berperan sebagai "champion" di masing-masing divisi untuk mendampingi rekan kerja mereka selama periode transisi.   
     
4) **Mitigasi R4: Selisih dan Ketidakakuratan Data Stok**   
   Perlakuan risiko: Mitigasi. Modul Inventory Odoo dikonfigurasi dengan automated stock alert yang memicu notifikasi kepada kepala gudang apabila stok aktual mendekati batas buffer stock yang telah ditetapkan. Prosedur cut-off harian diwajibkan bagi tim gudang untuk memastikan seluruh pergerakan stok tercatat di Odoo sebelum pukul tertentu setiap harinya. Fungsi stock adjustment dan physical inventory count di Odoo dijadwalkan secara berkala (mingguan) untuk mendeteksi selisih secara dini sebelum akumulasi menjadi masalah yang lebih besar.   
     
5) **Mitigasi R5: Kehilangan Jejak Informasi Kritis**   
   Perlakuan risiko: Mitigasi. Seluruh komunikasi komplain pelanggan dari platform Instagram, GoFood, dan WhatsApp diwajibkan untuk dicatat oleh admin ke dalam modul Helpdesk Odoo setiap harinya, dengan status yang terklasifikasi sebagai Open, In Progress, atau Closed. Fitur chatter (log komunikasi internal) pada setiap dokumen di Odoo digunakan secara aktif untuk mendokumentasikan keputusan manajerial yang relevan. Sebelum go-live, dilakukan proses migrasi data historis dari Excel ke Odoo secara selektif untuk data-data yang dinilai krusial bagi operasional dan kepatuhan.   
     
6) **Mitigasi R6: Keterlambatan Penanganan Komplain Pelanggan**   
   Perlakuan risiko: Mitigasi. Service Level Agreement (SLA) internal ditetapkan di dalam konfigurasi Helpdesk Odoo dengan target penyelesaian tiket per kategori komplain. Sistem secara otomatis akan memberikan peringatan (escalation alert) kepada supervisor apabila tiket melewati batas SLA yang telah ditetapkan tanpa respons yang memadai.   
     
7) **Mitigasi R7: Transisi Penuh ke Ekosistem Odoo sebagai Sistem Terpadu** Perlakuan risiko: Mitigasi jangka panjang melalui konsolidasi sistem. Solusi yang direncanakan adalah migrasi fungsi Point of Sale dari Moka POS ke modul POS bawaan Odoo secara bertahap. Odoo telah menyediakan modul Point of Sale yang terintegrasi secara native dengan modul Inventory, Sales, dan Accounting dalam satu ekosistem, sehingga setiap transaksi yang terjadi di outlet secara otomatis memperbarui stok, menciptakan entri jurnal, dan menghasilkan laporan penjualan tanpa memerlukan proses rekonsiliasi manual antarsistem.  
   Pada tahap awal implementasi ini, Moka POS masih digunakan di outlet mitra mengingat kebutuhan adaptasi yang bertahap dan pertimbangan kesiapan operasional di lapangan. Namun rencana jangka menengah menetapkan transisi ke Odoo POS sebagai target yang harus dicapai seiring perluasan jaringan outlet. Dengan seluruh operasional berjalan di atas satu platform Odoo, manajemen Mamma Roti akan memiliki visibilitas penuh terhadap data penjualan, stok, dan keuangan dari seluruh outlet dalam satu dashboard terpadu, tanpa celah data yang selama ini muncul akibat fragmentasi sistem.  
     
8) **Mitigasi R8: Ketergantungan pada Supplier Tunggal**   
   Perlakuan risiko: Mitigasi. Manajemen diarahkan untuk mulai melakukan identifikasi dan kualifikasi supplier alternatif untuk bahan baku kritikal sebagai bagian dari strategi diversifikasi rantai pasok jangka menengah. Di dalam Odoo, setiap produk bahan baku dapat dikonfigurasi dengan multiple vendors beserta prioritasnya, sehingga apabila supplier utama tidak dapat memenuhi pesanan, sistem secara otomatis dapat merekomendasikan alternatif yang telah dikualifikasi. 

### **9\. Dependencies** {#9.-dependencies}

#### **9.1 List of Dependencies** {#9.1-list-of-dependencies}

Keberhasilan implementasi ERP Mamma Roti memiliki ketergantungan yang signifikan terhadap pihak-pihak eksternal maupun internal berikut. Ketergantungan ini perlu dipantau secara aktif selama seluruh durasi proyek karena gangguan pada satu titik dependensi dapat berdampak langsung pada jadwal dan kualitas implementasi.

1) **D1: Moka POS sebagai Sistem Sementara dan Rencana Transisi ke Odoo POS (Dependensi Teknis, Kritis)**  
   Saat ini seluruh transaksi penjualan di outlet mitra diproses melalui Moka POS yang dikelola secara mandiri oleh masing-masing mitra. Pada fase implementasi awal ini, Moka POS masih akan tetap beroperasi mengingat proses transisi membutuhkan kesiapan teknis dan adaptasi operasional yang tidak dapat dilakukan sekaligus. Oleh karena itu, dependensi terhadap Moka POS bersifat sementara dan terbatas pada periode awal sebelum ekosistem Odoo sepenuhnya siap menggantikannya.  
   Rencana jangka menengah menetapkan migrasi fungsi kasir outlet ke modul Point of Sale Odoo sebagai target yang akan dieksekusi secara bertahap seiring kesiapan mitra dan infrastruktur. Dengan beralih sepenuhnya ke Odoo POS, seluruh transaksi penjualan akan langsung terintegrasi dengan modul Inventory, Sales, dan Accounting di Odoo tanpa memerlukan sistem pihak ketiga. Dependensi terhadap Moka POS akan berakhir seiring selesainya proses migrasi tersebut, dan pada titik itu Mamma Roti akan beroperasi di atas satu platform terpadu yang menghilangkan fragmentasi data antara outlet dan pusat.  
     
2) **D2: Supplier Bahan Baku Utama (Dependensi Rantai Pasok, Tinggi)** Kelancaran operasional harian dan keandalan data stok di Odoo bergantung pada konsistensi pengiriman dari Bogasari (tepung), pemasok margarine dan ragi domestik, serta importir cokelat dari Singapura. Gangguan pada rantai pasok bahan baku akan secara langsung mempengaruhi validitas perencanaan produksi (MRP) yang dihasilkan oleh Odoo, karena sistem merencanakan kebutuhan berdasarkan stok yang tersedia dan terjadwal masuk.   
     
3) **D3: Vendor Ekspedisi Logistik Pendingin (Dependensi Operasional, Tinggi)** Proses distribusi produk ke seluruh mitra sepenuhnya bergantung pada kapasitas dan keandalan Lalamove dan Deliveree untuk area Jabodetabek, serta vendor logistik pendingin frozen untuk pengiriman lintas pulau pada suhu minus 20 derajat Celsius. Keterlambatan atau kegagalan layanan dari vendor ini tidak hanya berdampak pada operasional, tetapi juga pada akurasi data pengiriman yang dicatat di modul Inventory Odoo.   
     
4) **D4: Konsultan Bisnis Eksternal (Dependensi Strategis, Sedang)** Mamma Roti saat ini sangat bergantung pada arahan konsultan bisnis eksternal yang melakukan evaluasi performa perusahaan secara bulanan, mencakup KPI, Profit and Loss, serta pencapaian target kuartal. Implementasi Odoo harus mampu menghasilkan laporan dan data yang kompatibel dengan kerangka evaluasi yang digunakan oleh konsultan tersebut. Tim implementasi perlu mengklarifikasi format laporan yang dibutuhkan konsultan agar konfigurasi modul Accounting dan dashboard Odoo dapat disesuaikan sejak awal.   
     
5) **D5: Software Accurate (Dependensi Sistem Existing, Sedang)** Saat ini Mamma Roti menggunakan Software Accurate sebagai sistem akuntansi di kantor pusat. Selama periode transisi, kedua sistem ini kemungkinan akan beroperasi secara paralel, sehingga perlu dipastikan tidak terjadi duplikasi pencatatan atau inkonsistensi data keuangan. Tim implementasi harus mendefinisikan secara jelas titik batas (boundary) antara fungsi yang akan dimigrasi ke Odoo dan fungsi yang untuk sementara atau permanen tetap dijalankan di Accurate.   
     
6) **D6: Infrastruktur Internet dan Perangkat di Outlet Mitra (Dependensi Infrastruktur, Sedang)** Kemampuan sistem Odoo untuk memberikan visibilitas data real-time dari seluruh outlet bergantung pada kualitas koneksi internet yang tersedia di masing-masing gerai mitra, terutama di wilayah luar Pulau Jawa. Outlet yang berada di lokasi dengan koneksi tidak stabil memerlukan mekanisme sinkronisasi alternatif yang harus dirancang sejak fase desain teknis. 

### **10\. Approval** {#10.-approval}

#### **10.1 Sign-off** {#10.1-sign-off}

Dokumen Business Requirements Document (BRD) ini disusun oleh Tim Implementator sebagai bagian dari tugas mata kuliah Sistem ERP di Universitas Pembangunan Nasional Veteran Jakarta. Seluruh data, informasi operasional, dan kebutuhan bisnis yang tertuang dalam dokumen ini diperoleh melalui wawancara langsung dengan pihak manajemen Mamma Roti serta kajian terhadap dokumen operasional internal perusahaan.

* Pihak Manajemen (Narasumber)  
  Nama: Reza Dwinanto  
  Jabatan: Owner and CEO Mamma Roti Indonesia  
* Dosen Pengampu  
  Nama: I Wayan Widi Pradnyana, [M.TI](http://M.TI)  
  Jabatan: Dosen Sistem ERP, Universitas Pembangunan Nasional Veteran Jakarta  
* Tim Penyusun (Mahasiswa UPNVJ)  
  Nama Tim: Pankrasius Aryo Wicaksono, Erlis Krisda Yanti Halawa, Nadya Rouli Br Sibuea, Gerson Sebastian  
  Program Studi: Sistem Informasi, UPNVJ
