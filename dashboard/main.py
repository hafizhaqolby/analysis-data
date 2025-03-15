import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import urllib.request
from io import StringIO

# ----------------- 1. Load Dataset dari GitHub dengan urllib ----------------- #
BASE_URL = "https://raw.githubusercontent.com/hafizhaqolby/analysis-data/main/data/"

def load_csv(url):
    response = urllib.request.urlopen(url)
    return pd.read_csv(StringIO(response.read().decode('utf-8')))

# Load datasets
orders = load_csv(BASE_URL + 'orders_dataset.csv')
items = load_csv(BASE_URL + 'order_items_dataset.csv')
products = load_csv(BASE_URL + 'products_dataset.csv')
payments = load_csv(BASE_URL + 'order_payments_dataset.csv')
reviews = load_csv(BASE_URL + 'order_reviews_dataset.csv')
customers = load_csv(BASE_URL + 'customers_dataset.csv')
sellers = load_csv(BASE_URL + 'sellers_dataset.csv')
geolocation = load_csv(BASE_URL + 'geolocation_dataset.csv')
category = load_csv(BASE_URL + 'product_category_name_translation.csv')

data = {
    'orders': orders,
    'items': items,
    'products': products,
    'payments': payments,
    'reviews': reviews,
    'customers': customers,
    'sellers': sellers,
    'geo': geolocation,
    'category': category
}

# ----------------- 2. Data Preprocessing ----------------- #
# Merge dataset orders dan items dengan produk
items_product = data['items'].merge(data['products'], on='product_id', how='inner')
orders_ip = data['orders'].merge(items_product, on='order_id', how='inner')

# Pivot table untuk menghitung total pendapatan dan probabilitas penjualan
product_revenue = orders_ip.pivot_table(index=['product_id'], aggfunc={'order_item_id': 'sum', 'price': 'mean'})
product_revenue['total'] = product_revenue['order_item_id'] * product_revenue['price']
product_revenue.rename(columns={'order_item_id': 'sell_probability'}, inplace=True)
product_revenue['sell_probability'] = product_revenue['sell_probability'] / len(product_revenue)
product_revenue.sort_values(by='total', ascending=False, inplace=True)

# ----------------- 3. Sidebar ----------------- #
with st.sidebar:
    # Nama & Logo
    st.title("Hafizha Nurul Q.")
    st.image("gcl.png", width=200)

    # Filter Rentang Tanggal
    datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date",
                     "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]

    for col in datetime_cols:
        if col in orders.columns:
            orders[col] = pd.to_datetime(orders[col], errors='coerce')
        else:
            print(f"Warning: Column {col} not found in orders dataset")

    min_date = orders["order_approved_at"].min()
    max_date = orders["order_approved_at"].max()

    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Filter Data
    filtered_orders = orders[(orders["order_approved_at"] >= str(start_date)) & 
                             (orders["order_approved_at"] <= str(end_date))]

# ----------------- 4. Visualisasi Produk ----------------- #
st.title("📊 Product Analysis")

x = np.log(product_revenue.sell_probability)
y = np.log(product_revenue.price)

fig, ax = plt.subplots(figsize=(8, 6))
sns.set(style='darkgrid')

hb = ax.hexbin(x, y, gridsize=14, C=product_revenue.total, reduce_C_function=np.sum, cmap='cividis')
cb = fig.colorbar(hb, ax=ax)
cb.set_label('Product Revenue (R$)', rotation=270, labelpad=20, fontsize=12)

plt.title('Product Price vs. Sell Probability', fontsize=16)
plt.xlabel('Log Sell Probability', fontsize=12)
plt.ylabel('Log Product Price', fontsize=12)

st.pyplot(fig)

# ----------------- 5. Visualisasi Geolocation ----------------- #
st.title("🗺️ Customer Geolocation in Brazil")

# Preprocessing Geolocation Data
geo_grouped = data['geo'].groupby(['geolocation_zip_code_prefix', 'geolocation_state'])\
    .size().reset_index(name='count')
geo_most_common_state = geo_grouped.drop_duplicates(subset='geolocation_zip_code_prefix')

geolocation_silver = data['geo'].groupby(['geolocation_zip_code_prefix', 'geolocation_city', 'geolocation_state'])[
    ['geolocation_lat', 'geolocation_lng']].median().reset_index()

geolocation_silver = geolocation_silver.merge(geo_most_common_state, on=['geolocation_zip_code_prefix', 'geolocation_state'], how='inner')
customers_silver = customers.merge(geolocation_silver, left_on='customer_zip_code_prefix',
                                   right_on='geolocation_zip_code_prefix', how='inner').drop_duplicates('customer_id')

# Plot Brazil Map
def plot_brazil_map(data):
    brazil_map_url = "https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg"
    brazil = plt.imread(urllib.request.urlopen(brazil_map_url), 'jpg')

    fig, ax = plt.subplots(figsize=(10, 10))
    data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(10, 10), alpha=0.3, s=0.3, c='maroon', ax=ax)
    ax.imshow(brazil, extent=[-73.98283055, -33.8, -33.75116944, 5.4])
    plt.axis('off')
    st.pyplot(fig)

# Menampilkan Peta
plot_brazil_map(customers_silver.drop_duplicates(subset='customer_unique_id'))

st.caption('© 2025 E-Commerce Analysis Dashboard')