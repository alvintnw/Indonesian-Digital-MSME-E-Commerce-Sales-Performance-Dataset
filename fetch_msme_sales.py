from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def generate_msme_sales_dataset():
  np.random.seed(42)
  n_rows = 1500

  # Tanggal transaksi dalam 90 hari terakhir
  end_date = datetime.now()
  start_date = end_date - timedelta(days=90)
  date_list = [
      start_date + timedelta(days=int(np.random.randint(0, 90)))
      for _ in range(n_rows)
  ]

  provinces = [
      "DKI Jakarta",
      "Jawa Barat",
      "Jawa Timur",
      "Jawa Tengah",
      "Banten",
      "DI Yogyakarta",
      "Sumatera Utara",
      "Bali",
  ]
  province_weights = [0.30, 0.25, 0.15, 0.10, 0.08, 0.05, 0.04, 0.03]

  categories = [
      "Fashion & Apparel",
      "Food & Beverage",
      "Beauty & Skincare",
      "Home & Living",
      "Gadgets & Accessories",
  ]
  channels = ["Tokopedia", "Shopee", "TikTok Shop", "WhatsApp Business"]
  payment_methods = ["QRIS", "Virtual Account", "Bank Transfer", "COD"]

  data = []
  for i in range(n_rows):
    prov = np.random.choice(provinces, p=province_weights)
    cat = np.random.choice(categories)
    channel = np.random.choice(channels)
    pay = np.random.choice(payment_methods)

    # Harga berdasarkan kategori produk (dalam Rupiah)
    if cat == "Fashion & Apparel":
      price = int(np.random.randint(75000, 350000))
    elif cat == "Food & Beverage":
      price = int(np.random.randint(25000, 120000))
    elif cat == "Beauty & Skincare":
      price = int(np.random.randint(50000, 250000))
    elif cat == "Home & Living":
      price = int(np.random.randint(100000, 750000))
    else:  # Gadgets
      price = int(np.random.randint(50000, 500000))

    qty = int(np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.3, 0.1, 0.05, 0.05]))
    revenue = price * qty
    rating = round(float(np.random.choice([4.0, 4.5, 4.8, 5.0], p=[0.1, 0.2, 0.3, 0.4])), 1)

    data.append({
        "order_id": f"ORD-{1000 + i}",
        "order_date": date_list[i].strftime("%Y-%m-%d"),
        "province": prov,
        "product_category": cat,
        "sales_channel": channel,
        "unit_price_idr": price,
        "quantity": qty,
        "total_revenue_idr": revenue,
        "customer_rating": rating,
        "payment_method": pay,
    })

  df = pd.DataFrame(data)
  filename = "indonesia_msme_sales_dataset.csv"
  df.to_csv(filename, index=False)
  print(
      f"Success! Dataset generated with {len(df)} records and saved as"
      f" '{filename}'"
  )


if __name__ == "__main__":
  generate_msme_sales_dataset()
