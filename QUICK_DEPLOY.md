# ⚡ Quick Deploy ANALYTIX ke Vercel

## 🎯 Cara Tercepat (5 Menit)

### Step 1: Install Vercel CLI
```powershell
npm install -g vercel
```

### Step 2: Login
```powershell
vercel login
```
Pilih **GitHub** atau **Email**

### Step 3: Deploy
```powershell
cd "d:\WEBSITE\SAAS WB"
vercel --prod
```

### Step 4: Selesai! 🎉
URL production Anda: `https://analytix-[random].vercel.app`

---

## 🤖 Atau Gunakan Script Otomatis

```powershell
.\deploy.ps1
```

Pilih option **1** untuk production deploy!

---

## 📝 Catatan Penting

### ⚠️ Batasan Vercel (Free Plan):
- ✅ **Unlimited** deployments
- ⚠️ **10 second** function timeout
- ⚠️ **No persistent storage** (CSV akan reset setiap deploy)

### 💡 Solusi untuk Data Persisten:
1. **Gunakan Database Cloud:**
   - Supabase (Free tier: 500MB)
   - MongoDB Atlas (Free tier: 512MB)
   - Vercel KV

2. **Upload CSV via Admin setiap deploy:**
   - Login admin → Upload CSV
   - Data tersimpan selama session

---

## 🔄 Update Website

Setelah edit code:
```powershell
vercel --prod
```

Vercel akan auto-deploy versi terbaru!

---

## 🌐 Custom Domain (Optional)

### Tambah domain:
```powershell
vercel domains add yourdomain.com
```

### Update DNS di domain registrar:
- **Type:** CNAME
- **Name:** @ atau subdomain
- **Value:** cname.vercel-dns.com

---

## 📱 Akses Dashboard

```powershell
# Buka di browser
start https://vercel.com/dashboard
```

Atau via script:
```powershell
.\deploy.ps1
```
Pilih option **5**

---

## ❓ Troubleshooting

### Error: "vercel: command not found"
**Fix:** Restart terminal setelah install vercel CLI

### Error: "Authentication required"
**Fix:** Run `vercel login` lagi

### Website tidak muncul
**Fix:** Tunggu 2-3 menit, Vercel masih building

### Data CSV tidak ada
**Fix:** Normal! Upload via admin dashboard setelah deploy

---

**Support:** Baca `DEPLOY_TO_VERCEL.md` untuk panduan lengkap

**Ready? Let's Deploy! 🚀**
