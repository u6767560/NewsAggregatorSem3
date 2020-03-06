#!/usr/bin/env python
# coding: utf-8

# # Links from feedparser are sent to newpaper3k to extract textual information such as summary,keywords,text.

# In[1]:
from pymongo import MongoClient
import math
import re
import sys
import feedparser

import requests


import pandas as pd

import datetime
import time

import pytz  # pip install pytz

from newspaper import Article

import fasttext

connection = MongoClient('localhost', 27017)  # Connect to mongodb
db2 = connection['Configure']
collection2 = db2['config']
cursor2 = collection2.find()
xyz = []
for doc in cursor2:
    xyz.append(doc)

if len(xyz) == 0:
    sys.exit("config file not setup. newsid wont be  updated,setup new config before run")

df = pd.read_csv('../../PythonFlask/Extraction/Sources/RSS_ExtractionFormatV2.csv', index_col=0)

# In[2]:


df2 = df[['Name', 'Rss', 'NTags', 'SCOPE', 'Type']]

# In[4]:

feedparser._open_resource = lambda *args, **kwargs: feedparser._StringIO(requests.get(args[0], timeout=15).content)
feeds = []
posts = []
description = []
counter = 0
for url in df2['Rss']:

    feed = feedparser.parse(url)
    Name = df2['Name'][counter]
    Ntags = df2['NTags'][counter]
    Scope = df2['SCOPE'][counter]
    Type = df2['Type'][counter]
    counter = counter + 1
    for post in feed.entries:

        try:

            post.author
        except Exception as e:
            posts.append((Name, Ntags, Scope, Type, post.title, post.link, post.published, Ntags))
            print(e)
            print(Ntags + " au continuing.....")
            continue

        posts.append((Name, Ntags, Scope, Type, post.title, post.link, post.published, post.author))

    for post in feed.entries:
        try:
            post.description
        except Exception as d:
            description.append("Not available")
            print(d)
            print(Ntags + " desc continuing")
            continue
        description.append(post.description)

df3 = pd.DataFrame(posts, columns=['source', 'Ntags', 'Scope', 'Tags', 'title', 'url', 'published', 'authors'])

# In[5]:

print("feed parsing complete")

df3['meta-description'] = description
print("total number of links parsed " + str(len(df3.index)))
# In[6]:


# remove all tags(image tags ,src tags.etc)
count = 0
for des in df3['meta-description']:
    clean = re.compile('<.*?>')

    df3['meta-description'][count] = re.sub(clean, '', df3['meta-description'][count])
    count = count + 1

df3['publishedTime'] = pd.to_datetime(df3.published)
df3['publishedDate'] = df3['publishedTime']
df3['publish_dateX'] = df3['publishedTime']
df3['publish_date'] = df3['publishedTime']

# In[8]:


count = 0
for pub in df3['publishedDate']:
    # pub = pub.utcnow().date()
    df3['publish_date'][count] = df3['publishedDate'][count].strftime('%Y%m%d%H%M%S')
    df3['publish_dateX'][count] = df3['publishedDate'][count].strftime('%Y%m%d%H%M%S')

    df3['publishedTime'][count] = int(df3['publishedTime'][count].timestamp())
    df3['publishedDate'][count] = str(df3['publishedDate'][count].date())
    # df3['timezone'][count] = df3['published'][count].strftime("%z")
    count = count + 1

count = 0
for pub in df3['publish_dateX']:
    df3['publish_dateX'][count] = int(df3['publish_dateX'][count])
    count = count + 1

# stored run time from previous run is used to remove already parsed/extracted links
with open("../../PythonFlask/Extraction/Sources/run_time.txt", "r") as myfile:
    previous_run = myfile.readline()
    if previous_run == "":
        previous_run = '00000000000000'

# In[11]:


previous_run = int(previous_run)
print("previous run time was at " + str(previous_run))

count = 0
Dlist = []
for x in df3['publish_dateX']:
    if df3['publish_dateX'][count] < previous_run:
        # print(df3['publish_dateX'][count])
        Dlist.append(count)
    count = count + 1

# In[13]:


df3 = df3.drop(df3.index[Dlist])

df3 = df3.reset_index()
del df3['index']

if df3.empty:
    sys.exit('no new feeds to extract from previous run time .nothing to update.')

# In[17]:


timezone = datetime.datetime.now(pytz.timezone('Australia/Sydney')).strftime('%z')

# In[18]:


