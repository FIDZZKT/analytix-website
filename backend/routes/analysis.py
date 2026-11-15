"""
analysis.py - Blueprint untuk endpoint analisis dan statistik Big Data
Endpoint: /api/analysis/*
"""

import pandas as pd
from flask import Blueprint, jsonify
from datetime import datetime
from models.database import get_products

analysis_bp = Blueprint('analysis_bp', __name__)


def _load_dataframe():
    """
    Memuat data produk dan mengonversinya ke DataFrame pandas
    untuk keperluan agregasi dan analisis.
    """
    products = get_products()
    if not products:
        return pd.DataFrame()
    df = pd.DataFrame(products)
    # Pastikan kolom numerik bertipe yang sesuai
    for col in ['price_idr', 'ram_gb', 'storage_gb', 'rating', 'review_count']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


@analysis_bp.route('/api/analysis/summary', methods=['GET'])
def get_summary():
    """
    Mengembalikan ringkasan statistik keseluruhan dataset.
    Mencakup total produk, marketplace, brand, harga rata-rata,
    produk termurah, produk termahal, dan waktu pembaruan terakhir.
    """
    try:
        df = _load_dataframe()
        if df.empty:
            return jsonify({
                'total_products'   : 0,
                'total_marketplaces': 0,
                'total_brands'     : 0,
                'avg_price'        : 0,
                'min_price_product': None,
                'max_price_product': None,
                'last_updated'     : datetime.now().isoformat()
            })

        # Produk dengan harga terendah
        min_row = df.loc[df['price_idr'].idxmin()]
        min_product = {
            'name'        : min_row.get('name'),
            'price'       : float(min_row.get('price_idr', 0)),
            'marketplace' : min_row.get('marketplace')
        }

        # Produk dengan harga tertinggi
        max_row = df.loc[df['price_idr'].idxmax()]
        max_product = {
            'name'        : max_row.get('name'),
            'price'       : float(max_row.get('price_idr', 0)),
            'marketplace' : max_row.get('marketplace')
        }

        # Waktu pembaruan dari kolom scraped_at jika tersedia
        last_updated = datetime.now().isoformat()
        if 'scraped_at' in df.columns:
            valid_dates = df['scraped_at'].dropna()
            if not valid_dates.empty:
                last_updated = str(valid_dates.max())

        return jsonify({
            'total_products'    : int(len(df)),
            'total_marketplaces': int(df['marketplace'].nunique()) if 'marketplace' in df.columns else 0,
            'total_brands'      : int(df['brand'].nunique()) if 'brand' in df.columns else 0,
            'avg_price'         : round(float(df['price_idr'].mean()), 0),
            'min_price_product' : min_product,
            'max_price_product' : max_product,
            'last_updated'      : last_updated
        })

    except Exception as e:
        return jsonify({'error': f'Gagal menghitung ringkasan: {str(e)}'}), 500


@analysis_bp.route('/api/analysis/marketplace', methods=['GET'])
def get_marketplace_analysis():
    """
    Mengembalikan rata-rata harga dan jumlah produk per marketplace.
    """
    try:
        df = _load_dataframe()
        if df.empty or 'marketplace' not in df.columns:
            return jsonify({'data': []})

        grouped = df.groupby('marketplace').agg(
            avg_price   =('price_idr', 'mean'),
            product_count=('price_idr', 'count')
        ).reset_index()

        result = [
            {
                'marketplace'  : row['marketplace'],
                'avg_price'    : round(float(row['avg_price']), 0),
                'product_count': int(row['product_count'])
            }
            for _, row in grouped.iterrows()
        ]

        return jsonify({'data': result})

    except Exception as e:
        return jsonify({'error': f'Gagal menganalisis marketplace: {str(e)}'}), 500


@analysis_bp.route('/api/analysis/brands', methods=['GET'])
def get_brands_analysis():
    """
    Mengembalikan jumlah produk per brand (top 10 terbanyak).
    """
    try:
        df = _load_dataframe()
        if df.empty or 'brand' not in df.columns:
            return jsonify({'data': []})

        brand_counts = (
            df['brand']
            .value_counts()
            .head(10)
            .reset_index()
        )
        brand_counts.columns = ['brand', 'product_count']

        result = [
            {
                'brand'        : row['brand'],
                'product_count': int(row['product_count'])
            }
            for _, row in brand_counts.iterrows()
        ]

        return jsonify({'data': result})

    except Exception as e:
        return jsonify({'error': f'Gagal menganalisis brand: {str(e)}'}), 500


