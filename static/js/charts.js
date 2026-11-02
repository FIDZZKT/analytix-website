// Chart instances storage
const chartInstances = {};

// Configure Chart.js defaults for dark theme
Chart.defaults.color = '#a0a0a0';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
Chart.defaults.font.family = 'system-ui, -apple-system, sans-serif';

// Initialize all charts
async function initCharts() {
    try {
        const response = await fetch('/api/analytics');
        const data = await response.json();
        
        // Destroy existing charts if reinitializing
        Object.keys(chartInstances).forEach(key => {
            if (chartInstances[key]) {
                chartInstances[key].destroy();
            }
        });
        
        // Chart 1: Products by Marketplace
        if (data.products_by_marketplace) {
            const ctx1 = document.getElementById('chart-marketplace');
            if (ctx1) {
                chartInstances.marketplace = new Chart(ctx1, {
                    type: 'bar',
                    data: {
                        labels: Object.keys(data.products_by_marketplace),
                        datasets: [{
                            label: 'Products',
                            data: Object.values(data.products_by_marketplace),
                            backgroundColor: 'rgba(132, 204, 22, 0.8)',
                            borderColor: '#84cc16',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Products by Marketplace',
                                color: '#ffffff',
                                font: { size: 16, weight: '600' }
                            },
                            legend: { display: false }
                        },
                        scales: {
                            x: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                ticks: { color: '#a0a0a0' }
                            },
                            y: {
                                grid: { display: false },
                                ticks: { color: '#a0a0a0' }
                            }
                        }
                    }
                });
            }
        }
        
        // Chart 2: Products by Brand (Top 10)
        if (data.products_by_brand) {
            const ctx2 = document.getElementById('chart-brand');
            if (ctx2) {
                chartInstances.brand = new Chart(ctx2, {
                    type: 'bar',
                    data: {
                        labels: Object.keys(data.products_by_brand),
                        datasets: [{
                            label: 'Products',
                            data: Object.values(data.products_by_brand),
                            backgroundColor: 'rgba(132, 204, 22, 0.8)',
                            borderColor: '#84cc16',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Top 10 Brands',
                                color: '#ffffff',
                                font: { size: 16, weight: '600' }
                            },
                            legend: { display: false }
                        },
                        scales: {
                            x: {
                                grid: { display: false },
                                ticks: { color: '#a0a0a0' }
                            },
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                ticks: { color: '#a0a0a0' }
                            }
                        }
                    }
                });
            }
        }
        
        // Chart 3: Price Distribution
        if (data.price_distribution) {
            const ctx3 = document.getElementById('chart-price-distribution');
            if (ctx3) {
                chartInstances.priceDistribution = new Chart(ctx3, {
                    type: 'bar',
                    data: {
                        labels: Object.keys(data.price_distribution),
                        datasets: [{
                            label: 'Products',
                            data: Object.values(data.price_distribution),
                            backgroundColor: 'rgba(132, 204, 22, 0.8)',
                            borderColor: '#84cc16',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Price Distribution',
                                color: '#ffffff',
                                font: { size: 16, weight: '600' }
                            },
                            legend: { display: false }
                        },
                        scales: {
                            x: {
                                grid: { display: false },
                                ticks: { 
                                    color: '#a0a0a0',
                                    maxRotation: 45,
                                    minRotation: 45
                                }
                            },
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                ticks: { color: '#a0a0a0' }
                            }
                        }
                    }
                });
            }
        }
        
        // Chart 4: Average Price by Marketplace
        if (data.avg_price_by_marketplace) {
            const ctx4 = document.getElementById('chart-avg-price');
            if (ctx4) {
                chartInstances.avgPrice = new Chart(ctx4, {
                    type: 'bar',
                    data: {
                        labels: Object.keys(data.avg_price_by_marketplace),
                        datasets: [{
                            label: 'Average Price (IDR)',
                            data: Object.values(data.avg_price_by_marketplace),
                            backgroundColor: 'rgba(132, 204, 22, 0.8)',
                            borderColor: '#84cc16',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Average Price by Marketplace',
                                color: '#ffffff',
                                font: { size: 16, weight: '600' }
                            },
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return 'Rp ' + Math.round(context.parsed.y).toLocaleString('id-ID');
                                    }
                                }
                            }
                        },
                        scales: {
                            x: {
                                grid: { display: false },
                                ticks: { color: '#a0a0a0' }
                            },
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                ticks: { 
                                    color: '#a0a0a0',
                                    callback: function(value) {
                                        return 'Rp ' + (value / 1000000).toFixed(1) + 'M';
                                    }
                                }
                            }
                        }
                    }
                });
            }
        }
        
        // Chart 5: Average Rating by Marketplace
        if (data.avg_rating_by_marketplace) {
            const ctx5 = document.getElementById('chart-avg-rating');
            if (ctx5) {
                chartInstances.avgRating = new Chart(ctx5, {
                    type: 'bar',
                    data: {
                        labels: Object.keys(data.avg_rating_by_marketplace),
                        datasets: [{
                            label: 'Average Rating',
                            data: Object.values(data.avg_rating_by_marketplace),
                            backgroundColor: 'rgba(132, 204, 22, 0.8)',
                            borderColor: '#84cc16',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Average Rating by Marketplace',
                                color: '#ffffff',
                                font: { size: 16, weight: '600' }
                            },
                            legend: { display: false }
                        },
                        scales: {
                            x: {
                                grid: { display: false },
                                ticks: { color: '#a0a0a0' }
                            },
                            y: {
                                beginAtZero: true,
                                max: 5,
                                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                ticks: { 
                                    color: '#a0a0a0',
                                    stepSize: 1
                                }
                            }
                        }
                    }
                });
            }
        }
        
    } catch (error) {
        console.error('Error initializing charts:', error);
    }
}

// Export for use in main.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initCharts };
}
