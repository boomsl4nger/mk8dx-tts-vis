import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

// Colouring cells
const standardsNames = [
    'God', 
    'Myth A', 'Myth B', 'Myth C', 
    'Titan A', 'Titan B', 'Titan C', 
    'Hero A', 'Hero B', 'Hero C', 
    'Exp A', 'Exp B', 'Exp C', 
    'Adv A', 'Adv B', 'Adv C', 
    'Int A', 'Int B', 'Int C', 
    'Beg A', 'Beg B', 'Beg C'
];

// See: https://d3js.org/d3-scale-chromatic
const rankColormap = new Map();
standardsNames.forEach((rank, i) => {
    // Evenly spaced color for each standard
    // rankColormap.set(rank, d3.interpolateTurbo(i / (standardsNames.length - 1)));

    // Some bullshit to group subranks closer together using tint
    let index = 0.05;
    let color = tintColor(d3.interpolateTurbo(index), 30);
    if (i > 0) {
        index += Math.floor((i+2)/3) * 0.9 / 7;
        color = d3.interpolateTurbo(index);
        if ((i-1) % 3 == 0) { color = tintColor(color, 10, true); }
        if ((i-1) % 3 == 1) { color = tintColor(color, 30); }
        if ((i-1) % 3 == 2) { color = tintColor(color, 50); }
    };
    rankColormap.set(rank, color);
});

const DIFF_MAX = 10;
const DIFF_STEP = 1.0;

function getWRDiffColor(diff) {
    if (isNaN(diff)) { return "white"}

    // Normalise based on diff range
    // let normalisedDiff = Math.max(DIFF_MIN, Math.min(diff, DIFF_MAX)) / DIFF_MAX;
    // return d3.interpolateSpectral(1 - normalizedDiff);

    // Set interval mapping
    let index = Math.max(0, Math.min(Math.floor(diff / DIFF_STEP) / (DIFF_MAX / DIFF_STEP), 1));
    return d3.interpolateSpectral(1 - index);
};

function tintColor(color, percent, darken = false) {
    let rgb = d3.color(color); // d3.color() parses any valid color
    if (!rgb) return color;

    // Lightens the given colour by default, otherwise darkens
    let bw = "#FFFFFF";
    if (darken) { bw = "#000000"; }

    return d3.interpolateRgb(color, bw)(percent / 100);;
};


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
