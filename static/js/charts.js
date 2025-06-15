/*
 * StockTracker Charts
 * A simple charting utility for displaying stock price data
 * Uses Chart.js library for basic line and bar charts
 */

class StockCharts {
    constructor() {
        // Basic chart options that apply to all charts
        this.defaultOptions = {
            responsive: true,  // Make charts responsive to container size
            maintainAspectRatio: false,  // Allow custom height
            plugins: {
                legend: {
                    display: false  // Hide legend by default
                }
            }
        };
    }

    /**
     * Creates a line chart for stock prices
     * @param {string} canvasId - The HTML canvas element ID
     * @param {Object} data - Contains labels and prices arrays
     * @param {string} symbol - Stock symbol for the chart title
     */
    createPriceChart(canvasId, data, symbol = '') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        // Prepare the data for the chart
        const chartData = {
            labels: data.labels,  // Dates on x-axis
            datasets: [{
                label: `${symbol} Price`,
                data: data.prices,  // Price values on y-axis
                borderColor: '#0d6efd',  // Blue line
                backgroundColor: 'rgba(13, 110, 253, 0.1)',  // Light blue fill
                borderWidth: 2,
                fill: true
            }]
        };

        // Basic chart options
        const options = {
            ...this.defaultOptions,
            scales: {
                x: {
                    grid: {
                        display: false  // Hide x-axis grid lines
                    }
                },
                y: {
                    beginAtZero: false,  // Start y-axis from actual data
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'  // Light gray grid lines
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);  // Format as currency
                        }
                    }
                }
            }
        };

        // Create and return the chart
        return new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: options
        });
    }

    /**
     * Creates a bar chart for trading volume
     * @param {string} canvasId - The HTML canvas element ID
     * @param {Object} data - Contains labels and volumes arrays
     * @param {string} symbol - Stock symbol for the chart title
     */
    createVolumeChart(canvasId, data, symbol = '') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        // Prepare the data for the chart
        const chartData = {
            labels: data.labels,  // Dates on x-axis
            datasets: [{
                label: `${symbol} Volume`,
                data: data.volumes,  // Volume values on y-axis
                backgroundColor: 'rgba(255, 193, 7, 0.6)',  // Yellow bars
                borderColor: '#ffc107',
                borderWidth: 1
            }]
        };

        // chart options
        const options = {
            ...this.defaultOptions,
            scales: {
                x: {
                    grid: {
                        display: false  // Hide x-axis grid lines
                    }
                },
                y: {
                    beginAtZero: true,  // Start y-axis from zero
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'  // Light gray grid lines
                    },
                    ticks: {
                        callback: function(value) {
                            return this.formatVolume(value);  // Format large numbers
                        }.bind(this)
                    }
                }
            }
        };

        // Create and return the chart
        return new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: options
        });
    }
    
    /**
     * Updates an existing chart with new data
     * @param {Chart} chart - The chart to update
     * @param {Object} newData - New data to display
     */
    updateChart(chart, newData) {
        if (!chart || !newData) return;
        chart.data.labels = newData.labels;
        chart.data.datasets[0].data = newData.data;
        chart.update();
    }
}

/**
 * Initialize charts when the page loads
 * This function is called from the HTML template
 */
function initializeCharts() {
    const stockCharts = new StockCharts();
    
    // Get chart data from the page
    const priceChartData = window.priceChartData;
    const volumeChartData = window.volumeChartData;
    const symbol = window.stockSymbol;

    // Create charts if data is available
    if (priceChartData) {
        stockCharts.createPriceChart('priceChart', priceChartData, symbol);
    }
    if (volumeChartData) {
        stockCharts.createVolumeChart('volumeChart', volumeChartData, symbol);
    }
}

// Initialize charts when the page is ready
document.addEventListener('DOMContentLoaded', initializeCharts);
