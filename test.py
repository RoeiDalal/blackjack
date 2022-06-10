import pandas as pd
import pymongo
"""
df = pd.read_excel(r'basic.xlsx', sheet_name='hard')
df.columns = ["2","3","4","5","6","7","8","9","10","11","12","13","14"]
print(df.loc[10-4][str(6)])
print(df)
"""

hard_df = pd.read_excel(r'basic.xlsx', sheet_name='hard')
soft_df = pd.read_excel(r'basic.xlsx', sheet_name='soft')
split_df = pd.read_excel(r'basic.xlsx', sheet_name='split')
cards_df = pd.read_excel(r'basic.xlsx', sheet_name='cards')
header = ["2","3","4","5","6","7","8","9","10","11","12","13","14"]
hard_df.columns = header
soft_df.columns = header
split_df.columns = header
cards_df.columns = header

mydict1 = {"name":"roei","price":12,"quantity":14}
mydict2= {"name":"ohad","price":12,"quantity":12}

mongodb_uri="mongodb://localhost:27017"
client = pymongo.MongoClient(mongodb_uri, 27017)

db = client["blackjack_db"]
records = db["records"]
records.insert_one(mydict1)
records.insert_one(mydict2)

card_values = {2:1,"3":1,"4":1,"5":1,"6":1,"7":0,"8":0,"9":0,10:-1,"11":-1,"12":-1,"13":-1,"14":-1}

print(card_values["14"])