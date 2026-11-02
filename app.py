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
    """Export current dataset as CSV."""
    global current_dataframe
    
    if current_dataframe is None:
        flash('No dataset to export', 'error')
        return redirect(url_for('admin_dashboard'))
    
    try:
        # Create CSV in memory
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

if __name__ == '__main__':
    # Auto-load sample dataset if it exists
    sample_path = os.path.join('data', 'data_laptop.csv')
    if os.path.exists(sample_path):
        try:
            process_csv(sample_path, 'data_laptop.csv')
            print(f"✅ Dataset loaded: {dataset_metadata.get('total_products', 0)} products from {dataset_metadata.get('unique_marketplaces', 0)} marketplaces")
        except Exception as e:
            print(f"❌ Error loading dataset: {str(e)}")
            # Fallback to old sample if exists
            old_sample = os.path.join('data', 'sample_laptops.csv')
            if os.path.exists(old_sample):
                process_csv(old_sample, 'sample_laptops.csv')
                print(f"✅ Fallback sample loaded: {dataset_metadata.get('total_products', 0)} products")
    
    app.run(debug=True, port=5000)
