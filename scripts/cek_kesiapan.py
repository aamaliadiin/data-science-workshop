"""
Cek kesiapan workshop — memastikan semua instalasi & konfigurasi selesai SEBELUM hari H.

Jalankan dari root repo:   python scripts/cek_kesiapan.py
atau lewat notebook:       notebooks/00_Cek_Kesiapan.ipynb  (wajib, sekaligus menguji kernel Jupyter)

Hasil disimpan ke submissions/cek_kesiapan.md (tanpa password) untuk di-commit & push ke fork Anda.
"""
import datetime
import importlib
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "submissions" / "cek_kesiapan.md"
UPSTREAM_USER = "AisahAlfiyatusR"
IN_NOTEBOOK = "ipykernel" in sys.modules   # dicek sebelum library lain di-import
LIBS = ["pandas", "requests", "sqlalchemy", "psycopg2", "plotly", "streamlit", "dotenv", "ipykernel", "nbformat"]

results = []   # (nama, ok, keterangan)


def check(name):
    def deco(fn):
        def run():
            try:
                ok, info = fn()
            except Exception as e:  # cek tidak boleh menghentikan cek lain
                msg = str(e).split("\n")[0][:160]
                hint = ""
                if "password authentication failed" in msg: hint = " → periksa DB_USER/DB_PASSWORD di .env"
                elif "could not translate host" in msg or "timeout" in msg.lower() or "Connection refused" in msg: hint = " → periksa DB_HOST / koneksi internet"
                elif "404" in msg: hint = " → periksa alamat repo/API"
                ok, info = False, f"{type(e).__name__}: {msg}{hint}"
            results.append((name, ok, info))
            print(f"{'✅' if ok else '❌'} {name:<26} {info}")
            return ok
        return run
    return deco


def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=15)


@check("Python 3.10+")
def c_python():
    v = sys.version_info
    return v >= (3, 10), f"{v.major}.{v.minor}.{v.micro}"


@check("Virtual environment")
def c_venv():
    in_venv = sys.prefix != sys.base_prefix or bool(os.getenv("CODESPACES"))
    where = "Codespaces" if os.getenv("CODESPACES") else sys.prefix
    return in_venv, where if in_venv else "belum aktif — pilih interpreter/kernel .venv"


@check("Library Python")
def c_libs():
    missing = []
    for lib in LIBS:
        try:
            importlib.import_module(lib)
        except ImportError:
            missing.append(lib)
    return not missing, "lengkap" if not missing else "kurang: " + ", ".join(missing) + " → pip install -r requirements.txt"


@check("Kernel Jupyter")
def c_kernel():
    if IN_NOTEBOOK:
        return True, "notebook berjalan di kernel " + Path(sys.executable).parent.parent.name
    return True, "dijalankan dari terminal — jalankan juga notebooks/00_Cek_Kesiapan.ipynb"


@check("Git")
def c_git():
    v = _git("--version")
    if v.returncode:
        return False, "git tidak ditemukan"
    name = _git("config", "user.name").stdout.strip()
    email = _git("config", "user.email").stdout.strip()
    if not (name and email):
        return False, "isi git config --global user.name / user.email"
    return True, f"{v.stdout.strip()} ({name})"


@check("Repo fork")
def c_fork():
    url = _git("remote", "get-url", "origin").stdout.strip()
    if not url:
        return bool(os.getenv("CODESPACES")), url or "remote origin tidak ditemukan — clone dari fork Anda"
    owner = url.rstrip("/").replace(".git", "").replace(":", "/").split("/")[-2]
    if owner.lower() == UPSTREAM_USER.lower():
        return False, f"ini repo pemateri ({owner}) — clone dari FORK Anda"
    return True, f"github.com/{owner}"


@check("File .env")
def c_env():
    from dotenv import dotenv_values
    p = ROOT / ".env"
    if not p.exists():
        return False, "belum ada — salin .env.example menjadi .env"
    v = dotenv_values(p)
    empty = [k for k in ("DB_HOST", "DB_USER", "DB_PASSWORD") if not v.get(k) or v.get(k, "").startswith("isi")]
    for k, val in v.items():
        if val is not None:
            os.environ.setdefault(k, val)
    return not empty, "terisi" if not empty else "belum diisi: " + ", ".join(empty)


