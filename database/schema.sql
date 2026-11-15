-- ============================================================
-- schema.sql - Skema Database Analytix
-- Database: laptop_bigdata
-- Deskripsi: Menyimpan data produk laptop dari berbagai marketplace
-- Dibuat untuk: Proyek Big Data Analytics Analytix
-- ============================================================

CREATE DATABASE IF NOT EXISTS laptop_bigdata
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE laptop_bigdata;

-- ------------------------------------------------------------
-- Tabel: marketplaces
-- Menyimpan informasi setiap marketplace yang didukung
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS marketplaces (
    id         INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL UNIQUE COMMENT 'Nama marketplace (Shopee, Tokopedia, dll)',
    url        VARCHAR(255)          COMMENT 'URL utama marketplace',
    logo_url   VARCHAR(255)          COMMENT 'URL logo marketplace',
    active     TINYINT(1)   NOT NULL DEFAULT 1 COMMENT '1 = aktif, 0 = nonaktif',
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='Daftar marketplace yang didukung Analytix';


-- ------------------------------------------------------------
-- Tabel: brands
-- Menyimpan informasi brand/merek laptop
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS brands (
    id             INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100) NOT NULL UNIQUE COMMENT 'Nama brand laptop',
    country_origin VARCHAR(100)          COMMENT 'Negara asal brand',
    description    TEXT                  COMMENT 'Deskripsi singkat brand'
) ENGINE=InnoDB COMMENT='Daftar brand laptop';


