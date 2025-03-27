function loadResources(path="") {
    if (path.endsWith("/") && path.length > 1) {
        path = path.slice(0, -1);
    }
    id =  ""
    if ((path.startsWith("/profile") && !path.endsWith("/profile")) || (path.startsWith("/post") && !path.endsWith("/post"))) {
        id = path.split("/")[2]
        path = `/${path.split("/")[1]}/`
    }
    switch (path) {
        case "/":
            fetchPosts()
            break;
        case "/home":
            fetchPosts()
            break;
        case "/compose/post":
            history.back()
            break;
        case "/profile":
            switch (OptionSelected) {
                case 0:
                    fetchPosts(USER_ID)
                    break;
                case 1:
                    fetchReposts(USER_ID)
                    break;
                case 2:
                    fetchLikes(USER_ID)
                    break;
                default:
                    break;
            }
            break;
        case "/profile/":
            switch (OptionSelected) {
                case 0:
                    fetchPosts(id)
                    break;
                case 1:
                    fetchReposts(id)
                    break;
                case 2:
                    fetchLikes(id)
                    break;
                default:
                    break;
            }
            break;
        case "/settings":
            loadSettingsPartial(option=parseInt(OptionSelected))
            break;
        case "/search":
            loadUsers()
            break;
        case "/post/":
            loadPost(id)
            break;
        default:
            break;
    }
}

function fetchPosts(userid="") {
    path = `/posts/${userid}`
    if (path.endsWith("/") && path.length > 1) {
        path = path.slice(0, -1);
    }
    fetch(path, { credentials: "include" })
    .then(response => response.text())
    .then(html => {
        const container = document.getElementById("post_container");
        container.innerHTML = html;
    })
    .catch(error => console.error("Error cargando datos:", error));
}

function fetchReposts(userid="") {
    fetch(`/reposts/${userid}`, { credentials: "include" })
    .then(response => response.text())
    .then(html => {
        const container = document.getElementById("post_container");
        container.innerHTML = html;
    })
    .catch(error => console.error("Error cargando datos:", error));
}

function fetchLikes(userid="") {
    fetch(`/likes/${userid}`, { credentials: "include" })
    .then(response => response.text())
    .then(html => {
        const container = document.getElementById("post_container");
        container.innerHTML = html;
    })
    .catch(error => console.error("Error cargando datos:", error));
}

function loadSettingsPartial(option=0,target="") {
    if (target == "") {
        target = document.querySelector(`.option_home_menu[number-option-target='${option}']`).getAttribute("data-target");
    }
    fetch(`/settings/${target}`, { headers: { "X-Requested-With": "XMLHttpRequest" }, credentials: "include" })
        .then(response => response.text())
        .then(html => {
            document.querySelector(".settings .column_menu").innerHTML = html;
        })
        .catch(err => console.error("Error cargando opciones:", err));
}

function toggleSelection(obj) {
    event.stopPropagation()
    let ignoredElements = ["INPUT", "BUTTON", "TEXTAREA", "SELECT"];
    if (ignoredElements.includes(event.target.tagName)) {
        return; 
    }
    obj.classList.toggle("selected");
}

function loadUsers() {
    fetch(`/users/`, { credentials: "include" })
    .then(response => response.text())
    .then(html => {
        const container = document.getElementById("post_container");
        container.innerHTML = html;
    })
    .catch(error => console.error("Error cargando datos:", error));
}

function loadPost(post_id) {
    console.log(post_id)
    fetch(`/comments/${post_id}`, { credentials: "include" })
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById("comments_container");
            container.innerHTML = html;
        })
        .catch(error => console.error("Error cargando datos:", error));
}