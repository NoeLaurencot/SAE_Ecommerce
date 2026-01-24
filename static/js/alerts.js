let alerts = document.getElementsByClassName("alert");

for (let i = 0; i < alerts.length; i++) {
    let alert = alerts[i];
    alert.style.left = "0";
    alert.style.bottom = (20 + i * 75) + "px";

    let closeBtn = alert.querySelector("button");
    closeBtn.addEventListener("click", function () {
        alert.style.left = "-100%";
        setTimeout(function () {
            alert.remove();
        }, 500);
    });
}