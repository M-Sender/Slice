from database import *
from fileParser import fileParser
from flask import Flask, request, jsonify

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
        packet = jsonify.jsonify(needsHandling)
        return packet
    except Exception as e:
        return str(e), 400

@app.route('/createInfo', methods=['POST'])
def handleNewInfo():
    try:
        reworkedData =  request.get_json()
        transactions = reworkedData["transactions"]
        merchantInfo  = reworkedData["merchantInfo"]
        #need to create all the new merchants + all info
        
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