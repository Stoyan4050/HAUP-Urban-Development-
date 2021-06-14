function change() {
    document.getElementById("form-error").style.display = "none";
}

function gainFocus() {
    let inputRow = window.event.target.parentNode.parentNode;
    let informationRow = inputRow.nextElementSibling;
    
    if (informationRow.className === "hidden-row help-message") {
        informationRow.className = "message";
    }
}

function loseFocus() {
    let inputRow = window.event.target.parentNode.parentNode;
    let informationRow = inputRow.nextElementSibling;

    if (informationRow.className === "message") {
        informationRow.className = "hidden-row help-message";
    }
}
