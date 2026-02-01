let arrowUpArr = document.getElementsByClassName('input-vetement-up');
let arrowDownArr = document.getElementsByClassName('input-vetement-down');

for (let i = 0; i < arrowUpArr.length; i++) {
    let arrowUp = arrowUpArr[i];
    let arrowDown = arrowDownArr[i];

    arrowUp.addEventListener('click', function () {
        let input = arrowUp.parentElement.querySelector('input');
        let value = parseInt(input.value);
        let max = parseInt(input.max);
        if (value < max) {
            input.value = value + 1;
        }
    });

    arrowDown.addEventListener('click', function () {
        let input = arrowDown.parentElement.querySelector('input');
        let value = parseInt(input.value);
        let min = parseInt(input.min);
        if (value > min) {
            input.value = value - 1;
        }
    });
}