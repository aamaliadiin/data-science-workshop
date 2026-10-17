"""
Dashboard Penjualan — Workshop Data Pipeline Sederhana (Streamlit)

Menjalankan:
    pip install -r requirements.txt
    streamlit run dashboard_app.py

Koneksi database dibaca dari environment variable / file .env:
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_SCHEMA (default = DB_USER), DB_TABLE (default sales_clean)
"""
import os

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

st.set_page_config(page_title="Dashboard Penjualan", page_icon="📊", layout="wide")
TEAL, AMBER, SLATE = "#0F766E", "#F59E0B", "#94A3B8"

SCHEMA = os.getenv("DB_SCHEMA", os.getenv("DB_USER", "ref"))
TABLE = f'{SCHEMA}.{os.getenv("DB_TABLE", "sales_clean")}'


@st.cache_resource
def get_engine():
    return create_engine(URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"), port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME", "workshop")),
        pool_size=1, max_overflow=1, pool_pre_ping=True)


@st.cache_data(ttl=300)
def load_data():
    with get_engine().connect() as conn:
        df = pd.read_sql(text(f"SELECT * FROM {TABLE}"), conn)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    return df


def rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")


st.title("📊 Dashboard Penjualan")
st.caption(f"Sumber: `{TABLE}` — hasil pipeline Extract → Transform → Load")

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal terhubung ke database: {e}")
    st.stop()

# ---------- Filter ----------
with st.sidebar:
    st.header("Filter")
    dmin, dmax = df.transaction_date.min().date(), df.transaction_date.max().date()
    rentang = st.date_input("Rentang tanggal", (dmin, dmax), min_value=dmin, max_value=dmax)
    kota = st.multiselect("Kota", sorted(df.city.unique()), default=sorted(df.city.unique()))
    kategori = st.multiselect("Kategori", sorted(df.category.unique()), default=sorted(df.category.unique()))
    if st.button("🔄 Muat ulang data"):
        st.cache_data.clear()
        st.rerun()

start, end = (rentang if isinstance(rentang, tuple) and len(rentang) == 2 else (dmin, dmax))
f = df[df.transaction_date.dt.date.between(start, end) & df.city.isin(kota) & df.category.isin(kategori)]
if f.empty:
    st.warning("Tidak ada data untuk filter ini.")
    st.stop()

# ---------- KPI ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", rupiah(f.total_amount.sum()))
c2.metric("Transaksi", f"{len(f):,}".replace(",", "."))
c3.metric("Pelanggan", f.customer_id.nunique())
c4.metric("Rata-rata / Transaksi", rupiah(f.total_amount.mean()))

# ---------- Tren ----------
harian = f.groupby(f.transaction_date.dt.date).total_amount.sum().reset_index()
harian.columns = ["Tanggal", "Revenue"]
harian["Rata-rata 7 hari"] = harian.Revenue.rolling(7, min_periods=1).mean()
fig = px.line(harian, x="Tanggal", y=["Revenue", "Rata-rata 7 hari"],
              color_discrete_sequence=[SLATE, TEAL], title="Revenue Harian")
fig.update_layout(legend_title="", yaxis_title="Rupiah")
st.plotly_chart(fig, use_container_width=True)

# ---------- Rincian ----------
l, r = st.columns(2)
kota_df = f.groupby("city").total_amount.sum().sort_values().reset_index()
l.plotly_chart(px.bar(kota_df, x="total_amount", y="city", orientation="h", title="Revenue per Kota",
                      color_discrete_sequence=[TEAL], labels={"total_amount": "Revenue", "city": ""}),
               use_container_width=True)
kat_df = f.groupby("category").total_amount.sum().reset_index()
r.plotly_chart(px.pie(kat_df, names="category", values="total_amount", hole=0.55, title="Komposisi Kategori",
                      color_discrete_sequence=[TEAL, AMBER, SLATE]), use_container_width=True)

st.subheader("Top Produk")
top = (f.groupby(["product_name", "category"])
         .agg(Qty=("quantity", "sum"), Revenue=("total_amount", "sum"))
         .sort_values("Revenue", ascending=False).reset_index())
top["Revenue"] = top["Revenue"].map(rupiah)
st.dataframe(top.rename(columns={"product_name": "Produk", "category": "Kategori"}),
             use_container_width=True, hide_index=True)

with st.expander("Lihat data mentah"):
    st.dataframe(f.sort_values("transaction_date", ascending=False), use_container_width=True, hide_index=True)
    st.download_button("⬇️ Unduh CSV", f.to_csv(index=False).encode(), "sales_filtered.csv", "text/csv")
