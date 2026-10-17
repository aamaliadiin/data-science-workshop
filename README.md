# Workshop: Membangun Data Pipeline Sederhana — dari API ke Dashboard

> 📦 **Repositori ini masih berisi kit persiapan.** Materi workshop (dataset, notebook latihan, SQL, dashboard, slide) akan ditambahkan pada **Sabtu, 17 Oktober 2026 pagi**. Silakan fork sekarang dan selesaikan setup — di awal sesi Anda cukup melakukan **Sync fork** lalu `git pull`.

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

## 📁 Isi repositori saat ini
```
notebooks/00_Cek_Kesiapan.ipynb   pengecekan kesiapan (wajib dijalankan)
scripts/cek_kesiapan.py           script pengecekan
docs/                             Panduan Instalasi & Setup
submissions/                      tempat laporan cek kesiapan
.vscode/  .devcontainer/          pengaturan VS Code & GitHub Codespaces
requirements.txt  .env.example
```

## 🔄 Hari Sabtu: mengambil materi
1. Buka halaman **fork Anda** di GitHub → klik **Sync fork → Update branch**.
2. Di VS Code: **Source Control → … → Pull** (atau ketik `git pull` di terminal).

Tidak perlu memasang ulang library.

## ⚠️ Keamanan
Password hanya disimpan di `.env` (diabaikan Git). Jangan menulis password di notebook atau file lain yang di-commit.
