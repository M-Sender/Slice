import sqlite3 as db
from sqlite3 import Error


'''
Need to know if the tables already exist
If they do, do nothing at this point
if not, create a few tables{
    transactionHistory [Date : Date, Merchant : String, Price : double, Category : String] :
    merchantInfo [Merchant : String, Category : String] :
    CategoryInfo [Category : String, Subgroup : String] : Hold all possible categories and subgroups (Food[Groceries, Restaurants], Travel[Plane, train], etc)
    userSecrets [bank/Service : String , userName: String , password : String] May go against
}

'''
class DatabaseConnect:
    
    '''Try to connect to database
    If does not exist/ any error, let user know and allow creation of new tables etc
    '''
    def __init__(self) -> None:
        self.cursor = self.connectToDatabase()
        
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
            return c
        except Error as e:
            print(e)
