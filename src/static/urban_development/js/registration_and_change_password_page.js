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
    
    if (informationRow.className === "hidden-row help-message") {
        if (errorRow.className === "message error") {
            errorRow.style.display = "none";
        }

        informationRow.className = "message";
    }
}

function loseFocus() {
    let inputRow = window.event.target.parentNode.parentNode;
    let informationRow = inputRow.nextElementSibling;
    let errorRow = informationRow.nextElementSibling;

    if (informationRow.className === "message") {
        if (errorRow.className === "message error") {
            errorRow.style.display = "block";
        }

        informationRow.className = "hidden-row help-message";
    }
}
