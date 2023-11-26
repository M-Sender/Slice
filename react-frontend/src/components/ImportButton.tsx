import React from "react";
import axios from "axios";
import csvtojson from 'csvtojson';
//import { async } from "q";
import config from "../config";



function ImportButton() {
    
    return(
        <div style= {{textAlign:"center"}}>
            <form id ="input-button" >
                <input type={"file"} accept={".csv"} onChange={(e) => sendCSV(e.target.value)}/>
                <input type = "submit" value = 'Upload'/>
            </form>
        </div>
    );
}

const sendCSV = (CSV : any ) =>{
    sendJsonToApi(convertCsvToJson(CSV));
}

const convertCsvToJson = async (csvFile) => {
    const jsonArray = await csvtojson().fromFile(csvFile.path);
    return jsonArray;
};

const sendJsonToApi = async(jsonData) =>{
    try {
        const response = await axios.post(config.server.route+"/uploadCSV",jsonData,{
            headers:{
                'Content-Type':'application/json',
            },
            
        });
        console.log(response.data);
    }catch (error){
        console.error('Error sending data to API:',error);
    }
};



export default ImportButton;