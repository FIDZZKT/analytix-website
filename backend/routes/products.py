"""
products.py - Blueprint untuk endpoint data produk laptop
Endpoint: /api/products dan /api/products/<id>
"""

from flask import Blueprint, jsonify, request
from models.database import get_products

products_bp = Blueprint('products_bp', __name__)


def _apply_filters(products, args):
    """
    Menerapkan filter dan pengurutan berdasarkan query parameter.
    Mengembalikan list produk yang sudah difilter dan diurutkan.
    """
    search        = args.get('search', '').strip().lower()
    marketplace   = args.get('marketplace', '').strip()
    brand         = args.get('brand', '').strip()
    min_price     = args.get('min_price', type=float)
    max_price     = args.get('max_price', type=float)
    ram_gb        = args.get('ram_gb', type=int)
    processor_type = args.get('processor_type', '').strip()
    gpu_type      = args.get('gpu_type', '').strip()
    sort          = args.get('sort', '').strip()

    result = products

    # Filter berdasarkan kata kunci nama produk
    if search:
        result = [
            p for p in result
            if search in str(p.get('name', '')).lower()
            or search in str(p.get('brand', '')).lower()
        ]

    # Filter berdasarkan marketplace
    if marketplace:
        result = [
            p for p in result
            if str(p.get('marketplace', '')).lower() == marketplace.lower()
        ]

    # Filter berdasarkan brand
    if brand:
        result = [
            p for p in result
            if str(p.get('brand', '')).lower() == brand.lower()
        ]

    # Filter berdasarkan rentang harga
    if min_price is not None:
        result = [
            p for p in result
            if p.get('price_idr') is not None and float(p['price_idr']) >= min_price
        ]
    if max_price is not None:
        result = [
            p for p in result
            if p.get('price_idr') is not None and float(p['price_idr']) <= max_price
        ]

    # Filter berdasarkan RAM
    if ram_gb is not None:
        result = [
            p for p in result
            if p.get('ram_gb') is not None and int(p['ram_gb']) == ram_gb
        ]

    # Filter berdasarkan jenis processor
    if processor_type:
        result = [
            p for p in result
            if str(p.get('processor_type', '')).lower() == processor_type.lower()
        ]

    # Filter berdasarkan jenis GPU
    if gpu_type:
        result = [
            p for p in result
            if str(p.get('gpu_type', '')).lower() == gpu_type.lower()
        ]

    # Pengurutan
    if sort == 'price_asc':
        result = sorted(result, key=lambda p: float(p.get('price_idr') or 0))
    elif sort == 'price_desc':
        result = sorted(result, key=lambda p: float(p.get('price_idr') or 0), reverse=True)
    elif sort == 'rating_desc':
        result = sorted(result, key=lambda p: float(p.get('rating') or 0), reverse=True)

    return result


@products_bp.route('/api/products', methods=['GET'])
def get_all_products():
    """
    Mengambil daftar produk laptop dengan dukungan filter, pencarian, dan paginasi.

    Query parameters:
      search         - kata kunci pencarian nama/brand
      marketplace    - filter marketplace (Shopee, Tokopedia, Lazada, Blibli)
      brand          - filter brand laptop
      min_price      - harga minimum (IDR)
      max_price      - harga maksimum (IDR)
      ram_gb         - filter RAM dalam GB
      processor_type - filter jenis processor (Intel, AMD)
      gpu_type       - filter jenis GPU (Dedicated, Integrated)
      sort           - urutan: price_asc | price_desc | rating_desc
      page           - nomor halaman (default: 1)
      per_page       - jumlah item per halaman (default: 12, maks: 100)
    """
    try:
        # Ambil semua produk dari sumber data
        all_products = get_products()

        # Terapkan filter
        filtered = _apply_filters(all_products, request.args)

        # Paginasi
        page     = max(1, request.args.get('page', 1, type=int))
        per_page = min(100, max(1, request.args.get('per_page', 12, type=int)))
        total    = len(filtered)
        start    = (page - 1) * per_page
        end      = start + per_page
        paginated = filtered[start:end]

        return jsonify({
            'data'     : paginated,
            'total'    : total,
            'page'     : page,
            'per_page' : per_page,
            'total_pages': (total + per_page - 1) // per_page
        })

    except Exception as e:
        return jsonify({'error': f'Gagal mengambil data produk: {str(e)}'}), 500


@products_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    """
    Mengambil detail satu produk berdasarkan ID.
    Mengembalikan 404 jika produk tidak ditemukan.
    """
    try:
        all_products = get_products()
        product = next(
            (p for p in all_products if p.get('id') == product_id),
            None
        )
        if product is None:
            return jsonify({'error': f'Produk dengan ID {product_id} tidak ditemukan'}), 404
        return jsonify({'data': product})

    except Exception as e:
        return jsonify({'error': f'Gagal mengambil detail produk: {str(e)}'}), 500
