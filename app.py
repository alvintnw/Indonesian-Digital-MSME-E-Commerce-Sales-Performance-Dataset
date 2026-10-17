import os
import pandas as pd
import plotly.express as px
import streamlit as st

# Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="Indonesian MSME Sales Dashboard", page_icon="🛍️", layout="wide"
)

st.title("🛍️ Indonesian Digital MSME & E-Commerce Sales Dashboard")
st.markdown(
    "Interactive business intelligence dashboard tracking digital sales revenue,"
    " channel performance, and customer satisfaction for Indonesian MSMEs"
    " (UMKM)."
)


# Fungsi untuk memuat dataset CSV
@st.cache_data
def load_sales_data():
  filename = "indonesia_msme_sales_dataset.csv"
  if os.path.exists(filename):
    df = pd.read_csv(filename)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df
  else:
    return pd.DataFrame()


df = load_sales_data()

if df.empty:
  st.warning(
      "Dataset file (`indonesia_msme_sales_dataset.csv`) not found. Please"
      " ensure the CSV file is uploaded."
  )
else:
  # Sidebar Filters
  st.sidebar.header("⚙️ Filter Options")

  provinces = sorted(df["province"].unique())
  selected_provinces = st.sidebar.multiselect(
      "Select Provinces:", options=provinces, default=provinces
  )

  categories = sorted(df["product_category"].unique())
  selected_categories = st.sidebar.multiselect(
      "Select Product Category:", options=categories, default=categories
  )

  channels = sorted(df["sales_channel"].unique())
  selected_channels = st.sidebar.multiselect(
      "Select Sales Channel:", options=channels, default=channels
  )

  # Filter DataFrame
  filtered_df = df[
      (df["province"].isin(selected_provinces))
      & (df["product_category"].isin(selected_categories))
      & (df["sales_channel"].isin(selected_channels))
  ]

  # Executive Metrics Overview
  st.subheader("📊 Executive Performance Summary")
  col1, col2, col3, col4 = st.columns(4)

  total_rev = filtered_df["total_revenue_idr"].sum() if not filtered_df.empty else 0
  total_orders = len(filtered_df)
  avg_order_val = total_rev / total_orders if total_orders > 0 else 0
  avg_rating = (
      filtered_df["customer_rating"].mean() if not filtered_df.empty else 0
  )

  with col1:
    st.metric(label="Total Revenue", value=f"Rp {total_rev:,.0f}")
  with col2:
    st.metric(label="Total Orders", value=f"{total_orders:,} Orders")
  with col3:
    st.metric(label="Avg. Order Value (AOV)", value=f"Rp {avg_order_val:,.0f}")
  with col4:
    st.metric(label="Avg. Customer Rating", value=f"⭐ {avg_rating:.2f} / 5.0")

  st.markdown("---")

  # Visualizations Layout
  col_a, col_b = st.columns(2)

  with col_a:
    st.subheader("💰 Revenue by Product Category")
    if not filtered_df.empty:
      cat_rev = (
          filtered_df.groupby("product_category")["total_revenue_idr"]
          .sum()
          .reset_index()
      )
      fig_cat = px.bar(
          cat_rev,
          x="product_category",
          y="total_revenue_idr",
          color="product_category",
          title="Total Revenue per Category (IDR)",
          labels={
              "product_category": "Category",
              "total_revenue_idr": "Revenue (IDR)",
          },
      )
      st.plotly_chart(fig_cat, use_container_width=True)

  with col_b:
    st.subheader("🛒 Sales Channel Performance")
    if not filtered_df.empty:
      channel_rev = (
          filtered_df.groupby("sales_channel")["total_revenue_idr"]
          .sum()
          .reset_index()
      )
      fig_chan = px.pie(
          channel_rev,
          names="sales_channel",
          values="total_revenue_idr",
          title="Revenue Share by Sales Channel",
          hole=0.4,
      )
      st.plotly_chart(fig_chan, use_container_width=True)

  # Timeline Trend
  st.subheader("📈 Daily Revenue Trend")
  if not filtered_df.empty:
    daily_trend = (
        filtered_df.groupby("order_date")["total_revenue_idr"].sum().reset_index()
    )
    fig_time = px.line(
        daily_trend,
        x="order_date",
        y="total_revenue_idr",
        title="Transaction Revenue Over Time",
        labels={"order_date": "Date", "total_revenue_idr": "Revenue (IDR)"},
    )
    st.plotly_chart(fig_time, use_container_width=True)

  # Raw Data Expander
  with st.expander("🔍 View Raw MSME Sales Dataset"):
    st.dataframe(df, use_container_width=True)
