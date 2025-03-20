document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts
    initActivityChart();
    initCategoryChart();
    initComparisonChart();
    initTrendChart();
    
    // Load summary data
    loadSummaryData();
    
    // Set up event listeners
    document.getElementById('view-weekly').addEventListener('click', function() {
        updateActivityChart('weekly');
    });
    
    document.getElementById('view-monthly').addEventListener('click', function() {
        updateActivityChart('monthly');
    });
    
    document.getElementById('view-yearly').addEventListener('click', function() {
        updateActivityChart('yearly');
    });
});

// Activity Chart
let activityChart;
function initActivityChart() {
    const ctx = document.getElementById('activityChart').getContext('2d');
    
    activityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Registros de Encuestas',
                data: [],
                backgroundColor: 'rgba(78, 115, 223, 0.05)',
                borderColor: 'rgba(78, 115, 223, 1)',
                pointRadius: 3,
                pointBackgroundColor: 'rgba(78, 115, 223, 1)',
                pointBorderColor: 'rgba(78, 115, 223, 1)',
                pointHoverRadius: 5,
                pointHoverBackgroundColor: 'rgba(78, 115, 223, 1)',
                pointHoverBorderColor: 'rgba(78, 115, 223, 1)',
                pointHitRadius: 10,
                pointBorderWidth: 2,
                fill: true
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Registros: ${context.raw}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 7
                    }
                },
                y: {
                    ticks: {
                        maxTicksLimit: 5,
                        padding: 10
                    },
                    grid: {
                        color: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                }
            }
        }
    });
    
    // Load initial data
    updateActivityChart('monthly');
}

function updateActivityChart(timeframe) {
    fetch(`/dashboard/api/chart-data/?chart_type=user_activity&timeframe=${timeframe}`)
        .then(response => response.json())
        .then(data => {
            activityChart.data.labels = data.labels;
            activityChart.data.datasets[0].data = data.datasets[0].data;
            activityChart.update();
        })
        .catch(error => console.error('Error loading activity chart data:', error));
}

// Category Chart
let categoryChart;
function initCategoryChart() {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    
    categoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#5a5c69', '#6f42c1', '#fd7e14', '#20c997', '#6c757d'],
                hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#dda20a', '#be2617', '#3a3b45', '#5a32a3', '#d96b12', '#17a47a', '#5a6268'],
                hoverBorderColor: "rgba(234, 236, 244, 1)",
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw} registros`;
                        }
                    }
                }
            },
            cutout: '70%'
        }
    });
    
    // Load initial data
    updateCategoryChart();
}

// Comparison Chart
let comparisonChart;
function initComparisonChart() {
    const ctx = document.getElementById('comparisonChart').getContext('2d');
    
    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.raw} registros`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    grid: {
                        borderDash: [2],
                        drawBorder: false
                    },
                    title: {
                        display: true,
                        text: 'Número de registros'
                    }
                }
            }
        }
    });
    
    // Load initial data
    updateComparisonChart();
}

// Trend Chart
let trendChart;
function initTrendChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');
    
    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Tendencia de Registros',
                data: [],
                backgroundColor: 'rgba(28, 200, 138, 0.05)',
                borderColor: 'rgba(28, 200, 138, 1)',
                pointRadius: 3,
                pointBackgroundColor: 'rgba(28, 200, 138, 1)',
                pointBorderColor: 'rgba(28, 200, 138, 1)',
                pointHoverRadius: 5,
                pointHoverBackgroundColor: 'rgba(28, 200, 138, 1)',
                pointHoverBorderColor: 'rgba(28, 200, 138, 1)',
                pointHitRadius: 10,
                pointBorderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Registros: ${context.raw}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    grid: {
                        borderDash: [2],
                        drawBorder: false
                    },
                    title: {
                        display: true,
                        text: 'Número de registros'
                    }
                }
            }
        }
    });
    
    // Load initial data
    updateTrendChart();
}

// Load summary data for the dashboard cards
function loadSummaryData() {
    fetch('/dashboard/api/summary-data/')
        .then(response => response.json())
        .then(data => {
            // Update summary cards with real data
            document.getElementById('total-records').textContent = data.total_records || 0;
            document.getElementById('average-value').textContent = data.average_value || 0;
            
            const completionRate = data.completion_rate || 0;
            document.getElementById('completion-rate').textContent = `${completionRate}%`;
            document.getElementById('completion-progress').style.width = `${completionRate}%`;
            document.getElementById('completion-progress').setAttribute('aria-valuenow', completionRate);
            
            document.getElementById('pending-items').textContent = data.pending_items || 0;
        })
        .catch(error => {
            console.error('Error loading summary data:', error);
            // Set default values in case of error
            document.getElementById('total-records').textContent = '0';
            document.getElementById('average-value').textContent = '0';
            document.getElementById('completion-rate').textContent = '0%';
            document.getElementById('completion-progress').style.width = '0%';
            document.getElementById('pending-items').textContent = '0';
        });
}

// Function to update category chart with real data
function updateCategoryChart() {
    fetch('/dashboard/api/chart-data/?chart_type=category_distribution')
        .then(response => response.json())
        .then(data => {
            categoryChart.data.labels = data.labels;
            categoryChart.data.datasets[0].data = data.datasets[0].data;
            categoryChart.update();
        })
        .catch(error => console.error('Error loading category data:', error));
}

// Function to update comparison chart with real data
function updateComparisonChart() {
    fetch('/dashboard/api/chart-data/?chart_type=yearly_comparison')
        .then(response => response.json())
        .then(data => {
            comparisonChart.data.labels = data.labels;
            comparisonChart.data.datasets = data.datasets;
            comparisonChart.update();
        })
        .catch(error => console.error('Error loading comparison data:', error));
}

// Function to update trend chart with real data
function updateTrendChart() {
    fetch('/dashboard/api/chart-data/?chart_type=monthly_trend')
        .then(response => response.json())
        .then(data => {
            trendChart.data.labels = data.labels;
            trendChart.data.datasets[0].data = data.datasets[0].data;
            trendChart.update();
        })
        .catch(error => console.error('Error loading trend data:', error));
}

// Function to refresh all dashboard data
function refreshDashboard() {
    loadSummaryData();
    updateActivityChart('monthly');
    updateCategoryChart();
    updateComparisonChart();
    updateTrendChart();
}

// Set up auto-refresh every 5 minutes
setInterval(refreshDashboard, 5 * 60 * 1000);