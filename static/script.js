function submitUsername() {
    var x = document.forms["myForm"]["fname"].value;
    if (x == "") {
        alert("Username must be filled out");
        return false;
    }
}