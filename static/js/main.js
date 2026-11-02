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
                <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="8" y="12" width="48" height="32" rx="2" stroke="white" stroke-width="2"/>
                    <rect x="4" y="44" width="56" height="4" rx="1" stroke="white" stroke-width="2"/>
                </svg>
            </div>
            <h3 class="product-name">${product.product_name || 'Unknown Product'}</h3>
            <p class="product-brand">${product.brand || 'Unknown'}</p>
            <p class="product-price">${formatPrice(product.price)}</p>
            <div class="product-meta">
                <span class="marketplace-badge">${product.marketplace || 'N/A'}</span>
                <span class="product-rating">
                    ${generateStars(product.rating || 0)}
                    ${(product.rating || 0).toFixed(1)}
                </span>
            </div>
            <a href="${product.product_url || '#'}" target="_blank" class="product-link">View Product →</a>
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
