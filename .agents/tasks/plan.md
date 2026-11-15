# Implementation Plan — Analytix Big Data Analytics Platform

**Project root:** `C:\Users\agung\Downloads\Analytix`
**Stack:** Pure HTML/CSS/JS frontend (no build step) + Python Flask backend + MySQL database

---

## Architecture Decisions

- **No build tool for frontend.** All 8 pages are standalone `.html` files that load shared CSS/JS via relative `<link>` and `<script>` tags. This matches the school-project brief, requires no npm, and lets pages open directly in a browser without running a dev server.
- **Chart.js from CDN.** Loaded via `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js">` in every page that needs charts. No bundler needed.
- **data.js as the single source of truth for demo data.** All frontend JS files import from `../js/data.js` so the 50+ laptop records only exist in one place. When Flask is connected, the JS files switch to `fetch('/api/...')` calls instead.
- **Flask serves the frontend.** `app.py` uses `send_from_directory` to serve the `frontend/` folder at `/`, so there is a single origin and no CORS complexity. The Flask API lives at `/api/*`.
- **SQLAlchemy + PyMySQL** for the ORM layer so `database.py` works with plain Python dicts and is easy to swap for a different driver.
- **MySQL schema uses foreign keys.** `products` ← `prices` (marketplace-keyed), `products` ← `reviews`, `products` ← `sellers`. One product can have offers from multiple marketplaces.
- **Prediction page is clearly labelled "simulasi."** A heuristic formula (weighted brand+RAM+GPU lookup table) is used when the ML model file is absent, with a banner stating the model is not connected.

---

## Sequencing Constraints

1. `data.js` must exist before any page JS file that references it.
2. `style.css` and `sidebar.css` must exist before any HTML page is written (they are linked in every page).
3. All HTML pages share the same sidebar markup — write a consistent sidebar block once, then replicate it.
4. `backend/models/database.py` must exist before the route files import it.
5. `backend/config.py` must exist before `app.py` imports it.
6. `database/schema.sql` is standalone — no dependency on Flask files — but should be written before routes so column names are already decided.
7. `backend/data/laptops_demo.csv` columns must exactly match `database/schema.sql` column names used in the seed script inside `database.py`.

---

## Risks

- **MySQL not installed.** Flask falls back gracefully: if the DB connection fails, every API route returns the demo CSV data instead. This is coded explicitly in `database.py`.
- **Python version.** Requirements pin to Flask 3.0.x and SQLAlchemy 2.x, which require Python 3.9+.
- **Chart.js CDN offline.** All chart canvases show a fallback `<p>` message if the CDN fails to load — handled in each JS file with a `typeof Chart === 'undefined'` guard.
- **Orange Data Mining integration.** The prediction route accepts an optional exported model file (`model.pkl`). If absent, the heuristic runs. No mock numbers are presented as real ML output.

---

## Implementation Plan

- [ ] 1. **Create the project directory tree (no files yet, just folders).**

  Create all subdirectories so subsequent steps can write files without worrying about parent paths:

  ```
  C:\Users\agung\Downloads\Analytix\
  ├── frontend\
  │   ├── css\
  │   ├── js\
  │   └── pages\
  ├── backend\
  │   ├── routes\
  │   ├── models\
  │   └── data\
  └── database\
  ```

  Files: (directories only, no files)
  Verify: `Get-ChildItem C:\Users\agung\Downloads\Analytix -Recurse -Directory` — all 8 directories present.

---

- [ ] 2. **Create `backend/data/laptops_demo.csv` — 55 laptop records.**

  This comes first because column names anchor every subsequent data contract. CSV columns:
  `id, name, brand, processor, ram_gb, storage_gb, storage_type, gpu, screen_size, marketplace, price, rating, review_count, seller, image_url, scraped_date`

  Brands: Asus, Lenovo, HP, Acer, Dell, MSI, Apple, Samsung — at least 7 brands. Marketplaces: Shopee, Tokopedia, Lazada, Blibli — all 4. Price range: Rp 3.500.000 – Rp 35.000.000. RAM: 4, 8, 16, 32 GB. GPU types: Integrated, NVIDIA GTX, NVIDIA RTX, AMD Radeon.

  Files: `backend/data/laptops_demo.csv`
  Verify: `(Import-Csv C:\Users\agung\Downloads\Analytix\backend\data\laptops_demo.csv).Count` → 55.

---

