import csv
import random
from datetime import datetime, timedelta

# Daftar variasi untuk membuat data lebih beragam
marketplaces = ['Shopee', 'Tokopedia', 'Lazada', 'Blibli']
cities = [
    'Kota Jakarta Pusat', 'Kota Jakarta Utara', 'Kota Jakarta Barat', 'Kota Jakarta Timur', 'Kota Jakarta Selatan',
    'Kota Bandung', 'Kota Surabaya', 'Kota Semarang', 'Kota Yogyakarta', 'Kota Medan',
    'Kota Bekasi', 'Kota Tangerang', 'Kota Depok', 'Kota Bogor', 'Kota Makassar',
    'Kab. Tangerang', 'Kab. Sleman', 'Kab. Gresik', 'Kab. Bandung', 'Kab. Bogor'
]

seller_prefixes = [
    'Toko', 'Store', 'Shop', 'Elektronik', 'Computer', 'Laptop', 'Official',
    'Technology', 'Digital', 'Gadget', 'Mega', 'Super', 'Global', 'Central'
]

seller_suffixes = [
    'Jaya', 'Makmur', 'Sejahtera', 'Abadi', 'Sentosa', 'Mulia', 'Pratama',
    'Tech', 'Comp', 'Store', 'Center', 'Shop', 'Mall', 'Plaza'
]

# Baca data asli
input_file = 'all-data laptop.csv'
output_file = 'all-data-laptop.csv'

print("Membaca data asli...")
# Try multiple encodings
for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
    try:
        with open(input_file, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=';')
            original_data = list(reader)
        print(f"✓ Berhasil dengan encoding: {encoding}")
        break
    except UnicodeDecodeError:
        continue
else:
    raise Exception("Tidak bisa membaca file dengan encoding apapun")

print(f"Data asli: {len(original_data)} rows")

# Generate data baru
new_data = []
target_count = 4000
iterations_needed = target_count - len(original_data)

print(f"Generating {iterations_needed} data tambahan...")

for i in range(iterations_needed):
    # Pilih random data dari original sebagai template
    template = random.choice(original_data)
    
    # Buat variasi data
    new_row = {}
    
    # Marketplace: random atau tetap dari template
    new_row['marketplace'] = random.choice([template['marketplace'], random.choice(marketplaces)])
    
    # Product name: tetap dari template
    new_row['product_name'] = template['product_name']
    
    # Brand: tetap dari template
    new_row['brand'] = template['brand']
    
    # Price: variasi ±10-20%
    try:
        original_price = int(template['price'])
        price_variation = random.uniform(0.8, 1.2)
        new_price = int(original_price * price_variation)
        # Bulatkan ke ribuan terdekat
        new_price = round(new_price / 1000) * 1000
        new_row['price'] = str(new_price)
    except:
        new_row['price'] = template['price']
    
    # Rating: variasi sedikit (4.0 - 5.0)
    try:
        original_rating = float(template['rating'].replace(',', '.'))
        new_rating = round(random.uniform(max(4.0, original_rating - 0.3), min(5.0, original_rating + 0.3)), 1)
        new_row['rating'] = str(new_rating).replace('.', ',')
    except:
        new_row['rating'] = template['rating']
    
    # Review count: variasi ±30%
    try:
        original_reviews = int(template['review_count'])
        reviews_variation = random.uniform(0.7, 1.3)
        new_reviews = max(1, int(original_reviews * reviews_variation))
        new_row['review_count'] = str(new_reviews)
    except:
        new_row['review_count'] = template['review_count']
    
    # Sold count: variasi ±40%
    try:
        original_sold = int(template['sold_count'])
        sold_variation = random.uniform(0.6, 1.4)
        new_sold = max(1, int(original_sold * sold_variation))
        new_row['sold_count'] = str(new_sold)
    except:
        new_row['sold_count'] = template['sold_count']
    
    # Seller name: generate random atau ambil dari template
    if random.random() > 0.5:
        seller_name = f"{random.choice(seller_prefixes)} {random.choice(seller_suffixes)}"
        new_row['seller_name'] = seller_name
    else:
        new_row['seller_name'] = template['seller_name']
    
    # Seller location: random dari daftar kota
    new_row['seller_location'] = random.choice(cities)
    
    # Product URL: tetap dari template (atau bisa di-modify)
    new_row['product_url'] = template['product_url']
    
    # Scraped date: variasi tanggal (1-60 hari yang lalu dari sekarang)
    days_ago = random.randint(1, 60)
    scraped_date = datetime.now() - timedelta(days=days_ago)
    new_row['scraped_date'] = scraped_date.strftime('%d/%m/%Y')
    
    new_data.append(new_row)
    
    # Progress indicator
    if (i + 1) % 100 == 0:
        print(f"Progress: {i + 1}/{iterations_needed} generated...")

# Gabungkan data asli dengan data baru
all_data = original_data + new_data

print(f"\nTotal data: {len(all_data)} rows")

# Tulis ke file baru
print(f"Menulis ke {output_file}...")
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['marketplace', 'product_name', 'brand', 'price', 'rating', 
                  'review_count', 'sold_count', 'seller_name', 'seller_location', 
                  'product_url', 'scraped_date']
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    
    writer.writeheader()
    writer.writerows(all_data)

print(f"✅ Selesai! File {output_file} berisi {len(all_data)} data laptop")
print(f"   - Data asli: {len(original_data)}")
print(f"   - Data generated: {len(new_data)}")
