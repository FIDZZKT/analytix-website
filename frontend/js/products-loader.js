// Products Loader - Load and display products from CSV
(function() {
    let allProducts = [];
    let filteredProducts = [];

    // Generate marketplace URL
    function generateMarketplaceURL(marketplace, productName) {
        const searchQuery = encodeURIComponent(productName);
        const urls = {
            'Shopee': `https://shopee.co.id/search?keyword=${searchQuery}`,
            'Tokopedia': `https://www.tokopedia.com/search?q=${searchQuery}`,
            'Lazada': `https://www.lazada.co.id/catalog/?q=${searchQuery}`,
            'Blibli': `https://www.blibli.com/search?s=${searchQuery}`
        };
        return urls[marketplace] || '#';
    }

    // Load products from CSV
    async function loadProducts() {
        try {
            const response = await fetch('all-data-laptop.csv');
            const csvText = await response.text();
            
            // Parse CSV
            allProducts = parseCSV(csvText);
            
            // Take first 20 products
            filteredProducts = allProducts.slice(0, 20);
            
            // Render products
            renderProducts(filteredProducts);
            updateProductCount(filteredProducts.length);
            
        } catch (error) {
            console.error('Error loading products:', error);
            document.getElementById('product-grid').innerHTML = 
                '<p style="color: var(--text-secondary); grid-column: 1 / -1; text-align: center; padding: 40px;">Error loading products</p>';
        }
    }

    // Parse CSV
    function parseCSV(text) {
        const lines = text.trim().split('\n');
        const firstLine = lines[0];
        
        // Detect delimiter (semicolon or comma)
        const delimiter = firstLine.includes(';') ? ';' : ',';
        const headers = firstLine.split(delimiter);
        
        return lines.slice(1).map(line => {
            const values = line.split(delimiter);
            const obj = {};
            headers.forEach((header, index) => {
                obj[header.trim()] = values[index] ? values[index].trim() : '';
            });
            return obj;
        });
    }

    // Parse CSV line handling quoted values
    function parseCSVLine(line) {
        const result = [];
        let current = '';
        let inQuotes = false;
        
        // Check if using semicolon or comma as delimiter
        const delimiter = line.includes(';') ? ';' : ',';
        
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === delimiter && !inQuotes) {
                result.push(current);
                current = '';
            } else {
                current += char;
            }
        }
        result.push(current);
        return result;
    }

    // Render products grid
    function renderProducts(products) {
        const grid = document.getElementById('product-grid');
        
        if (!products || products.length === 0) {
            grid.innerHTML = '<p style="color: var(--text-secondary); grid-column: 1 / -1; text-align: center; padding: 40px;">No products found</p>';
            return;
        }
        
        grid.innerHTML = products.map(product => {
            const productName = product.product_name || product.name || 'Unknown Product';
            const brand = product.brand || 'Unknown';
            const marketplace = product.marketplace || 'N/A';
            const productURL = product.product_url || '#';
            const price = formatPrice(product.price);
            const badge = getMarketplaceBadge(marketplace);
            
            return `
                <div class="product-card">
                    <div class="product-image">
                        <svg width="140" height="105" viewBox="0 0 140 105" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <!-- Laptop Illustration -->
                            <rect x="20" y="15" width="100" height="65" rx="4" fill="#1a1a1a" stroke="#9580ff" stroke-width="2"/>
                            <rect x="20" y="15" width="100" height="10" fill="#9580ff" opacity="0.3"/>
                            
                            <!-- Screen Content -->
                            <rect x="30" y="32" width="25" height="18" rx="2" fill="#2a2a2a" stroke="#9580ff" stroke-width="1" opacity="0.5"/>
                            <rect x="60" y="32" width="25" height="18" rx="2" fill="#2a2a2a" stroke="#9580ff" stroke-width="1" opacity="0.5"/>
                            <rect x="90" y="32" width="25" height="18" rx="2" fill="#2a2a2a" stroke="#9580ff" stroke-width="1" opacity="0.5"/>
                            
                            <line x1="30" y1="58" x2="110" y2="58" stroke="#9580ff" stroke-width="1" opacity="0.3"/>
                            <line x1="30" y1="65" x2="95" y2="65" stroke="#9580ff" stroke-width="1" opacity="0.3"/>
                            
                            <!-- Laptop Base -->
                            <path d="M 10 80 L 20 80 L 20 83 Q 70 87 120 83 L 120 80 L 130 80 L 125 95 L 15 95 Z" fill="#1a1a1a" stroke="#9580ff" stroke-width="2"/>
                            
                            <!-- Brand Badge -->
                            <circle cx="70" cy="85" r="3" fill="#9580ff"/>
                        </svg>
                    </div>
                    <div class="product-info">
                        <h3 class="product-name">${productName}</h3>
                        <p class="product-specs">${brand} • ${marketplace}</p>
                        <p class="product-price">${price}</p>
                        <div class="product-footer">
                            <span class="marketplace-badge ${badge.class}">${badge.text}</span>
                            <a href="${productURL}" target="_blank" class="product-link">
                                Lihat Produk →
                            </a>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    // Format price
    function formatPrice(price) {
        if (!price || price === 0) return 'Rp 0';
        
        // Remove any non-numeric characters except dots and commas
        let cleanPrice = String(price).replace(/[^\d.,]/g, '');
        
        // Replace comma with dot for decimal separator
        cleanPrice = cleanPrice.replace(',', '.');
        
        const num = parseFloat(cleanPrice);
        
        if (isNaN(num)) return 'Rp 0';
        
        if (num >= 1000000) {
            return 'Rp ' + (num / 1000000).toFixed(1).replace('.', ',') + ' juta';
        }
        
        if (num >= 1000) {
            return 'Rp ' + Math.round(num / 1000) + ' ribu';
        }
        
        return 'Rp ' + Math.round(num).toLocaleString('id-ID');
    }

    // Get marketplace badge styling
    function getMarketplaceBadge(marketplace) {
        const badges = {
            'Shopee': { text: 'SHOPEE', class: 'badge-shopee' },
            'Tokopedia': { text: 'TOKOPEDIA', class: 'badge-tokopedia' },
            'Lazada': { text: 'LAZADA', class: 'badge-lazada' },
            'Blibli': { text: 'BLIBLI', class: 'badge-blibli' }
        };
        return badges[marketplace] || { text: marketplace.toUpperCase(), class: '' };
    }

    // Update product count
    function updateProductCount(count) {
        document.getElementById('product-count-display').textContent = `${count} products`;
    }

    // Filter products
    function applyFilters() {
        const searchQuery = document.getElementById('search-input').value.toLowerCase();
        const marketplace = document.getElementById('marketplace-filter').value;
        const brand = document.getElementById('brand-filter').value;
        const minPrice = document.getElementById('price-min').value;
        const maxPrice = document.getElementById('price-max').value;
        const sortBy = document.getElementById('sort-select').value;
        
        // Filter
        let filtered = allProducts;
        
        if (searchQuery) {
            filtered = filtered.filter(p => {
                const name = (p.product_name || p.name || '').toLowerCase();
                const brandName = (p.brand || '').toLowerCase();
                return name.includes(searchQuery) || brandName.includes(searchQuery);
            });
        }
        
        if (marketplace) {
            filtered = filtered.filter(p => p.marketplace === marketplace);
        }
        
        if (brand) {
            filtered = filtered.filter(p => p.brand === brand);
        }
        
        if (minPrice) {
            filtered = filtered.filter(p => {
                const price = parseFloat(String(p.price).replace(/[^\d.,]/g, '').replace(',', '.'));
                return !isNaN(price) && price >= parseInt(minPrice);
            });
        }
        
        if (maxPrice) {
            filtered = filtered.filter(p => {
                const price = parseFloat(String(p.price).replace(/[^\d.,]/g, '').replace(',', '.'));
                return !isNaN(price) && price <= parseInt(maxPrice);
            });
        }
        
        // Sort
        if (sortBy === 'price_asc') {
            filtered.sort((a, b) => {
                const priceA = parseFloat(String(a.price).replace(/[^\d.,]/g, '').replace(',', '.'));
                const priceB = parseFloat(String(b.price).replace(/[^\d.,]/g, '').replace(',', '.'));
                return priceA - priceB;
            });
        } else if (sortBy === 'price_desc') {
            filtered.sort((a, b) => {
                const priceA = parseFloat(String(a.price).replace(/[^\d.,]/g, '').replace(',', '.'));
                const priceB = parseFloat(String(b.price).replace(/[^\d.,]/g, '').replace(',', '.'));
                return priceB - priceA;
            });
        } else if (sortBy === 'rating_desc') {
            filtered.sort((a, b) => {
                const ratingA = parseFloat(String(a.rating).replace(',', '.'));
                const ratingB = parseFloat(String(b.rating).replace(',', '.'));
                return ratingB - ratingA;
            });
        }
        
        // Take first 20
        filteredProducts = filtered.slice(0, 20);
        
        renderProducts(filteredProducts);
        updateProductCount(filteredProducts.length);
    }

    // Debounce
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

    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
        loadProducts();
        
        // Event listeners
        document.getElementById('search-input').addEventListener('input', debounce(applyFilters, 300));
        document.getElementById('marketplace-filter').addEventListener('change', applyFilters);
        document.getElementById('brand-filter').addEventListener('change', applyFilters);
        document.getElementById('price-min').addEventListener('input', debounce(applyFilters, 500));
        document.getElementById('price-max').addEventListener('input', debounce(applyFilters, 500));
        document.getElementById('sort-select').addEventListener('change', applyFilters);
    });
})();
