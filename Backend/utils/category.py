from utils.config import *
from typing import *
import sqlite3 as db

class category:
    def createNewCategories(info : List[Objects.Category],connection : db.Connection):
        cursor = connection.cursor
        cursor.executemany("INSERT INTO {0} ({1},{2},{3}) VALUES (?,?,?)".format(
                    Database.Tables.CategoryInfo,
                    Database.Items.Category.Category_ID,
                    Database.Items.Category.Category,
                    Database.Items.Subgroup.Subgroup_ID,
                    info))
        connection.commit()
    
    def createSubgroups(info: List[Objects.Subgroup],connection : db.Connection) -> None:
        cursor = connection.cursor
        cursor.executemany("INSERT INTO {0} ({1},{2}) VALUES (?,?)".format(
                    Database.Tables.Subgroup,
                    Database.Items.Subgroup.Subgroup_ID,
                    Database.Items.Subgroup.Subgroup,
                    info))
        connection.commit()
        pass