import React, { useState } from "react";
import axios from "axios";
import csvtojson from 'csvtojson';
import { async } from "q";

function Import_Button() {
    return(
        <div style= {{textAlign:"center"}}>
            <h1>Slice</h1>
            <form id ="input-button" >
                <input type={"file"} accept={".csv"}/>
                <input type = "submit" value = 'Upload'/>
                <button type='submit'>Import CSV Budget Sheet</button>
            </form>
        </div>
    );
}

const convertCsvToJson = async (csvFile) => {
    const jsonArray = await csvtojson().fromFile(csvFile.path);
    return jsonArray;
};

const sendJsonToApi = async(jsonData) =>{
    try {
        const response = await axios.post('API Endpoint',jsonData,{
            headers:{
                'Content-Type':'application/json',
            },
            
        });
        console.log(response.data);
    }catch (error){
        console.error('Error sending data to API:',error);
    }
};



export default Import_Button;