count = 0
for pub in df3['publish_date']:
    df3['publish_date'][count] = '' + df3['publish_date'][count] + timezone
    df3['publish_date'][count] = df3['publish_date'][count].replace('+', '')
    df3['authors'][count] = df3['authors'][count].split(',')
    df3['Tags'][count] = df3['Tags'][count].split(',')
    count = count + 1

# In[19]:


# df3.head(30)


# replacing + fro timezone shouldnt yield any problems as rss feeds are focused on canberra
# and usually have same timezone as sydney.
# in case of including world sources it might be better to convet time to local format and repalace +


# In[21]:


runtime = datetime.datetime.now(pytz.timezone('Australia/Sydney')).strftime('%Y%m%d%H%M%S')
# runtime = runtime.replace('+','')
print("current  run time  at " + str(runtime))
df3 = df3.rename(columns={'publish_date': 'publishdateX', 'publishedTime': 'publish_date'})
# In[22]:


# storing the run time- 
with open("../../PythonFlask/Extraction/Sources/run_time.txt", "w") as text_file:
    text_file.write(runtime)

# In[25]:

print("total number of links to extract " + str(len(df3.index)))
print("extracting ....")
Text = []
Summary = []
Keywords = []
for url in df3['url']:

    try:

        article = Article(url)
        article.download()
        # article.html
        article.parse()
    except Exception as e:
        print(url)
        Text.append('error')
        Summary.append('error')
        Keywords.append('error')
        print(e)
        print("continuing.....")
        continue
    text = article.text
    article.nlp()
    keywords = article.keywords
    summary = article.summary
    Text.append(text)
    Summary.append(summary)
    Keywords.append(keywords)

# In[26]:


df3['cleaned_text'] = Text
df3['summary'] = Summary
df3['meta_keywords'] = Keywords

# In[27]:


# fast text score


classifier_2 = fasttext.load_model('../../Rank/CanberraModel/Output/text_1200.bin', label_prefix='__label__')


## reused from upload.py
def generate_result(stri, classifier):  # use fasttext to predict the mails into spam or ham
    spam_rate = []  # store the result into the dict spam_rate
    if stri != "":
        predict_value = 1 if classifier.predict_proba([stri])[0][0][0] == '1' else 0
        if predict_value == 1:
            spam_rate.append(classifier.predict_proba([stri])[0][0][1])
        else:
            spam_rate.append(round(1.0 - float(classifier.predict_proba([stri])[0][0][1]), 6))
        return spam_rate[0]
    else:
        return 0


# In[ ]:
rank = []
approve = []
disapprove = []
category = []
timerank = []
print("calculating fasttext score...")
update_time = int(time.time())
count = 0
for pub in df3['publish_dateX']:
    score = round(generate_result(df3['title'][count], classifier_2), 2)
    rank.append(score)
    timerank.append((0.4 * score + 0.3) * math.pow(0.9, (update_time - df3['publish_date'][count]) / 86400))
    # print(df3['cleaned_text'][count])
    approve.append(int('0'))
    disapprove.append(int('0'))
    category.append('Canberra')
    count = count + 1

# In[ ]:


df3['rank'] = rank
df3['approve'] = approve
df3['disapprove'] = disapprove
df3['timerank'] = timerank
df3['category'] = category

'''
print("url" + df3['url'][3])

print("Title" + df3['title'][3])

print(df3['cleaned_text'][3])

print("Summary" + df3['summary'][3])

print("Meta -description" + df3['meta-description'][3])

print(df3['meta_keywords'][3])

print(rank)
print(timerank)
'''

df3 = df3.reset_index()
df3 = df3.rename(columns={'index': 'news_id'})

# print(connection.list_database_names())
db = connection['NewsAggregator']

collection = db['news']
cursor = collection.find().sort([('news_id', -1)]).limit(1)

xyt = []
''''''
for doc in cursor:
    xyt.append(doc)
    # print(xyt)

if len(xyt) != 0:
    dictt = xyt[0]

    news_idCount = (dictt.get("news_id") + 1)
    print("last news_id index in mongodb  = " + str(news_idCount - 1))
    df3.news_id = df3.news_id + news_idCount

my_list = df3.to_dict('records')
collection.insert_many(my_list)
print("data successfully updated to mongodb")
# update config config here  a function  to be created here for getting data from mongo

update_news_id = df3.news_id[len(df3.news_id) - 1]
print("new record news_id should begin at  " + str(update_news_id + 1))

dicttt = xyz[0]
ObjectId2 = (dicttt.get("_id"))
db2.config.update_one({
    '_id': ObjectId2}, {
    '$set': {
        'newsId': int(update_news_id)
    }
}, upsert=False)

print("config updated with newsid")
