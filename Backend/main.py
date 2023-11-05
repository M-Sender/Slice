from database import *
from fileParser import fileParser


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=["GET"])
def testConnection():
    try:
        #return all useful info
        return jsonify()
    except Exception as e:
        return str(e), 400


@app.route('/uploadCSV', methods=['POST'])
def something():
    try:
        request.get_json()
        return jsonify()
    except Exception as e:
        return str(e), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=8000)

#to do testing
#test = budgetTracker()
class budgetTracker:
    
    def __init__(self):
        db = DatabaseConnect()#create database session and connections
        #db.createDatabases()
        reader = fileParser() #create filereader
        reader.readFiles()
        db.storeNewTransactions(reader.transactions)
        pass