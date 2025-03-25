document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            let url = this.getAttribute("href");
            if (url.endsWith("/") && url.length > 1) {
                url = url.slice(0, -1);
            }
            if (url == "/") {
                url = "/home";
            }
            changeContent(url);
        });
    });

    window.addEventListener("popstate", function () {
        let p = location.pathname;
        if (p.endsWith("/") && p.length > 1) {
            p = p.slice(0, -1);
        }
        if (p == "/compose/post") {
            composePost(false);
        } else {
            closeComposePost();
            if (p == "/") {
                p = "/home";
            }
            fetch(p, { headers: { "X-Requested-With": "XMLHttpRequest" } })
                .then(response => response.text())
                .then(html => {
                    document.getElementById("content").innerHTML = html;
                    OptionSelected = 0;
                    changeIcon(location.pathname);
                });
        }
    });
    changeIcon(window.location.pathname);
});

function activeTextAreaPostCompose() {
    try {
        document.querySelectorAll(".post_compose_container .textarea_container textarea").forEach(area => {
            area.addEventListener("input", function () {
                this.style.height = "auto";
                this.style.height = (this.scrollHeight) + "px";
            });
        });
    } catch (error) {}
}

function activeRequestPostCompose() {
    document.querySelectorAll(".textarea_container").forEach(form => {
        // Verificamos si el formulario ya tiene el evento agregado
        if (form.dataset.eventAdded) return;
        form.dataset.eventAdded = "true"; // Marcamos que ya tiene el listener
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            let textarea = form.querySelector(".tweet_content");
            let content = textarea.value.trim();

            if (!content) {
                alert("El tweet no puede estar vacío");
                return;
            }

            let formData = new FormData(this);
            let headers = {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": formData.get("csrfmiddlewaretoken")
            };

            let path = window.location.pathname;
            if (path.startsWith("/") && path.length > 1) {
                path = `/${path.split("/")[1]}/`
            }
            if (path.endsWith("/") && path.length > 1) {
                path = path.slice(0, -1);
            }
            if (path === '/post') {
                formData = JSON.stringify({
                    tweet: document.querySelector('div[id-post]').getAttribute('id-post'),
                    content: content
                });
                headers["Content-Type"] = "application/json";
            }

            fetch(this.action, {
                method: this.method,
                body: formData,
                headers: headers,
                credentials: "include"
            })
            .then(response => {
                if (response.status === 201) {
                    return response.json();
                }
                throw new Error("Error en la solicitud, código: " + response.status);
            })
            .then(data => {
                textarea.value = "";
                loadResources(window.location.pathname);
            })
            .catch(error => {
                console.error("Error en la solicitud:", error);
                alert("No se pudo conectar con el servidor o hubo un problema");
            });
        });
    });
}

function activeHomeMenuOptions() {
    document.querySelectorAll(".option_home_menu").forEach(option => {
        option.addEventListener("click", function () {
            let p = location.pathname;
            if (p.endsWith("/") && p.length > 1) {
                p = p.slice(0, -1);
            }
            OptionSelected = parseInt(this.getAttribute("number-option-target"))
            loadResources(location.pathname);
            document.querySelectorAll(".option_home_menu").forEach(option =>{
                option.classList.remove("selected");
            })
            this.classList.add("selected");
        });
    });
}

function changeIcon(path) {
    setTimeout(() => {
        loadResources(path);
    }, 100);
    activeTextAreaPostCompose();
    activeRequestPostCompose()
    activeHomeMenuOptions();
    if (path.endsWith("/") && path.length > 1) {
        path = path.slice(0, -1);
    }
    if (path == "/compose/post") {
        history.pushState(null,"home","/");
        composePost(true);
    }
    if (path == "/home" || path == "/compose/post") {
        path = "/";
    }
    document.querySelectorAll(".icon_menu").forEach(icon => icon.setAttribute("fill", "none"));

    let activeLink = document.querySelector(`.nav-link[href="${path}"]`);
    if (activeLink) {
        activeLink.querySelector(".icon_menu").setAttribute("fill", "white");
    }
}

function isSamePath(url1, url2) {
    if (url1.endsWith("/") && url1.length > 1) {
        url1 = url1.slice(0, -1);
    }
    if (url1 == "/home") {
        url1="/"
    }
    if (url2.endsWith("/") && url2.length > 1) {
        url2 = url2.slice(0, -1);
    }
    if (url2 == "/home") {
        url2="/"
    }
    return url1 !== url2;
}

function composePost(bool) {
    document.getElementById("cobertor").classList.add("active");
    if(bool) {
        history.pushState(null, '', '/compose/post');
        console.log("si");
    }
}

function closeComposePost() {
    document.getElementById("cobertor").querySelector("textarea").value = "";
    document.getElementById("cobertor").classList.remove("active");
}