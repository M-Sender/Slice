import React, { useState } from "react";

function fileRead(){
    const [file,setFile] = useState()

    const fileReader = new FileReader()

    const handleOnChange = (e) => {
        setFile(e.target.files[0]);};

        
    const handleOnSubmit = (e) =>{
        e.preventDefault();
        
        if (file){
            fileReader.onload = function (event) {
                const fileOutput = event!.target!.result;
            };

            fileReader.readAsText(file);
        }
    };

    return(
        <div style = {{ textAlign:"center" }}>
            <h1>Import CSV</h1>
            <form>
                <input type={"file"} id={"csvFileInput"} accept={".csv"} onChange={handleOnChange}/>
                <button onClick={(e)=>{
                    handleOnSubmit(e);
                }}
                >
                    Import CSV
                </button>
            </form>
        </div>
    );
}




