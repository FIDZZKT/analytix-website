# 🚀 Panduan Deploy ANALYTIX ke Vercel

## 📋 Persiapan

### 1. Install Vercel CLI (jika belum)
Buka PowerShell/CMD dan jalankan:
```bash
npm install -g vercel
```

### 2. Cek Instalasi
```bash
vercel --version
```

---

## 🔐 Login ke Vercel

### Via CLI:
```bash
vercel login
```

Pilih metode login:
- **Email** (akan dapat link verifikasi)
- **GitHub** (recommended)
- **GitLab**
- **Bitbucket**

---

## 📤 Deploy Website

### Opsi 1: Deploy via CLI (Paling Mudah)

**Step 1:** Buka PowerShell/CMD, masuk ke folder project
```bash
cd "d:\WEBSITE\SAAS WB"
```

**Step 2:** Jalankan deploy command
```bash
vercel
```

**Step 3:** Ikuti Prompt Interaktif:
```
? Set up and deploy "d:\WEBSITE\SAAS WB"? [Y/n] Y
? Which scope do you want to deploy to? [pilih account Anda]
? Link to existing project? [N]
? What's your project's name? analytix-laptop
? In which directory is your code located? ./
? Want to override the settings? [N]
```

**Step 4:** Deploy!
Vercel akan otomatis:
- ✅ Build project
- ✅ Upload files
- ✅ Deploy ke URL production

**Step 5:** Dapatkan URL
Setelah selesai, akan muncul:
```
✅ Production: https://analytix-laptop.vercel.app
```

---

### Opsi 2: Deploy via Dashboard (Lebih Visual)

**Step 1:** Push ke GitHub
```bash
# Initialize git (jika belum)
git init
git add .
git commit -m "Deploy ANALYTIX to Vercel"

# Buat repository di GitHub, lalu:
git remote add origin https://github.com/USERNAME/analytix-laptop.git
git push -u origin main
```

**Step 2:** Import di Vercel Dashboard
1. Buka https://vercel.com/dashboard
2. Klik **"New Project"**
3. Klik **"Import Git Repository"**
4. Pilih repository: `analytix-laptop`
5. Klik **"Import"**

**Step 3:** Configure Project
- **Framework Preset:** Other
- **Root Directory:** ./
- **Build Command:** (kosongkan)
- **Output Directory:** (kosongkan)
- **Install Command:** pip install -r requirements.txt

**Step 4:** Deploy
Klik **"Deploy"** dan tunggu ~2-3 menit

---

## ⚙️ Konfigurasi Environment Variables (Optional)

Jika ada secret keys atau konfigurasi khusus:

### Via CLI:
```bash
vercel env add SECRET_KEY
```

### Via Dashboard:
1. Buka project di dashboard
2. **Settings** → **Environment Variables**
3. Tambahkan:
   - `SECRET_KEY` = your-secret-key
   - `FLASK_ENV` = production

---

## 🔄 Update & Redeploy

### Setiap kali ada perubahan:

**Via CLI:**
```bash
vercel --prod
```

**Via GitHub (jika pakai Opsi 2):**
```bash
git add .
git commit -m "Update: ..."
git push
```
Vercel akan auto-deploy setiap push!

---

## 🌐 Custom Domain (Optional)

### Via CLI:
```bash
vercel domains add yourdomain.com
```

### Via Dashboard:
1. Project → **Settings** → **Domains**
2. Add domain: `analytix.yourdomain.com`
3. Update DNS di registrar Anda:
   - Type: `CNAME`
   - Name: `analytix`
   - Value: `cname.vercel-dns.com`

---

## 🐛 Troubleshooting

### Error: "No such file or directory: 'data/...'"
**Solusi:** CSV file tidak ter-upload. Gunakan storage eksternal:
- Vercel KV (key-value database)
- Supabase
- MongoDB Atlas

### Error: "Module not found"
**Solusi:** 
```bash
vercel dev  # Test local dulu
```
Pastikan semua dependencies ada di `requirements.txt`

### Error: "Function timeout"
**Solusi:** Vercel serverless timeout max 10s (hobby) / 60s (pro)
- Optimasi query
- Cache data
- Upgrade ke Vercel Pro

---

## 📊 Analytics & Monitoring

Setelah deploy, Anda bisa monitor:
- **Traffic:** Dashboard → Analytics
- **Logs:** Dashboard → Deployments → View Function Logs
- **Performance:** Dashboard → Speed Insights

---

## 🎯 Hasil Akhir

Setelah deploy berhasil, website bisa diakses di:

```
https://analytix-laptop.vercel.app
```

atau custom domain Anda!

---

## 💡 Tips

1. **Gunakan GitHub:** Auto-deploy setiap push
2. **Preview Deployments:** Setiap branch = preview URL
3. **Rollback:** Bisa rollback ke deployment sebelumnya via dashboard
4. **Custom Domain:** Gratis SSL certificate
5. **Environment Variables:** Jangan commit sensitive data

---

## 📞 Support

- Documentation: https://vercel.com/docs
- Community: https://github.com/vercel/vercel/discussions
- Discord: https://vercel.com/discord

---

**Selamat Deploy! 🚀**
