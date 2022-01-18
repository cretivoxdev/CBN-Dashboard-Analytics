function required() {
    var empt = document.forms["form1"]["uName"].value;
    if (empt == "") {
        alert("Please input a Value");
        return false;
    }
}

var val = document.getElementById("verif").innerText
if (val == "False") {
    alert("This is False")
} else {
    alert("This is True")
}

// Passing Start
const noTab = document.getElementById('noTab')
const linkTab = document.getElementById('linkTab')
const dateTab = document.getElementById('dateTab')
const likeTab = document.getElementById('likeTab')
const commentTab = document.getElementById('commentTab')
const viewTab = document.getElementById('viewTab')

// Passing End
var text = document.getElementById("testSplit").innerText
const myArray = text.split(" ")

noTab.textContent = `${myArray[0]}`;
linkTab.textContent = `${myArray[1]}`;
dateTab.textContent = `${myArray[2] + " | " + myArray[3]}`;
likeTab.textContent = `${myArray[4]}`;
commentTab.textContent = `${myArray[5]}`;
viewTab.textContent = `${myArray[6]}`;

console.log(text)

// var text = document.getElementById("testSplit")
// const myArray = text.toTextString().split(" ", 2);
// console.log(myArray)
// document.getElementById("testSplit").innerHTML = myArray;
// console.log(myArray)