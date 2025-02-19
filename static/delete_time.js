document.addEventListener("DOMContentLoaded", function() {
    let deleteButtons = document.querySelectorAll(".delete-btn");
    let deleteForm = document.getElementById("deleteForm");
    let deleteTrack = document.getElementById("deleteTrack");
    let deleteTime = document.getElementById("deleteTime");
    let deleteCC = document.getElementById("deleteCC");
    let deleteItems = document.getElementById("deleteItems");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function() {
            let entryId = this.getAttribute("data-id");
            deleteTrack.textContent = this.getAttribute("data-track");
            deleteTime.textContent = this.getAttribute("data-time");
            deleteCC.textContent = this.getAttribute("data-cc");
            deleteItems.textContent = this.getAttribute("data-items");

            // deleteForm.action = "{{ url_for('delete_time', entry_id=0) }}".replace('0', entryId);
            deleteForm.action = deleteForm.dataset.baseUrl.replace('0', entryId);
        });
    });

    if (new URLSearchParams(window.location.search).has("deleted")) {
        document.getElementById("deleteSuccessAlert").classList.remove("d-none");
    }
});
