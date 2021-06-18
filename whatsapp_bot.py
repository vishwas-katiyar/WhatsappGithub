import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time as tm
from datetime import datetime
import re
import os
from twilio.rest import Client
import regex
# import getpass
import emoji
################################################################################################################

import pymongo

myclient = pymongo.MongoClient("mongodb+srv://Whatsapp_Analyser_DB:Whatsapp_Analyser_DB@cluster0.brk0t.mongodb.net/Whatsapp_Analyser_DB?retryWrites=true&w=majority")
mydb = myclient["Whatsapp_Analyser_DB"]
admin_colection=mydb['Admin_Collection']
colection = mydb["Generaldiscussiongroup"]

################################################################################################################
now = datetime.now()

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
# chrome_options.binary_location = GOOGLE_CHROME_PATH

browser = webdriver.Chrome()

account_sid = os.environ['ACCOUNT_SID']
auth_token =  os.environ['auth_token']
client = Client(account_sid, auth_token)


# options = webdriver.ChromeOptions() 
# options.add_argument("start-maximized")
# # options.add_argument(r"--user-data-dir=C:\Users\91887\AppData\Local\Google\Chrome\User Data".format(getpass.getuser()))
# browser = webdriver.Chrome(options=options,executable_path='chromedriver.exe')


URL="https://web.whatsapp.com/"


# msg='''
# Unique :'''+str(df.Author.unique())+'''
# Messages :'''+str(len(df))+'''
# Media:'''+str(media_messages)+'''
# Emojis :'''+str(emojis)+'''
# Links :'''+str(links)

# msg_sent='lool'



def make_emoji_list(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)
    return emoji_list



def Find_url(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    return len([x[0] for x in url]) 



browser.get(URL)
# print(browser.get_qr())
# canvas = browser.switch_to('app')
while True:
    try:
        browser.find_element_by_xpath("//canvas[@role='img']")
        canvas = browser.get_screenshot_as_file("screenshot.png")
        
        print('captured')
         
        
        try:
            message = client.messages.create(
                                    body='Hello there!',
                                    from_='whatsapp:+14155238886',
                                    media_url=['https://selinum-app.herokuapp.com/screenshot.png'],
                                    to='whatsapp:+917898868692'
                                )

            print(message.sid)
        except Exception as e :
            message = client.messages.create(
                                    # body=' there!',
                                    from_='whatsapp:+14155238886',
                                    body=e,
                                    to='whatsapp:+7898868692'
                                )
        # print(canvas.text)
        break
    except Exception as e:
        message = client.messages.create(
                                    # body=' there!',
                                    from_='whatsapp:+14155238886',
                                    body=e,
                                    to='whatsapp:+7898868692'
                                )
# get the canvas as a PNG base64 string
# canvas_base64 = browser.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
# # decode
# canvas_png = browser.b64decode(canvas_base64)

# # save to a file
# with open(r"canvas.png", 'wb') as f:
#     f.write(canvas_png)

# print(browser)
print('wwait')

# tm.sleep(15)
Group_Chat_name='Educational purposer'

while True:
    try:
        Group_Chat = browser.find_element_by_xpath("//span[@title='"+Group_Chat_name+"']")
        break
    except:
        pass
# print('pass')
Group_Chat.click()
final_msg=browser.find_elements_by_xpath("//span[@dir='ltr']")[-1].text
flag=False
while True:
    new_msg=browser.find_elements_by_xpath("//span[@dir='ltr']")[-1].text
    if new_msg != final_msg:
        print('differenttttttttt')
        final_msg=new_msg
        if final_msg == '/vishwas':
            admin_data=list(admin_colection.find({'_id':'admin'}))[0]
            msg_sent='''Sent By Vishwas Whatsapp Analyser :) 

                Unique Participents :  '''+str(len(admin_data['Unique_authors']))+'''
                Total Messages :  '''+str(admin_data['total_msg'])+'''
                Total Words :  '''+str(admin_data['total_words'])+'''
                Total URLs :  '''+str(admin_data['total_url'])+'''
                Total Letters Count  :  '''+str(admin_data['total_letter_count']+'''
                 ''')
            flag=True
            msg_box = browser.find_elements_by_xpath("//div[@dir='ltr']")[-1].send_keys(str(msg_sent))
            send_button=browser.find_elements_by_xpath("//button[@class='_2Ujuu']")[-1].click()
            
        elif final_msg[:19] == 'Total Letters Count' :
            print('response')
        else:
            author = browser.find_elements_by_xpath("//div[@class='copyable-text']")[-1].get_attribute('data-pre-plain-text').split(']',1)[-1][:-2]
            # print(author)
            data_insert={
                'Date':now.date().strftime("%d/%m/%Y"),
                'Time':now.strftime("%I:%M"),
                'Author':author,
                'Message':final_msg,
                'emoji':make_emoji_list(final_msg),
                'urlcount':Find_url(final_msg),
                'Letter_Count':len(final_msg),
                'Word_Count':len(final_msg.split()),
                'MessageCount': 1
                        }
            colection.insert_one(data_insert)   
            
            admin_update = list(admin_colection.find({'_id':'admin'}))[0]
            # print(admin_update)
            # print(admin_update[0])
            if not author in admin_update['Unique_authors']:
                update_author = admin_update['Unique_authors']
                update_author.append(author)
            else:
                update_author = admin_update['Unique_authors']
            
            mydata={
                'total_msg':int(admin_update['total_msg'])+1,
                'total_words':int(admin_update['total_words'])+len(final_msg.split()),
                'total_url':int(admin_update['total_url'])+Find_url(final_msg),
                'total_letter_count':int(admin_update['total_letter_count'])+len(final_msg),
                'Unique_authors':update_author
                }

            admin_colection.update_one({'_id':'admin'},{ "$set": mydata })     
            print('else')