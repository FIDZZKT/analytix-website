# Analytix - Platform Big Data Analytics

Platform analisis dan perbandingan produk laptop dari berbagai marketplace (Shopee, Tokopedia, Lazada, Blibli).

## 📁 Struktur Folder

```
Analytix/
├── backend/                  # Backend Flask API
│   ├── models/              # Database models
│   ├── routes/              # API endpoints
│   ├── data/                # Dataset
│   ├── app.py               # Main Flask app
│   ├── config.py            # Configuration
│   └── requirements.txt     # Dependencies
│
├── frontend/                # Frontend Web
│   ├── assets/              
│   │   ├── css/            
│   │   │   └── main.css    # Semua styling (satu file)
│   │   └── js/             
│   │       └── data.js     # Dataset JavaScript
│   │
│   ├── index.html          # Dashboard
│   ├── products.html       # Katalog produk
│   ├── comparison.html     # Perbandingan harga
│   ├── analysis.html       # Analisis data
│   ├── trends.html         # Tren harga
│   ├── prediction.html     # Prediksi harga
│   ├── recommendation.html # Rekomendasi
│   └── about.html          # Tentang
│
├── database/                # Database schema
│   └── schema.sql          # SQL schema
│
└── .agents/                 # AI agents artifacts
    └── tasks/              # Planning files
        └── plan.md
```

## 🎨 Desain

Website menggunakan desain **profesional SaaS** dengan karakteristik:

- **Layout**: Sidebar + Header + Content Area
- **Warna**: Navy, Blue, Gray (bukan dark theme)
- **Typography**: Inter font, hierarchy yang jelas
- **Components**: Card, Table, Stats, Charts
- **Spacing**: 4px grid system
- **Style**: Clean, minimalis, fungsional

## 🚀 Cara Menjalankan

### Frontend
Buka langsung file HTML di browser atau gunakan live server:
```bash
cd frontend
# Buka index.html di browser
```

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## 📝 Fitur

1. **Dashboard**: Overview statistik produk
2. **Produk**: Katalog dengan filter & search
3. **Perbandingan**: Compare harga antar marketplace
4. **Analisis**: Visualisasi distribusi data
5. **Tren**: Grafik perubahan harga
6. **Prediksi**: Prediksi harga ML
7. **Rekomendasi**: Saran produk
8. **Tentang**: Info proyek

## 💡 Catatan

- Data yang digunakan adalah **dataset demo**
- CSS disatukan dalam **satu file** (main.css) untuk kemudahan maintenance
- Desain dibuat **profesional** dan **tidak terlihat AI-generated**
- Struktur folder **sederhana** dan **mudah dikelola**

## 📄 License

Educational project - 2025