@analysis_bp.route('/api/analysis/price-distribution', methods=['GET'])
def get_price_distribution():
    """
    Mengembalikan distribusi harga laptop dalam bucket harga.
    Setiap bucket merepresentasikan rentang harga tertentu.
    """
    try:
        df = _load_dataframe()
        if df.empty or 'price_idr' not in df.columns:
            return jsonify({'data': []})

        # Definisikan bucket harga dalam jutaan rupiah
        bins   = [0, 3_000_000, 5_000_000, 8_000_000, 12_000_000, 20_000_000, float('inf')]
        labels = ['< 3 Juta', '3–5 Juta', '5–8 Juta', '8–12 Juta', '12–20 Juta', '> 20 Juta']

        df['price_bucket'] = pd.cut(
            df['price_idr'].dropna(),
            bins=bins,
            labels=labels,
            right=False
        )
        bucket_counts = df['price_bucket'].value_counts().sort_index()

        result = [
            {
                'range': str(label),
                'count': int(bucket_counts.get(label, 0))
            }
            for label in labels
        ]

        return jsonify({'data': result})

    except Exception as e:
        return jsonify({'error': f'Gagal menghitung distribusi harga: {str(e)}'}), 500


@analysis_bp.route('/api/analysis/ram-distribution', methods=['GET'])
def get_ram_distribution():
    """
    Mengembalikan jumlah produk berdasarkan kapasitas RAM.
    """
    try:
        df = _load_dataframe()
        if df.empty or 'ram_gb' not in df.columns:
            return jsonify({'data': []})

        ram_counts = (
            df['ram_gb']
            .dropna()
            .astype(int)
            .value_counts()
            .sort_index()
            .reset_index()
        )
        ram_counts.columns = ['ram_gb', 'count']

        result = [
            {
                'ram_gb': int(row['ram_gb']),
                'count' : int(row['count'])
            }
            for _, row in ram_counts.iterrows()
        ]

        return jsonify({'data': result})

    except Exception as e:
        return jsonify({'error': f'Gagal menghitung distribusi RAM: {str(e)}'}), 500


@analysis_bp.route('/api/analysis/charts', methods=['GET'])
def get_all_charts():
    """
    Mengembalikan semua data grafik dalam satu respons.
    Digunakan oleh halaman Analisis Big Data untuk efisiensi request.
    """
    try:
        df = _load_dataframe()
        if df.empty:
            return jsonify({
                'marketplace'       : [],
                'brands'            : [],
                'price_distribution': [],
                'ram_distribution'  : []
            })

        # --- Data per marketplace ---
        marketplace_data = []
        if 'marketplace' in df.columns:
            grouped = df.groupby('marketplace').agg(
                avg_price    =('price_idr', 'mean'),
                product_count=('price_idr', 'count')
            ).reset_index()
            marketplace_data = [
                {
                    'marketplace'  : row['marketplace'],
                    'avg_price'    : round(float(row['avg_price']), 0),
                    'product_count': int(row['product_count'])
                }
                for _, row in grouped.iterrows()
            ]

        # --- Data per brand (top 10) ---
        brands_data = []
        if 'brand' in df.columns:
            bc = df['brand'].value_counts().head(10).reset_index()
            bc.columns = ['brand', 'product_count']
            brands_data = [
                {'brand': r['brand'], 'product_count': int(r['product_count'])}
                for _, r in bc.iterrows()
            ]

        # --- Distribusi harga ---
        price_dist = []
        if 'price_idr' in df.columns:
            bins   = [0, 3_000_000, 5_000_000, 8_000_000, 12_000_000, 20_000_000, float('inf')]
            labels = ['< 3 Juta', '3–5 Juta', '5–8 Juta', '8–12 Juta', '12–20 Juta', '> 20 Juta']
            df['price_bucket'] = pd.cut(df['price_idr'], bins=bins, labels=labels, right=False)
            bc2 = df['price_bucket'].value_counts().sort_index()
            price_dist = [
                {'range': lbl, 'count': int(bc2.get(lbl, 0))}
                for lbl in labels
            ]

        # --- Distribusi RAM ---
        ram_dist = []
        if 'ram_gb' in df.columns:
            rc = df['ram_gb'].dropna().astype(int).value_counts().sort_index().reset_index()
            rc.columns = ['ram_gb', 'count']
            ram_dist = [
                {'ram_gb': int(r['ram_gb']), 'count': int(r['count'])}
                for _, r in rc.iterrows()
            ]

        # --- Distribusi GPU ---
        gpu_dist = []
        if 'gpu_type' in df.columns:
            gc = df['gpu_type'].value_counts().reset_index()
            gc.columns = ['gpu_type', 'count']
            gpu_dist = [
                {'gpu_type': r['gpu_type'], 'count': int(r['count'])}
                for _, r in gc.iterrows()
            ]

        # --- Distribusi processor ---
        processor_dist = []
        if 'processor_type' in df.columns:
            pc = df['processor_type'].value_counts().reset_index()
            pc.columns = ['processor_type', 'count']
            processor_dist = [
                {'processor_type': r['processor_type'], 'count': int(r['count'])}
                for _, r in pc.iterrows()
            ]

        return jsonify({
            'marketplace'       : marketplace_data,
            'brands'            : brands_data,
            'price_distribution': price_dist,
            'ram_distribution'  : ram_dist,
            'gpu_distribution'  : gpu_dist,
            'processor_distribution': processor_dist
        })

    except Exception as e:
        return jsonify({'error': f'Gagal mengambil data grafik: {str(e)}'}), 500
