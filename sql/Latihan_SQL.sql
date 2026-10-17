-- =====================================================================
-- LATIHAN SQL — Workshop Data Pipeline Sederhana
-- Tabel  : <schema_anda>.sales_clean  (atau ref.sales_clean jika Load belum berhasil)
-- Kolom  : transaction_id, transaction_date, customer_id, city, product_id,
--          product_name, category, quantity, unit_price, total_amount
-- Cara   : tulis query di bawah setiap soal, jalankan di DBeaver/pgAdmin/notebook.
--          Cocokkan hasil Anda dengan 'Petunjuk hasil'.
-- =====================================================================

-- Soal 1. 10 transaksi terbaru (urutkan dari tanggal paling baru).
-- Petunjuk hasil: 10 baris; transaksi paling atas bertanggal 2026-03-31



-- Soal 2. Total revenue per bulan.
-- Petunjuk hasil: 3 baris; Januari Rp 35.850.000



-- Soal 3. Ranking kota berdasarkan total revenue (tertinggi di atas).
-- Petunjuk hasil: Surabaya teratas, Rp 58.850.000



-- Soal 4. Produk terlaris berdasarkan total quantity.
-- Petunjuk hasil: Paket Internet 50 Mbps, 98 unit



-- Soal 5. Revenue per kategori beserta persentase kontribusinya (2 desimal).
-- Petunjuk hasil: Internet ±60,71%



-- Soal 6. Top 5 pelanggan berdasarkan total belanja.
-- Petunjuk hasil: C013 teratas, Rp 6.250.000



-- Soal 7. Jumlah transaksi dan rata-rata nilai transaksi per kota, hanya kota dengan > 30 transaksi.
-- Petunjuk hasil: 4 kota (Pasuruan tidak termasuk)



-- Soal 8. (Bonus) Pertumbuhan revenue month-over-month (%) menggunakan window function LAG().
-- Petunjuk hasil: Februari tumbuh ±44,49%



-- Ringkasan konsep: SELECT, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT, fungsi agregat,
-- DATE_TRUNC, CTE (WITH), window function (OVER, LAG).
