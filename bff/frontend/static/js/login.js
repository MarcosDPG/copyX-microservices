document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();  // Evita recargar la página

        const formData = new URLSearchParams(new FormData(form));

        try {
            const response = await fetch("/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
                body: formData.toString(),
            });

            const data = await response.json();  // Convierte la respuesta a JSON

            if (response.ok) {
                window.location.href = "/home/";  // Redirige si el login es exitoso
            } else {
                showError(data.message || "Usuario o contraseña incorrectos.");
            }
        } catch (error) {
            console.error("Error al iniciar sesión:", error);
            showError("Ocurrió un error. Inténtalo más tarde.");
        }
    });

    document.querySelector(".button-toggle").addEventListener("click", toggleInputType);

    function toggleInputType() {
        const inputElement = document.querySelector(".input-toggle");
        inputElement.type = inputElement.type === "text" ? "password" : "text";

        document.querySelector(".show-icon").classList.toggle("hidden");
        document.querySelector(".hide-icon").classList.toggle("show");
    }

    function showError(message) {
        let errorMessage = document.querySelector(".error-message");

        if (!errorMessage) {
            errorMessage = document.createElement("p");
            errorMessage.classList.add("error-message");
            errorMessage.style.color = "red";
            form.appendChild(errorMessage);
        }

        errorMessage.textContent = message;
        errorMessage.style.display = "block";
    }
});
