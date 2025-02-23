import { rankColormap, getWRDiffColor, tintColor } from "./colour_utils.js";

// Charts
const wrDiffCtx = document.getElementById('wrDiffChart').getContext('2d');
const wrDiffData = {
    labels: diff_labels,
    datasets: [{
        label: 'WR Diff Distribution',
        data: diff_data
    }]
};

new Chart(wrDiffCtx, {
    type: 'bar',
    data: wrDiffData,
    options: {
        responsive: true,
        aspectRatio: 1.4,
        scales: {
            y: { beginAtZero: true }
        }
    }
});

const rankCtx = document.getElementById('rankChart').getContext('2d');
const rankData = {
    labels: rank_labels,
    datasets: [{
        label: 'Rank Distribution',
        data: rank_data
    }]
};

new Chart(rankCtx, {
    type: 'bar',
    data: rankData,
    options: {
        responsive: true,
        aspectRatio: 1.4,
        indexAxis: 'y', // Vertical bar chart
        scales: {
            x: { beginAtZero: true }
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
    let table = new DataTable("#timesheetTable", {
        // See: https://datatables.net/manual/options
        paging: false,
        info: false,
        searching: false,
        columnDefs: [
            { className: "dt-head-left", targets: "_all" },
            { className: "dt-body-center", targets: [2, 3, 4, 5, 6, 7] },
            { width: "11%", targets: [2, 3, 4, 5, 6, 7] },
            // { orderable: false, targets: [0] }
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
