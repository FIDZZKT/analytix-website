// Dataset Info Handler - Populate dataset information section
(function() {
    let csvData = [];

    // Load CSV and populate dataset info
    async function loadDatasetInfo() {
        try {
            const response = await fetch('all-data-laptop.csv');
            const csvText = await response.text();
            
            // Parse CSV
            csvData = parseCSV(csvText);
            
            // Populate dataset information
            populateDatasetInfo(csvData);
            
        } catch (error) {
            console.error('Error loading dataset info:', error);
        }
    }

    // Parse CSV
    function parseCSV(text) {
        const lines = text.trim().split('\n');
        const firstLine = lines[0];
        
        // Detect delimiter
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

    // Populate dataset information
    function populateDatasetInfo(data) {
        // Filename
        const filenameEl = document.getElementById('info-filename');
        if (filenameEl) {
            filenameEl.textContent = 'all-data-laptop.csv';
        }

        // Total Products
        const totalEl = document.getElementById('info-total');
        if (totalEl) {
            totalEl.textContent = formatNumber(data.length);
        }

        // Unique Marketplaces
        const marketplaces = [...new Set(data.map(row => row.marketplace))].filter(Boolean);
        const marketplacesEl = document.getElementById('info-marketplaces');
        if (marketplacesEl) {
            marketplacesEl.textContent = `${marketplaces.length} marketplaces (${marketplaces.join(', ')})`;
        }

        // Unique Brands
        const brands = [...new Set(data.map(row => row.brand))].filter(Boolean);
        const brandsEl = document.getElementById('info-brands');
        if (brandsEl) {
            brandsEl.textContent = `${brands.length} brands`;
        }

        // Price Range
        const prices = data.map(row => parseFloat(String(row.price).replace(/[^\d.]/g, ''))).filter(p => !isNaN(p) && p > 0);
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const priceRangeEl = document.getElementById('info-price-range');
        if (priceRangeEl) {
            priceRangeEl.textContent = `${formatPrice(minPrice)} - ${formatPrice(maxPrice)}`;
        }

        // Last Updated (use most recent scraped_date)
        const dates = data.map(row => row.scraped_date).filter(Boolean);
        if (dates.length > 0) {
            // Parse dates (format: DD/MM/YYYY)
            const parsedDates = dates.map(dateStr => {
                const [day, month, year] = dateStr.split('/');
                return new Date(year, month - 1, day);
            }).filter(d => !isNaN(d));
            
            const latestDate = new Date(Math.max(...parsedDates));
            const timestampEl = document.getElementById('info-timestamp');
            if (timestampEl) {
                timestampEl.textContent = latestDate.toLocaleDateString('id-ID', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
            }
        }
    }

    // Format number
    function formatNumber(num) {
        if (!num) return '0';
        return parseInt(num).toLocaleString('id-ID');
    }

    // Format price
    function formatPrice(price) {
        if (!price || price === 0) return 'Rp 0';
        
        const num = parseFloat(price);
        
        if (isNaN(num)) return 'Rp 0';
        
        if (num >= 1000000) {
            return 'Rp ' + (num / 1000000).toFixed(1).replace('.', ',') + ' juta';
        }
        
        if (num >= 1000) {
            return 'Rp ' + Math.round(num / 1000) + ' ribu';
        }
        
        return 'Rp ' + Math.round(num).toLocaleString('id-ID');
    }

    // Download Full Dataset
    function downloadFullDataset() {
        const link = document.createElement('a');
        link.href = 'all-data-laptop.csv';
        link.download = 'analytix-laptop-dataset-full.csv';
        link.click();
    }

    // Download Filtered Dataset (same as full for now, could be enhanced)
    function downloadFilteredDataset() {
        downloadFullDataset();
    }

    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
        loadDatasetInfo();
        
        // Download buttons
        const downloadFullBtn = document.getElementById('download-full-btn');
        if (downloadFullBtn) {
            downloadFullBtn.addEventListener('click', downloadFullDataset);
        }
        
        const downloadFilteredBtn = document.getElementById('download-filtered-btn');
        if (downloadFilteredBtn) {
            downloadFilteredBtn.addEventListener('click', downloadFilteredDataset);
        }
    });
})();
