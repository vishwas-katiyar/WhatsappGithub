# import pymongo
# import pandas as pd

# myclient = pymongo.MongoClient("mongodb+srv://Whatsapp_Analyser_DB:Whatsapp_Analyser_DB@cluster0.brk0t.mongodb.net/Whatsapp_Analyser_DB?retryWrites=true&w=majority")
# mydb = myclient["Whatsapp_Analyser_DB"]
# admin_colection=mydb['Admin_DB']
# colection = mydb["Generaldiscussiongroup"]
# admin_colection = mydb["Admin_Collection"]


# # admin_update = list(colection.find())

# # print(admin_update)
# # df=colection.find({})
# df = pd.DataFrame(list(colection.find()))
    
# print(df)
'''

import requests

import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

gChromeOptions = webdriver.ChromeOptions()
gChromeOptions.add_argument("window-size=1920x1480")
gChromeOptions.add_argument("disable-dev-shm-usage")

browser=webdriver.Chrome(
    options=gChromeOptions)

browser.get("https://web.whatsapp.com/")
while True:
    try:
        page=browser.find_element_by_id('app')
        a=page.find_elements_by_class_name('landing-main')[0]
        
        while True:
            try:
                a.find_element_by_class_name('_132Kx')
            except Exception as e :
                print(e)
                break 
        a.find_element_by_tag_name('canvas')

        
        break
    except Exception as e:
        print(e)

# page.find_element_by_
a=browser.get_screenshot_as_base64()
print(a)
# print(type(a))

res=requests.post('http://127.0.0.1:8000/Base64_to_png/',{"imgstring":a
})

print(res.text)
'''
from chatterbot import ChatBot
   
# Inorder to train our bot, we have 
# to import a trainer package
# "ChatterBotCorpusTrainer"
from chatterbot.trainers import ChatterBotCorpusTrainer
  
   
# Give a name to the chatbot “corona bot”
# and assign a trainer component.
chatbot=ChatBot('corona bot')
  
# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)
   
# Now let us train our bot with multipple corpus
trainer.train("chatterbot.corpus.english.greetings",
              "chatterbot.corpus.english.botprofile",
              "chatterbot.corpus.english.computers",
              "chatterbot.corpus.english.conversations",
              "chatterbot.corpus.english.emotion",
              "chatterbot.corpus.english.food",
              "chatterbot.corpus.english.gossip",
              "chatterbot.corpus.english.greetings",
              "chatterbot.corpus.english.health",
              "chatterbot.corpus.english.history",
              "chatterbot.corpus.english.humor",
              "chatterbot.corpus.english.literature",
              "chatterbot.corpus.english.money",
              "chatterbot.corpus.english.movies",
              "chatterbot.corpus.english.politics",
              "chatterbot.corpus.english.psychology",
              "chatterbot.corpus.english.science",
              "chatterbot.corpus.english.sports",
              "chatterbot.corpus.english.trivia"



               )
   
while True:
    response = chatbot.get_response(input('vishwas : '))
    print(response)
  
response = chatbot.get_response('Who are you?')
print(response)