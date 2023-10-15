import pandas as pd
import re
import os

class fileParser:
    '''Assuming CSV to start'''
    def __init__(self) -> None:
        self.transactions = []
        pass
    
    def parseFile(self,filePath):
        df  = pd.read_csv(filePath)
        df = df[df['Category']!="Transfer" and df['Category']!="Payments and Credits"]
        #have dataframe
        for row in df.iterrows():
            date = row['Date']
            merchant = row['Description']
            amt  = abs(row['Amount'])
            date = pd.to_datetime(date)
            transactionID = date.to_string() + merchant.to_string() + amt.to_string()
            #find merchant_ID
            merchant = re.sub('[^a-zA-Z]+', '', merchant)
            #if does not exist, create and return id
            #grab category ID as well, if creating new merchant, have option to create new category/sub and return that
            self.transactions.append({'transactionID' : transactionID, 'date' : date, 'merchant' : merchant, 'amt' : amt})
    
    def readFiles(self):
        directory = '../data/transactionCSV'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
               self.parseFile(f)
    
    
    def createDictionary(self):
        pass