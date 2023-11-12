import React from "react";

function Submit_Button() {
    return(
        <div style= {{textAlign:"center"}}>
            <h1>Slice</h1>
            <form>
                <input type={"file"} accept={".csv"} />
                <button>Import CSV Budget Sheet</button>
            </form>
        </div>
    );
}