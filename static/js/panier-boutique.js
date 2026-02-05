document.addEventListener("DOMContentLoaded", function () {
    const panierWrapper = document.getElementById("panier-boutique-button")?.closest(".panier-boutique-wrapper");
    const panierBtn = document.getElementById("panier-boutique-button");
    const panierClose = document.getElementById("panier-boutique-close");

    if (!panierWrapper || !panierBtn) return;

    function openPanier() {
        panierWrapper.classList.add("panier-boutique-active");
    }

    function closePanier() {
        panierWrapper.classList.remove("panier-boutique-active");
    }

    function togglePanier() {
        if (panierWrapper.classList.contains("panier-boutique-active")) {
            closePanier();
        } else {
            openPanier();
        }
    }

    panierBtn.addEventListener("click", togglePanier);

    if (panierClose) {
        panierClose.addEventListener("click", closePanier);
    }

    document.addEventListener("click", function (event) {
        if (panierWrapper.classList.contains("panier-boutique-active")) {
            if (!panierWrapper.contains(event.target)) {
                closePanier();
            }
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && panierWrapper.classList.contains("panier-boutique-active")) {
            closePanier();
        }
    });
});
