// Global state
const state = {
    currentDataset: null,
    filteredProducts: [],
    allProducts: [],
    stats: {},
    currentFilters: {}
};

// Utility: Format price in IDR
function formatPrice(price) {
    if (!price || price === 0) return 'Rp 0';
    return 'Rp ' + Math.round(price).toLocaleString('id-ID');
}

// Utility: Format number with thousand separators
function formatNumber(num) {
    return Math.round(num).toLocaleString('id-ID');
}

// Utility: Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Generate star rating HTML
function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const emptyStars = 5 - fullStars;
    let html = '<span class="stars">';
    for (let i = 0; i < fullStars; i++) {
        html += '★';
    }
    for (let i = 0; i < emptyStars; i++) {
        html += '☆';
    }
    html += '</span>';
    return html;
}

// Load products from API
async function loadProducts(filters = {}) {
    try {
        const params = new URLSearchParams();
        
        if (filters.search) params.append('search', filters.search);
        if (filters.marketplace) params.append('marketplace', filters.marketplace);
        if (filters.brand) params.append('brand', filters.brand);
        if (filters.price_min) params.append('price_min', filters.price_min);
        if (filters.price_max) params.append('price_max', filters.price_max);
        if (filters.sort) params.append('sort', filters.sort);
        
        const response = await fetch(`/api/products?${params.toString()}`);
        const products = await response.json();
        
        state.filteredProducts = products;
        if (!filters || Object.keys(filters).length === 0) {
            state.allProducts = products;
        }
        
        renderProducts(products);
        updateProductCount(products.length);
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Render products to grid
function renderProducts(products) {
    const grid = document.getElementById('product-grid');
    
    if (!products || products.length === 0) {
        grid.innerHTML = '<p style="color: var(--text-secondary); grid-column: 1 / -1; text-align: center; padding: 40px;">No products found.</p>';
        return;
    }
    
    grid.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-image">
                <svg width="120" height="90" viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <!-- Laptop Screen -->
                    <rect x="15" y="10" width="90" height="55" rx="3" fill="#1a1a1a" stroke="#9580ff" stroke-width="2"/>
                    <rect x="15" y="10" width="90" height="8" fill="#9580ff" opacity="0.3"/>
                    
                    <!-- Screen Content -->
                    <rect x="25" y="25" width="20" height="15" rx="2" fill="#2a2a2a" stroke="#9580ff" stroke-width="1" opacity="0.5"/>
                    <rect x="50" y="25" width="20" height="15" rx="2" fill="#2a2a2a" stroke="#9580ff" stroke-width="1" opacity="0.5"/>
                    <rect x="75" y="25" width="20" height="15" rx="2" fill="#2a2a2a" stroke="#9580ff" stroke-width="1" opacity="0.5"/>
                    
                    <line x1="25" y1="50" x2="95" y2="50" stroke="#9580ff" stroke-width="1" opacity="0.3"/>
                    <line x1="25" y1="55" x2="80" y2="55" stroke="#9580ff" stroke-width="1" opacity="0.3"/>
                    
                    <!-- Laptop Base -->
                    <path d="M 5 65 L 15 65 L 15 70 Q 60 75 105 70 L 105 65 L 115 65 L 110 80 L 10 80 Z" fill="#1a1a1a" stroke="#9580ff" stroke-width="2"/>
                    
                    <!-- Brand Badge -->
                    <circle cx="60" cy="72" r="3" fill="#9580ff"/>
                </svg>
            </div>
            <div class="product-info">
                <h3 class="product-name">${product.product_name || 'Unknown Product'}</h3>
                <p class="product-price">${formatPrice(product.price)}</p>
                <div class="product-footer">
                    <span class="marketplace-badge">${product.marketplace || 'N/A'}</span>
                    <a href="${product.product_url || '#'}" target="_blank" class="product-link">
                        Lihat Produk →
                    </a>
                </div>
            </div>
        </div>
    `).join('');
}

// Update product count display
function updateProductCount(count) {
    const countDisplay = document.getElementById('product-count-display');
    countDisplay.textContent = `${formatNumber(count)} products`;
}

// Load and populate filter options
async function populateFilters() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        state.stats = stats;
        
        // Populate marketplace filter
        const marketplaceSelect = document.getElementById('marketplace-filter');
        if (stats.marketplaces && stats.marketplaces.length > 0) {
            stats.marketplaces.forEach(marketplace => {
                const option = document.createElement('option');
                option.value = marketplace;
                option.textContent = marketplace;
                marketplaceSelect.appendChild(option);
            });
        }
        
        // Populate brand filter
        const brandSelect = document.getElementById('brand-filter');
        if (stats.brands && stats.brands.length > 0) {
            stats.brands.forEach(brand => {
                const option = document.createElement('option');
                option.value = brand;
                option.textContent = brand;
                brandSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading filters:', error);
    }
}

// Apply filters
function applyFilters() {
    const filters = {
        search: document.getElementById('search-input').value.trim(),
        marketplace: document.getElementById('marketplace-filter').value,
        brand: document.getElementById('brand-filter').value,
        price_min: document.getElementById('price-min').value,
        price_max: document.getElementById('price-max').value,
        sort: document.getElementById('sort-select').value
    };
    
    state.currentFilters = filters;
    loadProducts(filters);
}

// Update dataset info display
async function updateDatasetInfo() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        document.getElementById('info-filename').textContent = stats.filename || '-';
        document.getElementById('info-total').textContent = formatNumber(stats.total_products || 0);
        document.getElementById('info-marketplaces').textContent = `${stats.unique_marketplaces || 0} marketplaces`;
        document.getElementById('info-brands').textContent = `${stats.unique_brands || 0} brands`;
        
        const priceRange = `${formatPrice(stats.price_min)} - ${formatPrice(stats.price_max)}`;
        document.getElementById('info-price-range').textContent = priceRange;
        
        if (stats.upload_timestamp) {
            const date = new Date(stats.upload_timestamp);
            document.getElementById('info-timestamp').textContent = date.toLocaleString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    } catch (error) {
        console.error('Error updating dataset info:', error);
    }
}

// Handle CSV upload
async function handleUpload(file) {
    const statusDiv = document.getElementById('upload-status');
    statusDiv.innerHTML = '<p>Processing CSV file...</p>';
    statusDiv.className = 'upload-status';
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Upload failed');
        }
        
        const stats = await response.json();
        
        statusDiv.innerHTML = `<p>✓ Successfully loaded ${formatNumber(stats.total_products)} products!</p>`;
        statusDiv.className = 'upload-status success';
        
        // Hide upload section after successful upload
        setTimeout(() => {
            document.getElementById('upload-section').style.display = 'none';
            initializeDataset();
        }, 1500);
        
    } catch (error) {
        statusDiv.innerHTML = '<p>✗ Error uploading file. Please try again.</p>';
        statusDiv.className = 'upload-status error';
        console.error('Upload error:', error);
    }
}

// Initialize dataset (after upload or on page load)
async function initializeDataset() {
    // Show dataset indicator
    document.getElementById('dataset-indicator').style.display = 'flex';
    
    // Load stats and update hero
    const response = await fetch('/api/stats');
    const stats = await response.json();
    
    if (stats.total_products) {
        document.getElementById('hero-product-count').textContent = 
            `${formatNumber(stats.total_products)} products available`;
    }
    
    // Load products and populate filters
    await loadProducts();
    await populateFilters();
    await updateDatasetInfo();
    
    // Initialize charts
    if (typeof initCharts === 'function') {
        initCharts();
    }
}

// Download handlers
async function downloadFull() {
    try {
        const response = await fetch('/download/full');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analytix_full_${Date.now()}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    } catch (error) {
        console.error('Download error:', error);
    }
}

async function downloadFiltered() {
    try {
        const params = new URLSearchParams(state.currentFilters);
        const response = await fetch(`/download/filtered?${params.toString()}`);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analytix_filtered_${Date.now()}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    } catch (error) {
        console.error('Download error:', error);
    }
}

// Mobile menu toggle
function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Check if sample dataset exists
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        if (stats.total_products && stats.total_products > 0) {
            // Dataset already loaded (sample)
            document.getElementById('upload-section').style.display = 'none';
            await initializeDataset();
        } else {
            // No dataset, show upload section
            document.getElementById('upload-section').style.display = 'block';
        }
    } catch (error) {
        // Show upload section if no dataset
        document.getElementById('upload-section').style.display = 'block';
    }
    
    // Setup event listeners
    document.getElementById('search-input').addEventListener('input', debounce(applyFilters, 300));
    document.getElementById('navbar-search').addEventListener('input', debounce((e) => {
        document.getElementById('search-input').value = e.target.value;
        applyFilters();
    }, 300));
    document.getElementById('marketplace-filter').addEventListener('change', applyFilters);
    document.getElementById('brand-filter').addEventListener('change', applyFilters);
    document.getElementById('price-min').addEventListener('input', debounce(applyFilters, 500));
    document.getElementById('price-max').addEventListener('input', debounce(applyFilters, 500));
    document.getElementById('sort-select').addEventListener('change', applyFilters);
    
    // Upload handlers
    document.getElementById('choose-file-btn').addEventListener('click', () => {
        document.getElementById('csv-file-input').click();
    });
    
    document.getElementById('csv-file-input').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            document.getElementById('file-name').textContent = file.name;
            document.getElementById('upload-btn').style.display = 'inline-block';
        }
    });
    
    document.getElementById('upload-btn').addEventListener('click', () => {
        const file = document.getElementById('csv-file-input').files[0];
        if (file) {
            handleUpload(file);
        }
    });
    
    // Download handlers
    document.getElementById('download-full-btn').addEventListener('click', downloadFull);
    document.getElementById('download-filtered-btn').addEventListener('click', downloadFiltered);
    
    // Mobile menu
    document.getElementById('mobile-menu-toggle').addEventListener('click', toggleMobileMenu);
});


// Animate numbers
function animateNumber(element, target) {
    const duration = 1500;
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target.toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}

// Smooth scroll for hero CTA buttons
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
