# ANALYTIX - Big Data Laptop Analytics Platform

A dark-themed, minimalist web platform for exploring and analyzing laptop product data scraped from Indonesian e-commerce marketplaces.

## Features

- **CSV Upload & Processing**: Upload and process laptop product datasets with automatic data cleaning and deduplication
- **Interactive Product Catalog**: Browse laptop products with real-time search, filtering, and sorting
- **Advanced Filters**: Filter by marketplace, brand, and price range
- **Data Analytics**: Five interactive Chart.js visualizations showing:
  - Product distribution by marketplace
  - Top 10 brands by product count
  - Price distribution histogram
  - Average price comparison across marketplaces
  - Average rating by marketplace
- **Dataset Statistics**: Real-time statistics including product counts, marketplace coverage, brand diversity, and price ranges
- **CSV Export**: Download full or filtered datasets
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Dark Minimalist UI**: Editorial-style design inspired by AOTY Explorer

## Tech Stack

- **Backend**: Python 3.8+, Flask 3.0, Pandas 2.1
- **Frontend**: HTML5, CSS3 (custom with CSS Grid/Flexbox), Vanilla JavaScript (ES6+)
- **Visualization**: Chart.js 4.x
- **Data Processing**: Pandas for CSV parsing, cleaning, and analytics

## Project Structure

```
SAAS WB/
├── app.py                      # Flask application with all routes
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── data/                       # CSV upload storage
│   └── sample_laptops.csv      # Sample dataset (demo purposes)
├── static/
│   ├── css/
│   │   └── style.css           # Dark minimalist styling
│   ├── js/
│   │   ├── main.js             # Core application logic
│   │   └── charts.js           # Chart.js visualizations
│   └── images/
│       └── placeholder-laptop.svg  # Product placeholder
└── templates/
    └── index.html              # Main HTML template
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd "d:\WEBSITE\SAAS WB"
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (Command Prompt):
     ```cmd
     venv\Scripts\activate.bat
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```
   Or alternatively:
   ```bash
   flask run
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. The application will automatically load the sample dataset (`sample_laptops.csv`) if available.

## CSV Format Requirements

Your CSV file must contain the following 10 columns:

| Column Name      | Data Type | Description                                    | Example                              |
|------------------|-----------|------------------------------------------------|--------------------------------------|
| `marketplace`    | String    | E-commerce platform name                       | Tokopedia, Shopee, Blibli, Lazada   |
| `product_name`   | String    | Full product name                              | ASUS VivoBook 14 A416JAO...         |
| `brand`          | String    | Laptop brand                                   | ASUS, Lenovo, HP, Acer, Dell        |
| `price`          | Number/String | Price in IDR (accepts multiple formats)    | 5499000 or Rp5.499.000 or Rp 5,499,000 |
| `rating`         | Float     | Product rating (0-5)                           | 4.7                                  |
| `review_count`   | Integer   | Number of reviews                              | 234                                  |
| `sold_count`     | Integer   | Number of units sold                           | 1200                                 |
| `seller_name`    | String    | Name of the seller                             | Asus Official Store                  |
| `seller_location`| String    | Seller location                                | Jakarta Pusat                        |
| `product_url`    | String    | Direct link to product page                    | https://tokopedia.com/...           |

### Price Format Handling

The system automatically handles various price formats:
- `5499000` (numeric)
- `Rp5.499.000` (with dot separators)
- `Rp 5,499,000` (with comma separators)
- `Rp 5499000` (with Rp prefix and no separators)

## Usage Guide

### Uploading a Dataset

1. If no dataset is loaded, you'll see an upload section on the homepage
2. Click "Choose CSV File" and select your CSV file
3. Click "Upload & Process" to process the dataset
4. The system will:
   - Parse and validate the CSV
   - Convert price formats to numeric values
   - Remove duplicate entries (same product_name + marketplace)
   - Calculate statistics
   - Display the data

### Browsing Products

