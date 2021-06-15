import pandas as pd
import pymongo
import re
import json

myclient = pymongo.MongoClient("mongodb+srv://Whatsapp_Analyser_DB:Whatsapp_Analyser_DB@cluster0.brk0t.mongodb.net/Whatsapp_Analyser_DB?retryWrites=true&w=majority")
mydb = myclient["Whatsapp_Analyser_DB"]
admin_colection=mydb['Admin_DB']
colection = mydb["Generaldiscussiongroup"]
admin_colection = mydb["Admin_Collection"]

# colection.insert_one({ "_id": 1, "name": "John", "address": "Highway 37"})
import regex
import pandas as pd
import numpy as np
import emoji
import re
from collections import Counter
import matplotlib.pyplot as plt
from os import path

def startsWithDateAndTime(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -' 
    result = re.match(pattern, s)
    if result:
        return True
    return False

def FindAuthor(s):
    s=s.split(":",1)
    if len(s)==2:
        return True
    else:
        return False

def getDataPoint(line):   
    splitLine = line.split(' - ') 
    dateTime = splitLine[0]
    date, time = dateTime.split(', ') 
    message = ' '.join(splitLine[1:])
    if FindAuthor(message): 
        splitMessage = message.split(': ') 
        author = splitMessage[0] 
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return date, time, author, message

parsedData = []
data = [] 
conversation = 'Generaldiscussiongroup.txt'
with open(conversation, encoding="utf-8") as fp:
    fp.readline() 
    messageBuffer = [] 
    date, time, author = None, None, None
    while True:
        line = fp.readline() 
        if not line: 
            break
        line = line.strip() 
        if startsWithDateAndTime(line): 
            if len(messageBuffer) > 0: 
                parsedData.append([date, time, author, ' '.join(messageBuffer)]) 
            messageBuffer.clear() 
            date, time, author, message = getDataPoint(line) 
            messageBuffer.append(message) 
        else:
            messageBuffer.append(line)

df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message']) # Initialising a pandas Dataframe.
# df["Date"] = pd.to_datetime(df["Date"])
df['_id']=range(len(df))
# print(df.head())
df=df.mask(df.astype(object).eq('None')).dropna()
# print(df.head())



# print(df[f['Author']=='A Sir')])
# print(df.tail(20))

# print(len(df.Author.unique()))


total_media_messages = df[df['Message'] == '<Media omitted>'].shape[0]
# print(total_media_messages)

def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)
    return emoji_list


df["emoji"] = df["Message"].apply(split_count)

total_emojis = sum(df['emoji'].str.len())
# print(total_emojis)

URLPATTERN = r'(https?://\S+)'
df['urlcount'] = df.Message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()
links = np.sum(df.urlcount)

# print(conversation.split('.')[0])
# print("Messages:",len(df))
# print("Media:",total_media_messages)
# print("total_emojis:",total_emojis)
# print("Links:",links)



media_messages_df = df[df['Message'] == '<Media omitted>']
cleaning_df = df.drop(media_messages_df.index)
# print(media_messages_df.head())

# cleaning_df.info()

cleaning_df['Letter_Count'] = cleaning_df['Message'].apply(lambda s : len(s))
cleaning_df['Word_Count'] = cleaning_df['Message'].apply(lambda s : len(s.split(' ')))
cleaning_df["MessageCount"]=1

# print(cleaning_df.head())
####################################################################################
l = ["Vishwas Katiyar"]
for i in range(len(l)):
	
	req_df= cleaning_df[cleaning_df["Author"] == l[i]]
	
	# print(f'Stats of {l[i]} -')
	
	# print('Messages Sent', req_df.shape[0])
	
	words_per_message = (np.sum(req_df['Word_Count']))/req_df.shape[0]
	# print('Words per message', words_per_message)
	
	media = media_messages_df[media_messages_df['Author'] == l[i]].shape[0]
	# print('Media Messages Sent', media)
	total_emojis = sum(req_df['emoji'].str.len())
	# print('total_emojis Sent', total_emojis)
	links = sum(req_df["urlcount"])   
	# print('Links Sent', links)   
	
###############################################################################################################

total_emojis_list = list([a for b in cleaning_df.emoji for a in b])

emoji_dict = dict(Counter(total_emojis_list))

emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)

xcc=[]

for i in emoji_dict:
    xcc.append(i)
    # print(i)

# print(cleaning_df.tail(20))

# cleaning_df=cleaning_df.mask(cleaning_df.astype(object).eq('None')).dropna()

# print(cleaning_df.tail(20)






records = json.loads(cleaning_df.T.to_json()).values()
colection.insert_many(records)
mydata={
    '_id':'admin',
    'total_msg':int(len(cleaning_df)),
    'total_words':int(cleaning_df['Word_Count'].sum()),
    'total_url':int(cleaning_df['urlcount'].sum()),
    'total_letter_count':int(cleaning_df['Letter_Count'].sum()),
    'Unique_authors':list(cleaning_df.Author.unique())

}
# admin_colection.insert_one(mydata)
# admin_update = list(admin_colection.find({'_id':'admin'}))
# df = admin_colection.find({'_id':'admin'})
# df = read_mongo(mydb, 'colection')
print(admin_update)


# def FindAuthor(s):
#     s=s.split(":",1)
#     print(s)
#     if len(s)==2:
#         return True
#     else:
#         return False

# print(FindAuthor('A Sir: Vishwas pls add to all other students of our class through https://chat.whatsapp.com/HdbwEPBAXJa3sTb9gsDxN5'))

# def getDataPoint(line):   
#     splitLine = line.split(' - ')
#     print(splitLine)
#     dateTime = splitLine[0]
#     date, time = dateTime.split(', ') 
#     message = ' '.join(splitLine[1:])
#     print(message)
#     if FindAuthor(message): 
#         splitMessage = message.split(': ') 
#         author = splitMessage[0] 
#         # print('splitMessage'+splitMessage)
#         print('author'+author)
#         message = ' '.join(splitMessage[1:])
#     else:
#         author = None
#     return date, time, author, message
# print(getDataPoint('16/07/20, 10:26 am - A Sir: Vishwas pls add to all other students of our class through https://chat.whatsapp.com/HdbwEPBAXJa3sTb9gsDxN5'))
# parsedData = []