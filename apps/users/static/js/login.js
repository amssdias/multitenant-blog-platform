document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();

    let formData = new FormData(this);

    fetch(loginUrl, {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Redirect User to Their Subdomain After Cookie Is Stored
        window.location.href = data.redirect_url;
    })
    .catch(error => console.error("Error:", error));
});
