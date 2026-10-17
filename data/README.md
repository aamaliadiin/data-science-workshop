# Data Dictionary — `sales_raw.csv`
Transaksi penjualan layanan internet & perangkat (fiktif) periode **1 Jan – 31 Mar 2026**. 304 baris mentah, 300 transaksi unik.

| Kolom | Tipe (setelah bersih) | Contoh | Keterangan |
|---|---|---|---|
| transaction_id | teks | TRX00001 | ID unik transaksi |
| transaction_date | tanggal | 2026-03-02 | Tanggal transaksi |
| customer_id | teks | C017 | ID pelanggan (relasi ke `customers`) |
| city | teks | Malang | Kota pelanggan |
| product_id | teks | P02 | ID produk |
| product_name | teks | Paket Internet 50 Mbps | Nama produk |
| category | teks | Internet / Perangkat / Layanan | Kategori produk |
| quantity | bilangan bulat | 1 | Jumlah unit |
| unit_price | angka | 400000 | Harga satuan (Rupiah) |

## Masalah kualitas data yang sengaja disisipkan (untuk Exercise 2)
| # | Masalah | Contoh | Penanganan yang diajarkan |
|---|---|---|---|
| 1 | Baris duplikat persis | 4 baris | `drop_duplicates()` |
| 2 | Format tanggal campuran | `2026-03-02` dan `02/03/2026` | parsing dua format lalu digabung |
| 3 | Nama kota tidak konsisten | `malang`, ` Malang`, `MALANG` | `str.strip().str.title()` |
| 4 | `quantity` kosong | `""` | diisi 1 (asumsi minimal pembelian 1 unit) |
| 5 | `unit_price` negatif | `-400000` | diambil nilai absolut (kesalahan input tanda) |

Hasil yang diharapkan: **300 baris**, 5 kota, kolom tambahan `total_amount = quantity × unit_price`.

---

# Data Dictionary — Dataset Mini Project

## `sales_q2_raw.csv` — transaksi 1 Apr – 30 Jun 2026
Struktur kolom sama dengan `sales_raw.csv` (lihat bagian atas dokumen ini), dengan masalah kualitas data yang sama. 264 baris mentah → **260 transaksi unik**. ID transaksi berawalan `TRQ`.

## `customers_raw.csv` — master pelanggan
| Kolom | Contoh | Masalah yang perlu dibersihkan |
|---|---|---|
| customer_id | C001 | 4 ID muncul dua kali (duplikat dengan penulisan nama berbeda) |
| customer_name | PT Maju Jaya | spasi berlebih, huruf kapital/kecil tidak konsisten |
| segment | Retail / SME / Corporate | variasi penulisan: `retail`, `Retail `, `sme`, `CORPORATE` |
| join_date | 2025-06-14 | sebagian kosong |

Hasil yang diharapkan: **60 pelanggan unik**, segmen hanya `Retail`, `SME`, `Corporate`; tabel gabungan 260 baris.

## Sumber via API
`api/static/sales_q2_page_{page}.json` dan `api/static/customers.json` (lihat `api/README.md`).
