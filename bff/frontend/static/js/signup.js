document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new URLSearchParams(new FormData(form));

        try {
            const response = await fetch("/signup/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
                body: formData.toString(),
            });

            if (response.ok) {
                window.location.href = "/login/";
            } else {
                const errorData = await response.json();
                alert(errorData.message);
                alert(response.statusText);
                console.log(errorData);
                console.error(response.body);
            }
        } catch (error) {
            console.error("Error al registrar:", error);
            alert("Ocurrió un error. Inténtalo más tarde.");
        }
    });

    document.querySelector(".button-toggle").addEventListener("click", toggleInputType);

    function toggleInputType(){
        const inputElement = document.querySelector(".input-toggle");
        inputElement.type = inputElement.type === "text" ? "password" : "text"
        
        const showIcon = document.querySelector(".show-icon").classList.toggle("hidden");
        const hideIcon = document.querySelector(".hide-icon").classList.toggle("show");
    }
    
});