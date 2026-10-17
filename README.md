# Workshop: Membangun Data Pipeline Sederhana — dari API ke Dashboard

Peserta membangun pipeline **Extract (API) → Transform (pandas) → Load (PostgreSQL) → SQL → Dashboard** menggunakan **VS Code**, Python, dan Git — alat yang sama dengan yang dipakai di dunia kerja.

Pemateri: **Aisah** (Data Engineer & Analyst)

> ⏰ **Workshop: Sabtu, 17 Oktober 2026.** Semua instalasi & setup harus selesai sebelumnya — pada hari workshop tidak ada sesi instalasi.
>
> | Waktu | Kegiatan |
> |---|---|
> | Kamis, 15 Okt, 21.00 WIB | Kirim laporan cek kesiapan pertama (apa pun statusnya) |
> | Jumat, 16 Okt (H-1) | Konsultasi online bagi yang belum SIAP |
> | Jumat, 16 Okt, 21.00 WIB | **Batas akhir** laporan berstatus SIAP |

---

## ✅ Daftar persiapan

| # | Yang disiapkan | Status | Link |
|---|---|---|---|
| 1 | Akun **GitHub** | Wajib | https://github.com/signup |
| 2 | **Python 3.11** (Windows: centang *Add python.exe to PATH*) | Wajib | https://www.python.org/downloads |
| 3 | **Git** | Wajib | https://git-scm.com/downloads |
| 4 | **VS Code** | Wajib | https://code.visualstudio.com |
| 5 | Extension VS Code **Python** & **Jupyter** (Microsoft) | Wajib | otomatis disarankan saat repo dibuka |
| 6 | Extension **SQLTools + PostgreSQL driver**, **Rainbow CSV** | Disarankan | otomatis disarankan saat repo dibuka |
| 7 | Akun **Google** (untuk Looker Studio di Exercise 5) | Disarankan | https://accounts.google.com/signup |
| 8 | **Kartu akses database** | Dari panitia | dikirim personal |

Panduan lengkap bergambar: [`docs/Panduan_Instalasi_Setup.docx`](docs/Panduan_Instalasi_Setup.docx)

## 🛠️ Langkah setup

**1. Atur identitas Git** (sekali saja, di terminal):
```bash
git config --global user.name "Nama Lengkap"
git config --global user.email "email-github@anda.com"
```

**2. Fork repo ini** — klik **Fork → Create fork** di kanan atas halaman ini.

**3. Clone fork Anda & buka di VS Code:**
```bash
git clone https://github.com/<username-anda>/data-science-workshop.git
cd data-science-workshop
code .
```
Saat VS Code menawarkan *"install recommended extensions"*, klik **Install**.

**4. Buat virtual environment & pasang library** (di terminal VS Code: menu **Terminal → New Terminal**):

| Windows (PowerShell) | macOS / Linux |
|---|---|
| `python -m venv .venv` | `python3 -m venv .venv` |
| `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| `pip install -r requirements.txt` | `pip install -r requirements.txt` |

> Windows: jika muncul error *running scripts is disabled*, jalankan sekali `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, lalu ulangi aktivasi.

**5. Isi data login database** — salin `.env.example` menjadi `.env`, lalu ganti seluruh isinya dengan 5 baris dari kartu akses yang dikirim panitia. File `.env` tidak akan ikut ter-commit.

**6. Jalankan cek kesiapan** — buka `notebooks/00_Cek_Kesiapan.ipynb` → pilih kernel **.venv** (pojok kanan atas) → **Run All**. Semua item harus ✅.

**7. Kirim bukti kesiapan** — panel **Source Control** → stage `submissions/cek_kesiapan.md` → Commit → **Sync Changes**. Pemateri memeriksa laporan ini langsung dari fork Anda.

### Instalasi gagal? Gunakan GitHub Codespaces
VS Code yang sama, berjalan di browser, tanpa instalasi: di halaman **fork Anda** klik **Code → Codespaces → Create codespace on main**. Library dan extension terpasang otomatis; cukup isi `.env`, lalu lanjut ke langkah 6.

---

## 📒 Notebook
| `00_Cek_Kesiapan.ipynb` | Cek kesiapan — **SIAP paling lambat Jumat, 16 Okt 2026, 21.00 WIB** |
| `00_Step_by_Step_Notebook.ipynb` | Diikuti bersama pemateri |
| `01_Exercise_1_Extract.ipynb` | Exercise 1 — Extract |
| `02_Exercise_2_Transform.ipynb` | Exercise 2 — Transform |
| `03_Exercise_3_Load.ipynb` | Exercise 3 — Load |
| `04_Exercise_4_SQL.ipynb` | Exercise 4 — SQL |
| `05_Exercise_5_Dashboard.ipynb` | Exercise 5 — Dashboard |
| `06_Mini_Project.ipynb` | Mini project |

## 📁 Isi repositori
```
data/          dataset mentah (CSV) + data dictionary
api/           API statis (JSON) + mock API FastAPI opsional
notebooks/     cek kesiapan, step-by-step, exercise 1–5, mini project
scripts/       cek_kesiapan.py
sql/           latihan SQL (8 soal)
dashboard/     template dashboard: preview HTML, Streamlit, panduan Looker Studio
docs/          slide, panduan peserta, panduan instalasi
submissions/   laporan cek kesiapan & mini project
.vscode/       rekomendasi extension & pengaturan workspace
.devcontainer/ konfigurasi GitHub Codespaces
```

## 🔄 Mendapatkan materi terbaru
Di halaman fork GitHub: **Sync fork → Update branch**, lalu di VS Code: **Source Control → … → Pull** (atau `git pull`).

## ⚠️ Keamanan
Password hanya disimpan di `.env` (diabaikan Git). Jangan menulis password di notebook atau file lain yang di-commit.

Data dalam repositori ini fiktif dan bebas digunakan untuk belajar.
