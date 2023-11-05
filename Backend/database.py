import sqlite3 as db
from sqlite3 import Error
import pandas as pd
from utils.config import *
#from fuzzywuzzy import fuzz
from typing import *


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
    connection :db.Connection
    cursor :db.Connection.cursor
    #transactions :pd.DataFrame
    #transactionIDs :pd.DataFrame
    #merchantInfo :pd.DataFrame
    #merchantNames :pd.DataFrame       
    
    def __init__(self) -> None:
        self.connectToDatabase()
      
    def createDatabases(self):
        # Create TransactionHistory table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS {0}
            ({1} TEXT PRIMARY KEY, {2} REAL, {3} INTEGER, {4} REAL, {5} INTEGER,
            FOREIGN KEY({5}) REFERENCES {6}({7}),
            FOREIGN KEY({4}) REFERENCES {8}({9})
            )
            '''.format(Database.Tables.TransactionHistory,
                    Database.Items.Transaction.Transaction_ID,
                    Database.Items.Transaction.Date,
                    Database.Items.Merchant.Merchant_ID,
                    Database.Items.Transaction.Price,
                    Database.Items.Category.Category_ID,
                    Database.Tables.CategoryInfo,
                    Database.Items.Category.Category_ID,
                    Database.Tables.MerchantInfo,
                    Database.Items.Merchant.Merchant_ID)
        )

        # Create MerchantInfo table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS {0}
            ({1} INTEGER PRIMARY KEY, {2} TEXT, {3} INTEGER, 
            FOREIGN KEY({3}) REFERENCES {4}({3})
            )
            '''.format(Database.Tables.MerchantInfo,
                    Database.Items.Merchant.Merchant_ID,
                    Database.Items.Merchant.merchant_Name,
                    Database.Items.Category.Category_ID,
                    Database.Tables.CategoryInfo,
                    Database.Items.Category.Category_ID)
        )

        # Create MerchantNames table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS {0}
            ({1} TEXT, {2} INTEGER, 
            FOREIGN KEY({2}) REFERENCES {3}({2})
            )
            '''.format(Database.Tables.MerchantNames,
                    Database.Items.Merchant.merchant_Name,
                    Database.Items.Merchant.Merchant_ID,
                    Database.Tables.MerchantInfo)
        )

        # Create CategoryInfo table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS {0}
            ({1} INTEGER PRIMARY KEY, {2} TEXT, {3} INTEGER,
            FOREIGN KEY({3}) REFERENCES {4}({3})
            )
            '''.format(Database.Tables.CategoryInfo,
                    Database.Items.Category.Category_ID,
                    Database.Items.Category.Category,
                    Database.Items.Subgroup.Subgroup_ID,
                    Database.Tables.Subgroup)
        )

        # Create SubgroupInfo table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS {0}
            ({1} INTEGER PRIMARY KEY, {2} TEXT)
            '''.format(Database.Tables.Subgroup,
                    Database.Items.Subgroup.Subgroup_ID,
                    Database.Items.Subgroup.Subgroup)
        )

        # Create BudgetInfo table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS {0}
            ({1} INTEGER PRIMARY KEY, {2} REAL,
            FOREIGN KEY({1}) REFERENCES {3}({4})
            )
            '''.format(Database.Tables.BudgetInfo,
                    Database.Items.Category.Category_ID,
                    Database.Items.Budget.Budget,
                    Database.Tables.CategoryInfo,
                    Database.Items.Category.Category_ID)
        )

        
        # Insert sample data into CategoryInfo
        category_data = [
            (0,"UNKNOWN",0),
            (1,'Groceries', 1 ),
            (2,'Restaurants',1),
            (3,'Plane Ticket',2),
            (4,'Train', 2),
            (5,'Gym',4),
            (6,'Bars',5),
            (7,'Rideshare',2),
            (8,'Online Shopping',0),
            (9,'Clothing',6),
            (10,'Shoes',6),
            (11,'New tech',7),
            (12,'Electric',8),
            (13,'Water',8),
            (14,'Gas',8)
            # Add more categories and subgroups as needed
        ]
        subgroup_Data = [
            (0,"UNKNOWN"),
            (1,"Food"),
            (2,"Travel"),
            (3,"HMPH"),
            (4,"Health"),
            (5,"Fun"),
            (6,"Clothing"),
            (7,"Technology"),
            (8,"Utilities")
        ]
        self.connection.commit()
        self.c.executemany('INSERT INTO {0} ({1},{2},{3}) VALUES (?, ?, ?)'.format(Database.Tables.CategoryInfo,Database.Items.Category.Category_ID,Database.Items.Category.Category,Database.Items.Subgroup.Subgroup_ID), category_data)
        self.c.executemany('INSERT INTO {0} ({1},{2}) VALUES (?, ?)'.format(Database.Tables.Subgroup,Database.Items.Subgroup.Subgroup_ID,Database.Items.Subgroup.Subgroup), subgroup_Data)
        self.c.execute('INSERT INTO {0} ({1},{2},{3}) VALUES (?, ?, ?)'.format(Database.Tables.MerchantInfo,Database.Items.Merchant.Merchant_ID,Database.Items.Merchant.merchant_Name,Database.Items.Category.Category_ID),(0,"UNKNOWN",0))
        self.c.execute('INSERT INTO {0} ({1},{2}) VALUES (?, ?)'.format(Database.Tables.MerchantNames,Database.Items.Merchant.merchant_Name,Database.Items.Merchant.Merchant_ID),("UNKOWN",0))
        
        self.connection.commit()
  
    def connectToDatabase(self):
        try:
            self.connection = db.connect(r"../data/database.db")
            self.c = self.connection.cursor()

        except Error as e:
            print(e)
    def storeNewTransactions(self,transactions : List[Objects.CSVParse]):
        #grab all transaction ids so we can check if we have duplicate before inserting in execmany
        #rows = self.cursor.execute("SELECT transactionID FROM {}".format("transactionHistory"))
        transactionIDs = pd.read_sql_query("SELECT {0} FROM {1}".format(Database.Items.Transaction.Transaction_ID,Database.Tables.TransactionHistory), self.connection)
        transactionIDs = transactionIDs[Database.Items.Transaction.Transaction_ID].to_list()
        #grab all merchants 
        merchantInfo :pd.DataFrame = pd.read_sql_query("SELECT * FROM {0}".format(Database.Tables.MerchantInfo),self.connection)
        
        #grab all merchant names
        merchantNames :pd.DataFrame  = pd.read_sql_query("SELECT * FROM {0}".format(Database.Tables.MerchantNames),self.connection)
        
        cleanedTransactions :List[Objects.Transaction] = []
        
        #loop through
        for transaction in transactions:
            if transaction.ID in transactionIDs: #have a duplicate , may need to make more sophisticated
                print(transaction.ID)
                continue
            #unique
            #match merchant to merchants and get catID
            catID = None
            #see if we have in merchantNames
            merchantMatch :pd.DataFrame= merchantNames.loc[merchantNames[Database.Items.Merchant.merchant_Name] == transaction.Merchant]
            if len(merchantMatch) !=0:
                merchantID = merchantMatch[Database.Items.Merchant.Merchant_ID].item()
                merchantName = merchantMatch[Database.Items.Merchant.merchant_Name].item()
                catID = merchantInfo.iloc[merchantID][Database.Items.Category.Category_ID]#grab cat id from match
            else:
                merchantID, merchantName, catID = self.createNewMerchant(transaction.Merchant,merchantNames) #return a dataframe
                MerchantFrame : Objects.Merchant= { Database.Items.Merchant.Merchant_ID:merchantID,
                                            Database.Items.Merchant.merchant_Name:merchantName,
                                            Database.Items.Category.Category_ID:catID}
                MerchantNameFrame = {Database.Items.Merchant.merchant_Name:transaction.Merchant,Database.Items.Merchant.Merchant_ID: merchantID}
                merchantInfo.loc[len(merchantInfo.index)] = MerchantFrame
                merchantNames.loc[len(merchantNames.index)] = MerchantNameFrame
            transactionIDs.append(transaction.ID)
            transactionObj :Objects.Transaction = (transaction.ID,
                                                   transaction.Date.toordinal(),
                                                   merchantID,
                                                   transaction.Price,
                                                   catID) 
                       
            '''{Database.Items.Transaction.Transaction_ID:transaction.ID,
                                                   Database.Items.Transaction.Date:transaction.Date,
                                                   Database.Items.Merchant.Merchant_ID: merchantID,
                                                   Database.Items.Transaction.Price: transaction.Price,
                                                   Database.Items.Category.Category_ID : catID
                                                   }'''
            cleanedTransactions.append(transactionObj)
            if len(cleanedTransactions) > 50:
                print(cleanedTransactions[0])
                self.c.executemany("INSERT INTO {0} ({1},{2},{3},{4},{5}) VALUES (?,?,?,?,?)".format(
                    Database.Tables.TransactionHistory,
                    Database.Items.Transaction.Transaction_ID,
                    Database.Items.Transaction.Date,
                    Database.Items.Merchant.Merchant_ID,
                    Database.Items.Transaction.Price,
                    Database.Items.Category.Category_ID), 
                cleanedTransactions)
                cleanedTransactions.clear()
                self.connection.commit()
        self.c.executemany("INSERT INTO {0} ({1},{2},{3},{4},{5}) VALUES (?,?,?,?,?)".format(
                    Database.Tables.TransactionHistory,
                    Database.Items.Transaction.Transaction_ID,
                    Database.Items.Transaction.Date,
                    Database.Items.Merchant.Merchant_ID,
                    Database.Items.Transaction.Price,
                    Database.Items.Category.Category_ID), 
                cleanedTransactions)
        self.connection.commit()
            #need to add merchant into tempmerchants to not have duplicates as sqlite will only be batched every 100?? and we want to be able to see them
            #build array to be stored in db
            #do commit every 100 and clear tempdb
            
            #DONE
        ## do final commit and clear temodb (more of a principal but unnesccary)
            
            
            
        pass
    def createNewMerchant(self,merchant: str, merchants: pd.DataFrame):
        #we have a new merchant, ask to map with current one or create a new
        ''' print(merchant)
        choice = input("Unknown merchant found. Create a new one or look to see if you can map with a current one?(1 or 2)")
        merchantID = None
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
            pass'''
        return [len(merchants),"UNKOWN",0]
        #return [merchantID, merchantName,  catID]
        
        