let searchbarOpenButton = document.getElementById("nav-search-open-button");
let searchbarCloseButton = document.getElementById("nav-search-close-button");
let search = document.getElementById("nav-search-container");
let input = document.getElementById('nav-searchbar');

searchbarOpenButton.addEventListener("click", function () {
    if (menuContainer.classList.contains("burger-menu-active")) {
        closeMenu();
    }
    search.classList.add("nav-search-active")
    setTimeout(function () {
        input.focus();
    }, 50);
});

searchbarCloseButton.addEventListener("click", function () {
    search.classList.remove("nav-search-active")
});

let suggestions = document.getElementById('search-suggestions');

input.addEventListener("keyup", function () {
    let value = input.value;
    if (value.length === 0) {
        suggestions.innerHTML = '';
        return;
    }
    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (request.readyState == 4 && request.status == 200) {
            var response =  (request.responseText)
            if (response == "Na") {
                suggestions.innerHTML = '';
            } else {
                let data = JSON.parse(response);
                suggestions.innerHTML = '';
                for (let i = 0; i < data.length; i++) {
                    let item = data[i];
                    let itemLink = document.createElement('a');
                    itemLink.className = 'search-suggestion-item';
                    itemLink.href = '/client/vetement/details?id_vetement=' + item.id_vetement;
                    itemLink.innerHTML = '<img src="/static/assets/images/clothes/' + item.photo + '" alt="' + item.nom_vetement + '">'
                        + '<div class="search-suggestion-text">'
                        + '<span class="search-suggestion-name">' + item.nom_vetement + '</span>'
                        + '<span class="search-suggestion-brand">' + item.marque + '</span>'
                        + '</div>';
                    suggestions.appendChild(itemLink);
                }
            }
        }
    }
    request.open("get", "/search/hint?search=" + value, true);
    request.send();
});

searchbarCloseButton.addEventListener("click", function () {
    suggestions.innerHTML = '';
});