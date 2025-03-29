const LIKE_URL = '/like/';
const RETWEET_URL = '/repost/';

function likeController(obj) {
    if (obj.classList.contains('liked') && obj.getAttribute('id-post') && obj.getAttribute('id-like')) {
        fetch(`${LIKE_URL}${obj.getAttribute('id-post')}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
        })
        .then(response => {
            if (response.status === 200) {
                return response.json();
            }
            throw new Error("Error en la solicitud, código: " + response.status);
        })
        .then(data => {
            let id_like = obj.getAttribute("id-like")
            let id_post = obj.getAttribute("id-post")
            objs = document.querySelectorAll("div[id-post][id-like]")
            objs.forEach(o => {
                if (o.getAttribute("id-post") == id_post) {
                    if (o.getAttribute("id-like") == id_like) {
                        o.setAttribute("id-like","")
                        o.classList.remove('liked');
                    }
                    o.nextElementSibling.textContent = parseInt(o.nextElementSibling.textContent) - 1;
                }
            });
        });
    } else {
        fetch(`${LIKE_URL}${obj.getAttribute('id-post')}/${parseInt(obj.getAttribute('type-post'))}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
        })
        .then(response => {
            if (response.status === 201) {
                return response.json();
            }
            throw new Error("Error en la solicitud, código: " + response.status);
        })
        .then(data => {
            let id_post = obj.getAttribute("id-post")
            objs = document.querySelectorAll("div[id-post][id-like]")
            objs.forEach(o => {
                if (o.getAttribute("id-post") == id_post) {
                    o.setAttribute('id-like', data.like_id || data.like);
                    o.classList.add('liked');
                    o.nextElementSibling.textContent = parseInt(o.nextElementSibling.textContent) + 1;
                }
            });
        });
    }
}

function repostController(obj) {
    if (obj.classList.contains('reposted') && obj.getAttribute('id-repost')) {
        fetch(`${RETWEET_URL}${obj.getAttribute('id-repost')}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
        })
        .then(response => {
            if (response.status === 200) {
                return response.json();
            }
            throw new Error("Error en la solicitud, código: " + response.status);
        })
        .then(data => {
            obj.removeAttribute('id-repost');
            obj.classList.remove('reposted');
            obj.nextElementSibling.textContent = parseInt(obj.nextElementSibling.textContent) - 1;
            loadResources(window.location.pathname);
        });
    } else {
        fetch(`${RETWEET_URL}${obj.getAttribute('id-post')}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include'
        })
        .then(response => {
            if (response.status === 201) {
                return response.json();
            }
            console.log(response.json());
            throw new Error("Error en la solicitud, código: " + response.status);
        })
        .then(data => {
            obj.setAttribute('id-repost', data.retweet_id);
            obj.classList.add('reposted');
            obj.nextElementSibling.textContent = parseInt(obj.nextElementSibling.textContent) + 1;
        });
    }
}

function commentController(obj) {
    path = window.location.pathname;
    if (path.startsWith("/") && path.length > 1) {
        path = `/${path.split("/")[1]}/`
    }
    if (path.endsWith("/") && path.length > 1) {
        path = path.slice(0, -1);
    }
    if (path != '/post') {
        url = `/post/${obj.getAttribute('id-post')}`
        changeContent(url)
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Busca el nombre del cookie al inicio de la cadena
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}