let filtreButton = document.getElementById("filtre-button");
let filtreContainer = document.getElementById("filtre-menu");

function openMenuFiltre() {
    filtreContainer.classList.add("filtre-menu-active");
}

function closeMenuFiltre() {
    filtreContainer.classList.remove("filtre-menu-active");
}

function toggleFiltre() {
    if (filtreContainer.classList.contains("filtre-menu-active")) {
        closeMenuFiltre();
    } else {
        openMenuFiltre();
    }
}

filtreButton.addEventListener("click", function() {
    toggleFiltre();
});