from dataclasses import dataclass
from datetime import datetime
class Database:
    class Tables:
        TransactionHistory = "TransactionHistory"
        MerchantInfo = "MerchantInfo"
        MerchantNames = "MerchantNames"
        CategoryInfo = "CategoryInfo"
        BudgetInfo = "BudgetInfo"
        Subgroup = "SubgroupInfo"
    class Items:
        class Transaction:
            Transaction_ID = "Transaction_ID"
            Date = "Date"
            Price = "Price"

        class Merchant:
            Merchant_ID = "Merchant_ID"
            merchant_Name = "merchant_Name"
            merchant_Synonym = "merchant_Synonym"

        class Category:
            Category_ID = "Category_ID"
            Category = "Category"

        class Budget:
            Budget = "Budget"

        class Subgroup:
            Subgroup_ID = "Subgroup_id"
            Subgroup = "Subgroup"
class Objects:
    '''Format   
        Transaction_ID :str
        Date :int
        Merchant_ID :int
        Price :float
        Category_ID :int
    '''
    @dataclass
    class Transaction:
        Transaction_ID :str
        Date :int
        Merchant_ID :int
        Price :float
        Category_ID :int
        
        #make csv parse for transactions
    
    @dataclass
    class CSVParse:
        ID :str
        merchant :str
        Date :datetime
        Price :float
        
    @dataclass
    class Merchant:
        Merchant_ID :int
        Merchant :str
        Categoty_ID :int
    
    @dataclass
    class Category:
        Category_ID :int
        Category :str
        Subgroup_ID :int
