import pandas as pd
import re
import os
from utils.config import *
from typing import *

class fileParser:
    '''Assuming CSV to start'''
    def __init__(self) -> None:
        self.transactions : List[Objects.CSVParse] = []
        pass
    
    #region Local Files
    def parseFile(self,filePath):
        df  = pd.read_csv(filePath)
        self.createTempTransactions(df)
        
    def readFiles(self):
        directory = '../data/transactionCSV'
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f) and filename[-4:]==".csv":
                self.parseFile(f)
    #endregion
    
    #region CSV Upload
    
    #endregion
    
    
    #region Shared Logic
    def createTempTransactions(self,df: List[Objects.CSVParse]):
        try:
            df = df[df['Category']!="Transfer" and df['Category']!="Payments and Credits"]
        except:
            pass
        #have dataframe
        for index,row in df.iterrows():
            
            date = row['Date']
            merchant :str = row['Description']
            amt  = abs(row['Amount'])
            date = pd.to_datetime(date)
            transactionID = hex(int((date.strftime("%Y%m%d")) + ''.join(str(ord(c)) for c in merchant) + str(amt).replace(".","")))
            #find merchant_ID
            merchant = re.sub('[^a-zA-Z]+', '', merchant)
            #if does not exist, create and return id
            #grab category ID as well, if creating new merchant, have option to create new category/sub and return that
            self.transactions.append(Objects.CSVParse(ID=transactionID,Merchant=merchant,Date=date,Price=amt))
    
    #endregion
    def createDictionary(self):
        pass