- **Search**: Type keywords in the search box to filter by product name
- **Marketplace Filter**: Select a specific marketplace to view only those products
- **Brand Filter**: Filter products by laptop brand
- **Price Range**: Enter minimum and/or maximum price to filter
- **Sort Options**:
  - Price: Low to High
  - Price: High to Low
  - Rating: Highest

### Viewing Analytics

Scroll to the "Data Analytics" section to view five interactive charts showing:
- Distribution of products across marketplaces
- Most popular laptop brands
- Price distribution across different ranges
- Average prices by marketplace
- Average ratings by marketplace

### Downloading Data

- **Download Full Dataset**: Export all products as CSV
- **Download Filtered Dataset**: Export only the currently filtered products as CSV

## Sample Data

The project includes `data/sample_laptops.csv` with 30 sample laptop products from Indonesian e-commerce platforms. This is **demo data for testing purposes only**. Replace it with real scraped data for production use.

---

## Deployment to Vercel

ANALYTIX is fully configured for deployment to Vercel's serverless platform.

### Quick Deploy

1. **Push to Git repository**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Vercel**:
   - Go to https://vercel.com/new
   - Import your repository
   - Click "Deploy"

### Detailed Instructions

See **[VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)** for:
- Step-by-step deployment guide
- Vercel CLI deployment
- Custom domain setup
- Handling CSV uploads in serverless environment
- Persistent storage solutions
- Troubleshooting tips

### Important Notes for Vercel

- ✅ **Sample dataset works** out of the box (read-only)
- ✅ **All features work** (search, filter, analytics, charts)
- ⚠️ **CSV uploads won't persist** between requests (serverless limitation)
- 💡 See deployment guide for **persistent storage solutions** (Vercel Blob, Supabase, MongoDB)

### Files Added for Vercel

- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function entry point
- `.vercelignore` - Files to exclude from deployment
- `VERCEL_DEPLOYMENT.md` - Complete deployment guide

---

## Troubleshooting

### CSV Encoding Issues

If you encounter encoding errors when uploading a CSV:
- Ensure your CSV is saved with UTF-8 encoding
- The application will automatically try latin-1 encoding as a fallback

### Price Parsing

The system automatically strips common price prefixes and separators:
- Removes "Rp", dots (`.`), commas (`,`), and spaces
- Converts to numeric value
- Invalid prices default to 0

### Path with Spaces

Since the project folder path contains a space (`SAAS WB`), always use quotes when referencing paths in commands:
```bash
cd "d:\WEBSITE\SAAS WB"
```

### Port Already in Use

If port 5000 is already in use, you can specify a different port:
```bash
flask run --port 5001
```

## Development Notes

- **In-Memory Storage**: The current dataset is stored in memory (global variable). Restarting the server will clear the data.
- **File Uploads**: Uploaded CSV files are saved in the `data/` directory with timestamps.
- **No Database Required**: This is a CSV-based application and doesn't require a database for the MVP.
- **Auto-load**: If `data/sample_laptops.csv` exists, it's automatically loaded on server start.

## Design Philosophy

ANALYTIX follows a dark minimalist editorial design inspired by AOTY Explorer:
- Dark background (#0a0a0a) for reduced eye strain
- Lime green accent (#84cc16) for calls-to-action and highlights
- Maximum content width of 1120px for optimal readability
- Ample whitespace and breathing room
- Clean typography with modern sans-serif fonts
- Thin separator lines (1px, rgba(255,255,255,0.1))
- No excessive decoration, gradients, or glassmorphism
- Focus on content and data exploration

## License

MIT License - feel free to use and modify for your projects.

## Contributing

Contributions are welcome! Please ensure:
- Code follows the existing style and conventions
- Dark theme consistency is maintained
- Features are tested across desktop, tablet, and mobile
- CSV processing handles edge cases gracefully

---

**Note**: This platform is designed for exploring e-commerce data. Ensure you have the right to collect and use any data you upload, and comply with the terms of service of the platforms you're scraping from.
