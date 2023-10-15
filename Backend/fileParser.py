import pandas as pd
import os

class fileParser:
    '''Assuming CSV to start'''
    def __init__(self,connection) -> None:
        self.conn = connection
        pass
    
    def parseFile(self,filePath):
        df  = pd.read_csv(filePath)
        df = df[df['Category']!="Transfer" and df['Category']!="Payments and Credits"]
        tempDB = []
        #have dataframe
        for row in df.iterrows():
            date = row['Date']
            desc = row['Description']
            amt  = abs(row['Amount'])
            date = pd.to_datetime(date)
            #find merchant_ID
            #if does not exist, create and return id
            #grab category ID as well, if creating new merchant, have option to create new category/sub and return that
            tempDB.append()
        self.conn.executemany('INSERT INTO TransactionInfo (Category, Subgroup) VALUES (?, ?)', tempDB)

            
    
    def readFiles(self):
        directory = '../data/transactionCSV'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                self.parseFile(f)
    
    
    def createDictionary(self):
        pass