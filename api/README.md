# API Data Penjualan

Workshop memakai **API statis** yang langsung di-host oleh GitHub — tidak perlu server.

## API statis (default)
| File | Isi |
|---|---|
| `static/sales_page_1.json` … `sales_page_4.json` | Transaksi Q1 2026 (304 baris, 100 per halaman) |
| `static/sales_q2_page_1.json` … `sales_q2_page_3.json` | Transaksi Q2 2026 — mini project |
| `static/customers.json` | Master pelanggan — mini project |

URL yang dipakai notebook:
```
https://raw.githubusercontent.com/AisahAlfiyatusR/data-science-workshop/main/api/static/sales_page_{page}.json
```
Struktur respons:
```json
{"page": 1, "page_size": 100, "total": 304, "has_next": true, "data": [{"transaction_id": "TRX00001", "...": "..."}]}
```
Semua nilai dikirim sebagai **string** — konversi tipe data adalah bagian latihan Transform.

## API server (opsional)
Untuk mencoba API "sungguhan" dengan parameter `?page=&page_size=`:
```bash
cd api
pip install -r requirements.txt
uvicorn mock_api:app --port 8000          # dokumentasi: http://localhost:8000/docs
```
Lalu di notebook: `API_URL = "http://localhost:8000/sales"`. Endpoint lain: `/sales-q2`, `/customers`, `/health`.
