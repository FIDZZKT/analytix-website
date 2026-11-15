import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurasi database MySQL
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'laptop_bigdata'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Path dataset demo
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'laptops_demo.csv')

# Konfigurasi Flask
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

# Marketplace yang didukung
SUPPORTED_MARKETPLACES = ['Shopee', 'Tokopedia', 'Lazada', 'Blibli']
