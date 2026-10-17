# Dashboard Template
Tiga pilihan, dari yang paling mudah:

| Opsi | File | Cocok untuk |
|---|---|---|
| Preview statis | `Dashboard_Template_Preview.html` | Melihat contoh hasil akhir (buka di browser) |
| Looker Studio | panduan di bawah | Peserta — tanpa coding |
| Streamlit | `dashboard_app.py` | Peserta yang ingin dashboard berbasis Python |
| Plotly di notebook | `notebooks/05_Exercise_5_Dashboard.ipynb` | Latihan di notebook |

## Opsi A — Streamlit
Kredensial otomatis dibaca dari file `.env` di root repo.
```bash
streamlit run dashboard/dashboard_app.py     # dari root repo, dengan .venv aktif
```
Fitur: filter tanggal/kota/kategori, 4 KPI, tren harian + rata-rata 7 hari, revenue per kota, komposisi kategori, tabel top produk, unduh CSV.

## Opsi B — Looker Studio (tanpa coding, direkomendasikan untuk peserta)
1. Buka https://lookerstudio.google.com → **Create → Report**.
2. Pilih konektor **PostgreSQL** → isi Host, Port `5432`, Database `workshop`, Username & Password dari kartu akses → **Authenticate**.
3. Pilih tabel `sales_clean` dari schema Anda → **Add to report**.
4. Susun komponen sesuai tata letak di bawah. Pengaturan tiap komponen:

| Komponen | Jenis chart | Dimension | Metric |
|---|---|---|---|
| Total Revenue | Scorecard | – | `total_amount` (SUM) |
| Transaksi | Scorecard | – | `Record Count` |
| Pelanggan | Scorecard | – | `customer_id` (COUNT DISTINCT) |
| Rata-rata/Transaksi | Scorecard | – | `total_amount` (AVG) |
| Revenue Harian | Time series | `transaction_date` | `total_amount` (SUM) |
| Revenue per Kota | Bar chart (horizontal) | `city` | `total_amount` (SUM) |
| Komposisi Kategori | Donut chart | `category` | `total_amount` (SUM) |
| Top Produk | Table | `product_name`, `category` | `quantity` (SUM), `total_amount` (SUM) |
| Filter | Date range control, Drop-down list (`city`, `category`) | | |

5. Atur **Theme** → warna utama `#0F766E`, aksen `#F59E0B`. Set format angka `total_amount` ke Currency (IDR).
6. **Share → Manage access → Anyone with the link can view** → bagikan link.

### Tata letak
```
┌────────────┬────────────┬────────────┬────────────┐
│ Revenue    │ Transaksi  │ Pelanggan  │ Rata-rata  │   ← KPI
├────────────┴────────────┴────────────┴────────────┤
│              Revenue Harian (time series)         │   ← Tren
├─────────────────────────┬─────────────────────────┤
│   Revenue per Kota      │  Komposisi Kategori     │   ← Rincian
├─────────────────────────┴─────────────────────────┤
│                 Tabel Top Produk                  │
└───────────────────────────────────────────────────┘
       Filter: [Rentang Tanggal] [Kota] [Kategori]
```
