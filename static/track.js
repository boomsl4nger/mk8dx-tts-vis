import { standardsNames, WRColor, rankColormap, getWRDiffColor, tintColor } from "./colour_utils.js";

let showRankBands = false;

// PB Progression Line
const pbDataset = {
    label: 'PB Progression',
    data: timesSec,
    borderColor: '#36A2EB',
    backgroundColor: '#9BD0F5',
    tension: 0.05,
    pointRadius: 6,
    pointHoverRadius: 10,
    fill: false
};

// WR Line
const wrDataset = {
    label: 'WR',
    data: wrData,
    borderColor: WRColor,
    borderDash: [20, 6],
    borderWidth: 3,
    pointRadius: 0,
    pointHoverRadius: 0,
    hidden: true  
};

// Function to create rank band annotations
// See: https://www.chartjs.org/chartjs-plugin-annotation/latest/samples/box/quarters.html
function getRankAnnotations(chart) {
    const yScale = chart.scales.y;
    const yMin = yScale.min;
    const yMax = yScale.max;
    let annotations = [];

    for (let i = 0; i < standards.length; i++) {
        let cutoffLow = standards[i - 1] || 0.0;
        let cutoffHigh = standards[i];

        if (cutoffHigh < yMin) continue;
        if (cutoffLow > yMax) break;

        annotations.push({
            type: 'box',
            yMin: Math.max(cutoffLow, yMin),
            yMax: Math.min(cutoffHigh, yMax),
            backgroundColor: tintColor(rankColormap.get(standardsNames[i]), 40),
            borderWidth: 0,
            label: {
                // See: https://www.chartjs.org/chartjs-plugin-annotation/latest/guide/types/box.html#label
                drawTime: 'afterDraw',
                display: true,
                content: standardsNames[i],
                position: {
                  x: 'start',
                  y: 'center'
                }
              }
        });
    }

    return annotations;
}

// Improvement chart
const ctx = document.getElementById('timeProgressChart').getContext('2d');
const timeChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: indices.length > 1 ? indices : wrLabels,
        datasets: [pbDataset, wrDataset]
    },
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
                        }
                        return null;
                    }
                }
            },
            legend: {
                onClick: null
            },
            annotation: { // Rank bands
                common: { drawTime: 'beforeDraw' },
                annotations: []
            }
        },
        // interaction: {
        //     intersect: false,
        //     mode: 'index',
        // },
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

// Function to update rank bands dynamically
function updateRankBands() {
    if (showRankBands) {
        timeChart.options.plugins.annotation.annotations = getRankAnnotations(timeChart);
    } else {
        timeChart.options.plugins.annotation.annotations = [];
    }
    timeChart.update();
}

// Toggle WR line visibility
document.getElementById("toggleWR").addEventListener("click", function() {
    let wrDataset = timeChart.data.datasets[1];
    wrDataset.hidden = !wrDataset.hidden;
    showRankBands = !showRankBands;
    updateRankBands();
    timeChart.update();

    showRankBands = !showRankBands;
    updateRankBands();
    timeChart.update();
});

// Toggle log-scale
document.getElementById("toggleScale").addEventListener("click", function() {
    let yScale = timeChart.options.scales.y;
    if ( yScale.type == "linear" ) {
        yScale.type = "logarithmic";
    } else { yScale.type = "linear"; }

    // yScale.beginAtZero = !yScale.beginAtZero

    timeChart.update();
});

// Toggle Rank Bands Button
document.getElementById("toggleRankBands").addEventListener("click", function () {
    showRankBands = !showRankBands;
    updateRankBands();
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
            { className: "dt-body-center", targets: [3, 4, 5, 6, 7, 8] },
            { width: "11%", targets: [3, 4, 5, 6, 7, 8] }
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
