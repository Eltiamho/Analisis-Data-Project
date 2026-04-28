import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tata letak halaman Streamlit
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛒", layout="wide")

# Fungsi untuk memuat data (menggunakan cache agar lebih cepat)
@st.cache_data
def load_data():
    # Mendapatkan path absolut dari direktori file dashboard.py saat ini
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Menggabungkan path direktori dengan nama file CSV
    file_path = os.path.join(current_dir, "main_data.csv")
    
    df = pd.read_csv(file_path)
    
    # Memastikan tipe data datetime
    datetime_cols = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col])
    return df

main_df = load_data()

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("Iamho Pegodang Eltiuzy")
st.sidebar.markdown("**Data Scientist - Dicoding**")
st.sidebar.write("Dashboard Analisis Data E-Commerce Public Dataset")

# ==============================
# MAIN PAGE
# ==============================
st.title("🛒 E-Commerce Data Analytics Dashboard")
st.markdown("Dashboard ini menampilkan hasil analisis data e-commerce, mencakup performa kategori produk, tren pesanan, dan segmentasi pelanggan (RFM Analysis).")

# ------------------------------
# 1. VISUALISASI PERTANYAAN 1
# ------------------------------
st.subheader("Pendapatan Kategori Produk (2017-2018)")
sales_17_18 = main_df[main_df['order_purchase_timestamp'].dt.year.isin([2017, 2018])]
category_revenue = sales_17_18.groupby('product_category_name_english')['price'].sum().reset_index()
category_revenue = category_revenue.sort_values(by='price', ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 5 Kategori Pendapatan Tertinggi")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_top = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(x="price", y="product_category_name_english", data=category_revenue.head(5), palette=colors_top, ax=ax)
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel(None)
    st.pyplot(fig)

with col2:
    st.markdown("#### 5 Kategori Pendapatan Terendah")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_bottom = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"] # Warna abu-abu seragam
    sns.barplot(x="price", y="product_category_name_english", data=category_revenue.tail(5).sort_values(by='price', ascending=True), palette=colors_bottom, ax=ax)
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel(None)
    ax.invert_xaxis()
    ax.yaxis.tick_right()
    st.pyplot(fig)

# ------------------------------
# 2. VISUALISASI PERTANYAAN 2
# ------------------------------
st.subheader("Tren Jumlah Transaksi Pesanan per Bulan (Tahun 2017)")
sales_2017 = main_df[main_df['order_purchase_timestamp'].dt.year == 2017].copy()
sales_2017['purchase_month'] = sales_2017['order_purchase_timestamp'].dt.month
monthly_orders = sales_2017.groupby('purchase_month')['order_id'].nunique().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_orders["purchase_month"], monthly_orders["order_id"], marker='o', linewidth=2, color="#72BCD4")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agt', 'Sep', 'Okt', 'Nov', 'Des'])
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# ------------------------------
# 3. ANALISIS LANJUTAN (RFM)
# ------------------------------
st.subheader("RFM Analysis (Recency, Frequency, Monetary)")
st.write("Metrik di bawah ini menunjukkan rata-rata perilaku pelanggan di platform:")

rfm_df = main_df.groupby("customer_id", as_index=False).agg({
    "order_purchase_timestamp": "max",
    "order_id": "nunique",
    "price": "sum"
})
rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
recent_date = main_df["order_purchase_timestamp"].max().date()
rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

col3, col4, col5 = st.columns(3)
col3.metric("Average Recency (Days)", round(rfm_df.recency.mean(), 1))
col4.metric("Average Frequency", round(rfm_df.frequency.mean(), 2))
col5.metric("Average Monetary", f"${round(rfm_df.monetary.mean(), 2)}")

st.caption("Copyright © Iamho Pegodang Eltiuzy 2026")