document.addEventListener('DOMContentLoaded', () => {
    if (!window.DASHBOARD_DATA) return;

    const data = window.DASHBOARD_DATA;
    const colors = ['#4f46e5', '#0d9488', '#f59e0b'];
    const clusterLabels = [
        'Group 0: Regular Fashion Shoppers',
        'Group 1: Big Spenders on Dining',
        'Group 2: Movie & Hangout Visitors'
    ];

    // --- 1. Customer Breakdown Donut Chart ---
    const ctxShare = document.getElementById('marketShareChart');
    if (ctxShare) {
        new Chart(ctxShare, {
            type: 'doughnut',
            data: {
                labels: clusterLabels,
                datasets: [{
                    data: [
                        data.clusterMetrics[0].count,
                        data.clusterMetrics[1].count,
                        data.clusterMetrics[2].count
                    ],
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const val = context.raw;
                                const total = 120;
                                const pct = ((val / total) * 100).toFixed(1);
                                return ` ${context.label}: ${val} people (${pct}%)`;
                            }
                        }
                    }
                },
                cutout: '72%'
            }
        });
    }

    // --- 2. Spend vs Visit Frequency Bar Chart ---
    const ctxSpend = document.getElementById('spendVisitChart');
    if (ctxSpend) {
        new Chart(ctxSpend, {
            type: 'bar',
            data: {
                labels: ['Group 0 (Fashion)', 'Group 1 (Dining)', 'Group 2 (Movies/Games)'],
                datasets: [
                    {
                        label: 'Avg Spend / Month ($)',
                        data: [
                            data.clusterMetrics[0].avg_spend,
                            data.clusterMetrics[1].avg_spend,
                            data.clusterMetrics[2].avg_spend
                        ],
                        backgroundColor: '#4f46e5',
                        borderRadius: 6,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Visits per Month',
                        data: [
                            data.clusterMetrics[0].avg_visits,
                            data.clusterMetrics[1].avg_visits,
                            data.clusterMetrics[2].avg_visits
                        ],
                        backgroundColor: '#0d9488',
                        borderRadius: 6,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: { display: true, text: 'Monthly Spend ($ USD)' },
                        grid: { color: '#f1f5f9' }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: { display: true, text: 'Visits / Month' },
                        grid: { drawOnChartArea: false }
                    },
                    x: {
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { boxWidth: 12, font: { size: 11 } }
                    }
                }
            }
        });
    }

    // --- 3. What each group buys (Category Bar Chart) ---
    const ctxCat = document.getElementById('categoryChart');
    if (ctxCat) {
        const categories = ['Fashion', 'Food', 'Entertainment', 'Electronics'];
        const displayCategories = ['Fashion & Clothes', 'Food & Dining', 'Entertainment & Movies', 'Electronics & Tech'];
        
        // Prepare datasets per cluster
        const datasets = [0, 1, 2].map((cid, i) => {
            const counts = categories.map(cat => {
                if (data.catByCluster[cid] && data.catByCluster[cid][cat]) {
                    return data.catByCluster[cid][cat];
                }
                return 0;
            });
            return {
                label: clusterLabels[i],
                data: counts,
                backgroundColor: colors[i],
                borderRadius: 5
            };
        });

        new Chart(ctxCat, {
            type: 'bar',
            data: {
                labels: displayCategories,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Number of Customers' },
                        grid: { color: '#f1f5f9' }
                    },
                    x: {
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { boxWidth: 12, font: { size: 10 } }
                    }
                }
            }
        });
    }

    // --- 4. Promotional Offer Sensitivity (Stacked Bar) ---
    const ctxOffer = document.getElementById('offerSensitivityChart');
    if (ctxOffer) {
        new Chart(ctxOffer, {
            type: 'bar',
            data: {
                labels: ['Group 0 (Fashion)', 'Group 1 (Dining)', 'Group 2 (Movies/Games)'],
                datasets: [
                    {
                        label: 'Uses Coupons (Yes)',
                        data: [
                            data.clusterMetrics[0].offer_yes,
                            data.clusterMetrics[1].offer_yes,
                            data.clusterMetrics[2].offer_yes
                        ],
                        backgroundColor: '#10b981',
                        borderRadius: 4
                    },
                    {
                        label: 'Pays Regular Price (No)',
                        data: [
                            data.clusterMetrics[0].offer_no,
                            data.clusterMetrics[1].offer_no,
                            data.clusterMetrics[2].offer_no
                        ],
                        backgroundColor: '#cbd5e1',
                        borderRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        stacked: true,
                        grid: { display: false }
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true,
                        title: { display: true, text: 'Number of Customers' },
                        grid: { color: '#f1f5f9' }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { boxWidth: 12, font: { size: 11 } }
                    }
                }
            }
        });
    }
});