@check("Akses GitHub/data")
def c_api():
    import requests
    raw = os.getenv("WORKSHOP_RAW_BASE") or f"https://raw.githubusercontent.com/{UPSTREAM_USER}/data-science-workshop/main"
    api = os.getenv("API_URL")
    if api:                                   # pemateri memberi alamat API server
        url = api.format(page=1) if "{page}" in api else f"{api}?page=1&page_size=5"
        r = requests.get(url, timeout=20); r.raise_for_status()
        return True, f"API server OK ({r.json()['total']} baris)"
    r = requests.get(f"{raw}/README.md", timeout=20)
    r.raise_for_status()
    if (ROOT / "data" / "sales_raw.csv").exists():   # tahap 2: materi sudah tersedia
        r2 = requests.get(f"{raw}/api/static/sales_page_1.json", timeout=20); r2.raise_for_status()
        return r2.json()["total"] == 304, f"repo pemateri & data API dapat diakses ({r2.json()['total']} baris)"
    return True, "repo pemateri dapat diakses (materi lengkap tersedia Sabtu)"


@check("Database")
def c_db():
    if not (os.getenv("DB_HOST") and os.getenv("DB_USER") and os.getenv("DB_PASSWORD")):
        return False, "dilewati — isi .env terlebih dahulu"
    from sqlalchemy import create_engine, text
    from sqlalchemy.engine import URL
    from sqlalchemy.pool import NullPool
    user = os.getenv("DB_USER")
    eng = create_engine(URL.create("postgresql+psycopg2", username=user, password=os.getenv("DB_PASSWORD"),
                                   host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT", 5432)),
                                   database=os.getenv("DB_NAME", "workshop")), connect_args={"connect_timeout": 10},
                        poolclass=NullPool)
    with eng.begin() as conn:
        n = conn.execute(text("SELECT COUNT(*) FROM ref.sales_clean")).scalar()
        conn.execute(text(f"CREATE TABLE IF NOT EXISTS {user}._cek_kesiapan (x int)"))
        conn.execute(text(f"DROP TABLE {user}._cek_kesiapan"))
    eng.dispose()
    return n == 300, f"login {user} OK, ref.sales_clean {n} baris, schema pribadi bisa ditulisi"


def write_report(all_ok):
    REPORT.parent.mkdir(exist_ok=True)
    rows = "\n".join(f"| {n} | {'✅' if ok else '❌'} | {i} |" for n, ok, i in results)
    REPORT.write_text(f"""# Hasil Cek Kesiapan Workshop

- STATUS: {'SIAP' if all_ok else 'BELUM SIAP'}
- Akun database: {os.getenv('DB_USER') or '-'}
- Waktu: {datetime.datetime.now():%Y-%m-%d %H:%M}
- Sistem: {platform.system()} {platform.release()} · Python {platform.python_version()}
- Dijalankan dari: {'notebook' if IN_NOTEBOOK else 'terminal'}

| Cek | Hasil | Keterangan |
|---|---|---|
{rows}
""", encoding="utf-8")


def main():
    results.clear()
    print("=" * 70 + "\nCEK KESIAPAN WORKSHOP\n" + "=" * 70)
    for fn in (c_python, c_venv, c_libs, c_kernel, c_git, c_fork, c_env, c_api, c_db):
        fn()
    all_ok = all(ok for _, ok, _ in results)
    write_report(all_ok)
    print("=" * 70)
    if all_ok:
        print("🎉 STATUS: SIAP. Commit & push file submissions/cek_kesiapan.md ke fork Anda.")
    else:
        print("⛔ STATUS: BELUM SIAP. Perbaiki item ❌ lalu jalankan ulang (lihat docs/Panduan_Instalasi_Setup.docx).")
    print(f"Laporan: {REPORT.relative_to(ROOT)}")
    return all_ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
