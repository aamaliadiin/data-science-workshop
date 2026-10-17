"""
Workshop Sales API — mock API untuk latihan Extract.

Menjalankan:
    cd api
    pip install -r requirements.txt
    uvicorn mock_api:app --host 0.0.0.0 --port 8000

Dokumentasi interaktif otomatis: http://<HOST>:8000/docs

Endpoint:
    GET /health                                   -> status API
    GET /sales?page=1&page_size=100               -> transaksi Q1 2026 (dataset utama)
    GET /sales-q2?page=1&page_size=100            -> transaksi Q2 2026 (mini project)
    GET /customers                                -> master pelanggan (mini project)
Header opsional: X-API-Key (aktif jika environment variable WORKSHOP_API_KEY di-set)
"""
import os
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Header, HTTPException, Query

BASE = Path(__file__).resolve().parent
DATA_DIR = BASE.parent / "data"
API_KEY = os.getenv("WORKSHOP_API_KEY")  # kosongkan untuk tanpa autentikasi


def _load(rel: str) -> pd.DataFrame:
    p = DATA_DIR / rel
    return pd.read_csv(p, dtype=str, keep_default_na=False)


SALES = _load("sales_raw.csv")
SALES_Q2 = _load("sales_q2_raw.csv")
CUSTOMERS = _load("customers_raw.csv")

app = FastAPI(title="Workshop Sales API", version="1.0",
              description="API latihan workshop Data Pipeline Sederhana")


def _check_key(x_api_key):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key tidak valid")


def _paginate(df: pd.DataFrame, page: int, page_size: int):
    start = (page - 1) * page_size
    chunk = df.iloc[start:start + page_size]
    return {
        "page": page,
        "page_size": page_size,
        "total": len(df),
        "has_next": start + page_size < len(df),
        "data": chunk.to_dict(orient="records"),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/sales")
def sales(page: int = Query(1, ge=1), page_size: int = Query(100, ge=1, le=500),
          x_api_key: str | None = Header(default=None)):
    _check_key(x_api_key)
    return _paginate(SALES, page, page_size)


@app.get("/sales-q2")
def sales_q2(page: int = Query(1, ge=1), page_size: int = Query(100, ge=1, le=500),
             x_api_key: str | None = Header(default=None)):
    _check_key(x_api_key)
    return _paginate(SALES_Q2, page, page_size)


@app.get("/customers")
def customers(x_api_key: str | None = Header(default=None)):
    _check_key(x_api_key)
    return {"total": len(CUSTOMERS), "data": CUSTOMERS.to_dict(orient="records")}
