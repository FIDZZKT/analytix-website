# 📊 Guide Mengolah Dataset Laptop di Orange Data Mining

## 🎯 Untuk Proyek Big Data Analysis

Dataset: **4000 produk laptop** dari marketplace Indonesia (Shopee, Tokopedia, Lazada, Blibli)

---

## 📁 Persiapan Data

### File yang Digunakan:
- **File CSV**: `all-data-laptop.csv` (1.24 MB, 4000 rows)
- **Delimiter**: Semicolon (`;`)
- **Encoding**: Latin-1 atau UTF-8

### Struktur Kolom:
1. `marketplace` - Nama marketplace (categorical)
2. `product_name` - Nama produk laptop (text)
3. `brand` - Brand laptop (categorical)
4. `price` - Harga dalam Rupiah (numeric)
5. `rating` - Rating produk (numeric, format: 4,8)
6. `review_count` - Jumlah review (numeric)
7. `sold_count` - Jumlah terjual (numeric)
8. `seller_name` - Nama penjual (text)
9. `seller_location` - Lokasi penjual (categorical)
10. `product_url` - Link produk (text/URL)
11. `scraped_date` - Tanggal scraping (date, format: DD/MM/YYYY)

---

## 🚀 Langkah-Langkah di Orange

### 1️⃣ **Import Data ke Orange**

#### A. Buka Orange Data Mining
- Download dari: https://orangedatamining.com/download/
- Install dan jalankan Orange

#### B. Import CSV File
1. Drag widget **File** ke canvas
2. Double-click widget File
3. Browse dan pilih file `all-data-laptop.csv`
4. Set delimiter: **Semicolon (`;`)**
5. Pastikan semua kolom ter-detect dengan benar

#### C. Cek Tipe Data
- `price`, `rating`, `review_count`, `sold_count` → **Numeric**
- `marketplace`, `brand`, `seller_location` → **Categorical**
- `product_name`, `seller_name` → **Text**
- `scraped_date` → **Time/Date**

⚠️ **PENTING**: Jika `rating` ter-detect sebagai text (karena koma sebagai desimal), lakukan preprocessing!

---

### 2️⃣ **Data Preprocessing**

#### A. Handle Format Indonesia
```
Rating menggunakan koma (,) sebagai desimal separator
Contoh: 4,8 → harus dikonversi ke 4.8
```

**Solusi di Orange:**
1. Gunakan widget **Python Script**
2. Code preprocessing:

```python
import pandas as pd
import numpy as np

# Convert rating dari format Indonesia (4,8) ke float (4.8)
if 'rating' in in_data.columns:
    in_data['rating'] = in_data['rating'].astype(str).str.replace(',', '.').astype(float)

# Clean price (remove text, convert to numeric)
if 'price' in in_data.columns:
    in_data['price'] = pd.to_numeric(in_data['price'], errors='coerce')

# Convert sold_count dan review_count ke numeric
for col in ['sold_count', 'review_count']:
    if col in in_data.columns:
        in_data[col] = pd.to_numeric(in_data[col], errors='coerce')

# Handle missing values
in_data = in_data.fillna({
    'rating': in_data['rating'].median(),
    'review_count': 0,
    'sold_count': 0,
    'price': in_data['price'].median()
})

out_data = in_data
```

#### B. Feature Engineering
Tambahkan widget **Feature Constructor** untuk membuat fitur baru:

1. **price_category** (Kategori harga):
```
if price < 3000000: "Budget"
elif price < 7000000: "Mid-Range"
elif price < 15000000: "Premium"
else: "High-End"
```

2. **popularity_score** (Skor popularitas):
```
(sold_count * 0.5) + (review_count * 0.3) + (rating * 1000 * 0.2)
```

3. **is_bestseller** (Bestseller flag):
```
sold_count > quantile(sold_count, 0.75)
```

4. **review_to_sold_ratio** (Engagement ratio):
```
review_count / (sold_count + 1)
```

---

### 3️⃣ **Exploratory Data Analysis (EDA)**

#### A. Statistik Deskriptif
**Widget: Data Table + Statistics**
- Lihat distribusi harga, rating, review, sold count
- Identifikasi outliers
- Mean, median, std deviation

#### B. Visualisasi Distribusi
**Widget: Distributions**
- Distribusi harga per marketplace
- Distribusi rating
- Distribusi brand

#### C. Box Plot
**Widget: Box Plot**
- Bandingkan harga antar marketplace
- Bandingkan rating antar brand
- Identifikasi outliers

#### D. Scatter Plot
**Widget: Scatter Plot**
- X-axis: `price`, Y-axis: `rating`
- X-axis: `price`, Y-axis: `sold_count`
- X-axis: `review_count`, Y-axis: `rating`
- Color by: `marketplace` atau `brand`

#### E. Heat Map (Correlation Matrix)
**Widget: Heat Map**
- Korelasi antar variabel numerik
- Cari hubungan price vs rating, sold_count vs review_count

---

### 4️⃣ **Analisis Lanjutan untuk Big Data Project**

