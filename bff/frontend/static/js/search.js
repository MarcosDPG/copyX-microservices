function activeSearch() {
    const searchInput = document.querySelector(".search-input");
    const searchButton = document.querySelector("#bt-buscar");

    function filterUsers(event) {
        if (event) event.preventDefault(); // Evita que el formulario se envíe

        let searchTerm = searchInput.value.toLowerCase().trim();
        let userCards = document.querySelectorAll(".user-card");

        userCards.forEach(card => {
            const name = card.querySelector("p").textContent.toLowerCase();
            const username = card.querySelector("a").textContent.toLowerCase();

            card.style.display = (searchTerm === "" || name.includes(searchTerm) || username.includes(searchTerm))
                ? "flex"  // Muestra coincidencias
                : "none";  // Oculta las que no coinciden
        });
    }

    try {
        // Activar búsqueda en tiempo real
        searchInput.addEventListener("input", filterUsers);

        // Evitar recargar la página al presionar el botón
        searchButton.addEventListener("click", function(event) {
            event.preventDefault();
            filterUsers();
        }); 
    } catch (error) {}  
}