- [ ] 3. **Create `database/schema.sql` — full MySQL schema for `laptop_bigdata`.**

  Five tables with proper foreign keys:
  - `marketplaces(id, name, url, logo_url)`
  - `products(id, name, brand, processor, ram_gb, storage_gb, storage_type, gpu, screen_size, image_url)`
  - `sellers(id, name, marketplace_id FK, seller_url, rating)`
  - `prices(id, product_id FK, marketplace_id FK, seller_id FK, price, scraped_date)`
  - `reviews(id, product_id FK, marketplace_id FK, rating, review_count, scraped_date)`

  Include: `CREATE DATABASE IF NOT EXISTS laptop_bigdata;`, `USE laptop_bigdata;`, `SET FOREIGN_KEY_CHECKS`, and a seed block that inserts the 4 marketplace rows.

  Files: `database/schema.sql`
  Verify: Open the file in a text editor and confirm all 5 `CREATE TABLE` statements and the 4 marketplace seed `INSERT` statements are present. (No MySQL required to pass plan.)

---

- [ ] 4. **Create `frontend/css/style.css` — global design system.**

  CSS custom properties (variables) for the full color palette:
  - `--color-primary: #0d2b6e` (dark blue)
  - `--color-secondary: #1a73e8` (light blue)
  - `--color-bg: #f0f4ff`
  - `--color-surface: #ffffff`
  - `--color-text: #1e2a45`
  - `--color-muted: #6b7a99`
  - `--color-accent: #00c6ff`
  - Font: `Inter` from Google Fonts

  Include: CSS reset, card component (`.card`), stat card (`.stat-card`), badge (`.badge`), button variants (`.btn`, `.btn-primary`, `.btn-outline`), table styles (`.data-table`), loading skeleton (`.skeleton`), responsive grid (`.grid-auto`), and utility classes.

  Files: `frontend/css/style.css`
  Verify: Open `frontend/pages/index.html` in a browser (after step 6) — no FOUC, correct colors, font loads.

---

- [ ] 5. **Create `frontend/css/sidebar.css` — sidebar layout and navigation styles.**

  Fixed left sidebar (250 px wide on desktop), collapsible on mobile via a hamburger toggle. Styles for:
  - `.sidebar` with the Analytix logo block at top
  - `.nav-item` with hover and `.active` states using `--color-secondary`
  - `.main-content` with `margin-left: 250px` on desktop
  - `@media (max-width: 768px)` rules that hide the sidebar and show a top-bar hamburger

  Files: `frontend/css/sidebar.css`
  Verify: Visually confirm sidebar renders correctly in `index.html` after step 6.

---

- [ ] 6. **Create `frontend/js/data.js` — shared demo dataset and helper functions.**

  Export a single `DEMO_DATA` array of 55 objects (matching the CSV columns from step 2) plus these helpers:
  - `getStats()` → `{ totalProducts, totalMarketplaces, totalBrands, avgPrice, cheapestProduct }`
  - `filterProducts(filters)` → filtered + sorted array
  - `getByBrand()` → `{ brand: count }` map
  - `getPriceDistribution(buckets)` → array of `{ label, count }`
  - `getMarketplaceAvgPrice()` → `{ marketplace: avgPrice }` map
  - `getRAMDistribution()` → `{ ram: count }` map
  - `getGPUDistribution()` → `{ gpu: count }` map
  - `getComparisonByName(name)` → array of same-name products across marketplaces

  **Important:** Keep data strictly inline (no `fetch`). Every number must match the CSV from step 2.

  Files: `frontend/js/data.js`
  Verify: Open browser console on any HTML page and run `DEMO_DATA.length` → 55; `getStats().totalBrands` → 8.

---

- [ ] 7. **Create `frontend/pages/index.html` — Dashboard page.**

  Sidebar navigation with 8 menu items (links to `./products.html`, `./comparison.html`, etc.). Main content:
  - 5 stat cards (total products, total marketplaces, total brands, avg price, cheapest product)
  - Bar chart: avg price per marketplace (Chart.js)
  - Bar chart: product count per brand (Chart.js)
  - Doughnut chart: price distribution (Chart.js)
  - Two smaller charts: RAM distribution, GPU distribution
  - Footer row: "Data terakhir diperbarui: [date from data.js]"

  Links: `../css/style.css`, `../css/sidebar.css`, Chart.js CDN, `../js/data.js`, `../js/dashboard.js`

  Files: `frontend/pages/index.html`
  Verify: Open in browser — all 5 stat cards show correct numbers, all 5 charts render without console errors.