#### A. **Price Prediction Model**
**Tujuan**: Prediksi harga laptop berdasarkan fitur

**Workflow Orange:**
```
File → Preprocess → Feature Selection 
  → Split Data (Train/Test) → Linear Regression / Random Forest
  → Test & Score → Predictions
```

**Features untuk prediksi harga:**
- `brand` (categorical)
- `rating` (numeric)
- `review_count` (numeric)
- `sold_count` (numeric)
- `marketplace` (categorical)
- `seller_location` (categorical)

**Widget Models:**
- Linear Regression
- Random Forest
- Gradient Boosting
- Neural Network

**Evaluasi:**
- RMSE (Root Mean Square Error)
- MAE (Mean Absolute Error)
- R² Score

#### B. **Clustering Analysis**
**Tujuan**: Grouping produk berdasarkan karakteristik

**Workflow Orange:**
```
File → Preprocess → Normalize → K-Means / Hierarchical Clustering
  → Silhouette Plot → Scatter Plot (colored by cluster)
```

**Features untuk clustering:**
- `price` (normalized)
- `rating` (normalized)
- `sold_count` (normalized)
- `review_count` (normalized)

**Interpretasi Cluster:**
- Cluster 1: Budget laptops (harga rendah, sold tinggi)
- Cluster 2: Premium laptops (harga tinggi, rating tinggi)
- Cluster 3: Niche products (sold rendah, harga sedang)

#### C. **Classification: Best Seller Prediction**
**Tujuan**: Prediksi apakah produk akan menjadi bestseller

**Workflow Orange:**
```
File → Preprocess → Feature Constructor (create bestseller label)
  → Split Data → Logistic Regression / SVM / Random Forest
  → Test & Score → Confusion Matrix → ROC Analysis
```

**Label (Target):**
- `is_bestseller` = 1 jika `sold_count` > median atau top 25%
- `is_bestseller` = 0 otherwise

**Features:**
- `price`
- `rating`
- `review_count`
- `marketplace`
- `brand`

**Evaluasi:**
- Accuracy
- Precision
- Recall
- F1-Score
- AUC-ROC

#### D. **Market Comparison Analysis**
**Tujuan**: Analisis perbandingan marketplace

**Widget: Group By + Bar Plot**
```sql
-- Average price per marketplace
GROUP BY marketplace
AGGREGATE AVG(price), AVG(rating), SUM(sold_count)

-- Top brands per marketplace
GROUP BY marketplace, brand
COUNT(*)
```

**Visualisasi:**
- Bar chart: Avg price per marketplace
- Stacked bar: Brand distribution per marketplace
- Line chart: Rating trend per marketplace

#### E. **Geospatial Analysis**
**Tujuan**: Analisis berdasarkan lokasi seller

**Widget: Geo Map (jika ada add-on)**
```
seller_location → Aggregate by city
  → Count products, Avg price, Avg rating
  → Visualize on Indonesia map
```

#### F. **Text Mining on Product Names**
**Tujuan**: Ekstrak keyword populer dari nama produk

**Workflow Orange:**
```
File → Preprocess Text → Word Cloud → Topic Modeling (LDA)
  → Most Frequent Terms
```

**Analisis:**
- Keyword paling sering: "Core i5", "SSD", "RAM 8GB"
- Topic modeling: identifikasi kategori laptop (Gaming, Office, Ultrabook)
- Sentiment dari review (jika ada text review)

#### G. **Time Series Analysis**
**Tujuan**: Trend harga dan penjualan berdasarkan waktu scraping

**Widget: Line Plot**
```
GROUP BY scraped_date
AGGREGATE AVG(price), COUNT(*)
```

**Analisis:**
- Trend harga laptop per bulan
- Volume scraping per hari
- Seasonal pattern (jika data > 1 tahun)

---

### 5️⃣ **Advanced Big Data Workflows**

#### A. **Association Rules Mining**
**Tujuan**: Temukan pola "Orang yang beli brand X cenderung dari marketplace Y"

**Widget: Associate Rules**
```
Basket: [brand, marketplace, seller_location, price_category]
Min Support: 0.05
Min Confidence: 0.5
```

#### B. **Anomaly Detection**
**Tujuan**: Deteksi produk dengan harga tidak wajar atau data outlier

**Widget: Outlier Detection**
- Isolation Forest
- Local Outlier Factor (LOF)

**Features:**
- `price` vs `rating`
- `sold_count` vs `review_count`

#### C. **Ensemble Models**
**Tujuan**: Kombinasi multiple models untuk prediksi lebih akurat

**Workflow:**
```
Split Data → [Random Forest, Gradient Boosting, SVM] 
  → Stack Models → Final Prediction → Test & Score
```

---

### 6️⃣ **Visualization untuk Presentasi**

