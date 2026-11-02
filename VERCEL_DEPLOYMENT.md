# ANALYTIX - Vercel Deployment Guide

## Prerequisites

1. **Vercel Account**: Sign up at https://vercel.com
2. **Vercel CLI** (optional): `npm install -g vercel`
3. **Git Repository**: Push your code to GitHub, GitLab, or Bitbucket

---

## Deployment Methods

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push to Git Repository**
   ```bash
   cd "d:\WEBSITE\SAAS WB"
   git init
   git add .
   git commit -m "Initial commit - ANALYTIX"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to https://vercel.com/dashboard
   - Click "Add New..." → "Project"
   - Import your Git repository
   - Vercel will auto-detect the configuration from `vercel.json`

3. **Configure Project**
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as default)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be live at `https://your-project-name.vercel.app`

---

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from Project Directory**
   ```bash
   cd "d:\WEBSITE\SAAS WB"
   vercel
   ```

4. **Follow CLI Prompts**
   - Set up and deploy: **Y**
   - Which scope: Select your account
   - Link to existing project: **N**
   - Project name: `analytix` (or your preferred name)
   - Directory: `./`
   - Override settings: **N**

5. **Production Deployment**
   ```bash
   vercel --prod
   ```

---

## Important Notes for Vercel Deployment

### 1. **CSV Upload Limitations**

Vercel serverless functions have **ephemeral file systems**. This means:
- ❌ Uploaded CSV files will NOT persist between requests
- ❌ The `data/` folder is read-only in production
- ✅ Sample dataset works (embedded in deployment)

**Solutions for Production:**
- Use **Vercel Blob Storage** for file uploads
- Use **external storage** (AWS S3, Google Cloud Storage)
- Use **database** (PostgreSQL, MongoDB) to store CSV data
- Implement **session-based uploads** (store in memory per user session)

### 2. **Static Files**

The `vercel.json` configuration ensures static files are served correctly:
- CSS: `/static/css/style.css`
- JS: `/static/js/main.js`, `/static/js/charts.js`
- Images: `/static/images/placeholder-laptop.svg`

### 3. **Environment Variables** (Optional)

If you need environment variables:
```bash
vercel env add FLASK_ENV
# Enter value: production
```

Or add via Vercel Dashboard:
- Project Settings → Environment Variables

### 4. **Sample Dataset**

The included `data/sample_laptops.csv` will be accessible as read-only in production.

---

## File Structure for Vercel

```
SAAS WB/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── static/               # Static assets (auto-served)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/            # Flask templates
│   └── index.html
├── data/                 # Read-only in production
│   └── sample_laptops.csv
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel configuration
└── .vercelignore        # Files to ignore during deployment
```

---

## Testing Deployment

1. **After Deployment**, Vercel provides a URL like:
   ```
   https://analytix-xyz123.vercel.app
   ```

2. **Test Features**:
   - ✅ Homepage loads with dark theme
   - ✅ Sample dataset displays 30 products
   - ✅ Search, filter, sort functionality works
   - ✅ Analytics charts render correctly
   - ✅ Dataset statistics display
   - ✅ Download full dataset works
   - ⚠️ CSV upload (won't persist between requests)

3. **Check Browser Console** for any errors

---

## Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Wait for DNS propagation (up to 48 hours)

---

## Updating Deployment

### Via Git (Automatic)
```bash
git add .
git commit -m "Update features"
git push origin main
```
Vercel will auto-deploy on push.

### Via CLI
```bash
vercel --prod
```

---

## Troubleshooting

### Issue: "Module not found" errors
**Solution**: Ensure all dependencies are in `requirements.txt`
```bash
pip freeze > requirements.txt
```

### Issue: Static files not loading
**Solution**: Check `vercel.json` routes configuration

### Issue: CSV upload doesn't work
**Solution**: This is expected due to Vercel's serverless architecture. Implement one of the solutions mentioned above.

### Issue: Deployment fails
**Solution**: Check Vercel deployment logs in dashboard

---

## Local vs Production Differences

| Feature | Local (`python app.py`) | Vercel Production |
|---------|------------------------|-------------------|
| CSV Upload | ✅ Persists in `data/` folder | ❌ Ephemeral (doesn't persist) |
| Sample Dataset | ✅ Works | ✅ Works (read-only) |
| Search/Filter/Sort | ✅ Works | ✅ Works |
| Analytics Charts | ✅ Works | ✅ Works |
| Download CSV | ✅ Works | ✅ Works |
| Hot Reload | ✅ Yes (debug mode) | ❌ No |

---

## Recommended: Add Persistent Storage

For production-ready CSV upload functionality, add one of these:

### Option 1: Vercel Blob Storage
```bash
npm install -g @vercel/blob
```
Update `app.py` to use Vercel Blob API.

### Option 2: Supabase Storage (Free tier available)
1. Sign up at https://supabase.com
2. Create a bucket for CSV files
3. Update `app.py` with Supabase client

### Option 3: MongoDB Atlas (Free tier available)
1. Sign up at https://mongodb.com/cloud/atlas
2. Store CSV data in database
3. Update `app.py` with MongoDB connection

---

## Support

- Vercel Documentation: https://vercel.com/docs
- Vercel Python Runtime: https://vercel.com/docs/runtimes#official-runtimes/python

---

**Your ANALYTIX website is now ready for Vercel deployment! 🚀**
