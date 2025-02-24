import { rankColormap, getWRDiffColor } from "./colour_utils.js";

const wrBarColors = diff_labels.map(label => {
    let diff = parseFloat(label);
    return getWRDiffColor(diff);
});

const rankColors = rank_labels.map(rank => rankColormap.get(rank) || "#CCCCCC"); // Default gray if not found

// Charts
const wrDiffCtx = document.getElementById('wrDiffChart').getContext('2d');
const wrDiffData = {
    labels: diff_labels,
    datasets: [{
        label: 'WR Diff Distribution',
        data: diff_data,
        backgroundColor: wrBarColors,
        borderColor: wrBarColors
    }]
};

new Chart(wrDiffCtx, {
    type: 'bar',
    data: wrDiffData,
    options: {
        responsive: true,
        aspectRatio: 1.4,
        plugins: {
            legend: {
                onClick: null
            }  
        },
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
        data: rank_data,
        backgroundColor: rankColors,
        borderColor: rankColors
    }]
};

new Chart(rankCtx, {
    type: 'bar',
    data: rankData,
    options: {
        responsive: true,
        aspectRatio: 1.4,
        plugins: {
            legend: {
                onClick: null
            }  
        },
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
            { className: "dt-body-center", targets: [3, 4, 5, 6, 7, 8] },
            { width: "11%", targets: [3, 4, 5, 6, 7, 8] },
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
