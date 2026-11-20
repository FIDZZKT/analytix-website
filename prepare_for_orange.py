"""
Script untuk mempersiapkan data laptop untuk Orange Data Mining
- Convert format Indonesia ke format internasional
- Clean dan handle missing values
- Add feature engineering
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*60)
print("PREPROCESSING DATA LAPTOP UNTUK ORANGE DATA MINING")
print("="*60)

# Read CSV
input_file = 'all-data-laptop.csv'
output_file = 'laptop_dataset_for_orange.csv'

print(f"\n📂 Membaca file: {input_file}")

# Try multiple encodings
for encoding in ['latin-1', 'utf-8', 'cp1252']:
    try:
        df = pd.read_csv(input_file, delimiter=';', encoding=encoding)
        print(f"✓ Berhasil dengan encoding: {encoding}")
        break
    except:
        continue

print(f"   Total records: {len(df)}")
print(f"   Kolom: {', '.join(df.columns.tolist())}")

# ===========================================
# 1. CLEAN & CONVERT DATA TYPES
# ===========================================
print("\n🔧 Preprocessing data...")

# Convert rating dari format Indonesia (4,8) ke float (4.8)
if 'rating' in df.columns:
    df['rating'] = df['rating'].astype(str).str.replace(',', '.').astype(float)
    print("   ✓ Rating converted: '4,8' → 4.8")

# Clean price (remove text, convert to numeric)
if 'price' in df.columns:
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    print("   ✓ Price cleaned and converted to numeric")

# Convert sold_count dan review_count ke numeric
for col in ['sold_count', 'review_count']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        print(f"   ✓ {col} converted to numeric")

# ===========================================
# 2. HANDLE MISSING VALUES
# ===========================================
print("\n🔍 Handling missing values...")

missing_before = df.isnull().sum().sum()

df['rating'] = df['rating'].fillna(df['rating'].median())
df['review_count'] = df['review_count'].fillna(0)
df['sold_count'] = df['sold_count'].fillna(0)
df['price'] = df['price'].fillna(df['price'].median())

missing_after = df.isnull().sum().sum()

print(f"   Missing values: {missing_before} → {missing_after}")

# ===========================================
# 3. FEATURE ENGINEERING
# ===========================================
print("\n✨ Feature engineering...")

# 1. Price Category
def categorize_price(price):
    if pd.isna(price):
        return 'Unknown'
    elif price < 3000000:
        return 'Budget'
    elif price < 7000000:
        return 'Mid-Range'
    elif price < 15000000:
        return 'Premium'
    else:
        return 'High-End'

df['price_category'] = df['price'].apply(categorize_price)
print("   ✓ price_category: Budget, Mid-Range, Premium, High-End")

# 2. Popularity Score
df['popularity_score'] = (
    df['sold_count'] * 0.5 + 
    df['review_count'] * 0.3 + 
    df['rating'] * 1000 * 0.2
)
print("   ✓ popularity_score: weighted score from sold, reviews, rating")

# 3. Is Bestseller
sold_threshold = df['sold_count'].quantile(0.75)
df['is_bestseller'] = (df['sold_count'] > sold_threshold).astype(int)
print(f"   ✓ is_bestseller: 1 if sold_count > {sold_threshold:.0f}")

# 4. Review to Sold Ratio (engagement)
df['review_to_sold_ratio'] = df['review_count'] / (df['sold_count'] + 1)
print("   ✓ review_to_sold_ratio: engagement metric")

# 5. High Rating Flag
df['is_high_rating'] = (df['rating'] >= 4.5).astype(int)
print("   ✓ is_high_rating: 1 if rating >= 4.5")

# 6. Price per Rating (value metric)
df['price_per_rating'] = df['price'] / (df['rating'] + 0.1)
print("   ✓ price_per_rating: value for money metric")

# 7. City Category
def categorize_city(location):
    if pd.isna(location):
        return 'Unknown'
    location = str(location).lower()
    if 'jakarta' in location:
        return 'Jakarta'
    elif 'bandung' in location:
        return 'Bandung'
    elif 'surabaya' in location:
        return 'Surabaya'
    elif 'semarang' in location:
        return 'Semarang'
    elif 'yogyakarta' in location or 'sleman' in location:
        return 'Yogyakarta'
    else:
        return 'Other'

df['city_category'] = df['seller_location'].apply(categorize_city)
print("   ✓ city_category: Jakarta, Bandung, Surabaya, Semarang, Yogyakarta, Other")

# 8. Extract brand category (major vs minor)
major_brands = ['Lenovo', 'ASUS', 'HP', 'Acer', 'Dell', 'Axioo']
df['brand_category'] = df['brand'].apply(
    lambda x: 'Major' if x in major_brands else 'Minor'
)
print("   ✓ brand_category: Major or Minor brand")

# ===========================================
# 4. DATA QUALITY CHECK
# ===========================================
print("\n📊 Data quality check...")

print(f"   Total records: {len(df)}")
print(f"   Total features: {len(df.columns)}")
print(f"\n   Numeric features:")
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
for col in numeric_cols:
    print(f"      - {col}: min={df[col].min():.2f}, max={df[col].max():.2f}, mean={df[col].mean():.2f}")

print(f"\n   Categorical features:")
cat_cols = df.select_dtypes(include=['object']).columns.tolist()
for col in cat_cols:
    unique_count = df[col].nunique()
    print(f"      - {col}: {unique_count} unique values")

# ===========================================
# 5. SAVE OUTPUT
# ===========================================
print(f"\n💾 Saving to: {output_file}")

df.to_csv(output_file, index=False, encoding='utf-8')

print(f"   ✓ File saved successfully!")
print(f"   File size: {len(df)} rows × {len(df.columns)} columns")

# ===========================================
# 6. SUMMARY STATISTICS
# ===========================================
print("\n" + "="*60)
print("SUMMARY STATISTICS")
print("="*60)

print("\n📈 Price Distribution:")
print(f"   Min:    Rp {df['price'].min():,.0f}")
print(f"   Q1:     Rp {df['price'].quantile(0.25):,.0f}")
print(f"   Median: Rp {df['price'].median():,.0f}")
print(f"   Q3:     Rp {df['price'].quantile(0.75):,.0f}")
print(f"   Max:    Rp {df['price'].max():,.0f}")
print(f"   Mean:   Rp {df['price'].mean():,.0f}")

print("\n⭐ Rating Distribution:")
print(f"   Min:    {df['rating'].min():.2f}")
print(f"   Median: {df['rating'].median():.2f}")
print(f"   Max:    {df['rating'].max():.2f}")
print(f"   Mean:   {df['rating'].mean():.2f}")

print("\n🛒 Sold Count Distribution:")
print(f"   Min:    {df['sold_count'].min():,.0f}")
print(f"   Median: {df['sold_count'].median():,.0f}")
print(f"   Max:    {df['sold_count'].max():,.0f}")
print(f"   Mean:   {df['sold_count'].mean():,.0f}")

print("\n💬 Review Count Distribution:")
print(f"   Min:    {df['review_count'].min():,.0f}")
print(f"   Median: {df['review_count'].median():,.0f}")
print(f"   Max:    {df['review_count'].max():,.0f}")
print(f"   Mean:   {df['review_count'].mean():,.0f}")

print("\n🏪 Marketplace Distribution:")
marketplace_dist = df['marketplace'].value_counts()
for marketplace, count in marketplace_dist.items():
    percentage = (count / len(df)) * 100
    print(f"   {marketplace}: {count} ({percentage:.1f}%)")

print("\n💻 Brand Distribution (Top 10):")
brand_dist = df['brand'].value_counts().head(10)
for brand, count in brand_dist.items():
    percentage = (count / len(df)) * 100
    print(f"   {brand}: {count} ({percentage:.1f}%)")

print("\n💰 Price Category Distribution:")
price_cat_dist = df['price_category'].value_counts()
for category, count in price_cat_dist.items():
    percentage = (count / len(df)) * 100
    print(f"   {category}: {count} ({percentage:.1f}%)")

print("\n🌟 Bestseller Distribution:")
bestseller_dist = df['is_bestseller'].value_counts()
print(f"   Not Bestseller (0): {bestseller_dist[0]} ({bestseller_dist[0]/len(df)*100:.1f}%)")
print(f"   Bestseller (1):     {bestseller_dist[1]} ({bestseller_dist[1]/len(df)*100:.1f}%)")

print("\n" + "="*60)
print("✅ DATA SIAP UNTUK ORANGE DATA MINING!")
print("="*60)
print(f"\n📄 Output file: {output_file}")
print("\n📚 Next Steps:")
print("   1. Buka Orange Data Mining")
print("   2. Import file CSV: laptop_dataset_for_orange.csv")
print("   3. Delimiter: Comma (,)")
print("   4. Encoding: UTF-8")
print("   5. Mulai analisis!")
print("\n💡 Baca panduan lengkap: ORANGE_DATA_MINING_GUIDE.md")
print("="*60)
