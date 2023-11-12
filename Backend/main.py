from database import *
from fileParser import fileParser
from flask import Flask, request, jsonify
from utils.category import *
from utils.config import *
from utils.merchant import *
import asyncio

db = DatabaseConnect()#create database session and connections
db.createDatabases()
#reader = fileParser() #create filereader
#reader.readFiles()
#db.storeNewTransactions(reader.transactions)


app = Flask(__name__)

@app.route('/', methods=["GET"])
def testConnection():
    try:
        #return all useful info
        return jsonify()
    except Exception as e:
        return str(e), 400


@app.route('/uploadCSV', methods=['POST'])
def handleCSVUpload():
    try:
        csvFile =  request.get_json()
        needsHandling = db.storeNewTransactions(csvFile)
        returnDictionary = {}
        returnDictionary["merchantHelp"] = needsHandling #decide if we need to just send merchant names/dates or price too
        returnDictionary["merchantInfo"] = merchant.getMerchants(db.connection) #merch+ids
        returnDictionary["categoryInfo"] = category.getCategories(db.connection)
        returnDictionary["subGroupInfo"] = category.getSubGroups(db.connection)
        packet = jsonify.jsonify(returnDictionary)
        #need to send over all merchant names/ids, cat/ids, subgroups/ids
        return packet
    except Exception as e:
        return str(e), 400

@app.route('/createInfo', methods=['POST'])
def handleNewInfo():
    try:
        reworkedData =  request.get_json()
        transactions : List[Objects.Transaction] = reworkedData["transactions"]
        subGroupInfo : List[Objects.Subgroup] = reworkedData["subGroupInfo"]
        categoryInfo : List[Objects.Category] = reworkedData["CategoryInfo"]
        
        
        newMerchantInfo : List[Objects.Merchant]  = reworkedData["newMerchantInfo"]
        newMerchantMapping : List[Objects.MerchantMapping] = reworkedData["newMerchantMappings"]
        
        #This order of operations are very importants
        #may need to do some working for create new ids for each increment
        #create new subgroups + categories
        category.createSubgroups(subGroupInfo,db.connection)
        category.createNewCategories(categoryInfo,db.connection)
        
        #create new merchants + mapping info
        merchant.createNewMerchants(newMerchantInfo,db.connection)
        merchant.createNewMerchantMappings(newMerchantMapping,db.connection)
        
        # then send using db.storeNewtransactions so everything is shared
        needsHandling = db.storeNewTransactions(transactions)
        if (needsHandling):
            #something went wrong as this should not be possible
            Error()
        pass
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=8000)