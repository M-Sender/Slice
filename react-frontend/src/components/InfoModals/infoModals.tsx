import React from "react";
import { Dropdown } from "react-bootstrap";
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Select from "react-dropdown-select";

export function MerchantModal({props}) {
    var merhchantID = undefined;
    var categoryID = undefined;
    var subgroupID = undefined;
    var merchantValues = {1:1,2:2};
    function setValues(){

    }
    //Call to Database to grab all merchant names, and send with ids to be sent back/ if needs to be created

    //Display all merchants and allow to select one or create a new one
    function mapNewMerchant(){
        //api with info create new mapping
    }

    function createNewCategory(){

    }

    function createNewSubgroup(){
        //api to create a new subgroup
    }



    //show modal to select a merchant to match
    //allow you to create a new merchant
    ////Input box + a select of category
    ////can create a new category
    //////category input field + select a subgroup
    //////can create a new subgroup
    ////////subgroup input box
    return(
        <div
      className="modal show"
      style={{ display: 'block', position: 'initial' }}
    >
      <Modal.Dialog>
        <Modal.Header closeButton>
          <Modal.Title>Select a Merchant to match {props.merchantName} with:</Modal.Title>
        </Modal.Header>

        <Modal.Body>
        <Modal.Dialog title="Merchant Select">
            <Select options={props.Merchants} onChange={mapNewMerchant} onChange={(values) => setValues(values)}/>
        </Modal.Dialog>
        <Modal.Dialog title="Category Select" id="CategoryModal"></Modal.Dialog>
        <Modal.Dialog title="Subgroup Select" id="SubgroupModal"></Modal.Dialog>

        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary">Close</Button>
          <Button variant="primary">Save changes</Button>
        </Modal.Footer>
      </Modal.Dialog>
    </div>
    );
}

export function CategoryModal({props}) {
    //Call to Database to grab all merchant names, and send with ids to be sent back/ if needs to be created

    //Display all merchants and allow to select one or create a new one

    return(
       <Modal>

       </Modal>
    );
}