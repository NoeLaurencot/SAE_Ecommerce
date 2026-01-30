
let menuBtn = document.getElementById("nav-burger-menu");
let menuContainer = document.getElementById("burger-menu");
let screenBlur = document.getElementById("screen-blur");

function openMenu() {
    menuBtn.classList.add("burger-menu-button-active");
    menuContainer.classList.add("burger-menu-active");
    screenBlur.classList.add("screen-blur-active");
    document.body.style.overflow = 'hidden';
    menuContainer.focus();
}

function closeMenu() {
    menuBtn.classList.remove("burger-menu-button-active");
    menuContainer.classList.remove("burger-menu-active");
    screenBlur.classList.remove("screen-blur-active");
    document.body.style.overflow = '';
    menuBtn.focus();
}

menuBtn.addEventListener("click", function () {
    if (menuContainer.classList.contains("burger-menu-active")) {
        closeMenu();
    } else {
        openMenu();
    }
});

screenBlur.addEventListener("click", function () {
    closeMenu();
});

document.addEventListener("keydown", function (event) {
    if (event.key === 'Escape' && menuContainer.classList.contains("burger-menu-active")) {
        closeMenu();
    }
    if (event.key === 'Enter' && document.activeElement === menuBtn) {
        if (menuContainer.classList.contains("burger-menu-active")) {
            closeMenu();
        } else {
            openMenu();
        }
    }
});