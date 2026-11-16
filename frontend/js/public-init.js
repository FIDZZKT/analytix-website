// Initialize public website
document.addEventListener('DOMContentLoaded', async () => {
    // Products are loaded from static CSV file, no need to check API
    // All sections are visible by default
    
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

// Show no data message (disabled - products loaded from CSV)
function showNoDataMessage() {
    // Do nothing - products are loaded from static CSV file
}




// Helper function - Debounce
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

// Apply filters (placeholder - actual filtering done in products-loader.js)
function applyFilters() {
    // This is handled by products-loader.js
    console.log('Filters applied');
}

// Download full CSV
function downloadFull() {
    const a = document.createElement('a');
    a.href = 'all-data-laptop.csv';
    a.download = 'analytix-full-dataset.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Download filtered CSV (same as full for now)
function downloadFiltered() {
    downloadFull();
}

// Toggle mobile menu
function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks) {
        navLinks.classList.toggle('active');
    }
}