#### Widget-widget Visualisasi:
1. **Bar Plot** - Perbandingan harga per marketplace/brand
2. **Scatter Plot** - Price vs Rating (colored by marketplace)
3. **Box Plot** - Distribusi harga per kategori
4. **Heat Map** - Correlation matrix
5. **Word Cloud** - Keyword dari product names
6. **Mosaic Display** - Hubungan categorical variables
7. **Silhouette Plot** - Kualitas clustering
8. **ROC Curve** - Performance classification model
9. **Tree Viewer** - Decision tree visualization
10. **Confusion Matrix** - Classification results

---

## 📊 Contoh Workflow Orange Lengkap

### **Workflow 1: Price Prediction Model**
```
[File] → [Python Script (Preprocessing)] 
  → [Feature Constructor] → [Select Columns]
  → [Split Data: 80/20]
     ├→ [Random Forest] → [Predictions]
     ├→ [Gradient Boosting] → [Predictions]
     └→ [Linear Regression] → [Predictions]
  → [Test & Score] → [Data Table]
```

### **Workflow 2: Market Segmentation**
```
[File] → [Preprocess] → [Normalize]
  → [K-Means (k=4)] → [Silhouette Plot]
  → [Scatter Plot (colored by cluster)]
  → [Box Plot (cluster vs price)]
  → [Data Table (with cluster labels)]
```

### **Workflow 3: Exploratory Data Analysis**
```
[File] → [Preprocess]
  ├→ [Data Table]
  ├→ [Distributions]
  ├→ [Statistics]
  ├→ [Box Plot]
  ├→ [Scatter Plot]
  ├→ [Heat Map]
  └→ [Bar Plot]
```

---

## 🎓 Tips untuk Proyek Big Data

### 1. **Problem Statement yang Jelas**
Contoh pertanyaan penelitian:
- Faktor apa yang paling mempengaruhi harga laptop di marketplace Indonesia?
- Apakah ada perbedaan signifikan harga antar marketplace?
- Bagaimana memprediksi produk bestseller?
- Apa karakteristik laptop paling populer?

### 2. **Metodologi yang Tepat**
- **Descriptive Analytics**: Statistik deskriptif, visualisasi
- **Diagnostic Analytics**: Correlation analysis, hypothesis testing
- **Predictive Analytics**: Regression, classification models
- **Prescriptive Analytics**: Recommendation system

### 3. **Validasi Model**
- Split data: Train (80%) / Test (20%)
- Cross-validation (k-fold)
- Compare multiple models
- Avoid overfitting

### 4. **Interpretasi Hasil**
- Jelaskan insight bisnis dari hasil analisis
- Bandingkan dengan domain knowledge
- Buat rekomendasi actionable

### 5. **Dokumentasi**
- Screenshot workflow Orange
- Export hasil visualisasi (PNG/SVG)
- Save model yang sudah ditraining
- Tulis laporan analisis

---

## 📥 Export Data dari Orange

### A. Export Hasil Preprocessing
**Widget: Save Data**
- Format: CSV, Excel, atau Pickle
- File: `laptop_clean.csv`

### B. Export Visualisasi
- Right-click pada widget visualisasi
- **Save Image** → PNG/SVG

### C. Export Model
**Widget: Save Model**
- Format: Pickle (.pkcls)
- Bisa di-load ulang untuk prediksi baru

---

## 🔗 Resources Tambahan

### Tutorial Orange:
- https://orangedatamining.com/docs/
- YouTube: Orange Data Mining Tutorials

### Dataset Info:
- Total records: 4000
- Marketplaces: Shopee, Tokopedia, Lazada, Blibli
- Periode: 60 hari terakhir (varied scraped_date)
- Brands: Lenovo, ASUS, HP, Acer, Dell, Axioo, Advan, dll

### Potential Analysis Topics:
1. ✅ Price Prediction Model (Regression)
2. ✅ Bestseller Classification (Classification)
3. ✅ Market Segmentation (Clustering)
4. ✅ Marketplace Comparison (Descriptive Stats)
5. ✅ Brand Analysis (Descriptive Stats)
6. ✅ Geographical Analysis (Location-based)
7. ✅ Product Name Text Mining (NLP)
8. ✅ Anomaly Detection (Outliers)
9. ✅ Association Rules (Pattern Mining)
10. ✅ Time Series Analysis (Trend)

---

## ✅ Checklist Proyek Big Data

- [ ] Import dan preprocess data di Orange
- [ ] Exploratory Data Analysis (EDA)
- [ ] Feature engineering
- [ ] Build dan train models
- [ ] Model evaluation dan comparison
- [ ] Visualisasi hasil
- [ ] Interpretasi insight bisnis
- [ ] Dokumentasi workflow
- [ ] Export hasil dan model
- [ ] Buat laporan/presentasi

---

## 🎯 Output yang Diharapkan

1. **Orange Workflow File** (.ows)
2. **Cleaned Dataset** (CSV)
3. **Trained Models** (.pkcls)
4. **Visualizations** (PNG/SVG)
5. **Analysis Report** (PDF/DOCX)
6. **Presentation Slides** (PPT)

---

**Good luck dengan proyek Big Data-nya! 🚀**

Jika ada pertanyaan atau butuh workflow Orange yang lebih spesifik, feel free to ask!
