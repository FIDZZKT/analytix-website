# ANALYTIX - Quick Start Guide

Get ANALYTIX running in 3 minutes!

## Prerequisites

- Python 3.8 or higher installed
- Terminal/PowerShell access

## Installation & Setup

### Option 1: Quick Start (Use Sample Data)

```powershell
# 1. Navigate to project directory
cd "d:\WEBSITE\SAAS WB"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start the server
python app.py
```

### Option 2: Using System Python (No Virtual Environment)

```powershell
# 1. Navigate to project directory
cd "d:\WEBSITE\SAAS WB"

# 2. Install dependencies globally
pip install flask pandas python-dateutil

# 3. Start the server
python app.py
```

## Access the Application

Once the server starts, you'll see:
```
* Running on http://127.0.0.1:5000
Sample dataset loaded: 30 products
```

**Open your browser** and go to:
```
http://localhost:5000
```

## What You'll See

✓ Dark themed homepage with ANALYTIX branding
✓ 30 sample laptop products already loaded
✓ Green "DATASET LOADED" indicator in navbar
✓ Hero section showing "30 products available"
✓ Product grid with laptop cards
✓ Analytics charts with marketplace and brand data
✓ Dataset statistics section

## Try These Features

1. **Search**: Type "ASUS" in the search box → filters to ASUS laptops
2. **Filter by Marketplace**: Select "Tokopedia" dropdown → shows only Tokopedia products
3. **Filter by Brand**: Select "Lenovo" dropdown → shows only Lenovo laptops
4. **Price Range**: Enter min 5000000, max 10000000 → filters by price
5. **Sort**: Select "Price: Low to High" → reorders products
6. **View Analytics**: Scroll to charts section → see 5 visualizations
7. **Download**: Click "Download Full Dataset" → exports CSV file
8. **Upload New Data**: Click upload button (if visible) → process your own CSV

## Upload Your Own Data

Your CSV must have these 10 columns:
```
marketplace, product_name, brand, price, rating, review_count,
sold_count, seller_name, seller_location, product_url
```

Example row:
```csv
Tokopedia,ASUS VivoBook 14,ASUS,Rp5.499.000,4.7,234,1200,Asus Store,Jakarta,https://...
```

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Troubleshooting

### "Python was not found"
Install Python from https://python.org or Microsoft Store

### "No module named 'flask'"
Run: `pip install -r requirements.txt`

### "Port 5000 already in use"
Run: `python app.py` or `flask run --port 5001`

### "Permission denied" when activating venv
Run PowerShell as Administrator or use:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Next Steps

- Read `README.md` for full documentation
- Check `VERIFICATION.md` for testing checklist
- Review `IMPLEMENTATION_SUMMARY.md` for technical details
- Explore the code in `app.py`, `static/js/main.js`, and `templates/index.html`

## Support

If you encounter issues:
1. Check Python version: `python --version` (should be 3.8+)
2. Verify dependencies: `pip list | findstr "flask pandas"`
3. Check port availability: `netstat -ano | findstr :5000`
4. Review console output for error messages

---

**Enjoy exploring laptop data with ANALYTIX!** 🚀
