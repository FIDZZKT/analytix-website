import os
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Global cache for the current dataset
current_dataframe = None
dataset_metadata = {}

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
    
    # Read CSV with encoding detection
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin-1')
    
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

if __name__ == '__main__':
    # Auto-load sample dataset if it exists
    sample_path = os.path.join('data', 'sample_laptops.csv')
    if os.path.exists(sample_path):
        process_csv(sample_path, 'sample_laptops.csv')
        print(f"Sample dataset loaded: {dataset_metadata.get('total_products', 0)} products")
    
    app.run(debug=True, port=5000)
