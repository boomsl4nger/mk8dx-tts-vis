import colormap from "https://cdn.jsdelivr.net/npm/colormap@2.3.2/+esm";

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
        let rank = cell.innerText.trim(); // Get text inside the cell
        if (rankColormap[rank]) {
            cell.style.backgroundColor = rankColormap[rank];
        }
    });

    // Colour WR Diff col
    document.querySelectorAll(".colour-diff").forEach(cell => {
        let diff = parseFloat(cell.getAttribute("data-sort")); // Convert to number
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

// See: https://www.jsdelivr.com/package/npm/colormap
const rankColors = colormap({
    colormap: "plasma",
    nshades: standardsNames.length,
    format: "hex",
    alpha: 1
});

let rankColormap = {};
for (let i = 0; i < standardsNames.length; i++) {
    rankColormap[standardsNames[i]] = rankColors[i]
};

const DIFF_MIN = 0;
const DIFF_MAX = 10;
const DIFF_STEP = 2;
const DIFF_COUNT = Math.floor((DIFF_MAX - DIFF_MIN) / DIFF_STEP) + 1;

const diffColors = colormap({
    colormap: "bluered",
    nshades: DIFF_COUNT,
    format: "hex",
    alpha: 1
});

function getWRDiffColor(diff) {
    let index = Math.max(0, Math.min(Math.floor(diff / DIFF_STEP), diffColors.length - 1));
    return diffColors[index];
};
