// ATS Score Chart
function createATSScoreChart(ctx, scores, labels) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'ATS Score',
                data: scores,
                backgroundColor: 'rgba(102, 126, 234, 0.5)',
                borderColor: 'rgb(102, 126, 234)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'ATS Score History'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Skills Radar Chart
function createSkillsRadarChart(ctx, skills, levels) {
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: skills,
            datasets: [{
                label: 'Skill Level',
                data: levels,
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                borderColor: 'rgb(102, 126, 234)',
                pointBackgroundColor: 'rgb(102, 126, 234)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Match Percentage Gauge
function createMatchGauge(ctx, percentage) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [percentage, 100 - percentage],
                backgroundColor: ['rgb(16, 185, 129)', 'rgb(229, 231, 235)'],
                borderWidth: 0
            }]
        },
        options: {
            cutout: '70%',
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
}