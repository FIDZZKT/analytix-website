// CSV Preview Handler
(function() {
    let csvData = [];
    let filteredData = [];

    // Load CSV file
    async function loadCSV() {
        try {
            const response = await fetch('all-data-laptop.csv');
            const csvText = await response.text();
            
            // Calculate file size
            const fileSize = new Blob([csvText]).size;
            document.getElementById('csv-file-size').textContent = formatFileSize(fileSize);
            
            // Parse CSV
            csvData = parseCSV(csvText);
            filteredData = csvData;
            
            // Update total records
            document.getElementById('csv-total-records').textContent = csvData.length.toLocaleString('id-ID');
            
            // Render table with ALL data (not just first 10)
            renderTable(csvData);
            
        } catch (error) {
            console.error('Error loading CSV:', error);
            document.getElementById('csv-preview-body').innerHTML = 
                '<tr><td colspan="11" class="loading-row" style="color: #ef4444;">Error loading data</td></tr>';
        }
    }

    // Parse CSV text to array of objects
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
        
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                result.push(current);
                current = '';
            } else {
                current += char;
            }
        }
        result.push(current);
        
        return result;
    }

    // Render table
    function renderTable(data) {
        const tbody = document.getElementById('csv-preview-body');
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="12" class="loading-row">No data found</td></tr>';
            return;
        }
        
        tbody.innerHTML = data.map((row, index) => `
            <tr>
                <td style="text-align: center; font-weight: 600; color: var(--text-secondary);">${index + 1}</td>
                <td>${row.marketplace || '-'}</td>
                <td style="max-width: 300px; white-space: normal;">${row.product_name || '-'}</td>
                <td>${row.brand || '-'}</td>
                <td style="white-space: nowrap;">${formatPrice(row.price)}</td>
                <td style="text-align: center;">
                    <span style="color: #fbbf24; font-weight: 600;">
                        ${row.rating || '-'}
                    </span>
                </td>
                <td style="text-align: right;">${formatNumber(row.review_count)}</td>
                <td style="text-align: right;">${formatNumber(row.sold_count)}</td>
                <td>${row.seller_name || '-'}</td>
                <td>${row.seller_location || '-'}</td>
                <td style="max-width: 200px; white-space: normal; word-break: break-all;">
                    <a href="${row.product_url || '#'}" target="_blank" style="color: #9580ff; text-decoration: none; font-weight: 500;">
                        ${row.product_url ? 'View Link →' : '-'}
                    </a>
                </td>
                <td style="white-space: nowrap;">${row.scraped_date || '-'}</td>
            </tr>
        `).join('');
    }

    // Search functionality
    function searchTable(query) {
        if (!query) {
            filteredData = csvData;
            renderTable(filteredData);
            return;
        }
        
        const lowerQuery = query.toLowerCase();
        filteredData = csvData.filter(row => {
            return Object.values(row).some(value => 
                String(value).toLowerCase().includes(lowerQuery)
            );
        });
        
        renderTable(filteredData);
    }

    // Format file size
    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    }

    // Format number
    function formatNumber(num) {
        if (!num) return '0';
        return parseInt(num).toLocaleString('id-ID');
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

    // Debounce function
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
        loadCSV();
        
        // Search handler
        const searchInput = document.getElementById('table-search');
        if (searchInput) {
            searchInput.addEventListener('input', debounce((e) => {
                searchTable(e.target.value);
            }, 300));
        }
        
        // Refresh button
        const refreshBtn = document.getElementById('refresh-preview');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                searchInput.value = '';
                loadCSV();
            });
        }
    });
})();
