# app.py - Aplikasi utama Analytix Backend
# Jalankan dengan: python app.py
# API tersedia di: http://localhost:5000

from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import blueprint routes
from routes.products import products_bp
from routes.analysis import analysis_bp
from routes.prediction import prediction_bp

app = Flask(__name__)
CORS(app)  # Izinkan cross-origin requests dari frontend

# Daftarkan blueprint
app.register_blueprint(products_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(prediction_bp)


@app.route('/')
def index():
    return jsonify({
        'nama'       : 'Analytix API',
        'versi'      : '1.0.0',
        'deskripsi'  : 'API backend untuk platform Big Data Analytics Analytix',
        'endpoints'  : [
            'GET  /api/products',
            'GET  /api/products/<id>',
            'GET  /api/analysis/summary',
            'GET  /api/analysis/marketplace',
            'GET  /api/analysis/brands',
            'GET  /api/analysis/price-distribution',
            'GET  /api/analysis/ram-distribution',
            'GET  /api/analysis/charts',
            'POST /api/predict'
        ]
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint tidak ditemukan'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Terjadi kesalahan server internal'}), 500


if __name__ == '__main__':
    from config import FLASK_HOST, FLASK_PORT, DEBUG
    print(f'Analytix API berjalan di http://{FLASK_HOST}:{FLASK_PORT}')
    print('Mode: Data Demo (CSV) - Koneksi MySQL belum aktif')
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG)
