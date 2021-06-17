from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import pandas as pd
from collections import Counter
import numpy as np
from pymongo import MongoClient
import calendar
import re
from django.views.decorators.csrf import csrf_exempt
import json 
import requests
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client 
 
account_sid = 'AC469bf41df225fa17e3007651a541e5c3' 
auth_token = '89dec2448a5aabd0d06bc7a4fddaf177' 
client = Client(account_sid, auth_token) 


myclient = MongoClient("mongodb+srv://Whatsapp_Analyser_DB:Whatsapp_Analyser_DB@cluster0.brk0t.mongodb.net/Whatsapp_Analyser_DB?retryWrites=true&w=majority")
mydb = myclient["Whatsapp_Analyser_DB"]
admin_colection=mydb['Admin_DB']
colection = mydb["Generaldiscussiongroup"]
admin_colection = mydb["Admin_Collection"]



def clean_url(s):
    URLPATTERN = r'(https?://\S+)'
    s = re.sub('This message was deleted','',s)
    s = re.sub(URLPATTERN, "", s)
    return s
    
# Create your views here.
def index(request):
    df = pd.DataFrame(list(colection.find()))
    # print(df)
    # print(type(df))
    l=df.Author.unique()
    MessagesSent=[]
    WordsPerMessage=[]
    Name=[]
    TotalEmoji=[]
    LinkSent=[]
    user=dict()
    temp=[]
    for i in range(len(l)):
        temp=[]
        req_df= df[df["Author"] == l[i]]
        MessagesSent.append(req_df.shape[0])
        temp.append(req_df.shape[0])
        # print(f'Stats of {l[i]} -')
        Name.append(l[i])
        temp.append(l[i])
        # print('Messages Sent', req_df.shape[0])
        
        words_per_message = (np.sum(req_df['Word_Count']))/req_df.shape[0]
        WordsPerMessage.append(words_per_message)
        temp.append(round(words_per_message,3))

        total_emojis = sum(req_df['emoji'].str.len())
        TotalEmoji.append(total_emojis)
        temp.append(total_emojis)

        links = sum(req_df["urlcount"])   
        # print('Links Sent', links)   
        LinkSent.append(links)
        temp.append(links)
        user[l[i]]=temp
    # total_emojis_list = list([a for b in df.emoji for a in b])
    # emoji_dict = Counter(total_emojis_list)
    # emoji_top=emoji_dict.most_common(10)
    # emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    # print(dict(df))
    context={
        'iterate':range(len(Name)),
        'user':user
        # 'Name':Name,
        # 'MessagesSent':MessagesSent,
        # 'WordsPerMessage':WordsPerMessage,
        # 'TotalEmoji':TotalEmoji,
        # 'LinkSent':LinkSent
    }
    return render(request,'index.html',context=context)


def features(request):
    # print(request.method)
    df = pd.DataFrame(list(admin_colection.find()))
    user_df= pd.DataFrame(list(colection.find()))
    # print(user_df)
    Avg_Letter_Count=(user_df['Letter_Count'].sum())/len(user_df)
    Avg_Word_Count=(user_df['Word_Count'].sum())/len(user_df)
    Avg_urlcount=(user_df['urlcount'].sum())/len(user_df)
    month_df=user_df['Date'].str[3:5].value_counts().sort_index()

    # print(month_df)
    # date_df=df.groupby(['Date']).count()
    # user_df['']
    # date_list=df['Date']
    month_dict=month_df.to_dict()
    month_dict_keys=[calendar.month_name[int(i)]for i in list(month_dict.keys())]
    # print(month_dict)
    time_24_Hrs = pd.to_datetime(user_df['Time']).dt.strftime('%H:%M:%S')
    weekday_series = pd.to_datetime(user_df['Date']).dt.day_name().value_counts().to_dict()
    
    # weekday_series_day = weekday_series
    # print(weekday_series)
    time_24_Hrs=time_24_Hrs.str[:2].value_counts().sort_index()
    time_24_Hrs_dict=time_24_Hrs.to_dict()
    time_24_Hrs_dict_hrs=[ str(i)+':00' for i in time_24_Hrs_dict.keys() ]

    color = tuple(np.random.choice(range(256), size=3))
     
    # print(['rgb'+str(color)]*24)
    color_24=['rgb'+str(color)]*24
    
    
    user_df['Message'] = user_df.Message.apply(lambda x: clean_url(x))
    
    word=user_df['Message'].str.cat(sep=' ')
        # word=word.join(i)
    # All_Word=[word=word.join(i) for i in user_df['Message']]
    # print(word.replace('This Message was Deleted',''))
    # word=word.replace('This Message was Deleted','')



    context={
        'word':word,
        'color':color,
        'weekday_series_keys':list(weekday_series.keys()),
        'weekday_series_values':list(weekday_series.values()),
        'color_24':color_24,
        'time_24_Hrs_dict_hrs':time_24_Hrs_dict_hrs,
        'time_24_Hrs_dict_msg':list(time_24_Hrs_dict.values()),
        'Avg_Letter_Count':round(Avg_Letter_Count,2),
        'Avg_Word_Count':round(Avg_Word_Count,2),
        'Avg_urlcount':round(Avg_urlcount,2),
        'total_words':user_df['Word_Count'].sum(),
        'total_msg':user_df['MessageCount'].sum(),
        'total_url':user_df['urlcount'].sum(),
        'total_letter_count':df['total_letter_count'][0],
        'month_dict_keys':month_dict_keys,
        'month_dict_values':list(month_dict.values())
    }
    # print(month_dict.keys())
    return render(request,'features.html',context=context)

def users(request):
    user_df= pd.DataFrame(list(colection.find()))
    if request.method == 'POST':
        requested_user=request.POST['request_user']
        requested_user_df=user_df[user_df['Author']==requested_user].to_html()
        # print(requested_user_df)
        
        # return render(request,'users.html',context=context)
    Top_10_Users=user_df['Author'].value_counts()[:10].to_dict()
    # print(Top_10_Users)
    print(user_df.columns)
    
    context={
        'All_Participents':user_df['Author'].unique(),
        'Top_10_Users_keys':list(Top_10_Users.keys()),
        'Top_10_Users_values':list(Top_10_Users.values())
    }
    try :
        context['requested_user_df']=requested_user_df
    except:
        pass
    # print(context)
    return render(request, 'users.html',context=context)

@csrf_exempt
def bot(request):
    print('jio')
    incoming_msg = request.POST['Body'].lower()
    print(request.POST)
    
    message = client.messages.create( 
                                from_='whatsapp:+14155238886',  
                                body=incoming_msg,      
                                to='whatsapp:+917898868692' 
                            ) 
    
    print(message.sid)    
    return HttpResponse(json.dumps({incoming_msg:incoming_msg}), content_type="application/json")