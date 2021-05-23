function change() {
    let inputRow = window.event.target.parentNode.parentNode;
    let informationRow = inputRow.nextElementSibling;
    let errorRow = informationRow.nextElementSibling;
    
    errorRow.className = "hidden-row";
}

function gainFocus() {
    let inputRow = window.event.target.parentNode.parentNode;
    let informationRow = inputRow.nextElementSibling;
    let errorRow = informationRow.nextElementSibling;
    let blankRow = errorRow.nextElementSibling;
    
    errorRow.style.display = "none";
    
    if (informationRow.firstElementChild.className === "help-message") {
        informationRow.style.display = "table-row";
        blankRow.className = "hidden-row";
    } else {
        informationRow.style.display = "none";
        blankRow.className = "blank-row";
    }
}

function loseFocus() {
    let inputRow = window.event.target.parentNode.parentNode;
    let informationRow = inputRow.nextElementSibling;
    let errorRow = informationRow.nextElementSibling;
    let blankRow = errorRow.nextElementSibling;
    
    informationRow.style.display = "none";
    
    if (errorRow.className === "error-message") {
        errorRow.style.display = "table-row";
        blankRow.className = "hidden-row";
    } else {
        errorRow.style.display = "none";
        blankRow.className = "blank-row";
    }
}
