"""
database.py - Modul koneksi database dan loading data untuk Analytix
Mendukung dua sumber data: MySQL (produksi) dan CSV (demo)
"""

import os
import pandas as pd
from config import DB_CONFIG, DATA_PATH


def get_connection():
    """
    Membuat koneksi ke database MySQL.
    Melempar exception dengan pesan yang jelas jika koneksi gagal.
    """
    try:
        import mysql.connector
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except ImportError:
        raise RuntimeError(
            "Modul mysql-connector-python belum terpasang. "
            "Jalankan: pip install mysql-connector-python"
        )
    except Exception as e:
        raise RuntimeError(
            f"Gagal terhubung ke MySQL: {e}. "
            "Pastikan MySQL berjalan dan konfigurasi di .env sudah benar."
        )


def load_demo_data():
    """
    Memuat dataset demo dari file CSV menggunakan pandas.
    Mengembalikan DataFrame atau DataFrame kosong jika file tidak ditemukan.
    """
    if not os.path.exists(DATA_PATH):
        # Kembalikan DataFrame kosong dengan kolom yang diharapkan
        return pd.DataFrame(columns=[
            'id', 'name', 'brand', 'marketplace', 'processor',
            'processor_type', 'ram_gb', 'storage_gb', 'storage_type',
            'gpu', 'gpu_type', 'screen_size', 'weight_kg', 'price_idr',
            'original_price_idr', 'discount_pct', 'rating', 'review_count',
            'sold_count', 'seller', 'condition', 'image_url', 'product_url',
            'scraped_at'
        ])
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except Exception as e:
        raise RuntimeError(f"Gagal memuat dataset demo: {e}")


def get_products_from_db(conn):
    """
    Mengambil data produk dari database MySQL.
    Mengembalikan list of dict yang merepresentasikan setiap produk.
    """
    query = """
        SELECT
            p.id,
            p.name,
            b.name        AS brand,
            p.processor,
            p.processor_type,
            p.ram_gb,
            p.storage_gb,
            p.storage_type,
            p.gpu,
            p.gpu_type,
            p.screen_size,
            p.weight_kg,
            p.condition,
            pr.price_idr,
            pr.original_price_idr,
            pr.discount_pct,
            m.name        AS marketplace,
            s.name        AS seller,
            r.rating,
            r.review_count,
            r.sold_count,
            pr.scraped_at
        FROM products p
        LEFT JOIN brands b          ON p.brand_id = b.id
        LEFT JOIN prices pr         ON pr.product_id = p.id AND pr.is_active = 1
        LEFT JOIN marketplaces m    ON pr.marketplace_id = m.id
        LEFT JOIN sellers s         ON pr.seller_id = s.id
        LEFT JOIN reviews r         ON r.product_id = p.id AND r.marketplace_id = pr.marketplace_id
        ORDER BY pr.price_idr ASC
    """
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    # Konversi tipe data agar JSON-serializable
    result = []
    for row in rows:
        item = dict(row)
        for key, val in item.items():
            if hasattr(val, 'isoformat'):
                item[key] = val.isoformat()
        result.append(item)
    return result


def get_products(use_db=False):
    """
    Mengambil data produk dari sumber yang tersedia.
    - use_db=True  : coba MySQL, fallback ke CSV jika gagal
    - use_db=False : langsung gunakan CSV demo
    Mengembalikan list of dict.
    """
    if use_db:
        try:
            conn = get_connection()
            products = get_products_from_db(conn)
            conn.close()
            return products
        except RuntimeError:
            # Fallback ke data demo jika MySQL tidak tersedia
            pass

    # Muat dari CSV demo
    df = load_demo_data()
    if df.empty:
        return []

    # Pastikan kolom numerik bertipe yang benar
    numeric_cols = [
        'id', 'ram_gb', 'storage_gb', 'price_idr',
        'original_price_idr', 'discount_pct', 'rating', 'review_count', 'sold_count'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Ganti NaN dengan None agar JSON-serializable
    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient='records')
