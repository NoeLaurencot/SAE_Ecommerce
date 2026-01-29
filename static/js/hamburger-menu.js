let menuBtn = document.getElementById("nav-burger-menu");
let menuContainer = document.getElementById("burger-menu");
let screenBlur = document.getElementById("screen-blur");

menuBtn.addEventListener("click", function () {
    menuBtn.classList.toggle("burger-menu-button-active");
    menuContainer.classList.toggle("burger-menu-active");
    screenBlur.classList.toggle("screen-blur-active");
    document.body.style.overflow = 'hidden';
    menuContainer.focus();
});

screenBlur.addEventListener("click", function () {
    menuBtn.classList.toggle("burger-menu-button-active");
    menuContainer.classList.toggle("burger-menu-active");
    screenBlur.classList.toggle("screen-blur-active");
    document.body.style.overflow = '';
});

document.addEventListener("keydown", function (event) {
    if (event.key === 'Escape' && menuContainer.classList.contains("burger-menu-active")) {
        menuBtn.classList.toggle("burger-menu-button-active");
        menuContainer.classList.toggle("burger-menu-active");
        screenBlur.classList.toggle("screen-blur-active");
        document.body.style.overflow = '';
    }

    if (event.key === 'Enter' && document.activeElement === menuBtn) {
        menuBtn.classList.toggle("burger-menu-button-active");
        menuContainer.classList.toggle("burger-menu-active");
        screenBlur.classList.toggle("screen-blur-active");
        document.body.style.overflow = 'hidden';
        menuContainer.focus();
    }
});