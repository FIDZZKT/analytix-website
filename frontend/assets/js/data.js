// Analytix - Demo Dataset
// 55 laptop entries covering Shopee, Tokopedia, Lazada, Blibli
// Data is for demonstration purposes only (labeled as demo data)

window.LAPTOP_DATA = [
  // ── ASUS (8 entries) ──────────────────────────────────────────────────────
  {
    id: 1, name: 'ASUS VivoBook 14 A1404ZA', brand: 'ASUS',
    processor: 'Intel Core i5-1235U', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.5,
    marketplace: 'Shopee', seller: 'ASUS Official Store',
    price_idr: 8499000, original_price_idr: 9999000, discount_pct: 15,
    rating: 4.8, review_count: 1247, sold_count: 3421,
    condition: 'Baru', date_scraped: '2025-01-15'
  },
  {
    id: 3, name: 'ASUS ROG Strix G15 G513QC', brand: 'ASUS',
    processor: 'AMD Ryzen 7 5800H', processor_type: 'AMD Ryzen 7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3050', gpu_type: 'NVIDIA RTX',
    screen_size: 15.6, weight_kg: 2.3,
    marketplace: 'Shopee', seller: 'ROG Official Store',
    price_idr: 16999000, original_price_idr: 19999000, discount_pct: 15,
    rating: 4.9, review_count: 567, sold_count: 1234,
    condition: 'Baru', date_scraped: '2025-01-15'
  },
  {
    id: 11, name: 'ASUS ZenBook 14 UX425EA', brand: 'ASUS',
    processor: 'Intel Core i7-1165G7', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.17,
    marketplace: 'Lazada', seller: 'ASUS Official Store',
    price_idr: 13999000, original_price_idr: 15999000, discount_pct: 13,
    rating: 4.8, review_count: 732, sold_count: 1876,
    condition: 'Baru', date_scraped: '2025-01-16'
  },
  {
    id: 12, name: 'ASUS TUF Gaming F15 FX507ZC', brand: 'ASUS',
    processor: 'Intel Core i5-12500H', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3050', gpu_type: 'NVIDIA RTX',
    screen_size: 15.6, weight_kg: 2.2,
    marketplace: 'Blibli', seller: 'ASUS Official Blibli',
    price_idr: 14499000, original_price_idr: 16999000, discount_pct: 15,
    rating: 4.7, review_count: 489, sold_count: 1102,
    condition: 'Baru', date_scraped: '2025-01-16'
  },
  {
    id: 13, name: 'ASUS VivoBook 15 M513UA', brand: 'ASUS',
    processor: 'AMD Ryzen 5 5500U', processor_type: 'AMD Ryzen 5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'AMD Radeon Graphics', gpu_type: 'Integrated',
    screen_size: 15.6, weight_kg: 1.8,
    marketplace: 'Tokopedia', seller: 'ASUS Partner Store',
    price_idr: 7999000, original_price_idr: 8999000, discount_pct: 11,
    rating: 4.6, review_count: 621, sold_count: 2034,
    condition: 'Baru', date_scraped: '2025-01-16'
  },
  {
    id: 14, name: 'ASUS ProArt Studiobook 16 H5600QM', brand: 'ASUS',
    processor: 'AMD Ryzen 9 5900HX', processor_type: 'AMD Ryzen 9',
    ram_gb: 32, storage_gb: 1000, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3070', gpu_type: 'NVIDIA RTX',
    screen_size: 16, weight_kg: 2.4,
    marketplace: 'Shopee', seller: 'ASUS Official Store',
    price_idr: 29999000, original_price_idr: 34999000, discount_pct: 14,
    rating: 4.9, review_count: 211, sold_count: 432,
    condition: 'Baru', date_scraped: '2025-01-16'
  },
  {
    id: 15, name: 'ASUS ExpertBook B1 B1500CBA', brand: 'ASUS',
    processor: 'Intel Core i3-1215U', processor_type: 'Intel Core i3',
    ram_gb: 4, storage_gb: 256, storage_type: 'SSD',
    gpu: 'Intel UHD Graphics', gpu_type: 'Integrated',
    screen_size: 15.6, weight_kg: 1.9,
    marketplace: 'Tokopedia', seller: 'ASUS Reseller',
    price_idr: 5499000, original_price_idr: 6499000, discount_pct: 15,
    rating: 4.5, review_count: 314, sold_count: 987,
    condition: 'Baru', date_scraped: '2025-01-17'
  },
  {
    id: 16, name: 'ASUS ROG Zephyrus G14 GA401QM', brand: 'ASUS',
    processor: 'AMD Ryzen 9 5900HS', processor_type: 'AMD Ryzen 9',
    ram_gb: 16, storage_gb: 1000, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3060', gpu_type: 'NVIDIA RTX',
    screen_size: 14, weight_kg: 1.72,
    marketplace: 'Lazada', seller: 'ROG Official Lazada',
    price_idr: 24999000, original_price_idr: 27999000, discount_pct: 11,
    rating: 4.9, review_count: 345, sold_count: 876,
    condition: 'Baru', date_scraped: '2025-01-17'
  },

  // ── Lenovo (8 entries) ────────────────────────────────────────────────────
  {
    id: 2, name: 'Lenovo IdeaPad Slim 3 15IAH8', brand: 'Lenovo',
    processor: 'Intel Core i5-12450H', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel UHD Graphics', gpu_type: 'Integrated',
    screen_size: 15.6, weight_kg: 1.7,
    marketplace: 'Tokopedia', seller: 'Lenovo Official',
    price_idr: 7999000, original_price_idr: 8999000, discount_pct: 11,
    rating: 4.7, review_count: 892, sold_count: 2103,
    condition: 'Baru', date_scraped: '2025-01-15'
  },
  {
    id: 17, name: 'Lenovo ThinkPad X1 Carbon Gen 10', brand: 'Lenovo',
    processor: 'Intel Core i7-1265U', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.12,
    marketplace: 'Blibli', seller: 'Lenovo Official Blibli',
    price_idr: 21999000, original_price_idr: 24999000, discount_pct: 12,
    rating: 4.8, review_count: 276, sold_count: 643,
    condition: 'Baru', date_scraped: '2025-01-17'
  },
  {
    id: 18, name: 'Lenovo Legion 5 15ACH6H', brand: 'Lenovo',
    processor: 'AMD Ryzen 7 5800H', processor_type: 'AMD Ryzen 7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3060', gpu_type: 'NVIDIA RTX',
    screen_size: 15.6, weight_kg: 2.4,
    marketplace: 'Shopee', seller: 'Lenovo Official Store',
    price_idr: 19999000, original_price_idr: 22999000, discount_pct: 13,
    rating: 4.8, review_count: 412, sold_count: 987,
    condition: 'Baru', date_scraped: '2025-01-17'
  },
  {
    id: 19, name: 'Lenovo IdeaPad Gaming 3 15IHU6', brand: 'Lenovo',
    processor: 'Intel Core i5-11300H', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce GTX 1650', gpu_type: 'NVIDIA GTX',
    screen_size: 15.6, weight_kg: 2.2,
    marketplace: 'Lazada', seller: 'Lenovo Official Lazada',
    price_idr: 11499000, original_price_idr: 12999000, discount_pct: 12,
    rating: 4.6, review_count: 534, sold_count: 1432,
    condition: 'Baru', date_scraped: '2025-01-17'
  },
  {
    id: 20, name: 'Lenovo Yoga Slim 7 Pro 14ACH5', brand: 'Lenovo',
    processor: 'AMD Ryzen 7 5800U', processor_type: 'AMD Ryzen 7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce MX450', gpu_type: 'NVIDIA GTX',
    screen_size: 14, weight_kg: 1.35,
    marketplace: 'Tokopedia', seller: 'Lenovo Premium Partner',
    price_idr: 16499000, original_price_idr: 18499000, discount_pct: 11,
    rating: 4.7, review_count: 298, sold_count: 765,
    condition: 'Baru', date_scraped: '2025-01-18'
  },
  {
    id: 21, name: 'Lenovo V15 G2 ITL', brand: 'Lenovo',
    processor: 'Intel Core i3-1115G4', processor_type: 'Intel Core i3',
    ram_gb: 4, storage_gb: 256, storage_type: 'SSD',
    gpu: 'Intel UHD Graphics', gpu_type: 'Integrated',
    screen_size: 15.6, weight_kg: 1.85,
    marketplace: 'Blibli', seller: 'Lenovo Reseller',
    price_idr: 4999000, original_price_idr: 5799000, discount_pct: 14,
    rating: 4.4, review_count: 421, sold_count: 1321,
    condition: 'Baru', date_scraped: '2025-01-18'
  },
  {
    id: 22, name: 'Lenovo ThinkBook 15 G3 ACL', brand: 'Lenovo',
    processor: 'AMD Ryzen 5 5500U', processor_type: 'AMD Ryzen 5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'AMD Radeon Graphics', gpu_type: 'Integrated',
    screen_size: 15.6, weight_kg: 1.8,
    marketplace: 'Shopee', seller: 'Lenovo Official Store',
    price_idr: 9499000, original_price_idr: 10999000, discount_pct: 14,
    rating: 4.6, review_count: 356, sold_count: 987,
    condition: 'Baru', date_scraped: '2025-01-18'
  },
  {
    id: 23, name: 'Lenovo Legion 7 16ACHG6', brand: 'Lenovo',
    processor: 'AMD Ryzen 9 5900HX', processor_type: 'AMD Ryzen 9',
    ram_gb: 32, storage_gb: 1000, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3080', gpu_type: 'NVIDIA RTX',
    screen_size: 16, weight_kg: 2.5,
    marketplace: 'Lazada', seller: 'Lenovo Official Lazada',
    price_idr: 32999000, original_price_idr: 36999000, discount_pct: 11,
    rating: 4.9, review_count: 187, sold_count: 342,
    condition: 'Baru', date_scraped: '2025-01-18'
  },

  // ── HP (7 entries) ────────────────────────────────────────────────────────
  {
    id: 5, name: 'HP Pavilion 14-ec1xxx', brand: 'HP',
    processor: 'AMD Ryzen 5 5625U', processor_type: 'AMD Ryzen 5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'AMD Radeon Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.41,
    marketplace: 'Lazada', seller: 'HP Official Store',
    price_idr: 8799000, original_price_idr: 9999000, discount_pct: 12,
    rating: 4.6, review_count: 445, sold_count: 1102,
    condition: 'Baru', date_scraped: '2025-01-15'
  },
  {
    id: 24, name: 'HP Envy x360 13-ay1xxx', brand: 'HP',
    processor: 'AMD Ryzen 7 5700U', processor_type: 'AMD Ryzen 7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'AMD Radeon Graphics', gpu_type: 'Integrated',
    screen_size: 13.3, weight_kg: 1.36,
    marketplace: 'Tokopedia', seller: 'HP Official Store',
    price_idr: 13999000, original_price_idr: 15999000, discount_pct: 13,
    rating: 4.7, review_count: 321, sold_count: 876,
    condition: 'Baru', date_scraped: '2025-01-18'
  },
  {
    id: 25, name: 'HP Omen 16-b1xxx', brand: 'HP',
    processor: 'Intel Core i7-12700H', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3060', gpu_type: 'NVIDIA RTX',
    screen_size: 16.1, weight_kg: 2.37,
    marketplace: 'Blibli', seller: 'HP Official Blibli',
    price_idr: 21499000, original_price_idr: 23999000, discount_pct: 10,
    rating: 4.8, review_count: 234, sold_count: 567,
    condition: 'Baru', date_scraped: '2025-01-18'
  },
  {
    id: 26, name: 'HP 14s-dq2xxx', brand: 'HP',
    processor: 'Intel Core i3-1115G4', processor_type: 'Intel Core i3',
    ram_gb: 4, storage_gb: 256, storage_type: 'SSD',
    gpu: 'Intel UHD Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.46,
    marketplace: 'Shopee', seller: 'HP Store Reseller',
    price_idr: 5299000, original_price_idr: 5999000, discount_pct: 12,
    rating: 4.4, review_count: 678, sold_count: 2134,
    condition: 'Baru', date_scraped: '2025-01-19'
  },
  {
    id: 27, name: 'HP Spectre x360 14-ef2xxx', brand: 'HP',
    processor: 'Intel Core i7-1355U', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 1000, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 13.5, weight_kg: 1.42,
    marketplace: 'Lazada', seller: 'HP Premium Store',
    price_idr: 24999000, original_price_idr: 27999000, discount_pct: 11,
    rating: 4.8, review_count: 156, sold_count: 345,
    condition: 'Baru', date_scraped: '2025-01-19'
  },
  {
    id: 28, name: 'HP Victus 15-fb0xxx', brand: 'HP',
    processor: 'AMD Ryzen 5 5600H', processor_type: 'AMD Ryzen 5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce GTX 1650', gpu_type: 'NVIDIA GTX',
    screen_size: 15.6, weight_kg: 2.29,
    marketplace: 'Tokopedia', seller: 'HP Official Store',
    price_idr: 10999000, original_price_idr: 12499000, discount_pct: 12,
    rating: 4.6, review_count: 398, sold_count: 1056,
    condition: 'Baru', date_scraped: '2025-01-19'
  },
  {
    id: 29, name: 'HP EliteBook 840 G9', brand: 'HP',
    processor: 'Intel Core i7-1255U', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.33,
    marketplace: 'Blibli', seller: 'HP Business Store',
    price_idr: 18999000, original_price_idr: 21499000, discount_pct: 12,
    rating: 4.7, review_count: 143, sold_count: 312,
    condition: 'Baru', date_scraped: '2025-01-19'
  },

  // ── Acer (7 entries) ──────────────────────────────────────────────────────
  {
    id: 30, name: 'Acer Aspire 5 A514-54', brand: 'Acer',
    processor: 'Intel Core i5-1135G7', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce MX350', gpu_type: 'NVIDIA GTX',
    screen_size: 14, weight_kg: 1.5,
    marketplace: 'Shopee', seller: 'Acer Official Store',
    price_idr: 8299000, original_price_idr: 9499000, discount_pct: 13,
    rating: 4.6, review_count: 567, sold_count: 1876,
    condition: 'Baru', date_scraped: '2025-01-19'
  },
  {
    id: 31, name: 'Acer Predator Helios 300 PH315-55', brand: 'Acer',
    processor: 'Intel Core i7-12700H', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3060', gpu_type: 'NVIDIA RTX',
    screen_size: 15.6, weight_kg: 2.3,
    marketplace: 'Tokopedia', seller: 'Acer Official Store',
    price_idr: 19999000, original_price_idr: 22999000, discount_pct: 13,
    rating: 4.8, review_count: 423, sold_count: 987,
    condition: 'Baru', date_scraped: '2025-01-19'
  },
  {
    id: 32, name: 'Acer Swift 3 SF314-512', brand: 'Acer',
    processor: 'Intel Core i5-1240P', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.2,
    marketplace: 'Lazada', seller: 'Acer Official Lazada',
    price_idr: 9499000, original_price_idr: 10999000, discount_pct: 14,
    rating: 4.7, review_count: 312, sold_count: 876,
    condition: 'Baru', date_scraped: '2025-01-20'
  },
  {
    id: 33, name: 'Acer Nitro 5 AN515-58', brand: 'Acer',
    processor: 'Intel Core i5-12500H', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3050', gpu_type: 'NVIDIA RTX',
    screen_size: 15.6, weight_kg: 2.5,
    marketplace: 'Blibli', seller: 'Acer Official Blibli',
    price_idr: 12999000, original_price_idr: 14999000, discount_pct: 13,
    rating: 4.7, review_count: 521, sold_count: 1432,
    condition: 'Baru', date_scraped: '2025-01-20'
  },
  {
    id: 34, name: 'Acer Chromebook Spin 514 CP514-3HH', brand: 'Acer',
    processor: 'AMD Ryzen 5 5625C', processor_type: 'AMD Ryzen 5',
    ram_gb: 8, storage_gb: 256, storage_type: 'SSD',
    gpu: 'AMD Radeon Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.57,
    marketplace: 'Shopee', seller: 'Acer Partner Store',
    price_idr: 6999000, original_price_idr: 7999000, discount_pct: 13,
    rating: 4.4, review_count: 198, sold_count: 543,
    condition: 'Baru', date_scraped: '2025-01-20'
  },
  {
    id: 35, name: 'Acer ConceptD 5 Pro CN516-72P', brand: 'Acer',
    processor: 'Intel Core i7-11800H', processor_type: 'Intel Core i7',
    ram_gb: 32, storage_gb: 1000, storage_type: 'SSD',
    gpu: 'NVIDIA RTX A3000', gpu_type: 'NVIDIA RTX',
    screen_size: 16, weight_kg: 2.1,
    marketplace: 'Tokopedia', seller: 'Acer Premium',
    price_idr: 34999000, original_price_idr: 39999000, discount_pct: 13,
    rating: 4.9, review_count: 87, sold_count: 134,
    condition: 'Baru', date_scraped: '2025-01-20'
  },
  {
    id: 36, name: 'Acer Extensa 15 EX215-54', brand: 'Acer',
    processor: 'Intel Core i3-1115G4', processor_type: 'Intel Core i3',
    ram_gb: 4, storage_gb: 256, storage_type: 'SSD',
    gpu: 'Intel UHD Graphics', gpu_type: 'Integrated',
    screen_size: 15.6, weight_kg: 1.9,
    marketplace: 'Lazada', seller: 'Acer Official Lazada',
    price_idr: 4799000, original_price_idr: 5499000, discount_pct: 13,
    rating: 4.3, review_count: 345, sold_count: 1234,
    condition: 'Baru', date_scraped: '2025-01-20'
  },

  // ── Dell (6 entries) ──────────────────────────────────────────────────────
  {
    id: 37, name: 'Dell XPS 13 9315', brand: 'Dell',
    processor: 'Intel Core i7-1250U', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 13.4, weight_kg: 1.17,
    marketplace: 'Shopee', seller: 'Dell Official Store',
    price_idr: 22999000, original_price_idr: 25999000, discount_pct: 12,
    rating: 4.8, review_count: 234, sold_count: 543,
    condition: 'Baru', date_scraped: '2025-01-20'
  },
  {
    id: 38, name: 'Dell Inspiron 15 3511', brand: 'Dell',
    processor: 'Intel Core i5-1135G7', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce MX350', gpu_type: 'NVIDIA GTX',
    screen_size: 15.6, weight_kg: 1.8,
    marketplace: 'Blibli', seller: 'Dell Official Blibli',
    price_idr: 9999000, original_price_idr: 11499000, discount_pct: 13,
    rating: 4.6, review_count: 512, sold_count: 1432,
    condition: 'Baru', date_scraped: '2025-01-20'
  },
  {
    id: 39, name: 'Dell G15 5520', brand: 'Dell',
    processor: 'Intel Core i5-12500H', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3050', gpu_type: 'NVIDIA RTX',
    screen_size: 15.6, weight_kg: 2.5,
    marketplace: 'Lazada', seller: 'Dell Official Lazada',
    price_idr: 13999000, original_price_idr: 15999000, discount_pct: 13,
    rating: 4.7, review_count: 378, sold_count: 987,
    condition: 'Baru', date_scraped: '2025-01-21'
  },
  {
    id: 40, name: 'Dell Latitude 5520', brand: 'Dell',
    processor: 'Intel Core i7-1185G7', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 15.6, weight_kg: 1.78,
    marketplace: 'Tokopedia', seller: 'Dell Business Store',
    price_idr: 19999000, original_price_idr: 22999000, discount_pct: 13,
    rating: 4.7, review_count: 189, sold_count: 432,
    condition: 'Baru', date_scraped: '2025-01-21'
  },
  {
    id: 41, name: 'Dell Alienware m15 R7', brand: 'Dell',
    processor: 'AMD Ryzen 9 6900HX', processor_type: 'AMD Ryzen 9',
    ram_gb: 32, storage_gb: 1000, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3070 Ti', gpu_type: 'NVIDIA RTX',
    screen_size: 15.6, weight_kg: 2.78,
    marketplace: 'Shopee', seller: 'Dell Official Store',
    price_idr: 34999000, original_price_idr: 39999000, discount_pct: 13,
    rating: 4.9, review_count: 134, sold_count: 243,
    condition: 'Baru', date_scraped: '2025-01-21'
  },
  {
    id: 42, name: 'Dell Vostro 14 5415', brand: 'Dell',
    processor: 'AMD Ryzen 5 5500U', processor_type: 'AMD Ryzen 5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'AMD Radeon Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.54,
    marketplace: 'Blibli', seller: 'Dell Reseller Blibli',
    price_idr: 9499000, original_price_idr: 10999000, discount_pct: 14,
    rating: 4.5, review_count: 267, sold_count: 765,
    condition: 'Baru', date_scraped: '2025-01-21'
  },

  // ── MSI (5 entries) ───────────────────────────────────────────────────────
  {
    id: 43, name: 'MSI GF63 Thin 11SC', brand: 'MSI',
    processor: 'Intel Core i5-11400H', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce GTX 1650', gpu_type: 'NVIDIA GTX',
    screen_size: 15.6, weight_kg: 1.86,
    marketplace: 'Shopee', seller: 'MSI Official Store',
    price_idr: 10999000, original_price_idr: 12499000, discount_pct: 12,
    rating: 4.6, review_count: 432, sold_count: 1234,
    condition: 'Baru', date_scraped: '2025-01-21'
  },
  {
    id: 44, name: 'MSI Raider GE76 12UHS', brand: 'MSI',
    processor: 'Intel Core i9-12900HK', processor_type: 'Intel Core i9',
    ram_gb: 32, storage_gb: 1000, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3080 Ti', gpu_type: 'NVIDIA RTX',
    screen_size: 17.3, weight_kg: 2.9,
    marketplace: 'Tokopedia', seller: 'MSI Premium Store',
    price_idr: 35000000, original_price_idr: 39999000, discount_pct: 13,
    rating: 4.9, review_count: 98, sold_count: 176,
    condition: 'Baru', date_scraped: '2025-01-21'
  },
  {
    id: 45, name: 'MSI Prestige 14 A12SC', brand: 'MSI',
    processor: 'Intel Core i7-1280P', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce GTX 1650', gpu_type: 'NVIDIA GTX',
    screen_size: 14, weight_kg: 1.29,
    marketplace: 'Lazada', seller: 'MSI Official Lazada',
    price_idr: 17999000, original_price_idr: 19999000, discount_pct: 10,
    rating: 4.7, review_count: 187, sold_count: 432,
    condition: 'Baru', date_scraped: '2025-01-21'
  },
  {
    id: 46, name: 'MSI Katana GF66 12UGS', brand: 'MSI',
    processor: 'Intel Core i7-12650H', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 3070', gpu_type: 'NVIDIA RTX',
    screen_size: 15.6, weight_kg: 2.25,
    marketplace: 'Blibli', seller: 'MSI Official Blibli',
    price_idr: 22999000, original_price_idr: 25999000, discount_pct: 12,
    rating: 4.8, review_count: 213, sold_count: 543,
    condition: 'Baru', date_scraped: '2025-01-22'
  },
  {
    id: 47, name: 'MSI Modern 14 B11MOU', brand: 'MSI',
    processor: 'Intel Core i5-1155G7', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.3,
    marketplace: 'Shopee', seller: 'MSI Official Store',
    price_idr: 9999000, original_price_idr: 11499000, discount_pct: 13,
    rating: 4.6, review_count: 276, sold_count: 765,
    condition: 'Baru', date_scraped: '2025-01-22'
  },

  // ── Apple (5 entries) ─────────────────────────────────────────────────────
  {
    id: 4, name: 'Apple MacBook Air M2', brand: 'Apple',
    processor: 'Apple M2', processor_type: 'Apple M2',
    ram_gb: 8, storage_gb: 256, storage_type: 'SSD',
    gpu: 'Apple M2 GPU 8-core', gpu_type: 'Apple GPU',
    screen_size: 13.6, weight_kg: 1.24,
    marketplace: 'Tokopedia', seller: 'iBox Official',
    price_idr: 18999000, original_price_idr: 19999000, discount_pct: 5,
    rating: 4.9, review_count: 2341, sold_count: 5678,
    condition: 'Baru', date_scraped: '2025-01-15'
  },
  {
    id: 48, name: 'Apple MacBook Pro 14 M3 Pro', brand: 'Apple',
    processor: 'Apple M3 Pro', processor_type: 'Apple M3',
    ram_gb: 18, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Apple M3 Pro GPU 18-core', gpu_type: 'Apple GPU',
    screen_size: 14.2, weight_kg: 1.61,
    marketplace: 'Shopee', seller: 'iBox Reseller',
    price_idr: 32999000, original_price_idr: 34999000, discount_pct: 6,
    rating: 4.9, review_count: 876, sold_count: 2134,
    condition: 'Baru', date_scraped: '2025-01-22'
  },
  {
    id: 49, name: 'Apple MacBook Air M1', brand: 'Apple',
    processor: 'Apple M1', processor_type: 'Apple M1',
    ram_gb: 8, storage_gb: 256, storage_type: 'SSD',
    gpu: 'Apple M1 GPU 7-core', gpu_type: 'Apple GPU',
    screen_size: 13.3, weight_kg: 1.29,
    marketplace: 'Lazada', seller: 'iStore Lazada',
    price_idr: 14999000, original_price_idr: 15999000, discount_pct: 6,
    rating: 4.8, review_count: 1543, sold_count: 4321,
    condition: 'Baru', date_scraped: '2025-01-22'
  },
  {
    id: 50, name: 'Apple MacBook Pro 13 M2', brand: 'Apple',
    processor: 'Apple M2', processor_type: 'Apple M2',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Apple M2 GPU 10-core', gpu_type: 'Apple GPU',
    screen_size: 13.3, weight_kg: 1.4,
    marketplace: 'Blibli', seller: 'iBox Official Blibli',
    price_idr: 21999000, original_price_idr: 23999000, discount_pct: 8,
    rating: 4.9, review_count: 1123, sold_count: 2876,
    condition: 'Baru', date_scraped: '2025-01-22'
  },
  {
    id: 51, name: 'Apple MacBook Air 15 M2', brand: 'Apple',
    processor: 'Apple M2', processor_type: 'Apple M2',
    ram_gb: 8, storage_gb: 256, storage_type: 'SSD',
    gpu: 'Apple M2 GPU 10-core', gpu_type: 'Apple GPU',
    screen_size: 15.3, weight_kg: 1.51,
    marketplace: 'Tokopedia', seller: 'iBox Premium',
    price_idr: 23999000, original_price_idr: 25999000, discount_pct: 8,
    rating: 4.9, review_count: 654, sold_count: 1432,
    condition: 'Baru', date_scraped: '2025-01-22'
  },

  // ── Samsung (4 entries) ───────────────────────────────────────────────────
  {
    id: 52, name: 'Samsung Galaxy Book3 Pro 16', brand: 'Samsung',
    processor: 'Intel Core i7-1360P', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 16, weight_kg: 1.56,
    marketplace: 'Shopee', seller: 'Samsung Official Store',
    price_idr: 21999000, original_price_idr: 24999000, discount_pct: 12,
    rating: 4.8, review_count: 312, sold_count: 765,
    condition: 'Baru', date_scraped: '2025-01-22'
  },
  {
    id: 53, name: 'Samsung Galaxy Book2 360', brand: 'Samsung',
    processor: 'Intel Core i5-1235U', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 256, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 13.3, weight_kg: 1.06,
    marketplace: 'Tokopedia', seller: 'Samsung Official Store',
    price_idr: 14999000, original_price_idr: 16999000, discount_pct: 12,
    rating: 4.7, review_count: 234, sold_count: 543,
    condition: 'Baru', date_scraped: '2025-01-22'
  },
  {
    id: 54, name: 'Samsung Galaxy Book3 Ultra', brand: 'Samsung',
    processor: 'Intel Core i9-13900H', processor_type: 'Intel Core i9',
    ram_gb: 32, storage_gb: 1000, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce RTX 4070', gpu_type: 'NVIDIA RTX',
    screen_size: 16, weight_kg: 1.79,
    marketplace: 'Lazada', seller: 'Samsung Premium Lazada',
    price_idr: 34999000, original_price_idr: 38999000, discount_pct: 10,
    rating: 4.9, review_count: 145, sold_count: 287,
    condition: 'Baru', date_scraped: '2025-01-23'
  },
  {
    id: 55, name: 'Samsung Galaxy Book2 Pro 360 15', brand: 'Samsung',
    processor: 'Intel Core i7-1260P', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 15.6, weight_kg: 1.39,
    marketplace: 'Blibli', seller: 'Samsung Official Blibli',
    price_idr: 19999000, original_price_idr: 22999000, discount_pct: 13,
    rating: 4.8, review_count: 198, sold_count: 432,
    condition: 'Baru', date_scraped: '2025-01-23'
  },

  // ── Xiaomi (5 entries) ────────────────────────────────────────────────────
  {
    id: 6, name: 'Xiaomi RedmiBook 15 Pro', brand: 'Xiaomi',
    processor: 'Intel Core i5-11320H', processor_type: 'Intel Core i5',
    ram_gb: 8, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 15.6, weight_kg: 1.9,
    marketplace: 'Lazada', seller: 'Mi Store Official',
    price_idr: 7499000, original_price_idr: 8499000, discount_pct: 12,
    rating: 4.5, review_count: 876, sold_count: 2567,
    condition: 'Baru', date_scraped: '2025-01-15'
  },
  {
    id: 7, name: 'Xiaomi Mi Notebook Pro 14 2021', brand: 'Xiaomi',
    processor: 'Intel Core i5-11300H', processor_type: 'Intel Core i5',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce MX450', gpu_type: 'NVIDIA GTX',
    screen_size: 14, weight_kg: 1.4,
    marketplace: 'Tokopedia', seller: 'Xiaomi Partner',
    price_idr: 11999000, original_price_idr: 13499000, discount_pct: 11,
    rating: 4.6, review_count: 432, sold_count: 1234,
    condition: 'Baru', date_scraped: '2025-01-15'
  },
  {
    id: 8, name: 'Xiaomi Mi Notebook Ultra 15.6', brand: 'Xiaomi',
    processor: 'Intel Core i7-11390H', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'NVIDIA GeForce MX450', gpu_type: 'NVIDIA GTX',
    screen_size: 15.6, weight_kg: 1.6,
    marketplace: 'Blibli', seller: 'Xiaomi Official Blibli',
    price_idr: 13999000, original_price_idr: 15999000, discount_pct: 13,
    rating: 4.7, review_count: 321, sold_count: 876,
    condition: 'Baru', date_scraped: '2025-01-15'
  },
  {
    id: 9, name: 'Xiaomi Book Pro 16 2022', brand: 'Xiaomi',
    processor: 'Intel Core i7-1260P', processor_type: 'Intel Core i7',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 16, weight_kg: 1.8,
    marketplace: 'Shopee', seller: 'Xiaomi Store',
    price_idr: 16999000, original_price_idr: 18999000, discount_pct: 11,
    rating: 4.7, review_count: 234, sold_count: 654,
    condition: 'Baru', date_scraped: '2025-01-15'
  },
  {
    id: 10, name: 'Xiaomi RedmiBook 14 2024', brand: 'Xiaomi',
    processor: 'Intel Core i5-13500H', processor_type: 'Intel Core i5',
    ram_gb: 16, storage_gb: 512, storage_type: 'SSD',
    gpu: 'Intel Iris Xe Graphics', gpu_type: 'Integrated',
    screen_size: 14, weight_kg: 1.38,
    marketplace: 'Lazada', seller: 'Xiaomi Official Lazada',
    price_idr: 9999000, original_price_idr: 11499000, discount_pct: 13,
    rating: 4.7, review_count: 567, sold_count: 1543,
    condition: 'Baru', date_scraped: '2025-01-15'
  }
];

// ── Helper utilities ──────────────────────────────────────────────────────────
window.getUniqueValues = (field) => [...new Set(window.LAPTOP_DATA.map(l => l[field]))];
window.formatIDR = (n) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(n);
window.calcAvg = (arr) => arr.length ? Math.round(arr.reduce((a, b) => a + b, 0) / arr.length) : 0;
