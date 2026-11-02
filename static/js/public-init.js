// Initialize public website
document.addEventListener('DOMContentLoaded', async () => {
    // Check if dataset exists (loaded by admin)
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        if (stats.total_products && stats.total_products > 0) {
            // Dataset available, show products
            document.getElementById('products').style.display = 'block';
            document.getElementById('analytics').style.display = 'block';
            document.getElementById('dataset').style.display = 'block';
            
            // Show dataset indicator
            document.getElementById('dataset-indicator').style.display = 'flex';
            
            // Load products and populate filters
            await loadProducts();
            await populateFilters();
            await updateDatasetInfo();
            
            // Initialize charts
            if (typeof initCharts === 'function') {
                initCharts();
            }
        } else {
            // No dataset, show message
            showNoDataMessage();
        }
    } catch (error) {
        // No dataset available
        showNoDataMessage();
    }
    
    // Setup event listeners for filters (with null checks)
    const searchInput = document.getElementById('search-input');
    const navbarSearch = document.getElementById('navbar-search');
    const marketplaceFilter = document.getElementById('marketplace-filter');
    const brandFilter = document.getElementById('brand-filter');
    const priceMin = document.getElementById('price-min');
    const priceMax = document.getElementById('price-max');
    const sortSelect = document.getElementById('sort-select');
    
    if (searchInput) searchInput.addEventListener('input', debounce(applyFilters, 300));
    if (navbarSearch) navbarSearch.addEventListener('input', debounce((e) => {
        if (searchInput) searchInput.value = e.target.value;
        applyFilters();
    }, 300));
    if (marketplaceFilter) marketplaceFilter.addEventListener('change', applyFilters);
    if (brandFilter) brandFilter.addEventListener('change', applyFilters);
    if (priceMin) priceMin.addEventListener('input', debounce(applyFilters, 500));
    if (priceMax) priceMax.addEventListener('input', debounce(applyFilters, 500));
    if (sortSelect) sortSelect.addEventListener('change', applyFilters);
    
    // Download handlers (with null checks)
    const downloadFullBtn = document.getElementById('download-full-btn');
    const downloadFilteredBtn = document.getElementById('download-filtered-btn');
    
    if (downloadFullBtn) downloadFullBtn.addEventListener('click', downloadFull);
    if (downloadFilteredBtn) downloadFilteredBtn.addEventListener('click', downloadFiltered);
    
    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', toggleMobileMenu);
    }
});

// Show no data message
function showNoDataMessage() {
    const separator = document.querySelector('.separator');
    if (separator) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'no-data-message';
        messageDiv.innerHTML = `
            <div class="container" style="text-align: center; padding: 80px 24px;">
                <div style="font-size: 64px; margin-bottom: 24px;">📦</div>
                <h2 style="font-size: 28px; margin-bottom: 16px; color: var(--text-primary);">No Products Available</h2>
                <p style="color: var(--text-secondary); margin-bottom: 24px; font-size: 16px;">
                    The administrator hasn't uploaded any laptop data yet.
                </p>
                <p style="color: var(--text-muted); font-size: 14px;">
                    Please check back later or contact the administrator.
                </p>
            </div>
        `;
        separator.parentNode.insertBefore(messageDiv, separator.nextSibling);
    }
}
