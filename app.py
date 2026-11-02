import os
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this!

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Simple user class (in production, use database)
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# Admin credentials (in production, store in database)
# Default: username='admin', password='admin123'
ADMIN_USER = User(
    id=1,
    username='admin',
    password_hash=generate_password_hash('admin123')
)

@login_manager.user_loader
def load_user(user_id):
    if int(user_id) == ADMIN_USER.id:
        return ADMIN_USER
    return None

# Global cache for the current dataset
current_dataframe = None
dataset_metadata = {}

# Default laptop products (hardcoded for Vercel deployment with VALID product links)
DEFAULT_LAPTOP_PRODUCTS = [
    {"marketplace": "Tokopedia", "product_name": "Laptop HP OmniBook X Flip Intel Core Ultra 5 16GB RAM 512GB SSD Touchscreen", "brand": "HP", "price": 20090500, "rating": 4.7, "review_count": 0, "sold_count": 50, "seller_name": "HP Indonesia", "seller_location": "Jakarta Utara", "product_url": "https://www.tokopedia.com/hp/laptop-hp-envy-x360-intel-core-ultra-5-16gb-ram-512gb-ssd-w11-home-1735479136959498115"},
    {"marketplace": "Tokopedia", "product_name": "LENOVO IdeaPad Slim 3 14IRH8 i7-13620H 16GB 512SSD 14 FHD W11+OHS", "brand": "Lenovo", "price": 18999000, "rating": 5.0, "review_count": 0, "sold_count": 100, "seller_name": "Lenovo Yoga Official", "seller_location": "Jakarta Utara", "product_url": "https://www.tokopedia.com/lenovoyogaofficial/lenovo-ideapad-slim-3-14irh8-i7-13620h-16gb-512ssd-14-fhd-w11-ohs-1730843897075959147"},
    {"marketplace": "Tokopedia", "product_name": "Acer Swift Go 14 AI 100% sRGB Ultra 5-125H 16GB 512GB SSD", "brand": "Acer", "price": 16579999, "rating": 5.0, "review_count": 0, "sold_count": 40, "seller_name": "Acer Official Store", "seller_location": "Jakarta Pusat", "product_url": "https://www.tokopedia.com/acerid/gajian-sale-acer-swift-go-14-ai-100-srgb-ultra-5-125h-with-ai-boost-16gb-512gb-ssd-intel-arc-graphics-14-2k-ips-100-srgb-w11-ohs21-pure-silver-sfg-73-5135-nx-kv4sn-005-1731239366357451797-1737641156311548949"},
    {"marketplace": "Tokopedia", "product_name": "Mac Book Air M2 & M3 13-15 inch RAM 8GB/16GB/24GB SSD 256GB/512GB", "brand": "Apple", "price": 14575000, "rating": 4.9, "review_count": 0, "sold_count": 40, "seller_name": "Hobi Mac", "seller_location": "Kab. Sleman", "product_url": "https://www.tokopedia.com/hobimac/macbook-air-m2-ram-8-16-gb-ssd-256-512-gb-1731368418575026028-1737303077756438384"},
    {"marketplace": "Tokopedia", "product_name": "HP Laptop AI Ultra 5 225U 512GB SSD 8GB FHD Win11+OHS", "brand": "HP", "price": 13999000, "rating": 4.9, "review_count": 0, "sold_count": 100, "seller_name": "Sinarmulia Sukses Makmur", "seller_location": "Jakarta Barat", "product_url": "https://www.tokopedia.com/sinarmulia/laptop-hp-pavilion-aero-13-be2001au-2002au-ryzen-5-7535u-512gb-ssd-16g-1730834997541307562"},
    {"marketplace": "Tokopedia", "product_name": "ACER Swift Lite 14 AI AMD Ryzen 7 260 16/512GB SSD Windows 11", "brand": "Acer", "price": 13489000, "rating": 5.0, "review_count": 0, "sold_count": 20, "seller_name": "Acer Authorized Store", "seller_location": "Jakarta Utara", "product_url": "https://www.tokopedia.com/acer-jakarta/promo-co-funded-acer-swift-lite-14-ai-sfl14-41m-r0gs-air-edition-amd-ryzen-7-260-16-512gb-ssd-windows-11-ohs-m365b-14-inch-wuxga-ips-light-silver-1737045575798719636-1737045971709101204"},
    {"marketplace": "Tokopedia", "product_name": "ASUS Vivobook Go E1404FA-Ryzen 5 7520U 16GB-512GB-14inch-WIN11+OHS", "brand": "ASUS", "price": 11799000, "rating": 4.9, "review_count": 0, "sold_count": 100, "seller_name": "ASUS ROG Indonesia", "seller_location": "Jakarta Utara", "product_url": "https://www.tokopedia.com/asusrogindonesia/asus-vivobook-go-e1404fa-ryzen-5-7520u-amd-radeon-graphics-16gb-512gb-14inch-win11-ohs-m365-1731040641983612554"},
    {"marketplace": "Tokopedia", "product_name": "ASUS VivoBook S16 FLIP OLED TOUCH i5-1335U 8GB/16GB 512GB W11", "brand": "ASUS", "price": 11780010, "rating": 4.9, "review_count": 0, "sold_count": 70, "seller_name": "Deca Computer", "seller_location": "Jakarta Utara", "product_url": "https://www.tokopedia.com/decacom/asus-vivobook-s16-flip-oled-touch-i5-1335u-8gb-16gb-512gb-w11-16-0fhd-ips-tp3604va-1731133924531931103"},
    {"marketplace": "Blibli", "product_name": "HP 14-ep1155TU Laptop Silver Core 5-120U 16GB 512GB Win11+OHS24+M365", "brand": "HP", "price": 11499000, "rating": 5.0, "review_count": 14, "sold_count": 760, "seller_name": "Blibli Flagship Store", "seller_location": "Kota Bekasi", "product_url": "https://www.blibli.com/p/hp-14-ep1155tu-laptop-silver-core-5-120u-16gb-512gb-win11-ohs24-m365-copilot-backlit-kb-14-fhd-250nits-free-bag/ps--BLG-60035-03508"},
    {"marketplace": "Blibli", "product_name": "Lenovo IdeaPad Slim 3 14IRH10 Notebook Arctic Grey Intel Core i5-13420H 8GB 512GB SSD", "brand": "Lenovo", "price": 10999000, "rating": 4.6, "review_count": 19, "sold_count": 1180, "seller_name": "Blibli Flagship Store", "seller_location": "Kota Bekasi", "product_url": "https://www.blibli.com/p/lenovo-ideapad-slim-3-14irh10-83k000cvid-notebook-artic-grey-intel-core-i5-13420h-8gb-512gb-ssd-14-ips-win11-ohs2024-m365-bag/ps--BLL-60036-04038"},
    {"marketplace": "Tokopedia", "product_name": "LENOVO IDEAPAD SLIM 3 14 I5 13420H 16GB 512GB W11+OHS 14.0 WUXGA IPS", "brand": "Lenovo", "price": 10999000, "rating": 5.0, "review_count": 0, "sold_count": 1, "seller_name": "AGRES ID", "seller_location": "Jakarta Utara", "product_url": "https://www.tokopedia.com/agresid/sp-lenovo-ideapad-slim-3-14-i5-13420h-16gb-512gb-w11-ohs-14-0wuxga-ips-1732187126727803971-1737214770502403139"},
    {"marketplace": "Tokopedia", "product_name": "ASUS Vivobook Go 14 E1404FA-Ryzen 5 7520U 8GB-512GB-14inch-WIN11+OHS", "brand": "ASUS", "price": 10599000, "rating": 5.0, "review_count": 0, "sold_count": 21, "seller_name": "ASUS ROG Indonesia", "seller_location": "Jakarta Utara", "product_url": "https://www.tokopedia.com/asusrogindonesia/asus-vivobook-go-14-e1404fa-ryzen-5-7520u-radeon-graphics-8gb-512gb-14inch-win11-ohs-1731040347406042762"},
    {"marketplace": "Blibli", "product_name": "HP 14-ep0261TU Laptop Silver i3-1315U 8GB 512GB Win11+OHS24+M365", "brand": "HP", "price": 8999000, "rating": 4.8, "review_count": 29, "sold_count": 3300, "seller_name": "Blibli Flagship Store", "seller_location": "Kota Semarang", "product_url": "https://www.blibli.com/p/hp-14-ep0261tu-laptop-silver-i3-1315u-8gb-512gb-win11-ohs24-m365-copilot-backlit-kb-14-fhd-250nits-free-bag/ps--BLG-60035-03504"},
    {"marketplace": "Blibli", "product_name": "Axioo Mybook Hype 5 G12 Notebook Black i5-1235U 16GB 512GB SSD", "brand": "Axioo", "price": 8999000, "rating": 5.0, "review_count": 25, "sold_count": 1220, "seller_name": "Blibli Laptop Store", "seller_location": "Kota Jakarta Timur", "product_url": "https://www.blibli.com/p/axioo-mybook-hype-5-g12-notebook-black-i5-1235u-16gb-512gb-ssd-uma-14-fhd-ips-dos/ps--BLL-70058-00805"},
    {"marketplace": "Tokopedia", "product_name": "ACER Aspire Go AG14-72P-38GD Laptop Silver i3-1315U 8GB 512GB Win11 OHS24", "brand": "ACER", "price": 8699000, "rating": 5.0, "review_count": 9, "sold_count": 690, "seller_name": "Blibli Flagship Store", "seller_location": "Kab. Sleman", "product_url": "https://www.tokopedia.com/acer/aspire-go-ag14-72p-38gd"},
    {"marketplace": "Tokopedia", "product_name": "ASUS Vivobook Go 14 E1404FA AMD Ryzen 3 7320U 8GB 512GB 14inch WIN11", "brand": "ASUS", "price": 8599000, "rating": 5.0, "review_count": 0, "sold_count": 250, "seller_name": "AGRES ID BOGOR", "seller_location": "Bogor", "product_url": "https://www.tokopedia.com/agresidbogor/laptop-asus-vivobook-go-14-e1404fa-amd-ryzen-3-7320u-ram-8gb-512gb-ssd-14-0-full-hd-1730811700220560815"},
    {"marketplace": "Tokopedia", "product_name": "ADVAN Workplus Heritage Ryzen 5 7535HS 16GB/1TB 14 IPS FHD Windows 11", "brand": "Advan", "price": 8599000, "rating": 4.9, "review_count": 0, "sold_count": 500, "seller_name": "ADVAN INDONESIA", "seller_location": "Kab. Tangerang", "product_url": "https://www.tokopedia.com/advanstore/advan-workplus-heritage-ryzen-5-7535hs-16gb-1tb-14-ips-fhd-wuxga-1920-x-1200-16-10-lightweigth-free-windows-11-garansi-resmi-2-tahun-laptop-notebook-desain-eksklusif-batik-megamendung-1731520651113432935-1737317949335701351"},
    {"marketplace": "Blibli", "product_name": "Axioo Mybook Hype 1 Notebook Grey N4020 4GB 128GB SSD 14.1 HD Win11", "brand": "Axioo", "price": 3899000, "rating": 4.9, "review_count": 264, "sold_count": 15640, "seller_name": "Blibli Laptop Store", "seller_location": "Kota Bandung", "product_url": "https://www.blibli.com/p/axioo-mybook-hype-1-notebook-grey-n4020-4gb-128gb-ssd-uma-14-1-hd-win11/ps--BLL-70058-00789"},
    {"marketplace": "Lazada", "product_name": "Lenovo ThinkPad T460 T460S L460 E460 Core I5 I7 Generation 6 Laptop", "brand": "Lenovo", "price": 2300000, "rating": 4.8, "review_count": 213, "sold_count": 385, "seller_name": "Unlimited Laptop", "seller_location": "Kota Jakarta Utara", "product_url": "https://www.lazada.co.id/products/pdp-i7925850831.html"},
    {"marketplace": "Lazada", "product_name": "Lenovo Laptop Core I7 I5 I3 Ram 8 GB Ssd 256 GB Infinity Technology", "brand": "Lenovo", "price": 1525000, "rating": 4.8, "review_count": 674, "sold_count": 1300, "seller_name": "Infinity Technology", "seller_location": "Kota Jakarta Pusat", "product_url": "https://www.lazada.co.id/products/pdp-i5560826335.html"},
]

