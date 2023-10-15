import sqlite3 as db
from sqlite3 import Error
import pandas as pd


'''
Need to know if the tables already exist
If they do, do nothing at this point
if not, create a few tables{
    transactionHistory [Date : Date, Merchant : String, Price : double, Category : String] :
    merchantInfo [Merchant : String, Category : String] :
    CategoryInfo [Category : String, Subgroup : String] : Hold all possible categories and subgroups (Food[Groceries, Restaurants], Travel[Plane, train], etc)
   
}

'''
class DatabaseConnect:
    
    '''Try to connect to database
    If does not exist/ any error, let user know and allow creation of new tables etc
    '''
    def __init__(self) -> None:
        self.connection, self.cursor = self.connectToDatabase()
        
    def connectToDatabase(self):
        try:
            connection = db.connect(r"../data/database.db")
            c = connection.cursor()
            c.execute('''
                    CREATE TABLE IF NOT EXISTS transactionHistory
                    (Transaction_ID INTEGER PRIMARY KEY, Date REAL, Merchant_ID INTEGER, Price REAL, Category_ID INTEGER,
                    FOREIGN KEY(Category_ID) REFERENCES CategoryInfo(Category_ID),
                    FOREIGN KEY(Merchant_ID) REFERENCES MerchantInfo(Merchant_ID))
                    ''')
            c.execute('''
                    CREATE TABLE IF NOT EXISTS MerchantInfo
                    (Merchant_ID INTEGER PRIMARY KEY, Merchant_Name TEXT, Category INTEGERY, 
                    FOREIGN KEY(Category) REFERENCES CategoryInfo(Category_ID))
                    ''')
            c.execute('''
                    CREATE TABLE IF NOT EXISTS MerchantNames
                    (Merchant_Name TEXT, Merchant_ID INTEGER, 
                    FOREIGN KEY(Merchant_ID) REFERENCES MerchantInfo(Merchant_ID))
                    ''')
            c.execute('''
                    CREATE TABLE IF NOT EXISTS CategoryInfo
                    (Category_ID INTEGER PRIMARY KEY, Category TEXT, Subgroup TEXT)
                    ''')
            c.execute('''
                    CREATE TABLE IF NOT EXISTS BudgetInfo
                    (Category_ID INTEGER PRIMARY KEY
                    , Budget REAL,
                    FOREIGN KEY(Category_ID) REFERENCES CategoryInfo(Category_ID))
                    ''')
           
            # Insert sample data into CategoryInfo
            category_data = [
                (1,'Groceries', 'Food', ),
                (2,'Restaurants', 'Food'),
                (3,'Plane Ticket','Travel'),
                (4,'Train', 'Travel'),
                (5,'Gym','Health'),
                (6,'Bars','Going Out'),
                (7,'Rideshare','Travel'),
                (8,'Online Shopping','Etc'),
                (9,'Clothing','Clothing'),
                (10,'Shoes','Clothing'),
                (11,'New tech','Technology'),
                (12,'Electric','Utilities'),
                (13,'Water','Utilities'),
                (14,'Gas','Utilities')
                # Add more categories and subgroups as needed
            ]

            try:
                c.executemany('INSERT INTO CategoryInfo (Category_ID,Category, Subgroup) VALUES (?, ?, ?)', category_data)
            except:
                pass
            connection.commit()
            return connection,c
        except Error as e:
            print(e)

    def storeNewTransactions(self,transactions):
        #grab all transaction ids so we can check if we have duplicate before inserting in execmany
        #rows = self.cursor.execute("SELECT transactionID FROM {}".format("transactionHistory"))
        transactionIDs = pd.read_sql_query("SELECT transactionID FROM {}".format("transactionHistory"), self.connection)
        transactionIDs = transactionIDs["transactionIDs"].to_list()
        #grab all merchants 
        merchants = pd.read_sql_query("SELECT * FROM table_info({})".format("merchantInfo"),self.connection)
        
        #loop through db
        
        for transaction in transactions:
            if transaction.transactionID in transactionIDs:
                continue
            #unique
            #match merchant to merchants and get catID
            catID = None
            merchantMatch = merchants.loc[merchants['merchantID'] == transaction.merchant]
            if merchantMatch:
                merchantID,merchantName,catID = merchantMatch["merchant_ID"], merchantMatch["merchantName"],merchantMatch["Category_ID"]#grab cat id from match
            else:
                merchantID, merchantName, catID = self.createNewMerchant(transaction.merchant,merchants)
                #need to add merchant into tempmerchants to not have duplicates as sqlite will only be batched every 100?? and we want to be able to see them
            #build array to be stored in db
            #do commit every 100 and clear tempdb
            
            #DONE
        ## do final commit and clear temodb (more of a principal but unnesccary)
            
            
            
        pass
    def createNewMerchant(merchant,merchants):
        #we have a new merchant, ask to map with current one or create a new
        print(merchant)
        choice = input("Unknown merchant found. Create a new one or look to see if you can map with a current one?(1 or 2)")
        merchantID =None
        catID = None
        merchantName = None
        if choice==1:
            #create a new one
            #ask for display name
            #need to assign a category
            #can create a new category, Maybe new sub categories too instead of just choosing?? (later date)
            #if creating a new category, ask for name and (subgroups need to be considered), return catID for use
            #if reusing, return catID
            #create a merchant in merchantInfo
            #make mapping in merchantInfo
            pass
        else:
            #map with current one 
            #do this by having user select which id their new merchant matches with
            #add to merchantName table to map theirs with officical name and send back merchantID and the cat
            pass
        return [merchantID, merchantName,  catID]
        