---

- [ ] 8. **Create `frontend/js/dashboard.js` — Dashboard page logic.**

  Reads `DEMO_DATA` via `getStats()`, `getMarketplaceAvgPrice()`, `getByBrand()`, `getPriceDistribution()`, `getRAMDistribution()`, `getGPUDistribution()`, then:
  - Injects stat card values into the DOM
  - Instantiates 5 Chart.js instances
  - Adds `Chart === undefined` guard that shows a fallback message per canvas

  Files: `frontend/js/dashboard.js`
  Verify: Open `index.html` in browser — no JS errors in console, stat cards and charts populated.

---

- [ ] 9. **Create `frontend/pages/products.html` + `frontend/js/products.js` — Product Catalog page.**

  HTML: sidebar, search bar, filter panel (marketplace checkboxes, brand checkboxes, price range slider, RAM select, GPU select), sort dropdown (termurah / termahal), product card grid, pagination controls.

  JS (`products.js`):
  - On load, render all 55 products as cards
  - Each card: image placeholder, product name, brand badge, price, rating stars, marketplace badge, "Lihat Detail" button that opens a modal
  - Modal shows full specs (processor, RAM, storage, GPU, screen size, seller)
  - Search input filters in real time (`input` event)
  - All filter controls trigger `filterProducts(filters)` and re-render
  - Pagination: 12 cards per page

  Files: `frontend/pages/products.html`, `frontend/js/products.js`
  Verify: Open in browser — search for "asus" shows only Asus products; price filter narrows list; modal opens on "Lihat Detail".

---

- [ ] 10. **Create `frontend/pages/comparison.html` + `frontend/js/comparison.js` — Price Comparison page.**

  HTML: sidebar, search/autocomplete input for product name, comparison table with columns (Marketplace, Harga, Rating, Seller, Status).

  JS (`comparison.js`):
  - Autocomplete suggests product names as user types (from `DEMO_DATA` unique names)
  - On selection, calls `getComparisonByName(name)` to find same-product rows across marketplaces
  - Renders comparison table: highlights cheapest price row with a green badge, shows price gap and savings potential
  - If fewer than 2 marketplaces have the product, shows "Produk ini hanya tersedia di 1 marketplace"

  Files: `frontend/pages/comparison.html`, `frontend/js/comparison.js`
  Verify: Search "Asus VivoBook 14" — table shows rows for each marketplace with the lowest price highlighted.

---

- [ ] 11. **Create `frontend/pages/analysis.html` + `frontend/js/analysis.js` — Big Data Analysis page.**

  HTML: sidebar, 8 chart cards in a responsive 2-column grid, each with title, canvas, and data-source caption.

  JS (`analysis.js`) — instantiates 8 Chart.js charts:
  1. Bar: avg price per marketplace
  2. Histogram (bar): price distribution in 5 buckets
  3. Horizontal bar: brand availability count
  4. Scatter: RAM vs. price (x=RAM, y=price)
  5. Scatter: GPU tier vs. price
  6. Doughnut: processor distribution (Intel Core i3/i5/i7/i9, AMD Ryzen)
  7. Grouped bar: avg rating per marketplace
  8. Line: scraped_date trend (uses `scraped_date` from demo data, groups by week)

  Files: `frontend/pages/analysis.html`, `frontend/js/analysis.js`
  Verify: Open in browser — 8 charts render; tooltip shows on hover; no console errors.

---

- [ ] 12. **Create `frontend/pages/trends.html` + `frontend/js/trends.js` — Price Trends page.**

  HTML: sidebar, product search input, line chart canvas, summary cards (harga tertinggi, terendah, perubahan %).

  JS (`trends.js`):
  - Checks if product has multiple `scraped_date` entries in `DEMO_DATA`
  - If yes: renders line chart with dates on x-axis, price on y-axis, one line per marketplace
  - **If no historical data exists:** displays a styled info box: "Riwayat harga untuk produk ini belum tersedia. Data akan muncul setelah beberapa periode pengambilan data." — does NOT fabricate fake trend data.
  - Summary cards only shown when real multi-date data exists

  Files: `frontend/pages/trends.html`, `frontend/js/trends.js`
  Verify: Open in browser, search any product — info box appears if no multi-date data; no fake price lines rendered.

---

