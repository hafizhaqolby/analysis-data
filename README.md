# analysis-data
**E-Commerce Dashboard**

📌 Deskripsi
E-Commerce Dashboard adalah aplikasi berbasis Streamlit yang digunakan untuk menganalisis data transaksi e-commerce. Dashboard ini menampilkan berbagai visualisasi data seperti jumlah pesanan harian, pengeluaran pelanggan, jumlah item terjual, skor ulasan, serta demografi pelanggan.

🚀 Fitur Utama
Analisis Pesanan Harian: Menampilkan jumlah pesanan harian beserta total pendapatan.
Pengeluaran Pelanggan: Melihat total dan rata-rata pengeluaran pelanggan.
Jumlah Item Terjual: Menampilkan jumlah produk yang terjual dan kategori paling laris.
Skor Ulasan Pelanggan: Menganalisis rating yang diberikan pelanggan.
Demografi Pelanggan: Melihat distribusi pelanggan berdasarkan negara bagian dan status pesanan.
Visualisasi Geolokasi: Menampilkan peta distribusi pelanggan di Brasil.

📂 Struktur Folder <br>
```
│-- dashboard/<br>
│   │-- main.py<br>
│   │-- func.py<br>
│   │-- gcl.png<br>
│-- data/<br>
│   │-- all_data.csv<br>
│   │-- geolocation.csv<br>
│-- requirements.txt<br>
│-- README.md<br>
│-- Proyek_Analisis_Data.ipynb<br>
```

🔧 Instalasi dan Menjalankan Aplikasi
- Clone repositori (jika menggunakan GitHub):
```git clone https://github.com/hafizhaqolby/analysis-data.git
cd analysis-data
```
- Buat Virtual Environment (Opsional, tapi disarankan)
```python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```
- Install dependensi
```
pip install -r requirements.txt
```
- Arahkan ke folder dashboard
```
cd dashboard
```
- Jalankan Streamlit App
```
streamlit run main.py
```

📜 Requirements<br>
Daftar pustaka yang digunakan ada di requirements.txt. Jika belum dibuat, bisa di-generate dengan:
```
pipreqs . --force
```

📊 Dataset<br>
Dataset yang digunakan dalam proyek ini berasal dari Olist E-Commerce Public Dataset.

📞 Kontak<br>
Dibuat oleh Hafizha Nurul Q.<br>
📧 Email: hafizhaqolby@gmail.com<br>
🌐 LinkedIn: linkedin.com/in/hafizhaqolby<br>
