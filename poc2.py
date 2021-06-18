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

account_sid = os.environ['ACCOUNT_SID']
auth_token =  os.environ['auth_token']
client = Client(account_sid, auth_token)

message = client.messages.create(
                                    body='Hello there!',
                                    from_='whatsapp:+14155238886',
                                    # body='loll',
                                    to='whatsapp:+7898869692'
                                )

print(message.sid)