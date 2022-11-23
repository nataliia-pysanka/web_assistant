window.onload = function() {
    (function() {
        let todayDate = new Date().toISOString().slice(0, 10);

        const inputs = document.querySelectorAll('.add-form__input');
        const modal = document.getElementById("modal");
        const inputAdress = document.getElementById("adress");
        const inputGroup = document.getElementById("group");
        const plus_btn = document.getElementById("plus_btn");
        const inputBirth = document.getElementById("birthday");

        let width = modal.offsetWidth / 4;

        for (const input of inputs) {
            input.style.width = (width).toString() + "px";
        };

        inputAdress.style.width = (width * 2 + 30).toString() + "px";
        inputBirth.style.width = (width + 10).toString() + "px";
        inputGroup.style.width = (width - plus_btn.offsetWidth).toString() + "px";

        let inputDate = document.getElementById("birthday");
        inputDate.setAttribute("max", todayDate);
        inputDate.classList.add('no-date');

        inputDate.addEventListener('focus', function() {
            if (! this.value) {
                    this.classList.remove('no-date');
                    this.classList.add('date');
                }
        });

        inputDate.addEventListener('blur', function() {
            if (! this.value) {
                    this.classList.remove('date');
                    this.classList.add('no-date');
                }
        });

        inputs.forEach( function(input) {
            input.addEventListener('focus', function() {
                this.classList.add('focus');
                this.parentElement.querySelector('.add-form__placeholder').classList.add('focus');
            });
            input.addEventListener('blur', function() {
                this.classList.remove('focus');
                if (! this.value) {
                    this.parentElement.querySelector('.add-form__placeholder').classList.remove('focus');
                }
            });
        });
    })();
};

// function strToDate(date_str) {
//     let parts = date_str.split('-');
//     let date = new Date(parts[0], parts[1] - 1, parts[2]);
//     return date.toDateString();
// };
//
// function checkDate(date_str, min, max) {
//     if (strToDate(date_str) > strToDate(max) || strToDate(date_str) < min) {
//         return
//     }
// }