- [ ] 13. **Create `frontend/pages/prediction.html` + `frontend/js/prediction.js` — Price Prediction page.**

  HTML: sidebar, prominent "⚠️ Fitur Simulasi" banner (orange), form inputs (brand select, processor select, RAM select, storage select, GPU select, screen size number), "Prediksi Harga" button, result card.

  JS (`prediction.js`):
  - On form submit: first tries `fetch('/api/predict', { method:'POST', body: JSON.stringify(inputs) })`
  - On network error / non-200: falls back to a heuristic lookup table (base price per brand + RAM multiplier + GPU tier premium)
  - Result card always shows: estimated price range, and a note "Hasil ini berasal dari simulasi heuristik, bukan model Machine Learning terlatih."
  - If API returns `{ model_connected: true }`, note changes to "Hasil berasal dari model ML (Orange Data Mining)."

  Files: `frontend/pages/prediction.html`, `frontend/js/prediction.js`
  Verify: Open in browser, fill form and click Prediksi — result card appears with heuristic price and disclaimer note; no claim of real ML output.

---

- [ ] 14. **Create `frontend/pages/recommendation.html` + `frontend/js/recommendation.js` — Recommendation page.**

  HTML: sidebar, filter form (budget range, brand multi-select, min RAM select, min storage select, GPU type select, use-case radio: Sekolah / Pekerjaan / Desain / Gaming), "Cari Rekomendasi" button, results grid.

  JS (`recommendation.js`):
  - Scoring function: price ≤ budget (+3), brand match (+1), RAM ≥ minRam (+2), storage ≥ minStorage (+1), GPU match (+2), use-case match (+2 if applicable specs)
  - Renders products sorted by score descending, with score badge on each card
  - Use-case presets: Gaming → GPU must contain "GTX" or "RTX"; Desain → RAM ≥ 16; Sekolah → price ≤ Rp 8.000.000; Pekerjaan → RAM ≥ 8

  Files: `frontend/pages/recommendation.html`, `frontend/js/recommendation.js`
  Verify: Set use-case to Gaming, click Cari — only products with dedicated GPU appear at top of list.

---

- [ ] 15. **Create `frontend/pages/about.html` — About Analytix page.**

  Static HTML: sidebar, hero section with Analytix logo SVG (inline), project description, tech stack table (HTML/CSS/JS, Chart.js, Python Flask, MySQL, Pandas, Orange Data Mining), team/school info placeholder, disclaimer that data is for educational purposes.

  Files: `frontend/pages/about.html`
  Verify: Opens in browser without errors; sidebar navigation works.

---

- [ ] 16. **Create `backend/config.py` — Flask configuration.**

  Python dataclass / plain class `Config` with:
  - `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB` read from `os.environ` with safe defaults
  - `DEMO_CSV_PATH`: absolute path to `backend/data/laptops_demo.csv`
  - `SECRET_KEY`: `os.environ.get('SECRET_KEY', 'analytix-dev-key')`
  - `ML_MODEL_PATH`: `os.environ.get('MODEL_PATH', None)` — None means simulation mode

  Files: `backend/config.py`
  Verify: `python -c "from config import Config; print(Config.MYSQL_DB)"` inside `backend/` → prints `laptop_bigdata`.

---

- [ ] 17. **Create `backend/models/database.py` — database connection and CSV fallback.**

  `get_db_connection()` tries `pymysql.connect(...)` using `Config` values; on any exception logs a warning and returns `None`.

  `query(sql, params)` helper: if connection is None, raises `RuntimeError('db_unavailable')`.

  `load_demo_csv()`: reads `Config.DEMO_CSV_PATH` with `pandas.read_csv()`, returns list of dicts with all columns cast to correct Python types (price → int, rating → float, etc.).

  Files: `backend/models/database.py`
  Verify: `python -c "from models.database import load_demo_csv; print(len(load_demo_csv()))"` inside `backend/` → prints `55`.

---

- [ ] 18. **Create `backend/routes/products.py` — Flask blueprint for `/api/products`.**

  Blueprint `products_bp` registered at `/api/products`. Routes:
  - `GET /api/products` — query params: `search`, `brand`, `marketplace`, `min_price`, `max_price`, `ram`, `gpu`, `sort` (`price_asc` / `price_desc`), `page` (default 1), `per_page` (default 12)
  - `GET /api/products/<int:id>` — single product detail

  Logic: try DB query first; on `RuntimeError('db_unavailable')` fall back to filtering `load_demo_csv()` in Python. Return JSON: `{ data: [...], total, page, per_page }`.

  Files: `backend/routes/products.py`
  Verify: `python app.py` in `backend/` then `curl http://localhost:5000/api/products` returns JSON with a `data` array of 55 items.

