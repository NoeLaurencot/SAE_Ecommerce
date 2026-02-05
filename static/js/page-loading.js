let startTime = new Date();

window.addEventListener("load", function() {
    let body = document.getElementById("page-loader")
    let finishTime = new Date() - startTime;
    console.log(finishTime)
    if (finishTime > 1000) {
        body.style.transition = "0.4s filter";
    }

    body.removeAttribute("id");
});