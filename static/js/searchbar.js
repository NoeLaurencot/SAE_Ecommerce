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