def parse_price(price_str):
    """Convert price string to numeric value."""
    if pd.isna(price_str):
        return 0
    if isinstance(price_str, (int, float)):
        return float(price_str)
    
    # Remove 'Rp', dots, commas, and spaces
    price_cleaned = str(price_str).replace('Rp', '').replace('.', '').replace(',', '').replace(' ', '').strip()
    try:
        return float(price_cleaned)
    except ValueError:
        return 0

def normalize_column_names(df):
    """Normalize column names to lowercase and handle variants."""
    column_mapping = {}
    for col in df.columns:
        col_lower = col.lower().strip().replace(' ', '_')
        column_mapping[col] = col_lower
    return df.rename(columns=column_mapping)

def process_csv(file_path, filename):
    """Process uploaded CSV file and cache it."""
    global current_dataframe, dataset_metadata
    
    # Read CSV with encoding detection and better error handling
    try:
        # Try UTF-8 first
        df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
    except UnicodeDecodeError:
        try:
            # Try latin-1 if UTF-8 fails
            df = pd.read_csv(file_path, encoding='latin-1', on_bad_lines='skip')
        except Exception as e:
            # Try ISO-8859-1 as fallback
            try:
                df = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip')
            except Exception as e:
                raise Exception(f"Failed to read CSV: {str(e)}")
    except Exception as e:
        raise Exception(f"Error parsing CSV: {str(e)}")
    
    # Check if dataframe is empty
    if df.empty:
        raise Exception("CSV file is empty or could not be parsed")
    
    # Normalize column names
    df = normalize_column_names(df)
    
    # Convert price to numeric
    if 'price' in df.columns:
        df['price'] = df['price'].apply(parse_price)
    
    # Handle missing data
    if 'rating' in df.columns:
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)
    if 'review_count' in df.columns:
        df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce').fillna(0)
    if 'sold_count' in df.columns:
        df['sold_count'] = pd.to_numeric(df['sold_count'], errors='coerce').fillna(0)
    
    # Remove exact duplicates by product_name and marketplace
    if 'product_name' in df.columns and 'marketplace' in df.columns:
        df = df.drop_duplicates(subset=['product_name', 'marketplace'], keep='first')
    
    # Cache the dataframe
    current_dataframe = df
    
    # Calculate statistics
    stats = {
        'filename': filename,
        'total_products': len(df),
        'unique_marketplaces': df['marketplace'].nunique() if 'marketplace' in df.columns else 0,
        'unique_brands': df['brand'].nunique() if 'brand' in df.columns else 0,
        'marketplaces': df['marketplace'].unique().tolist() if 'marketplace' in df.columns else [],
        'brands': sorted(df['brand'].unique().tolist()) if 'brand' in df.columns else [],
        'upload_timestamp': datetime.now().isoformat(),
        'price_min': float(df['price'].min()) if 'price' in df.columns else 0,
        'price_max': float(df['price'].max()) if 'price' in df.columns else 0,
        'price_avg': float(df['price'].mean()) if 'price' in df.columns else 0,
        'rating_min': float(df['rating'].min()) if 'rating' in df.columns else 0,
        'rating_max': float(df['rating'].max()) if 'rating' in df.columns else 0,
        'rating_avg': float(df['rating'].mean()) if 'rating' in df.columns else 0,
    }
    
    dataset_metadata = stats
    return stats

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    """Handle CSV file upload."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400
        
        # Save file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join('data', filename)
        file.save(file_path)
        
        # Process the CSV
        stats = process_csv(file_path, file.filename)
        
        return jsonify(stats)
    
    except Exception as e:
        # Log error and return user-friendly message
        print(f"Upload error: {str(e)}")
        return jsonify({'error': f'Error processing CSV: {str(e)}'}), 500

@app.route('/api/products')
def get_products():
    """Get filtered and sorted products."""
    global current_dataframe
    
    if current_dataframe is None:
        return jsonify([])
    
    df = current_dataframe.copy()
    
    # Apply filters
    search = request.args.get('search', '').strip()
    if search and 'product_name' in df.columns:
        df = df[df['product_name'].str.contains(search, case=False, na=False)]
    
    marketplace = request.args.get('marketplace', '').strip()
    if marketplace and 'marketplace' in df.columns:
        df = df[df['marketplace'] == marketplace]
    
    brand = request.args.get('brand', '').strip()
    if brand and 'brand' in df.columns:
        df = df[df['brand'] == brand]
    
    price_min = request.args.get('price_min', '').strip()
    if price_min and 'price' in df.columns:
        try:
            df = df[df['price'] >= float(price_min)]
        except ValueError:
            pass
    
    price_max = request.args.get('price_max', '').strip()
    if price_max and 'price' in df.columns:
        try:
            df = df[df['price'] <= float(price_max)]
        except ValueError:
            pass
    
    # Apply sorting
    sort = request.args.get('sort', '').strip()
    if sort == 'price_asc' and 'price' in df.columns:
        df = df.sort_values('price', ascending=True)
    elif sort == 'price_desc' and 'price' in df.columns:
        df = df.sort_values('price', ascending=False)
    elif sort == 'rating_desc' and 'rating' in df.columns:
        df = df.sort_values('rating', ascending=False)
    
    # Convert to dict
    products = df.to_dict('records')
    
    return jsonify(products)

@app.route('/api/stats')
def get_stats():
    """Get dataset statistics."""
    return jsonify(dataset_metadata)

@app.route('/api/analytics')
def get_analytics():
    """Get analytics data for charts."""
    global current_dataframe
    
    if current_dataframe is None:
        return jsonify({})
    
    df = current_dataframe
    
    analytics = {}
    
    # Products by marketplace
    if 'marketplace' in df.columns:
        products_by_marketplace = df['marketplace'].value_counts().to_dict()
        analytics['products_by_marketplace'] = products_by_marketplace
    
    # Products by brand (top 10)
    if 'brand' in df.columns:
        products_by_brand = df['brand'].value_counts().head(10).to_dict()
        analytics['products_by_brand'] = products_by_brand
    
    # Price distribution (5 buckets)
    if 'price' in df.columns:
        price_min = df['price'].min()
        price_max = df['price'].max()
        bins = 5
        step = (price_max - price_min) / bins
        ranges = []
        price_distribution = {}
        
        for i in range(bins):
            range_min = price_min + (i * step)
            range_max = price_min + ((i + 1) * step)
            range_label = f"Rp {int(range_min/1000)}k - {int(range_max/1000)}k"
            count = len(df[(df['price'] >= range_min) & (df['price'] < range_max)])
            price_distribution[range_label] = count
        
        analytics['price_distribution'] = price_distribution
    
    # Average price by marketplace
    if 'marketplace' in df.columns and 'price' in df.columns:
        avg_price_by_marketplace = df.groupby('marketplace')['price'].mean().to_dict()
        analytics['avg_price_by_marketplace'] = avg_price_by_marketplace
    
    # Average rating by marketplace
    if 'marketplace' in df.columns and 'rating' in df.columns:
        avg_rating_by_marketplace = df.groupby('marketplace')['rating'].mean().to_dict()
        analytics['avg_rating_by_marketplace'] = avg_rating_by_marketplace
    
    return jsonify(analytics)

@app.route('/download/full')
def download_full():
    """Download full dataset as CSV."""
    global current_dataframe
    
    if current_dataframe is None:
        return jsonify({'error': 'No dataset loaded'}), 404
    
    # Convert to CSV
    output = BytesIO()
    current_dataframe.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"analytix_full_{timestamp}.csv"
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@app.route('/download/filtered')
def download_filtered():
    """Download filtered dataset as CSV."""
    global current_dataframe
    
    if current_dataframe is None:
        return jsonify({'error': 'No dataset loaded'}), 404
    
    df = current_dataframe.copy()
    
    # Apply same filters as /api/products
    search = request.args.get('search', '').strip()
    if search and 'product_name' in df.columns:
        df = df[df['product_name'].str.contains(search, case=False, na=False)]
    
    marketplace = request.args.get('marketplace', '').strip()
    if marketplace and 'marketplace' in df.columns:
        df = df[df['marketplace'] == marketplace]
    
    brand = request.args.get('brand', '').strip()
    if brand and 'brand' in df.columns:
        df = df[df['brand'] == brand]
    
    price_min = request.args.get('price_min', '').strip()
    if price_min and 'price' in df.columns:
        try:
            df = df[df['price'] >= float(price_min)]
        except ValueError:
            pass
    
    price_max = request.args.get('price_max', '').strip()
    if price_max and 'price' in df.columns:
        try:
            df = df[df['price'] <= float(price_max)]
        except ValueError:
            pass
    
    # Convert to CSV
    output = BytesIO()
    df.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"analytix_filtered_{timestamp}.csv"
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

# ============= ADMIN ROUTES =============

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USER.username and check_password_hash(ADMIN_USER.password_hash, password):
            login_user(ADMIN_USER)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout."""
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard."""
    global dataset_metadata, current_dataframe
    
    stats = {
        'total_products': len(current_dataframe) if current_dataframe is not None else 0,
        'filename': dataset_metadata.get('filename', 'No dataset loaded'),
        'upload_timestamp': dataset_metadata.get('upload_timestamp', 'N/A'),
        'unique_marketplaces': dataset_metadata.get('unique_marketplaces', 0),
        'unique_brands': dataset_metadata.get('unique_brands', 0),
    }
    
    return render_template('admin_dashboard.html', stats=stats)

@app.route('/admin/products')
@login_required
def admin_products():
    """Admin product management page."""
    global current_dataframe
    
    if current_dataframe is None:
        flash('No dataset loaded', 'warning')
        return redirect(url_for('admin_dashboard'))
    
    # Get all products as list of dictionaries
    products = current_dataframe.to_dict('records')
    
    return render_template('admin_products.html', products=products)

@app.route('/admin/product/edit/<int:index>', methods=['GET', 'POST'])
@login_required
def admin_edit_product(index):
    """Edit a product."""
    global current_dataframe
    
    if current_dataframe is None:
        flash('No dataset loaded', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if index < 0 or index >= len(current_dataframe):
        flash('Product not found', 'error')
        return redirect(url_for('admin_products'))
    
    if request.method == 'POST':
        # Update product data
        try:
            for col in current_dataframe.columns:
                if col in request.form:
                    value = request.form[col]
                    # Handle numeric conversion
                    if col == 'price':
                        current_dataframe.at[index, col] = float(value) if value else 0
                    elif col in ['rating', 'review_count', 'sold_count']:
                        current_dataframe.at[index, col] = float(value) if value else 0
                    else:
                        current_dataframe.at[index, col] = value
            
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin_products'))
        except Exception as e:
            flash(f'Error updating product: {str(e)}', 'error')
    
    # Get product data
    product = current_dataframe.iloc[index].to_dict()
    product['index'] = index
    
    return render_template('admin_edit_product.html', product=product)

@app.route('/admin/product/delete/<int:index>', methods=['POST'])
@login_required
def admin_delete_product(index):
    """Delete a product."""
    global current_dataframe, dataset_metadata
    
    if current_dataframe is None:
        return jsonify({'error': 'No dataset loaded'}), 400
    
    if index < 0 or index >= len(current_dataframe):
        return jsonify({'error': 'Product not found'}), 404
    
    try:
        # Drop the product
        current_dataframe = current_dataframe.drop(index).reset_index(drop=True)
        
        # Update metadata
        dataset_metadata['total_products'] = len(current_dataframe)
        
        flash('Product deleted successfully!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    """Add a new product."""
    global current_dataframe, dataset_metadata
    
    if current_dataframe is None:
        flash('No dataset loaded. Please upload a CSV first.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        try:
            # Create new product row
            new_product = {}
            for col in current_dataframe.columns:
                if col in request.form:
                    value = request.form[col]
                    # Handle numeric conversion
                    if col == 'price':
                        new_product[col] = float(value) if value else 0
                    elif col in ['rating', 'review_count', 'sold_count']:
                        new_product[col] = float(value) if value else 0
                    else:
                        new_product[col] = value
                else:
                    new_product[col] = ''
            
            # Add to dataframe
            current_dataframe = pd.concat([current_dataframe, pd.DataFrame([new_product])], ignore_index=True)
            
            # Update metadata
            dataset_metadata['total_products'] = len(current_dataframe)
            dataset_metadata['unique_brands'] = current_dataframe['brand'].nunique() if 'brand' in current_dataframe.columns else 0
            dataset_metadata['unique_marketplaces'] = current_dataframe['marketplace'].nunique() if 'marketplace' in current_dataframe.columns else 0
            
            flash('Product added successfully!', 'success')
            return redirect(url_for('admin_products'))
        except Exception as e:
            flash(f'Error adding product: {str(e)}', 'error')
    
    # Get column names for form
    columns = current_dataframe.columns.tolist()
    
    return render_template('admin_add_product.html', columns=columns)

@app.route('/admin/upload', methods=['POST'])
@login_required
def admin_upload_csv():
    """Admin CSV upload (replaces current dataset)."""
    try:
        if 'file' not in request.files:
            flash('No file provided', 'error')
            return redirect(url_for('admin_dashboard'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('admin_dashboard'))
        
        if not file.filename.endswith('.csv'):
            flash('File must be a CSV', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Save file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join('data', filename)
        file.save(file_path)
        
        # Process the CSV
        stats = process_csv(file_path, file.filename)
        
        flash(f'CSV uploaded successfully! {stats["total_products"]} products loaded. Redirecting to homepage...', 'success')
        
        # Redirect to homepage to show products
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Error uploading CSV: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/export', methods=['GET'])
@login_required
def admin_export_csv():
    """Export full dataset as CSV (all 500+ products from original file)."""
    
    # Try to export from uploaded CSV files first
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and f != 'data_laptop.csv']
    
    # Sort by modification time, get the latest
    if csv_files:
        csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), reverse=True)
        latest_csv = os.path.join(data_dir, csv_files[0])
    else:
        # Fallback to full_dataset_laptop.csv if exists
        latest_csv = os.path.join(data_dir, 'full_dataset_laptop.csv')
    
    try:
        if os.path.exists(latest_csv):
            # Read and export the full CSV file
            df_full = pd.read_csv(latest_csv, encoding='utf-8', on_bad_lines='skip', sep=';')
            
            output = BytesIO()
            df_full.to_csv(output, index=False, encoding='utf-8', sep=';')
            output.seek(0)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'analytix_full_export_{timestamp}.csv'
            
            return send_file(
                output,
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
        else:
            # Fallback to current dataframe (20 products)
            global current_dataframe
            if current_dataframe is None:
                flash('No dataset to export', 'error')
                return redirect(url_for('admin_dashboard'))
            
            output = BytesIO()
            current_dataframe.to_csv(output, index=False, encoding='utf-8')
            output.seek(0)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'analytix_export_{timestamp}.csv'
            
            return send_file(
                output,
                mimetype='text/csv',
                as_attachment=True,
                download_name=filename
            )
    except Exception as e:
        flash(f'Error exporting CSV: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))

# Auto-load sample dataset on app initialization
def init_default_data():
    """Load default dataset if available."""
    global current_dataframe, dataset_metadata
    
    # First try to load from CSV file
    sample_path = os.path.join('data', 'data_laptop.csv')
    if os.path.exists(sample_path):
        try:
            process_csv(sample_path, 'data_laptop.csv')
            print(f"✅ Dataset loaded from CSV: {dataset_metadata.get('total_products', 0)} products")
            return
        except Exception as e:
            print(f"⚠️ Error loading CSV: {str(e)}, using hardcoded defaults")
    
    # Fallback to hardcoded default products
    try:
        df = pd.DataFrame(DEFAULT_LAPTOP_PRODUCTS)
        current_dataframe = df
        
        # Calculate statistics
        dataset_metadata = {
            'filename': 'default_laptops.json',
            'total_products': len(df),
            'unique_marketplaces': df['marketplace'].nunique(),
            'unique_brands': df['brand'].nunique(),
            'marketplaces': df['marketplace'].unique().tolist(),
            'brands': sorted(df['brand'].unique().tolist()),
            'upload_timestamp': datetime.now().isoformat(),
            'price_min': float(df['price'].min()),
            'price_max': float(df['price'].max()),
            'price_avg': float(df['price'].mean()),
            'rating_min': float(df['rating'].min()),
            'rating_max': float(df['rating'].max()),
            'rating_avg': float(df['rating'].mean()),
        }
        print(f"✅ Default dataset loaded: {len(df)} products from {df['marketplace'].nunique()} marketplaces")
    except Exception as e:
        print(f"❌ Error loading default data: {str(e)}")

# Initialize data on import (works in both local and Vercel)
init_default_data()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
