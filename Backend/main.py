from database import *
from fileParser import fileParser
import os
class budgetTracker:
    
    def __init__(self):
        db = DatabaseConnect()#create database session and connections
        #db.createDatabases()
        reader = fileParser() #create filereader
        reader.readFiles()
        db.storeNewTransactions(reader.transactions)
        #reader.readFiles() #readfiles
        #reader.storeInfo()



        
        pass