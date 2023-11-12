import React from "react"


function button() {

    function correctFileType(){
        var userInput = document.getElementById("User-File") as HTMLInputElement;
        
        var userFilePath = userInput.value;

        var allowedDocTypes = /(\.csv)$/i;

        if(!allowedDocTypes.exec(userFilePath)){
            alert("Invalid file type, must select a CSV file");
            userInput.value='';
            return false;
        }
    }
    const fileImptButton = document.getElementById("User-File") as HTMLInputElement;
    const customButton = document.getElementById("Input-Button");
    const displayText = document.getElementById("text");
    
    if (customButton&&fileImptButton){
    customButton.addEventListener("click", function() {
        fileImptButton.click();
    });}

    if(fileImptButton&&displayText){
    fileImptButton.addEventListener("change",function() {
    if(fileImptButton.value) {
        displayText.innerHTML = fileImptButton.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
    }
    else{
        displayText.innerHTML = "No file was selected";
    }})
    
    return(
        <div>
        <input type="file" id="User-File" hidden onChange={correctFileType}/>
        <button type="button" id="Input-Button"> Select a File</button>
        <span id="text"> No file was selected</span>
         </div>


    )
}}