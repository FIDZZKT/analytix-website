# ANALYTIX - Quick Deploy Script untuk Vercel
# PowerShell Script

Write-Host "🚀 ANALYTIX - Vercel Deployment Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Vercel CLI is installed
Write-Host "📦 Checking Vercel CLI..." -ForegroundColor Yellow
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue

if (-not $vercelInstalled) {
    Write-Host "❌ Vercel CLI tidak ditemukan!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install Vercel CLI dengan command:" -ForegroundColor Yellow
    Write-Host "npm install -g vercel" -ForegroundColor Green
    Write-Host ""
    exit 1
}

Write-Host "✅ Vercel CLI ditemukan: $($vercelInstalled.Version)" -ForegroundColor Green
Write-Host ""

# Ask user what to do
Write-Host "Pilih aksi:" -ForegroundColor Cyan
Write-Host "1. Deploy ke Production" -ForegroundColor White
Write-Host "2. Deploy Preview (Testing)" -ForegroundColor White
Write-Host "3. Test Local (vercel dev)" -ForegroundColor White
Write-Host "4. Check Status" -ForegroundColor White
Write-Host "5. Open Dashboard" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Masukkan pilihan (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🚀 Deploying ke PRODUCTION..." -ForegroundColor Green
        Write-Host ""
        vercel --prod
    }
    "2" {
        Write-Host ""
        Write-Host "🧪 Deploying PREVIEW..." -ForegroundColor Yellow
        Write-Host ""
        vercel
    }
    "3" {
        Write-Host ""
        Write-Host "💻 Starting local development server..." -ForegroundColor Cyan
        Write-Host ""
        vercel dev
    }
    "4" {
        Write-Host ""
        Write-Host "📊 Project Status:" -ForegroundColor Cyan
        Write-Host ""
        vercel ls
    }
    "5" {
        Write-Host ""
        Write-Host "🌐 Opening Vercel Dashboard..." -ForegroundColor Cyan
        Start-Process "https://vercel.com/dashboard"
    }
    default {
        Write-Host ""
        Write-Host "❌ Pilihan tidak valid!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Selesai!" -ForegroundColor Green
Write-Host ""
