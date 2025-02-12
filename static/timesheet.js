import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

document.addEventListener("DOMContentLoaded", function() {
    let table = new DataTable("#timesheetTable", {
        // See: https://datatables.net/manual/options
        paging: false,
        info: false,
        searching: false,
        columnDefs: [
            {className: "dt-head-left", targets: "_all"},
            {className: "dt-body-center", targets: [2, 3, 4, 5, 6, 7]},
            {width: "12%", targets: [2, 3, 4, 5, 6, 7]},
            // {orderable: false, targets: [0]}
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
});

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
    // Check input is numeric
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
