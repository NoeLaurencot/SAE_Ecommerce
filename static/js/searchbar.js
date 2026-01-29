let searchbarButton = document.getElementById("nav-search-button");
let search = document.getElementById("nav-search-container");
let isActive = false;

searchbarButton.addEventListener("click", function() {
    if (!isActive) {
        search.classList.add('nav-search-active');
        isActive = true;
    } else {
        search.classList.remove('nav-search-active');
        isActive = false;
    }
});