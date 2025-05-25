document.addEventListener("DOMContentLoaded", function () {
    
    const modal = document.getElementById("deleteModal");
    modal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute("data-url");

        // Show loader
        const contentContainer = document.getElementById('deleteModalContent');
        contentContainer.innerHTML = `
        <div class="d-flex justify-content-center align-items-center" style="min-height: 200px;">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        `;

        fetch(url).then(response => response.text())
        .then(html => {
            document.getElementById("deleteModalContent").innerHTML = html;
        });
    });
});
