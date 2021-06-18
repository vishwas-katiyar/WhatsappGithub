'''import pymongo
import pandas as pd

myclient = pymongo.MongoClient("mongodb+srv://Whatsapp_Analyser_DB:Whatsapp_Analyser_DB@cluster0.brk0t.mongodb.net/Whatsapp_Analyser_DB?retryWrites=true&w=majority")
mydb = myclient["Whatsapp_Analyser_DB"]
admin_colection=mydb['Admin_DB']
colection = mydb["Generaldiscussiongroup"]
admin_colection = mydb["Admin_Collection"]


# admin_update = list(colection.find())

# print(admin_update)
# df=colection.find({})
df = pd.DataFrame(list(colection.find()))
    
print(df)

'''

from twilio.rest import Client
account_sid = 'AC469bf41df225fa17e3007651a541e5c3' 
auth_token = 'a8794b4f8e0b55f6b322c9b4572eb4a3' 
client = Client(account_sid, auth_token)

for sms in client.messages.list():
    print(sms.uri)