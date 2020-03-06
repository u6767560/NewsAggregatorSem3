# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:13:14 2019
@author: 12645
"""

from pymongo import MongoClient
from pymongo import InsertOne
import CatchNewsListCBRRSS
from goose3 import Goose
from NewsEntity import NewsEntity
import os, base64
import requests as req
from PIL import Image
from io import BytesIO
import re
import utility
import schedule
import time
import fasttext
import sys, os
import math

# rootPath = os.path.split(os.getcwd())[0]
# print(rootPath)
# sys.path.append(rootPath)
# sys.path.append(rootPath+'/Bert_Pytorch')
# sys.path.append(rootPath+'/Bert_Pytorch/pytorch_pretrained_bert')
# sys.path.append(rootPath+'/Bert_Pytorch/pytorch_pretrained_bert/file_utils')
# from Bert_Pytorch.output.reload import model,tokenizer,predict
static_news_id = 0


def insert():
    # print(global_news)
    config = db_config.config.find()
    client = MongoClient('mongodb://user:1234@localhost:27017')
    # a dictionary match the name of the website and the newslist
    news_list, time_list = CatchNewsListCBRRSS.get_news_list_rss(CatchNewsListCBRRSS.rss_url)
    # change the newest time of the news
    nearest_time = {}

    for i in CatchNewsListCBRRSS.rss_url:
        nearest_time[i] = config[0][i + 'LastTime']
        # original_nearest_time[i] = config[0][i + 'LastTime']

    # print(original_nearest_time)
    print(len(news_list))

    for website in news_list:
        # print("______"+website[:3])
        if '_' in website:
            insert_news_from_list(nearest_time, news_list.get(website), nearest_time[website], website, time_list,
                                  website.replace("_", " "))
        else:
            insert_news_from_list(nearest_time, news_list.get(website), nearest_time[website], website, time_list,
                                  website)

    # for i in CatchNewsListCBRRSS.rss_url:
    #     myquery = {i + "LastTime": original_nearest_time[i]}
    #     newvalues = {"$set": {i + "LastTime": nearest_time[i]}}
    #     db_config.config.update_one(myquery, newvalues)

    print(db_config.config.find())
    print("success, newest time is:",nearest_time)
    # myquery = {"newsId": original_id}
    # newvalues = {"$set": {"newsId": static_news_id}}
    # db_config.config.update_one(myquery, newvalues)
    print("All finished")
    # upload the newest time into db


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


def insert_news_from_list(nearest_time, news_list, nearest_time_web, website, time_list, source):
    print(website+'with news')
    print(len(news_list))
    original_nearest_time = {}
    for i in CatchNewsListCBRRSS.rss_url:
        # nearest_time[i] = config[0][i + 'LastTime']
        original_nearest_time[i] = config[0][i + 'LastTime']

    global static_news_id

    # print(static_news_id)

    nearest_time_one = nearest_time_web
    new_nearest_time = 0

    update_time = int(time.time())
    title_list = db.news.distinct('title')
    for url in news_list[:50]:
        article = g.extract(url=url)
        if article.title in title_list:
            continue
        news_time = time_list[url]

        if news_time == None:
            continue
        news_timestamp = time.mktime(news_time)


        if news_timestamp <= nearest_time_one:  # if the time of the news less than the newest time in the memory
            continue

        if news_timestamp >= new_nearest_time:
            new_nearest_time = news_timestamp

        

        news_entity = NewsEntity(article.title, article.authors, news_timestamp, article.meta_description,
                                 article.meta_keywords, article.cleaned_text, url)

        news_entity.category = "Canberra"

        if len(article.authors) == 0:
            news_entity.authors = ['Anonymous']

        # news_temp = []
        # news_temp.append(news_entity.cleaned_text)
        # for word in Australian_list:
        #     if word in news_entity.cleaned_text:
        #         news_entity.category = "Australia"
        #         break
        # score = round(classifier_2.predict_proba(news_temp)[0][0][1],2)

        # Ignored one line below because of plan B
        score = round(generate_result(news_entity.cleaned_text, classifier_2), 2)


        # score = round(0.9,2)
        # bert
        # score = predict(news_entity.cleaned_text, model, tokenizer)

        # if score == 0:
        #    continue

        db.news.insert_one({"news_id": int(int(static_news_id) + 1),
                            "title": news_entity.title,
                            "authors": news_entity.authors,
                            "publish_date": news_entity.publish_date,
                            "meta_description": news_entity.meta_description,
                            "meta_keywords": news_entity.meta_keywords,
                            "cleaned_text": news_entity.cleaned_text,
                            "rank": score,
                            "timerank": (0.4*score+0.3)*math.pow(0.9,(update_time-news_entity.publish_date)/86400),
                            # Following is plan B
                            # "rank": news_entity.publish_date,
                            # "timerank": news_entity.publish_date,
                            "url": url,
                            "source": source,
                            'category': news_entity.category,
                            'approve': 0,
                            'disapprove': 0
                            })
        static_news_id = static_news_id + 1

        if new_nearest_time != 0:
            nearest_time[website] = new_nearest_time

        myquery = {"id": "config"}

        for i in CatchNewsListCBRRSS.rss_url:
            newvalues = {"$set": {i + "LastTime": nearest_time[i]}}
            db_config.config.update_one(myquery, newvalues)
        newvalues = {"$set": {"newsId": static_news_id}}
        db_config.config.update_one(myquery, newvalues)



if __name__ == '__main__':
    client = MongoClient()
    db = client.NewsAggregator

    db_config = client.Configure
    config = db_config.config.find()
    global_news = config[0]['newsId']
    static_news_id = global_news
    # Ignored 2 lines because of plan B
    classifier_2 = fasttext.load_model('../../../Rank/FastText/Output/300k_headline.bin', label_prefix='__label__')

    # print(global_news)
    original_id = config[0]['newsId']

    f = open("Australia_vocb.txt")
    Australian_list = []
    for line in f:
        Australian_list.append(line.strip())
    f.close()
    g = Goose()
    insert()
    client.close()

#     schedule.every(1).hour.do(insert)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)

    # insert()
