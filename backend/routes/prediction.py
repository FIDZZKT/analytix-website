"""
prediction.py - Blueprint untuk endpoint prediksi harga laptop
Endpoint: POST /api/predict
Menggunakan simulasi berbasis data demo (bukan model ML nyata)
"""

import pandas as pd
from flask import Blueprint, jsonify, request
from models.database import get_products

prediction_bp = Blueprint('prediction_bp', __name__)

# Pesan disclaimer yang ditampilkan pada setiap respons prediksi
DISCLAIMER = (
    "Simulasi berdasarkan data demo. Hasil prediksi bukan berasal dari model "
    "Machine Learning terlatih dan hanya mencerminkan rata-rata harga produk "
    "dengan spesifikasi serupa dalam dataset."
)


@prediction_bp.route('/api/predict', methods=['POST'])
def predict_price():
    """
    Memprediksi estimasi harga laptop berdasarkan spesifikasi yang diberikan.

    Body JSON:
      brand          - brand laptop (opsional)
      processor_type - jenis processor: Intel | AMD (opsional)
      ram_gb         - kapasitas RAM dalam GB (opsional)
      storage_gb     - kapasitas storage dalam GB (opsional)
      gpu_type       - jenis GPU: Dedicated | Integrated (opsional)

    Respons:
      estimated_price - estimasi harga rata-rata (IDR)
      price_range     - rentang harga {min, max}
      match_count     - jumlah produk yang cocok
      confidence      - tingkat kepercayaan: high | medium | low
      disclaimer      - pesan bahwa ini adalah simulasi
    """
    try:
        body = request.get_json(silent=True) or {}

        # Ambil parameter dari body request
        brand          = str(body.get('brand', '')).strip().lower()
        processor_type = str(body.get('processor_type', '')).strip().lower()
        ram_gb         = body.get('ram_gb')
        storage_gb     = body.get('storage_gb')
        gpu_type       = str(body.get('gpu_type', '')).strip().lower()

        # Muat semua produk ke DataFrame
        products = get_products()
        if not products:
            return jsonify({'error': 'Dataset tidak tersedia untuk prediksi'}), 500

        df = pd.DataFrame(products)
        for col in ['price_idr', 'ram_gb', 'storage_gb']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        filtered = df.copy()

        # Terapkan filter sesuai spesifikasi yang diberikan
        if brand:
            filtered = filtered[
                filtered['brand'].str.lower().str.strip() == brand
            ]
        if processor_type:
            filtered = filtered[
                filtered['processor_type'].str.lower().str.strip() == processor_type
            ]
        if ram_gb is not None:
            try:
                filtered = filtered[filtered['ram_gb'] == int(ram_gb)]
            except (ValueError, TypeError):
                pass
        if storage_gb is not None:
            try:
                filtered = filtered[filtered['storage_gb'] == int(storage_gb)]
            except (ValueError, TypeError):
                pass
        if gpu_type:
            filtered = filtered[
                filtered['gpu_type'].str.lower().str.strip() == gpu_type
            ]

        # Hilangkan baris tanpa harga
        valid = filtered.dropna(subset=['price_idr'])

        # Tentukan estimasi berdasarkan jumlah kecocokan
        match_count = len(valid)

        if match_count > 0:
            avg_price = float(valid['price_idr'].mean())
            confidence = (
                'high'   if match_count >= 10
                else 'medium' if match_count >= 3
                else 'low'
            )
        else:
            # Tidak ada kecocokan — gunakan rata-rata keseluruhan sebagai fallback
            overall = df.dropna(subset=['price_idr'])
            avg_price  = float(overall['price_idr'].mean()) if not overall.empty else 0
            confidence = 'low'

        # Rentang harga estimasi ±15%
        price_min = round(avg_price * 0.85, 0)
        price_max = round(avg_price * 1.15, 0)

        return jsonify({
            'estimated_price': round(avg_price, 0),
            'price_range'    : {
                'min': price_min,
                'max': price_max
            },
            'match_count'    : match_count,
            'confidence'     : confidence,
            'disclaimer'     : DISCLAIMER
        })

    except Exception as e:
        return jsonify({'error': f'Gagal melakukan prediksi: {str(e)}'}), 500