---

- [ ] 19. **Create `backend/routes/analysis.py` — Flask blueprint for `/api/analysis`.**

  Blueprint `analysis_bp` at `/api/analysis`. Routes:
  - `GET /api/analysis/summary` → marketplace avg prices, brand counts, price distribution, RAM distribution, GPU distribution, processor distribution, avg rating per marketplace
  - `GET /api/analysis/trends` → grouped price data by `scraped_date`

  All computations done with Pandas on the CSV (or DB if available). Return pre-computed chart-ready JSON that the frontend JS can pass directly to Chart.js `data.datasets`.

  Files: `backend/routes/analysis.py`
  Verify: `curl http://localhost:5000/api/analysis/summary` returns JSON with keys `marketplace_avg_price`, `brand_counts`, `price_distribution`.

---

- [ ] 20. **Create `backend/routes/prediction.py` — Flask blueprint for `/api/predict`.**

  Blueprint `prediction_bp` at `/api/predict`. One route:
  - `POST /api/predict` — body: `{ brand, processor, ram_gb, storage_gb, gpu, screen_size }`

  Logic:
  1. If `Config.ML_MODEL_PATH` is set and the file exists: load with `pickle.load`, call `model.predict([[ram_gb, price_weight_for_brand, gpu_tier]])`, return `{ predicted_price, model_connected: true }`.
  2. Otherwise: heuristic lookup table → return `{ predicted_price_min, predicted_price_max, model_connected: false, note: "Hasil dari simulasi heuristik." }`.

  Input validation with `flask.request.get_json()` — return 400 if required fields missing.

  Files: `backend/routes/prediction.py`
  Verify: `curl -X POST http://localhost:5000/api/predict -H "Content-Type: application/json" -d '{"brand":"Asus","processor":"Intel Core i5","ram_gb":8,"storage_gb":512,"gpu":"Integrated","screen_size":14}'` → returns JSON with `model_connected: false` and a price range.

---

- [ ] 21. **Create `backend/app.py` — Flask application entry point.**

  Creates Flask app, registers the 3 blueprints, serves the `frontend/` directory at `/` using `send_from_directory`, and adds a `404` handler that returns the requested page or the index if not found.

  ```python
  from flask import Flask, send_from_directory
  from config import Config
  from routes.products import products_bp
  from routes.analysis import analysis_bp
  from routes.prediction import prediction_bp
  import os

  app = Flask(__name__, static_folder=None)
  app.config.from_object(Config)

  app.register_blueprint(products_bp)
  app.register_blueprint(analysis_bp)
  app.register_blueprint(prediction_bp)

  FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

  @app.route('/', defaults={'path': 'pages/index.html'})
  @app.route('/<path:path>')
  def serve_frontend(path):
      return send_from_directory(FRONTEND_DIR, path)

  if __name__ == '__main__':
      app.run(debug=True, port=5000)
  ```

  Files: `backend/app.py`
  Verify: `python app.py` starts without import errors; `http://localhost:5000/` serves the dashboard HTML.

---

- [ ] 22. **Create `backend/requirements.txt` — pinned Python dependencies.**

  ```
  Flask==3.0.3
  flask-cors==4.0.1
  SQLAlchemy==2.0.30
  PyMySQL==1.1.1
  pandas==2.2.2
  numpy==1.26.4
  scikit-learn==1.5.0
  python-dotenv==1.0.1
  ```

  Files: `backend/requirements.txt`
  Verify: `pip install -r requirements.txt` completes without dependency conflicts (run in a venv).

---

## Final Checklist (run after all steps complete)

- `python backend/app.py` starts on port 5000 without errors.
- Opening `http://localhost:5000/` loads the Dashboard with 5 stat cards and 5 charts.
- All 8 sidebar links navigate to the correct pages.
- Product catalog: search, filter, and modal all work.
- Comparison page: selecting a product shows a multi-marketplace table.
- Trends page: shows "belum tersedia" message (no fabricated data).
- Prediction page: shows heuristic result with simulation disclaimer.
- Recommendation page: Gaming filter returns only discrete-GPU laptops.
- `http://localhost:5000/api/products` returns 55-item JSON array.
- No console errors on any page.
