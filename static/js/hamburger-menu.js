let menuBtn = document.getElementById("nav-burger-menu");
let menuContainer = document.getElementById("burger-menu");
let screenBlur = document.getElementById("screen-blur");

menuBtn.addEventListener("click", function () {
    menuBtn.classList.toggle("burger-menu-button-active");
    menuContainer.classList.toggle("burger-menu-active");
    screenBlur.classList.toggle("screen-blur-active");
});

screenBlur.addEventListener("click", function () {
    menuBtn.classList.toggle("burger-menu-button-active");
    menuContainer.classList.toggle("burger-menu-active");
    screenBlur.classList.toggle("screen-blur-active");
});

document.addEventListener("keydown", function (event) {
    if (event.key === 'Escape' && menuContainer.classList.contains("burger-menu-active")) {
        menuBtn.classList.toggle("burger-menu-button-active");
        menuContainer.classList.toggle("burger-menu-active");
        screenBlur.classList.toggle("screen-blur-active");
    }

    if (event.key === 'Enter' && document.activeElement === menuBtn) {
        menuBtn.classList.toggle("burger-menu-button-active");
        menuContainer.classList.toggle("burger-menu-active");
        screenBlur.classList.toggle("screen-blur-active");
    }
});