-- ------------------------------------------------------------
-- Tabel: sellers
-- Menyimpan informasi penjual di setiap marketplace
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sellers (
    id             INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(255) NOT NULL COMMENT 'Nama toko/seller',
    marketplace_id INT          UNSIGNED NOT NULL COMMENT 'FK ke tabel marketplaces',
    store_url      VARCHAR(255)          COMMENT 'URL halaman toko seller',
    rating         DECIMAL(3,2)          COMMENT 'Rating seller (0.00–5.00)',
    total_products INT          UNSIGNED          COMMENT 'Jumlah produk yang dijual',
    verified       TINYINT(1)   NOT NULL DEFAULT 0 COMMENT '1 = seller terverifikasi',
    CONSTRAINT fk_seller_marketplace
        FOREIGN KEY (marketplace_id) REFERENCES marketplaces(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Informasi penjual di setiap marketplace';


-- ------------------------------------------------------------
-- Tabel: products
-- Menyimpan identitas dan spesifikasi laptop
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    id             INT           UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(255)  NOT NULL COMMENT 'Nama lengkap produk laptop',
    brand_id       INT           UNSIGNED NOT NULL COMMENT 'FK ke tabel brands',
    processor      VARCHAR(255)           COMMENT 'Model processor (contoh: Intel Core i7-1255U)',
    processor_type VARCHAR(50)            COMMENT 'Jenis processor: Intel | AMD',
    ram_gb         TINYINT       UNSIGNED COMMENT 'Kapasitas RAM dalam GB',
    storage_gb     SMALLINT      UNSIGNED COMMENT 'Kapasitas storage dalam GB',
    storage_type   VARCHAR(20)            COMMENT 'Jenis storage: SSD | HDD | eMMC',
    gpu            VARCHAR(255)           COMMENT 'Model GPU (contoh: NVIDIA RTX 3050)',
    gpu_type       VARCHAR(20)            COMMENT 'Jenis GPU: Dedicated | Integrated',
    screen_size    DECIMAL(4,1)           COMMENT 'Ukuran layar dalam inci',
    weight_kg      DECIMAL(4,2)           COMMENT 'Berat laptop dalam kg',
    condition      VARCHAR(20)   NOT NULL DEFAULT 'Baru' COMMENT 'Kondisi: Baru | Bekas',
    created_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_brand
        FOREIGN KEY (brand_id) REFERENCES brands(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_brand_id      (brand_id),
    INDEX idx_processor_type(processor_type),
    INDEX idx_ram_gb        (ram_gb),
    INDEX idx_gpu_type      (gpu_type)
) ENGINE=InnoDB COMMENT='Identitas dan spesifikasi produk laptop';


-- ------------------------------------------------------------
-- Tabel: prices
-- Menyimpan harga dan riwayat harga dari setiap marketplace
-- Satu produk dapat memiliki beberapa entri harga dari marketplace berbeda
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS prices (
    id                  INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_id          INT          UNSIGNED NOT NULL COMMENT 'FK ke tabel products',
    marketplace_id      INT          UNSIGNED NOT NULL COMMENT 'FK ke tabel marketplaces',
    seller_id           INT          UNSIGNED          COMMENT 'FK ke tabel sellers',
    price_idr           BIGINT       UNSIGNED NOT NULL COMMENT 'Harga saat ini dalam Rupiah',
    original_price_idr  BIGINT       UNSIGNED          COMMENT 'Harga sebelum diskon (jika ada)',
    discount_pct        TINYINT      UNSIGNED          COMMENT 'Persentase diskon (0–100)',
    is_active           TINYINT(1)   NOT NULL DEFAULT 1 COMMENT '1 = harga masih berlaku',
    scraped_at          DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu pengambilan data',
    CONSTRAINT fk_price_product
        FOREIGN KEY (product_id) REFERENCES products(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_price_marketplace
        FOREIGN KEY (marketplace_id) REFERENCES marketplaces(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_price_seller
        FOREIGN KEY (seller_id) REFERENCES sellers(id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_price_product    (product_id),
    INDEX idx_price_marketplace(marketplace_id),
    INDEX idx_price_scraped_at (scraped_at)
) ENGINE=InnoDB COMMENT='Harga produk per marketplace beserta riwayat scraping';


-- ------------------------------------------------------------
-- Tabel: reviews
-- Menyimpan rating dan jumlah ulasan per produk per marketplace
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reviews (
    id             INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_id     INT          UNSIGNED NOT NULL COMMENT 'FK ke tabel products',
    marketplace_id INT          UNSIGNED NOT NULL COMMENT 'FK ke tabel marketplaces',
    rating         DECIMAL(3,2)          COMMENT 'Rata-rata rating (0.00–5.00)',
    review_count   INT          UNSIGNED COMMENT 'Jumlah ulasan tertulis',
    sold_count     INT          UNSIGNED COMMENT 'Jumlah terjual (jika tersedia)',
    updated_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_product
        FOREIGN KEY (product_id) REFERENCES products(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_review_marketplace
        FOREIGN KEY (marketplace_id) REFERENCES marketplaces(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Rating dan ulasan produk per marketplace';


-- ------------------------------------------------------------
-- Tabel: price_history
-- Menyimpan riwayat perubahan harga untuk analisis tren
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS price_history (
    id             INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_id     INT          UNSIGNED NOT NULL COMMENT 'FK ke tabel products',
    marketplace_id INT          UNSIGNED NOT NULL COMMENT 'FK ke tabel marketplaces',
    price_idr      BIGINT       UNSIGNED NOT NULL COMMENT 'Harga pada waktu pencatatan',
    recorded_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu pencatatan harga',
    CONSTRAINT fk_history_product
        FOREIGN KEY (product_id) REFERENCES products(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_history_marketplace
        FOREIGN KEY (marketplace_id) REFERENCES marketplaces(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_history_product    (product_id),
    INDEX idx_history_recorded_at(recorded_at)
) ENGINE=InnoDB COMMENT='Riwayat perubahan harga untuk analisis tren';


-- ============================================================
-- DATA CONTOH (5 produk dari berbagai marketplace)
-- ============================================================

-- Marketplace
INSERT IGNORE INTO marketplaces (id, name, url, logo_url, active) VALUES
(1, 'Shopee',    'https://shopee.co.id',    '/static/img/shopee.png',    1),
(2, 'Tokopedia', 'https://tokopedia.com',   '/static/img/tokopedia.png', 1),
(3, 'Lazada',    'https://lazada.co.id',    '/static/img/lazada.png',    1),
(4, 'Blibli',    'https://blibli.com',      '/static/img/blibli.png',    1);

-- Brand
INSERT IGNORE INTO brands (id, name, country_origin, description) VALUES
(1, 'ASUS',    'Taiwan',  'Produsen laptop dan komponen komputer asal Taiwan'),
(2, 'Lenovo',  'China',   'Produsen perangkat teknologi asal Tiongkok'),
(3, 'HP',      'USA',     'Hewlett-Packard, produsen komputer asal Amerika Serikat'),
(4, 'Acer',    'Taiwan',  'Produsen laptop dan monitor asal Taiwan'),
(5, 'Dell',    'USA',     'Produsen komputer dan laptop asal Amerika Serikat');

-- Seller
INSERT IGNORE INTO sellers (id, name, marketplace_id, rating, verified) VALUES
(1, 'ASUS Official Store',    1, 4.90, 1),
(2, 'Lenovo Official',        2, 4.85, 1),
(3, 'HP Store Indonesia',     3, 4.80, 1),
(4, 'Acer Indonesia',         1, 4.75, 1),
(5, 'Dell Official Blibli',   4, 4.88, 1);

-- Produk
INSERT IGNORE INTO products (id, name, brand_id, processor, processor_type, ram_gb, storage_gb, storage_type, gpu, gpu_type, screen_size, weight_kg, condition) VALUES
(1, 'ASUS VivoBook 15 A1502ZA',    1, 'Intel Core i5-12500H', 'Intel', 8,  512, 'SSD', 'Intel Iris Xe Graphics',  'Integrated', 15.6, 1.70, 'Baru'),
(2, 'Lenovo IdeaPad Slim 5i Gen 8',2, 'Intel Core i7-1355U',  'Intel', 16, 512, 'SSD', 'Intel Iris Xe Graphics',  'Integrated', 14.0, 1.46, 'Baru'),
(3, 'HP Pavilion 14-ec2xxx',       3, 'AMD Ryzen 5 7530U',    'AMD',   8,  512, 'SSD', 'AMD Radeon Graphics',     'Integrated', 14.0, 1.41, 'Baru'),
(4, 'Acer Aspire 5 A514-55',       4, 'Intel Core i3-1215U',  'Intel', 8,  256, 'SSD', 'Intel UHD Graphics',      'Integrated', 14.0, 1.65, 'Baru'),
(5, 'Dell Inspiron 15 3520',       5, 'Intel Core i5-1235U',  'Intel', 16, 512, 'SSD', 'Intel Iris Xe Graphics',  'Integrated', 15.6, 1.83, 'Baru');

-- Harga aktif
INSERT IGNORE INTO prices (id, product_id, marketplace_id, seller_id, price_idr, original_price_idr, discount_pct, is_active, scraped_at) VALUES
(1, 1, 1, 1,  7499000,  8299000, 10, 1, '2024-01-15 10:00:00'),
(2, 2, 2, 2, 10999000, 12499000, 12, 1, '2024-01-15 10:00:00'),
(3, 3, 3, 3,  7299000,  7999000,  9, 1, '2024-01-15 10:00:00'),
(4, 4, 1, 4,  5499000,  5999000,  8, 1, '2024-01-15 10:00:00'),
(5, 5, 4, 5, 10499000, 11299000,  7, 1, '2024-01-15 10:00:00');

-- Ulasan
INSERT IGNORE INTO reviews (id, product_id, marketplace_id, rating, review_count, sold_count) VALUES
(1, 1, 1, 4.80, 1250, 3400),
(2, 2, 2, 4.75,  980, 2100),
(3, 3, 3, 4.70,  750, 1800),
(4, 4, 1, 4.60,  620, 1500),
(5, 5, 4, 4.85,  870, 2300);

-- Riwayat harga (contoh 3 titik data per produk)
INSERT IGNORE INTO price_history (product_id, marketplace_id, price_idr, recorded_at) VALUES
(1, 1,  8299000, '2023-11-01 00:00:00'),
(1, 1,  7899000, '2023-12-01 00:00:00'),
(1, 1,  7499000, '2024-01-01 00:00:00'),
(2, 2, 12499000, '2023-11-01 00:00:00'),
(2, 2, 11499000, '2023-12-01 00:00:00'),
(2, 2, 10999000, '2024-01-01 00:00:00'),
(3, 3,  7999000, '2023-11-01 00:00:00'),
(3, 3,  7599000, '2023-12-01 00:00:00'),
(3, 3,  7299000, '2024-01-01 00:00:00');
