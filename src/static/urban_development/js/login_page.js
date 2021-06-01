// function change() {
//     let inputRow = window.event.target.parentNode.parentNode;
//     let errorRow = inputRow.parentNode.firstElementChild;
//     let blankRow = errorRow.nextElementSibling;

//     errorRow.className = "hidden-row";
//     blankRow.className = "hidden-row";
// }

// function gainFocus() {
//     let inputRow = window.event.target.parentNode.parentNode;
//     let informationRow = inputRow.nextElementSibling;
//     let blankRow = informationRow.nextElementSibling;

//     if (informationRow.firstElementChild.className === "help-message") {
//         informationRow.style.display = "table-row";
//         blankRow.className = "hidden-row";
//     } else {
//         informationRow.style.display = "none";
//         blankRow.className = "blank-row";
//     }
// }

// function loseFocus() {
//     let inputRow = window.event.target.parentNode.parentNode;
//     let informationRow = inputRow.nextElementSibling;
//     let blankRow = informationRow.nextElementSibling;

//     informationRow.style.display = "none";
//     blankRow.className = "blank-row";
// }
