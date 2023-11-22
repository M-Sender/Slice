import sqlite3 as db
from utils.config import *
from typing import *
class merchant:
    
    def createNewMerchantMappings(newMappings : List[Objects.MerchantMapping],connection : db.Connection) -> None:
        cursor = connection.cursor
        cursor.executemany("INSERT INTO {0} ({1},{2}) VALUES (?,?)".format(
                    Database.Tables.MerchantNames,
                    Database.Items.Merchant.merchant_Name,
                    Database.Items.Merchant.Merchant_ID,
                    newMappings))
        connection.commit()
    def createNewMerchants(newMerchants: List[Objects.Merchant],connection : db.Connection) -> None:
        cursor = connection.cursor
        cursor.executemany("INSERT INTO {0} ({1},{2},{3}) VALUES (?,?,?)".format(
                    Database.Tables.MerchantInfo,
                    Database.Items.Merchant.Merchant_ID,
                    Database.Items.Merchant.merchant_Name,
                    Database.Items.Category.Category_ID,
                    newMerchants))
        connection.commit()
    
    def getMerchants(connection : db.Connection) -> List[Objects.Merchant]:
        
        pass