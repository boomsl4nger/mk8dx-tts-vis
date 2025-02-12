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
});