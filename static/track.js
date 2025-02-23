import { rankColormap, getWRDiffColor, tintColor } from "./colour_utils.js";

// Improvement chart
const ctx = document.getElementById('timeProgressChart').getContext('2d');
const timeData = {
    labels: indices.length > 1 ? indices : wrLabels,
    datasets: [
        { // PB lines
            label: 'PB Progression',
            data: timesSec,
            borderColor: '#36A2EB',
            backgroundColor: '#9BD0F5',
            // stepped: true,
            tension: 0.05,
            pointRadius: 6,
            pointHoverRadius: 10,
            fill: false,
        },
        { // WR line
            label: 'WR',
            data: wrData,
            borderColor: "red",
            borderWidth: 2,
            borderDash: [10, 5],
            pointRadius: 0,
            hidden: true  // Initially hidden
        }
    ]
};

const timeChart = new Chart(ctx, {
    type: 'line',
    data: timeData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        // Ensure custom tooltip only applies to the main dataset (index 0)
                        if (tooltipItem.datasetIndex === 0) {
                            const index = tooltipItem.dataIndex;
                            return `${timesStr[index]} (${timesSec[index].toFixed(3)})`;
                        } else { return null; }
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

// Toggle WR line visibility
document.getElementById("toggleWR").addEventListener("click", function() {
    let wrDataset = timeChart.data.datasets[1];
    wrDataset.hidden = !wrDataset.hidden;
    timeChart.update();
});

// Toggle WR line visibility
document.getElementById("toggleScale").addEventListener("click", function() {
    let curScale = timeChart.options.scales.y;
    if ( curScale.type == "linear" ) {
        curScale.type = "logarithmic";
    } else { curScale.type = "linear"; }
    timeChart.update();
});

document.addEventListener("DOMContentLoaded", function() {
    new DataTable("#tsExcerpt", {
        // See: https://datatables.net/manual/options
        paging: false,
        info: false,
        searching: false,
        ordering: false,
        columnDefs: [
            { className: "dt-head-left", targets: "_all" },
            { className: "dt-body-center", targets: [2, 3, 4, 5, 6, 7] },
            { width: "11%", targets: [2, 3, 4, 5, 6, 7] }
        ]
    });

    // Colour Standard col
    document.querySelectorAll(".colour-rank").forEach(cell => {
        let rank = cell.innerText.trim();
        if (rankColormap.has(rank)) {
            cell.style.backgroundColor = rankColormap.get(rank);
        }
    });

    // Colour WR Diff col
    document.querySelectorAll(".colour-diff").forEach(cell => {
        let diff = parseFloat(cell.getAttribute("data-sort"));
        cell.style.backgroundColor = getWRDiffColor(diff);
    });

    new DataTable("#timesTable", {
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
