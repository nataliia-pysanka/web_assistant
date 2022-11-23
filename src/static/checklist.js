window.onload = (event) => {
  initMultiselect();
};

function initMultiselect() {
  checkboxStatusChange();

  document.addEventListener("click", function(evt) {
    let flyoutElement = document.getElementById('myMultiselect'),
      targetElement = evt.target; // clicked element

    do {
      if (targetElement == flyoutElement) {
        // This is a click inside. Do nothing, just return.
        //console.log('click inside');
        return;
      }

      // Go up the DOM
      targetElement = targetElement.parentNode;
    } while (targetElement);

    // This is a click outside.
    toggleCheckboxArea(true);
    //console.log('click outside');
  });
}

function checkboxStatusChange() {
  let multiselect = document.getElementById("mySelectLabel");
  let multiselectOption = multiselect.getElementsByTagName('option')[0];

  let values = [];
  let checkboxes = document.getElementById("mySelectOptions");
  let checkedCheckboxes = checkboxes.querySelectorAll('input[type=checkbox]:checked');

  for (const item of checkedCheckboxes) {
    let checkboxValue = item.getAttribute('value');
    values.push(checkboxValue);
  }

  let dropdownValue = "Nothing is selected";
  if (values.length > 0) {
    dropdownValue = values.join(', ');
  }

  multiselectOption.innerText = dropdownValue;
}

function toggleCheckboxArea(onlyHide = false) {
  let checkboxes = document.getElementById("mySelectOptions");
  let displayValue = checkboxes.style.display;

  if (displayValue != "block") {
    if (onlyHide == false) {
      checkboxes.style.display = "block";
    }
  } else {
    checkboxes.style.display = "none";
  }
}