const ctx = document.getElementById('timeProgressChart').getContext('2d');
const timeData = {
    labels: indices,
    datasets: [{
        label: 'PB Progression',
        data: timesSec,
        // stepped: true,
        tension: 0.05,
        pointRadius: 6,
        pointHoverRadius: 10,
        fill: false,
    }]
};

new Chart(ctx, {
    type: 'line',
    data: timeData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        const index = tooltipItem.dataIndex;
                        return `${timesStr[index]} (${timesSec[index].toFixed(3)})`;
                    }
                }
            }
        },
        interaction: {
            intersect: false,
            mode: 'index',
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: "Improvement #",
                    font: { size: 14, weight: "bold" }
                }
            },
            y: {
                title: {
                    display: true,
                    text: "Time (s)",
                    font: { size: 14, weight: "bold" }
                },
                beginAtZero: false
            }
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
    let table = new DataTable("#timesTable", {
        paging: true,
        pageLength: 10,
        lengthChange: false,
        searching: false,
        ordering: true,
        order: [[0, "desc"]],
        columnDefs: [
            { orderable: true, targets: 0 },
            { orderable: false, targets: "_all" },
            { className: "dt-head-left", targets: "_all" },
            { className: "dt-body-center", targets: [1, 2, 3] },
        ],
        layout: {
            bottomEnd: {
                paging: {
                    numbers: false
                }
            }
        }
    });
});
