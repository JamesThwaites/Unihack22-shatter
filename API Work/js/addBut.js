
let subs_array = new Array();

function addSub(id) {
    let value = document.getElementById(id).value;
    subs_array.push(value)
    document.getElementById(id).value = "";
    console.log(subs_array)
}