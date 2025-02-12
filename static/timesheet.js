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
    rankColormap.set(rank, d3.interpolateViridis(i / (standardsNames.length - 1)));
});

const DIFF_MAX = 10;
const DIFF_STEP = 1.0;

function getWRDiffColor(diff) {
    // Normalise based on diff range
    // let normalisedDiff = Math.max(DIFF_MIN, Math.min(diff, DIFF_MAX)) / DIFF_MAX;
    // return d3.interpolateSpectral(1 - normalizedDiff);

    // Set interval mapping
    let index = Math.max(0, Math.min(Math.floor(diff / DIFF_STEP) / (DIFF_MAX / DIFF_STEP), 1));
    return d3.interpolateSpectral(1 - index);
};
