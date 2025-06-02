// Chart.js configurations and utilities for stock data visualization

class StockCharts {
    constructor() {
        this.defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        };
    }

    // Create price line chart
    createPriceChart(canvasId, data, symbol = '') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const chartData = {
            labels: data.labels,
            datasets: [{
                label: `${symbol} Price`,
                data: data.prices,
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#0d6efd',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        };

        const options = {
            ...this.defaultOptions,
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                },
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            },
            plugins: {
                ...this.defaultOptions.plugins,
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#0d6efd',
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            return `Price: $${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        };

        return new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: options
        });
    }

    // Create volume bar chart
    createVolumeChart(canvasId, data, symbol = '') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const chartData = {
            labels: data.labels,
            datasets: [{
                label: `${symbol} Volume`,
                data: data.volumes,
                backgroundColor: 'rgba(255, 193, 7, 0.6)',
                borderColor: '#ffc107',
                borderWidth: 1,
                borderRadius: 2
            }]
        };

        const options = {
            ...this.defaultOptions,
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        callback: function(value) {
                            return this.formatVolume(value);
                        }.bind(this)
                    }
                }
            },
            plugins: {
                ...this.defaultOptions.plugins,
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#ffc107',
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            return `Volume: ${this.formatVolume(context.parsed.y)}`;
                        }.bind(this)
                    }
                }
            }
        };

        return new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: options
        });
    }

    // Create candlestick chart (if OHLC data available)
    createCandlestickChart(canvasId, data, symbol = '') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        // Transform OHLC data for candlestick chart
        const candlestickData = data.ohlc.map((item, index) => ({
            x: data.labels[index],
            o: item.open,
            h: item.high,
            l: item.low,
            c: item.close
        }));

        const chartData = {
            datasets: [{
                label: `${symbol} OHLC`,
                data: candlestickData,
                borderColor: function(ctx) {
                    const dataPoint = ctx.parsed;
                    return dataPoint.c >= dataPoint.o ? '#198754' : '#dc3545';
                },
                backgroundColor: function(ctx) {
                    const dataPoint = ctx.parsed;
                    return dataPoint.c >= dataPoint.o ? 
                           'rgba(25, 135, 84, 0.8)' : 
                           'rgba(220, 53, 69, 0.8)';
                }
            }]
        };

        const options = {
            ...this.defaultOptions,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            }
        };

        return new Chart(ctx, {
            type: 'candlestick',
            data: chartData,
            options: options
        });
    }

    // Utility function to format volume numbers
    formatVolume(value) {
        if (value >= 1000000000) {
            return (value / 1000000000).toFixed(1) + 'B';
        } else if (value >= 1000000) {
            return (value / 1000000).toFixed(1) + 'M';
        } else if (value >= 1000) {
            return (value / 1000).toFixed(1) + 'K';
        }
        return value.toLocaleString();
    }

    // Add real-time updates to charts
    updateChart(chart, newData) {
        if (!chart || !newData) return;

        chart.data.labels = newData.labels;
        chart.data.datasets[0].data = newData.data;
        chart.update('none'); // No animation for real-time updates
    }

    // Create mini sparkline chart for dashboard
    createSparkline(canvasId, data, color = '#0d6efd') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const chartData = {
            labels: data.labels,
            datasets: [{
                data: data.values,
                borderColor: color,
                backgroundColor: 'transparent',
                borderWidth: 2,
                fill: false,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 0
            }]
        };

        const options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    display: false
                }
            },
            elements: {
                line: {
                    borderJoinStyle: 'round'
                }
            }
        };

        return new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: options
        });
    }

    // Destroy chart instance
    destroyChart(chart) {
        if (chart && typeof chart.destroy === 'function') {
            chart.destroy();
        }
    }
}

// Initialize chart utilities
const stockCharts = new StockCharts();

// Global chart instances
let priceChart = null;
let volumeChart = null;

// Chart initialization helper
function initializeCharts() {
    // Clean up existing charts
    if (priceChart) stockCharts.destroyChart(priceChart);
    if (volumeChart) stockCharts.destroyChart(volumeChart);

    // Initialize new charts if elements exist
    const priceCanvas = document.getElementById('priceChart');
    const volumeCanvas = document.getElementById('volumeChart');

    if (priceCanvas && window.chartData) {
        priceChart = stockCharts.createPriceChart('priceChart', window.chartData, window.symbol || '');
    }

    if (volumeCanvas && window.chartData) {
        volumeChart = stockCharts.createVolumeChart('volumeChart', window.chartData, window.symbol || '');
    }
}

// Auto-initialize charts when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });

    // Initialize charts if data is available
    if (typeof window.chartData !== 'undefined') {
        initializeCharts();
    }
});

// Window resize handler for charts
window.addEventListener('resize', function() {
    if (priceChart) priceChart.resize();
    if (volumeChart) volumeChart.resize();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StockCharts;
}
