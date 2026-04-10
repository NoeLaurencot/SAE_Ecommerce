function loadFile(event) {
    
}

let arrowUpArr = document.getElementsByClassName('input-vetement-up');
let arrowDownArr = document.getElementsByClassName('input-vetement-down');

for (let i = 0; i < arrowUpArr.length; i++) {
    let arrowUp = arrowUpArr[i];
    let arrowDown = arrowDownArr[i];

    arrowUp.addEventListener('click', function () {
        let input = arrowUp.parentElement.querySelector('input');
        let value = parseInt(input.value, 10);
        let min = parseInt(input.min, 10);
        let max = parseInt(input.max, 10);

        if (Number.isNaN(min)) {
            min = 0;
        }
        if (Number.isNaN(value)) {
            value = min;
        }

        if (Number.isNaN(max) || value < max) {
            input.value = value + 1;
        }
    });

    arrowDown.addEventListener('click', function () {
        let input = arrowDown.parentElement.querySelector('input');
        let value = parseInt(input.value, 10);
        let min = parseInt(input.min, 10);

        if (Number.isNaN(min)) {
            min = 0;
        }
        if (Number.isNaN(value)) {
            value = min;
        }

        if (value > min) {
            input.value = value - 1;
        }
    });
}