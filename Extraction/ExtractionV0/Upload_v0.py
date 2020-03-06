# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:13:14 2019
@author: 12645
"""

from pymongo import MongoClient
from pymongo import InsertOne
import CatchNewsList
from goose3 import Goose
from NewsEntity import NewsEntity
import os, base64
import requests as req
from PIL import Image
from io import BytesIO
import re
import utility
#import schedule
import time
import fasttext
import sys, os
import re
import math

# rootPath = os.path.split(os.getcwd())[0]
# print(rootPath)

# sys.path.append(rootPath+'/Bert_Pytorch')
# sys.path.append(rootPath+'/Bert_Pytorch/pytorch_pretrained_bert')
# sys.path.append(rootPath+'/Bert_Pytorch/pytorch_pretrained_bert/file_utils')
# from Bert_Pytorch.output.reload import model,tokenizer,predict
static_news_id = 0
inserted_cnt = 0


def insert():
    # print(global_news)
    config = db_config.config.find()
    # client = MongoClient('mongodb://user:1234@localhost:27017')

    news_list = {}  # a dictionary match the name of the website and the newslist
    news_list['ABC'] = CatchNewsList.get_news_list_abc()
    news_list['SBS'] = CatchNewsList.get_news_list_sbs()
    news_list['Canberra_Times'] = CatchNewsList.get_news_list_cbr_times()
    news_list['UC'] = CatchNewsList.get_news_list_uc()
    news_list['Her_Canberra'] = CatchNewsList.get_news_list_hercbr()
    news_list['Tidbinbilla'] = CatchNewsList.get_news_list_tidbinbilla()
    news_list['Canberra_Museum_and_Gallery'] = CatchNewsList.get_news_list_cmag()
    # change the newest time of the news
    nearest_time = {}
    nearest_time['ABC'] = config[0]['ABCLastTime']
    nearest_time['SBS'] = config[0]['SBSLastTime']
    nearest_time['Canberra_Times'] = config[0]['Canberra_TimesLastTime']
    nearest_time['UC'] = config[0]['UC_LastTime']
    nearest_time['Her_Canberra'] = config[0]['Her_CanberraLastTime']
    nearest_time['Tidbinbilla'] = config[0]['TidbinbillaLastTime']
    nearest_time['Canberra_Museum_and_Gallery'] = config[0]['Canberra_Museum_and_GalleryLastTime']

    original_nearest_time = {}
    original_nearest_time['ABC'] = config[0]['ABCLastTime']
    original_nearest_time['SBS'] = config[0]['SBSLastTime']
    original_nearest_time['Canberra_Times'] = config[0]['Canberra_TimesLastTime']
    original_nearest_time['UC'] = config[0]['UC_LastTime']
    original_nearest_time['Her_Canberra'] = config[0]['Her_CanberraLastTime']
    original_nearest_time['Tidbinbilla'] = config[0]['TidbinbillaLastTime']
    original_nearest_time['Canberra_Museum_and_Gallery'] = config[0]['Canberra_Museum_and_GalleryLastTime']

    print(original_nearest_time)
    print("in insert len(newsL):", len(news_list))

    global inserted_cnt
    inserted_cnt = 0

    # for website in news_list:
    #     # print(global_news)
    #     insert_news_from_list(nearest_time, news_list.get(website), nearest_time[website], website, source)

    for website in news_list:
        # print("______"+website[:3])
        if '_' in website:
            insert_news_from_list(nearest_time, news_list.get(website), nearest_time[website], website,
                                  website.replace("_", " "))
        else:
            insert_news_from_list(nearest_time, news_list.get(website), nearest_time[website], website,
                                  website)

    print('===== Insert finished! Totally ', inserted_cnt, ' news added. =====')

    print(db_config.config.find())
    print("==== success! ====")
    print('latest timestamp is:', nearest_time)

    # myquery = {"newsId": original_id}
    # newvalues = {"$set": {"newsId": static_news_id}}
    # db_config.config.update_one(myquery, newvalues)
    # upload the newest time into db


def generate_result(stri, classifier):  # use fasttext to predict the mails into spam or ham
    spam_rate = []  # store the result into the dict spam_rate
    predict_value = 1 if classifier.predict_proba([stri])[0][0][0] == '1' else 0
    if predict_value == 1:
        spam_rate.append(classifier.predict_proba([stri])[0][0][1])
    else:
        spam_rate.append(round(1.0 - float(classifier.predict_proba([stri])[0][0][1]), 6))
    return spam_rate[0]


def insert_news_from_list(nearest_time, list, nearest_time_web, website,source):
    print('inseNewsFroL: got ', website, ' with news:', len(list))
    update_time = int(time.time())
    original_nearest_time = {}
    original_nearest_time['ABC'] = config[0]['ABCLastTime']
    original_nearest_time['SBS'] = config[0]['SBSLastTime']
    original_nearest_time['Canberra_Times'] = config[0]['Canberra_TimesLastTime']
    original_nearest_time['UC'] = config[0]['UC_LastTime']
    original_nearest_time['Her_Canberra'] = config[0]['Her_CanberraLastTime']
    original_nearest_time['Tidbinbilla'] = config[0]['TidbinbillaLastTime']
    original_nearest_time['Canberra_Museum_and_Gallery'] = config[0]['Canberra_Museum_and_GalleryLastTime']

    # print(original_nearest_time)

    global static_news_id
    nearest_time = nearest_time

    # print(static_news_id)

    nearest_time_one = nearest_time_web
    news_list = list
    new_nearest_time = 0
    title_list = db.news.distinct('title') # get all titles from the db, in order to skip inserting the existent news
    for url in news_list[:len(news_list) - 1]:
        article = g.extract(url=url)
        # skip the duplicate news from checking title's existence
        if article.title in title_list:
            continue
        
        if website == 'ABC':
            news_time = utility.find_time_abc(url)
        elif website == 'SBS':
            news_time = utility.find_time_sbs(url)
        elif website == 'Canberra_Times':
            news_time = utility.find_time_cbt(url)
        elif website == 'UC':
            news_time = utility.find_time_uc(url)
        elif website == 'Her_Canberra':
            news_time = utility.find_time_hercbr(url)
        elif website == 'Tidbinbilla':
            news_time = utility.find_time_tidbinbilla(url)
        elif website == 'Canberra_Museum_and_Gallery':
            news_time = utility.find_time_cmag(url)
        if news_time == None:  # skip news which cannot find standard publish times. no time to improve
            continue

        time_array = time.strptime(news_time.replace('T', ' ')[:-6], "%Y-%m-%d %H:%M:%S")
        news_timestamp = time.mktime(time_array)

        if website == 'ABC' or website == 'SBS' or website == 'Canberra_Times':
            news_timestamp-=28800

        # if website == 'uc':
        #     print('uc news_timestamp:', news_timestamp," == one = ",nearest_time_one)
        # elif website == 'hercbr':
        #     print('hercbr news_timestamp:', news_timestamp)

        if isinstance(news_timestamp, str):
            # print('news_timestamp str:', news_timestamp)
            news_timestamp = float(news_timestamp)
        if isinstance(nearest_time_one, str):
            # print('nearest_time_one str', nearest_time_one)
            nearest_time_one = float(nearest_time_one)

        if news_timestamp <= nearest_time_one and website != 'Tidbinbilla':  # if the time of the news less than the newest time in the memory
            continue

        if news_timestamp >= new_nearest_time:
            new_nearest_time = news_timestamp

        
        # print(article)
        news_entity = NewsEntity(article.title, article.authors, news_timestamp, article.meta_description,
                                 article.meta_keywords, article.cleaned_text, url)
        # print(news_entity.title.split(" "))

        with open("Australia_vocb.txt") as words_file:
            for rows in words_file:
                rows = rows.replace("\n","")
                # print(rows)
                if rows in news_entity.title.split(" "):
                    # print(news_entity.title.split(" "))
                    news_entity.category = "Australia"

        if "Canberra" in news_entity.title.split(" "):
            print(news_entity.title.split(" "))
            news_entity.category = "Canberra"
        if source == 'Tidbinbilla' or source == "UC" or source == "Her_Canberra".replace("_"," ") or source == "Canberra_Museum_and_Gallery".replace("_"," "):
            news_entity.category = "Canberra"
        # print(url)
        # print("metakeywords"+article.meta_keywords)
        # print(type(article.meta_keywords))
        for keywords in re.split(",",article.meta_keywords.replace(" ","")):
            # print(keywords)
            if "australia" in keywords or "australian" in keywords:
                news_entity.category = "Australia"

        if len(article.authors) == 0:
            news_entity.authors = ['Anonymous']
        news_temp = []
        news_temp.append(news_entity.cleaned_text)

        for word in Australian_list:
            if word in news_entity.cleaned_text:
                news_entity.category = "Australia"
                break
        # score = round(classifier_2.predict_proba(news_temp)[0][0][1],2)
        score = round(generate_result(news_entity.title, classifier_2),2)
        #score = round(0.9, 2)
        # bert
        # score = predict(news_entity.cleaned_text, model, tokenizer)
        # if score == 0:
        #     continue

        # if website == 'abc' or website == 'sbs' or website == 'cbr_times':
        # print('insert origin')
        # if website == 'uc':
        #     print('insert uc title:', news_entity.title, " with ct:", news_entity.cleaned_text)
        # elif website == 'hercbr':
        #     print('insert hercbr title:', news_entity.title, " with ct:", news_entity.cleaned_text)


        timerank = score*math.pow(0.9,(update_time-news_entity.publish_date)/86400)
        if news_entity.category == "Canberra":
            timerank = (0.4*score+0.3)*math.pow(0.9,(update_time-news_entity.publish_date)/86400)
        db.news.insert_one({"news_id": int(int(static_news_id) + 1),
                            "title": news_entity.title,
                            "authors": news_entity.authors,
                            "publish_date": news_entity.publish_date,
                            "meta_description": news_entity.meta_description,
                            "meta_keywords": news_entity.meta_keywords,
                            "cleaned_text": news_entity.cleaned_text,
                            "rank": score,
                            "timerank": timerank,
                            "url": url,
                            'category': news_entity.category,
                            'approve': 0,
                            'source':source,
                            'disapprove': 0
                            })
        static_news_id = static_news_id + 1

        if new_nearest_time != 0:
            if website == 'ABC':
                nearest_time['ABC'] = new_nearest_time
            elif website == 'SBS':
                nearest_time['SBS'] = new_nearest_time
            elif website == 'Canberra_Times':
                nearest_time['Canberra_Times'] = new_nearest_time
            elif website == 'UC':
                nearest_time['UC'] = new_nearest_time
            elif website == 'Her_Canberra':
                nearest_time['Her_Canberra'] = new_nearest_time
            elif website == 'Tidbinbilla':
                nearest_time['Tidbinbilla'] = new_nearest_time
            elif website == 'Canberra_Museum_and_Gallery':
                nearest_time['Canberra_Museum_and_Gallery'] = new_nearest_time

        myquery = {"id": "config"}
        # myquery = {"abcLastTime": original_nearest_time['abc']}
        newvalues = {"$set": {"ABCLastTime": nearest_time['ABC']}}
        db_config.config.update_one(myquery, newvalues)

        # myquery = {"sbsLastTime": original_nearest_time['sbs']}
        newvalues = {"$set": {"SBSLastTime": nearest_time['SBS']}}
        db_config.config.update_one(myquery, newvalues)

        # myquery = {"cbr_timesLastTime": original_nearest_time['cbr_times']}
        newvalues = {"$set": {"Canberra_TimesLastTime": nearest_time['Canberra_Times']}}
        db_config.config.update_one(myquery, newvalues)

        # myquery = {"ucLastTime": original_nearest_time['uc']}
        newvalues = {"$set": {"UCLastTime": nearest_time['UC']}}
        db_config.config.update_one(myquery, newvalues)

        # myquery = {"hercbrLastTime": original_nearest_time['hercbr']}
        newvalues = {"$set": {"Her_CanberraLastTime": nearest_time['Her_Canberra']}}
        db_config.config.update_one(myquery, newvalues)

        # myquery = {"tidbinbillaLastTime": original_nearest_time['tidbinbilla']}
        newvalues = {"$set": {"TidbinbillaLastTime": nearest_time['Tidbinbilla']}}
        db_config.config.update_one(myquery, newvalues)

        # myquery = {"cmagLastTime": original_nearest_time['cmag']}
        newvalues = {"$set": {"Canberra_Museum_and_GalleryLastTime": nearest_time['Canberra_Museum_and_Gallery']}}
        db_config.config.update_one(myquery, newvalues)

        # myquery = {"id": "config"}
        newvalues = {"$set": {"newsId": static_news_id}}
        db_config.config.update_one(myquery, newvalues)

        global inserted_cnt
        inserted_cnt += 1




if __name__ == '__main__':
    client = MongoClient()
    db = client.NewsAggregator

    db_config = client.Configure  # db
    config = db_config.config.find()  # collection
    global_news = config[0]['newsId']
    static_news_id = global_news
    classifier_2 = fasttext.load_model('../../../Rank/FastText/Output/300k_headline.bin', label_prefix='__label__')
    #    print(classifier_2)
    # print(global_news)
    original_id = config[0]['newsId']

    # f = open("Australia_vocb.txt")
    Australian_list = []
    # for line in f:
    #     Australian_list.append(line.strip())
    # f.close()
    g = Goose()
    print(global_news)
    insert()
    
    # close the client
    client.close()
    #schedule.every(1).hour.do(insert)

    #while True:
        #schedule.run_pending()
        #time.sleep(1)

    # insert()
