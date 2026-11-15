# 📊 Analytix - Laptop Price Comparison Platform

**Analytix** adalah platform perbandingan harga laptop dari 4 marketplace terbesar di Indonesia: **Shopee**, **Tokopedia**, **Lazada**, dan **Blibli**.

![Analytix Dashboard](https://img.shields.io/badge/Version-1.0.0-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Fitur Utama

### 📈 Dashboard Analytics
- **Real-time Statistics** - Total produk, marketplace, brand, dan harga rata-rata
- **Interactive Charts** - Visualisasi data dengan Chart.js
- **Price Distribution** - Analisis distribusi harga laptop
- **Brand Comparison** - Perbandingan brand berdasarkan jumlah produk

### 💻 Katalog Produk
- **Advanced Filtering** - Filter berdasarkan brand, marketplace, harga, RAM, GPU
- **Real-time Search** - Pencarian produk instan
- **Product Details** - Informasi lengkap spesifikasi laptop
- **Pagination** - Tampilan data yang optimal

### ⚖️ Perbandingan Harga
- **Multi-marketplace Comparison** - Bandingkan harga produk yang sama dari berbagai marketplace
- **Best Price Highlight** - Otomatis highlight harga terbaik
- **Savings Calculator** - Hitung potensi penghematan

### 📉 Analisis & Tren
- **8 Chart Visualizations** - Analisis mendalam dengan berbagai jenis chart
- **Price Trends** - Trend harga dari waktu ke waktu
- **GPU vs Price Analysis** - Korelasi spesifikasi dengan harga

### 🔮 Prediksi Harga
- **Price Prediction** - Estimasi harga berdasarkan spesifikasi
- **Simulation Mode** - Heuristic-based price estimation
- **Spec-based Calculator** - Input spesifikasi untuk prediksi harga

### ⭐ Rekomendasi
- **Smart Recommendations** - Rekomendasi laptop berdasarkan kebutuhan
- **Budget Filter** - Sesuaikan dengan budget Anda
- **Use Case Presets** - Gaming, Desain, Sekolah, Pekerjaan
- **Scoring System** - Sistem scoring otomatis berdasarkan kriteria

### 📁 Data CSV
- **CSV Preview** - Preview file CSV langsung di browser
- **Download Raw Data** - Download dataset lengkap (55 records)
- **Export Filtered Data** - Export data yang sudah difilter
- **Dataset Metadata** - Informasi lengkap tentang dataset

## 🚀 Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom design system (no frameworks)
- **Vanilla JavaScript** - No dependencies
- **Chart.js** - Data visualization
- **Google Fonts** - Inter font family

### Backend (Optional)
- **Python Flask** - REST API
- **MySQL** - Database
- **Pandas** - Data processing
- **BeautifulSoup4** - Web scraping (future)

## 📦 Dataset

- **Total Records**: 55 laptop
- **Brands**: ASUS, Lenovo, HP, Acer, Dell, MSI, Apple, Samsung, Xiaomi
- **Marketplaces**: Shopee, Tokopedia, Lazada, Blibli
- **Columns**: 22 fields (ID, Name, Brand, Processor, RAM, Storage, GPU, Price, Rating, dll)
- **Format**: CSV (UTF-8)

## 🎨 Design System

### Colors
- **Primary**: #2563eb (Blue)
- **Navy**: #0a0a0a
- **Gray Scale**: #f9fafb to #111827
- **Success**: #10b981
- **Warning**: #f59e0b
- **Danger**: #ef4444

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 400, 500, 600, 700

### Layout
- **Sidebar**: 260px fixed
- **Header**: 64px height
- **Border Radius**: 6px, 8px, 12px
- **Spacing**: 4px base unit

## 📂 Project Structure

```
Analytix/
├── frontend/
│   ├── assets/
│   │   ├── css/
│   │   │   └── main.css          # Main stylesheet
│   │   └── js/
│   │       ├── data.js            # Dataset
│   │       ├── dashboard.js       # Dashboard logic
│   │       ├── products.js        # Product catalog
│   │       ├── comparison.js      # Price comparison
│   │       ├── analysis.js        # Analytics
│   │       ├── trends.js          # Price trends
│   │       ├── prediction.js      # Price prediction
│   │       └── recommendation.js  # Recommendations
│   ├── index.html                 # Dashboard page
│   ├── products.html              # Product catalog
│   ├── comparison.html            # Price comparison
│   ├── analysis.html              # Analytics
│   ├── trends.html                # Price trends
│   ├── prediction.html            # Prediction
│   ├── recommendation.html        # Recommendations
│   ├── data.html                  # CSV Data page
│   ├── about.html                 # About page
│   └── all-data-laptop.csv        # Dataset file
├── backend/                       # (Optional - for API)
│   ├── app.py
│   ├── config.py
│   ├── routes/
│   ├── models/
│   └── data/
├── database/                      # (Optional - for MySQL)
│   └── schema.sql
└── README.md
```

## 🚀 Deployment

### Vercel (Recommended)

1. Push repository ke GitHub
2. Buka [Vercel](https://vercel.com)
3. Import repository Analytix
4. Set **Root Directory**: `frontend`
5. Framework Preset: **Other**
6. Deploy!

### Manual Deployment

1. Upload folder `frontend/` ke web hosting
2. Pastikan `index.html` sebagai default page
3. Akses melalui domain Anda

## 🔧 Development

### Local Setup

1. Clone repository:
```bash
git clone https://github.com/USERNAME/Analytix.git
cd Analytix
```

2. Open in browser:
```bash
cd frontend
# Open index.html in your browser
```

3. (Optional) Run with Python HTTP Server:
```bash
cd frontend
python -m http.server 8000
# Access at http://localhost:8000
```

## 📊 Features Roadmap

- [x] Dashboard with statistics
- [x] Product catalog with filters
- [x] Price comparison
- [x] Analytics with charts
- [x] Price trends visualization
- [x] Price prediction
- [x] Smart recommendations
- [x] CSV data preview & download
- [ ] Real marketplace scraping
- [ ] User authentication
- [ ] Wishlist feature
- [ ] Price alerts
- [ ] Mobile app

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Analytix Team**
- Website: [analytix.vercel.app](https://analytix.vercel.app)
- GitHub: [@USERNAME](https://github.com/USERNAME)

## 🙏 Acknowledgments

- Chart.js for data visualization
- Google Fonts for Inter font family
- All marketplace platforms for inspiration

---

**Made with ❤️ for Indonesian laptop shoppers**
