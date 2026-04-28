import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛒", layout="wide")

# Memastikan path file benar untuk Streamlit Cloud maupun Lokal
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(file_path)
    datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column])
    return df

main_df = load_data()

# --- SIDEBAR (FITUR INTERAKTIF) ---
min_date = main_df["order_purchase_timestamp"].min().date()
max_date = main_df["order_purchase_timestamp"].max().date()

with st.sidebar:
    st.title("Iamho Pegodang Eltiuzy")
    st.write("Learning Path: Data Scientist")
    
    # Menambahkan filter rentang waktu
    try:
        start_date, end_date = st.date_input(
            label='Pilih Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    except ValueError:
        st.error("Silakan pilih tanggal awal dan akhir.")
        st.stop()

# Menghubungkan filter dengan dataframe
filtered_df = main_df[(main_df["order_purchase_timestamp"].dt.date >= start_date) & 
                      (main_df["order_purchase_timestamp"].dt.date <= end_date)]

# --- DASHBOARD UTAMA ---
st.header('E-Commerce Data Analysis Dashboard 🛒')

# Visualisasi 1: Pendapatan Produk
st.subheader("Total Revenue berdasarkan Kategori Produk")
category_revenue = filtered_df.groupby("product_category_name_english")["price"].sum().sort_values(ascending=False).reset_index()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 5 Kategori Pendapatan Tertinggi")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_top = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    if not category_revenue.empty:
        sns.barplot(x="price", y="product_category_name_english", data=category_revenue.head(5), palette=colors_top, ax=ax)
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel(None)
    st.pyplot(fig)

with col2:
    st.markdown("#### 5 Kategori Pendapatan Terendah")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_bottom = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    if not category_revenue.empty:
        sns.barplot(x="price", y="product_category_name_english", data=category_revenue.tail(5).sort_values(by='price', ascending=True), palette=colors_bottom, ax=ax)
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel(None)
    ax.invert_xaxis()
    ax.yaxis.tick_right()
    st.pyplot(fig)

# Visualisasi 2: Tren Bulanan
st.subheader("Tren Pemesanan Bulanan")
# ERROR FIX: 'M' diubah menjadi 'ME'
monthly_orders = filtered_df.resample(rule='ME', on='order_purchase_timestamp').agg({"order_id": "nunique"}).reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_orders["order_purchase_timestamp"], monthly_orders["order_id"], marker='o', linewidth=2, color="#72BCD4")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# Visualisasi 3: RFM
st.subheader("RFM Analysis (Recency, Frequency, Monetary)")
rfm_df = filtered_df.groupby("customer_id", as_index=False).agg({
    "order_purchase_timestamp": "max",
    "order_id": "nunique",
    "price": "sum"
})
rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
recent_date = filtered_df["order_purchase_timestamp"].max().date() if not filtered_df.empty else max_date
rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

col3, col4, col5 = st.columns(3)
col3.metric("Average Recency (Days)", round(rfm_df.recency.mean(), 1) if not rfm_df.empty else 0)
col4.metric("Average Frequency", round(rfm_df.frequency.mean(), 2) if not rfm_df.empty else 0)
col5.metric("Average Monetary", f"${round(rfm_df.monetary.mean(), 2)}" if not rfm_df.empty else "$0")

st.caption("Copyright © Iamho Pegodang Eltiuzy 2026")