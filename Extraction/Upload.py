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
# import schedule
import time
import fasttext
import sys, os
import re

# rootPath = os.path.split(os.getcwd())[0]
# print(rootPath)

# sys.path.append(rootPath+'/Bert_Pytorch')
# sys.path.append(rootPath+'/Bert_Pytorch/pytorch_pretrained_bert')
# sys.path.append(rootPath+'/Bert_Pytorch/pytorch_pretrained_bert/file_utils')
# from Bert_Pytorch.output.reload import model,tokenizer,predict
from PythonFlask.Extraction import Catch_Canberra_WithoutRSS

static_news_id = 0
inserted_cnt = 0


def insert():
    # print(global_news)
    config = db_config.config.find()
    # client = MongoClient('mongodb://user:1234@localhost:27017')

    # news_list
    news_list = {}  # a dictionary match the name of the website and the newslist
    news_list['abc'] = CatchNewsList.get_news_list_abc()
    news_list['sbs'] = CatchNewsList.get_news_list_sbs()
    news_list['cbr_times'] = CatchNewsList.get_news_list_cbr_times()
    news_list['uc'] = CatchNewsList.get_news_list_uc()
    news_list['hercbr'] = CatchNewsList.get_news_list_hercbr()
    news_list['tidbinbilla'] = CatchNewsList.get_news_list_tidbinbilla()
    news_list['cmag'] = Catch_Canberra_WithoutRSS.catch_National_Aboretum_Canberra()
    news_list['national_arboretum'] = Catch_Canberra_WithoutRSS.catch_National_Aboretum_Canberra()
    news_list['bom'] = Catch_Canberra_WithoutRSS.catch_Canberra_Forecast()
    news_list['multi_cultural_festival'] = Catch_Canberra_WithoutRSS.catch_Multicultural_Festival()
    news_list['nca'] = Catch_Canberra_WithoutRSS.catch_National_Capital_Authority()
    news_list['unsw'] = Catch_Canberra_WithoutRSS.catch_UNSW_Canberra()
    news_list['iconwater'] = Catch_Canberra_WithoutRSS.catch_Icon_Water()
    news_list['greens'] = Catch_Canberra_WithoutRSS.catch_ACT_Greens()
    news_list['thestreet'] = Catch_Canberra_WithoutRSS.catch_The_Street_Theatre()
    news_list['anu'] = Catch_Canberra_WithoutRSS.catch_The_Australian_National_University()
    news_list['moadoph'] = Catch_Canberra_WithoutRSS.catch_Museum_of_Australian_Democracy()

    # None timestamps group:
    news_list['anu_botanical_gardens'] = Catch_Canberra_WithoutRSS.catch_Australian_National_Botanical_Gardnes()
    # news_list['cbr_house'] = Catch_Canberra_WithoutRSS.catch_Canberra_House() #lost connection
    #    news_list['visit_cbr'] = Catch_Canberra_WithoutRSS.catch_Visit_Canberra()
    news_list['experience_AIS'] = Catch_Canberra_WithoutRSS.catch_Experience_AIS()
    news_list['llewellyn_hall'] = Catch_Canberra_WithoutRSS.catch_Llewellyn_Hall()
    news_list['national_conv_centre_cbr'] = Catch_Canberra_WithoutRSS.catch_National_Convention_Centre_Canberra()
    news_list['the_phoenix'] = Catch_Canberra_WithoutRSS.catch_The_Phoenix()
    # news_list['smiths_alternative'] = Catch_Canberra_WithoutRSS.catch_Smiths_Alternative()
    news_list['cbr_intel_music_fes'] = Catch_Canberra_WithoutRSS.catch_Canberra_International_Music_Festival()
    news_list['cbr_opera'] = Catch_Canberra_WithoutRSS.catch_Canberra_Opera()
    news_list['RSL_ACT_brunch'] = Catch_Canberra_WithoutRSS.catch_RSL_ACT_Branch()
    news_list['cbr_conv_bureau'] = Catch_Canberra_WithoutRSS.catch_Canberra_Convention_Bureau()
    news_list['cbr_glassworks'] = Catch_Canberra_WithoutRSS.catch_Canberra_Glassworks()

    # ValueError: Unicode strings with encoding declaration are not supported.Please use bytes input or XML fragments without declaration.
    #  news_list['cbr_linux_users_groups'] = Catch_Canberra_WithoutRSS.catch_Canberra_Linux_Users_Group()

    #    news_list['ACT_labor'] = Catch_Canberra_WithoutRSS.catch_ACT_Labor()
    #    news_list['events_ACT'] = Catch_Canberra_WithoutRSS.catch_Events_ACT()
    news_list['ACT_LAQ_time'] = Catch_Canberra_WithoutRSS.catch_ACT_Legislative_Assembly_Question_Time()
    news_list['national_library_AU'] = Catch_Canberra_WithoutRSS.catch_National_Library_of_Australia()
    news_list['national_portrait_gallery'] = Catch_Canberra_WithoutRSS.catch_National_Portrait_Gallery()
    news_list['AU_war_memorial'] = Catch_Canberra_WithoutRSS.catch_Australian_War_Memorial()
    news_list['ACT_LAeP'] = Catch_Canberra_WithoutRSS.catch_ACT_Legislative_Assembly_ePetitions()

    # change the newest time of the news
    nearest_time = {}
    nearest_time['abc'] = config[0]['abcLastTime']
    nearest_time['sbs'] = config[0]['sbsLastTime']
    nearest_time['cbr_times'] = config[0]['cbr_timesLastTime']
    nearest_time['uc'] = config[0]['ucLastTime']
    nearest_time['hercbr'] = config[0]['hercbrLastTime']
    nearest_time['tidbinbilla'] = config[0]['tidbinbillaLastTime']
    nearest_time['cmag'] = config[0]['cmagLastTime']
    nearest_time['national_arboretum'] = config[0]['national_arboretumLastTime']
    nearest_time['bom'] = config[0]['bomLastTime']
    nearest_time['multi_cultural_festival'] = config[0]['multi_cultural_festivalLastTime']
    nearest_time['nca'] = config[0]['ncaLastTime']
    nearest_time['unsw'] = config[0]['unswLastTime']
    nearest_time['iconwater'] = config[0]['iconwaterLastTime']
    nearest_time['greens'] = config[0]['greensLastTime']
    nearest_time['thestreet'] = config[0]['thestreetLastTime']
    nearest_time['anu'] = config[0]['anuLastTime']
    nearest_time['moadoph'] = config[0]['moadophLastTime']

    # None timestamps group for newest time of the news:
    nearest_time['anu_botanical_gardens'] = config[0]['anu_botanical_gardensLastTime']
    nearest_time['cbr_house'] = config[0]['cbr_houseLastTime']
    nearest_time['visit_cbr'] = config[0]['visit_cbrLastTime']
    nearest_time['experience_AIS'] = config[0]['experience_AISLastTime']
    nearest_time['llewellyn_hall'] = config[0]['llewellyn_hallLastTime']
    nearest_time['national_conv_centre_cbr'] = config[0]['national_conv_centre_cbrLastTime']
    nearest_time['the_phoenix'] = config[0]['the_phoenixLastTime']
    nearest_time['smiths_alternative'] = config[0]['smiths_alternativeLastTime']
    nearest_time['cbr_intel_music_fes'] = config[0]['cbr_intel_music_fesLastTime']
    nearest_time['cbr_opera'] = config[0]['cbr_operaLastTime']
    nearest_time['RSL_ACT_brunch'] = config[0]['RSL_ACT_brunchLastTime']
    nearest_time['cbr_conv_bureau'] = config[0]['cbr_conv_bureauLastTime']
    nearest_time['cbr_glassworks'] = config[0]['cbr_glassworksLastTime']
    nearest_time['cbr_linux_users_groups'] = config[0]['cbr_linux_users_groupsLastTime']
    nearest_time['ACT_labor'] = config[0]['ACT_laborLastTime']
    nearest_time['events_ACT'] = config[0]['events_ACTLastTime']
    nearest_time['ACT_LAQ_time'] = config[0]['ACT_LAQ_timeLastTime']
    nearest_time['national_library_AU'] = config[0]['national_library_AULastTime']
    nearest_time['national_portrait_gallery'] = config[0]['national_portrait_galleryLastTime']
    nearest_time['AU_war_memorial'] = config[0]['AU_war_memorialLastTime']
    nearest_time['ACT_LAeP'] = config[0]['ACT_LAePLastTime']

    # original newest time of the news
    original_nearest_time = {}
    original_nearest_time['abc'] = config[0]['abcLastTime']
    original_nearest_time['sbs'] = config[0]['sbsLastTime']
    original_nearest_time['cbr_times'] = config[0]['cbr_timesLastTime']
    original_nearest_time['uc'] = config[0]['ucLastTime']
    original_nearest_time['hercbr'] = config[0]['hercbrLastTime']
    original_nearest_time['tidbinbilla'] = config[0]['tidbinbillaLastTime']
    original_nearest_time['cmag'] = config[0]['cmagLastTime']
    original_nearest_time['national_arboretum'] = config[0]['national_arboretumLastTime']
    original_nearest_time['bom'] = config[0]['bomLastTime']
    original_nearest_time['multi_cultural_festival'] = config[0]['multi_cultural_festivalLastTime']
    original_nearest_time['nca'] = config[0]['ncaLastTime']
    original_nearest_time['unsw'] = config[0]['unswLastTime']
    original_nearest_time['iconwater'] = config[0]['iconwaterLastTime']
    original_nearest_time['greens'] = config[0]['greensLastTime']
    original_nearest_time['thestreet'] = config[0]['thestreetLastTime']
    original_nearest_time['anu'] = config[0]['anuLastTime']
    original_nearest_time['moadoph'] = config[0]['moadophLastTime']

    # None timestamps group for original newest time of the news:
    original_nearest_time['anu_botanical_gardens'] = config[0]['anu_botanical_gardensLastTime']
    original_nearest_time['cbr_house'] = config[0]['cbr_houseLastTime']
    original_nearest_time['visit_cbr'] = config[0]['visit_cbrLastTime']
    original_nearest_time['experience_AIS'] = config[0]['experience_AISLastTime']
    original_nearest_time['llewellyn_hall'] = config[0]['llewellyn_hallLastTime']
    original_nearest_time['national_conv_centre_cbr'] = config[0]['national_conv_centre_cbrLastTime']
    original_nearest_time['the_phoenix'] = config[0]['the_phoenixLastTime']
    original_nearest_time['smiths_alternative'] = config[0]['smiths_alternativeLastTime']
    original_nearest_time['cbr_intel_music_fes'] = config[0]['cbr_intel_music_fesLastTime']
    original_nearest_time['cbr_opera'] = config[0]['cbr_operaLastTime']
    original_nearest_time['RSL_ACT_brunch'] = config[0]['RSL_ACT_brunchLastTime']
    original_nearest_time['cbr_conv_bureau'] = config[0]['cbr_conv_bureauLastTime']
    original_nearest_time['cbr_glassworks'] = config[0]['cbr_glassworksLastTime']
    original_nearest_time['cbr_linux_users_groups'] = config[0]['cbr_linux_users_groupsLastTime']
    original_nearest_time['ACT_labor'] = config[0]['ACT_laborLastTime']
    original_nearest_time['events_ACT'] = config[0]['events_ACTLastTime']
    original_nearest_time['ACT_LAQ_time'] = config[0]['ACT_LAQ_timeLastTime']
    original_nearest_time['national_library_AU'] = config[0]['national_library_AULastTime']
    original_nearest_time['national_portrait_gallery'] = config[0]['national_portrait_galleryLastTime']
    original_nearest_time['AU_war_memorial'] = config[0]['AU_war_memorialLastTime']
    original_nearest_time['ACT_LAeP'] = config[0]['ACT_LAePLastTime']

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
                                  website[:3].replace("_", ""))
        else:
            insert_news_from_list(nearest_time, news_list.get(website), nearest_time[website], website,
                                  website)

    print('===== Insert finished! Totally ', inserted_cnt, ' news added. =====')

    myquery = {"abcLastTime": original_nearest_time['abc']}
    newvalues = {"$set": {"abcLastTime": nearest_time['abc']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"sbsLastTime": original_nearest_time['sbs']}
    newvalues = {"$set": {"sbsLastTime": nearest_time['sbs']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"cbr_timesLastTime": original_nearest_time['cbr_times']}
    newvalues = {"$set": {"cbr_timesLastTime": nearest_time['cbr_times']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"ucLastTime": original_nearest_time['uc']}
    newvalues = {"$set": {"ucLastTime": nearest_time['uc']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"hercbrLastTime": original_nearest_time['hercbr']}
    newvalues = {"$set": {"hercbrLastTime": nearest_time['hercbr']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"tidbinbillaLastTime": original_nearest_time['tidbinbilla']}
    newvalues = {"$set": {"tidbinbillaLastTime": nearest_time['tidbinbilla']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"cmagLastTime": original_nearest_time['cmag']}
    newvalues = {"$set": {"cmagLastTime": nearest_time['cmag']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"national_arboretumLastTime": original_nearest_time['national_arboretum']}
    newvalues = {"$set": {"national_arboretumLastTime": nearest_time['national_arboretum']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"bomLastTime": original_nearest_time['bom']}
    newvalues = {"$set": {"bomLastTime": nearest_time['bom']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"multi_cultural_festivalLastTime": original_nearest_time['multi_cultural_festival']}
    newvalues = {"$set": {"multi_cultural_festivalLastTime": nearest_time['multi_cultural_festival']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"ncaLastTime": original_nearest_time['nca']}
    newvalues = {"$set": {"ncaLastTime": nearest_time['nca']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"unswLastTime": original_nearest_time['unsw']}
    newvalues = {"$set": {"unswLastTime": nearest_time['unsw']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"iconwaterLastTime": original_nearest_time['iconwater']}
    newvalues = {"$set": {"iconwaterLastTime": nearest_time['iconwater']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"greensLastTime": original_nearest_time['greens']}
    newvalues = {"$set": {"greensLastTime": nearest_time['greens']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"thestreetLastTime": original_nearest_time['thestreet']}
    newvalues = {"$set": {"thestreetLastTime": nearest_time['thestreet']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"anuLastTime": original_nearest_time['anu']}
    newvalues = {"$set": {"anuLastTime": nearest_time['anu']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"moadophLastTime": original_nearest_time['moadoph']}
    newvalues = {"$set": {"moadophLastTime": nearest_time['moadoph']}}
    db_config.config.update_one(myquery, newvalues)

    # insert to db for none timestamps groups
    myquery = {"cbr_houseLastTime": original_nearest_time['cbr_house']}
    newvalues = {"$set": {"cbr_houseLastTime": nearest_time['cbr_house']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"visit_cbrLastTime": original_nearest_time['visit_cbr']}
    newvalues = {"$set": {"visit_cbrLastTime": nearest_time['visit_cbr']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"experience_AISLastTime": original_nearest_time['experience_AIS']}
    newvalues = {"$set": {"experience_AISLastTime": nearest_time['experience_AIS']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"llewellyn_hallLastTime": original_nearest_time['llewellyn_hall']}
    newvalues = {"$set": {"llewellyn_hallLastTime": nearest_time['llewellyn_hall']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"national_conv_centre_cbrLastTime": original_nearest_time['national_conv_centre_cbr']}
    newvalues = {"$set": {"national_conv_centre_cbrLastTime": nearest_time['national_conv_centre_cbr']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"the_phoenixLastTime": original_nearest_time['the_phoenix']}
    newvalues = {"$set": {"the_phoenixLastTime": nearest_time['the_phoenix']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"smiths_alternativeLastTime": original_nearest_time['smiths_alternative']}
    newvalues = {"$set": {"smiths_alternativeLastTime": nearest_time['smiths_alternative']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"cbr_intel_music_fesLastTime": original_nearest_time['cbr_intel_music_fes']}
    newvalues = {"$set": {"cbr_intel_music_fesLastTime": nearest_time['cbr_intel_music_fes']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"cbr_operaLastTime": original_nearest_time['cbr_opera']}
    newvalues = {"$set": {"cbr_operaLastTime": nearest_time['cbr_opera']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"RSL_ACT_brunchLastTime": original_nearest_time['RSL_ACT_brunch']}
    newvalues = {"$set": {"RSL_ACT_brunchLastTime": nearest_time['RSL_ACT_brunch']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"cbr_conv_bureauLastTime": original_nearest_time['cbr_conv_bureau']}
    newvalues = {"$set": {"cbr_conv_bureauLastTime": nearest_time['cbr_conv_bureau']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"cbr_glassworksLastTime": original_nearest_time['cbr_glassworks']}
    newvalues = {"$set": {"cbr_glassworksLastTime": nearest_time['cbr_glassworks']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"cbr_linux_users_groupsLastTime": original_nearest_time['cbr_linux_users_groups']}
    newvalues = {"$set": {"cbr_linux_users_groupsLastTime": nearest_time['cbr_linux_users_groups']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"ACT_laborLastTime": original_nearest_time['ACT_labor']}
    newvalues = {"$set": {"ACT_laborLastTime": nearest_time['ACT_labor']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"events_ACTLastTime": original_nearest_time['events_ACT']}
    newvalues = {"$set": {"events_ACTLastTime": nearest_time['events_ACT']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"ACT_LAQ_timeLastTime": original_nearest_time['ACT_LAQ_time']}
    newvalues = {"$set": {"ACT_LAQ_timeLastTime": nearest_time['ACT_LAQ_time']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"national_library_AULastTime": original_nearest_time['national_library_AU']}
    newvalues = {"$set": {"national_library_AULastTime": nearest_time['national_library_AU']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"national_portrait_galleryLastTime": original_nearest_time['national_portrait_gallery']}
    newvalues = {"$set": {"national_portrait_galleryLastTime": nearest_time['national_portrait_gallery']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"AU_war_memorialLastTime": original_nearest_time['AU_war_memorial']}
    newvalues = {"$set": {"AU_war_memorialLastTime": nearest_time['AU_war_memorial']}}
    db_config.config.update_one(myquery, newvalues)

    myquery = {"ACT_LAePLastTime": original_nearest_time['ACT_LAeP']}
    newvalues = {"$set": {"ACT_LAePLastTime": nearest_time['ACT_LAeP']}}
    db_config.config.update_one(myquery, newvalues)

    print(db_config.config.find())
    print("==== success! ====")
    print('latest timestamp is:', nearest_time)
    myquery = {"newsId": original_id}
    newvalues = {"$set": {"newsId": static_news_id}}

    db_config.config.update_one(myquery, newvalues)
    # upload the newest time into db


def generate_result(stri, classifier):  # use fasttext to predict the mails into spam or ham
    spam_rate = []  # store the result into the dict spam_rate
    predict_value = 1 if classifier.predict_proba([stri])[0][0][0] == '1' else 0
    if predict_value == 1:
        spam_rate.append(classifier.predict_proba([stri])[0][0][1])
    else:
        spam_rate.append(round(1.0 - float(classifier.predict_proba([stri])[0][0][1]), 6))
    return spam_rate[0]


def insert_news_from_list(nearest_time, list, nearest_time_web, website, source):
    print('inseNewsFroL: got ', website, ' with news:', len(list))

    global static_news_id
    nearest_time = nearest_time

    # print(static_news_id)

    nearest_time_one = nearest_time_web
    news_list = list
    new_nearest_time = 0

    for url in news_list[:len(news_list) - 1]:
        if website == 'abc':
            news_time = utility.find_time_abc(url)
        elif website == 'sbs':
            news_time = utility.find_time_sbs(url)
        elif website == 'cbr_times':
            news_time = utility.find_time_cbt(url)
        elif website == 'uc':
            news_time = utility.find_time_uc(url)
        elif website == 'tidbinbilla':
            news_time = utility.find_time_tidbinbilla(url)
        elif website == 'cmag':
            news_time = utility.find_time_cmag(url)
        elif website == 'national_arboretum':
            news_time = utility.find_time_national_arboretum(url)
        elif website == 'bom':
            news_time = utility.find_time_bom(url)
        elif website == 'find_time_multi_cultural_festival':
            news_time = utility.find_time_find_time_multi_cultural_festival(url)
        # elif website == 'nca': # lack of seconds
        #     news_time = utility.find_time_nca(url)
        # elif website == 'unsw': # strange as it is a text data
        #     news_time = utility.find_time_unsw(url)
        # elif website == 'iconwater': # strange as it is a text data
        #     news_time = utility.find_time_iconwater(url)
        elif website == 'greens':
            news_time = utility.find_time_greens(url)
        elif website == 'thestreet':
            news_time = utility.find_time_thestreet(url)
        elif website == 'anu':
            news_time = utility.find_time_anu(url)
        elif website == 'moadoph':
            news_time = utility.find_time_moadoph(url)
        else:
            news_time = utility.find_time_general(url)
        if news_time == None:  # skip news which cannot find standard publish times. no time to improve
            continue

        time_array = time.strptime(news_time.replace('T', ' ')[:-6], "%Y-%m-%d %H:%M:%S")
        news_timestamp = time.mktime(time_array)

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

        if news_timestamp <= nearest_time_one and website != 'tidbinbilla':  # if the time of the news less than the newest time in the memory
            continue

        if news_timestamp >= new_nearest_time:
            new_nearest_time = news_timestamp

        article = g.extract(url=url)
        # print(article)
        news_entity = NewsEntity(article.title, article.authors, news_timestamp, article.meta_description,
                                 article.meta_keywords, article.cleaned_text, url)

        # print(url)
        # print("metakeywords"+article.meta_keywords)
        # print(type(article.meta_keywords))
        for keywords in re.split(",", article.meta_keywords.replace(" ", "")):
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
        # fixme( need changed in win)
        score = round(generate_result(news_entity.cleaned_text, classifier_2), 2)
        # score = round(0.9, 2)
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

        db.news.insert_one({"news_id": int(int(static_news_id) + 1),
                            "title": news_entity.title,
                            "authors": news_entity.authors,
                            "publish_date": news_entity.publish_date,
                            "meta_description": news_entity.meta_description,
                            "meta_keywords": news_entity.meta_keywords,
                            "cleaned_text": news_entity.cleaned_text,
                            "rank": score,
                            "timerank": score,
                            "url": url,
                            'category': news_entity.category,
                            'approve': 0,
                            'source': source,
                            'disapprove': 0
                            })
        static_news_id = static_news_id + 1
        global inserted_cnt
        inserted_cnt += 1

    if new_nearest_time != 0:
        if website == 'abc':
            nearest_time['abc'] = new_nearest_time
        elif website == 'sbs':
            nearest_time['sbs'] = new_nearest_time
        elif website == 'cbr_times':
            nearest_time['cbr_times'] = new_nearest_time
        elif website == 'uc':
            nearest_time['uc'] = new_nearest_time
        elif website == 'hercbr':
            nearest_time['hercbr'] = new_nearest_time
        elif website == 'tidbinbilla':
            nearest_time['tidbinbilla'] = new_nearest_time
        elif website == 'cmag':
            nearest_time['cmag'] = new_nearest_time


if __name__ == '__main__':
    client = MongoClient()
    db = client.NewsAggregator

    db_config = client.Configure  # db
    config = db_config.config.find()  # collection
    global_news = config[0]['newsId']
    static_news_id = global_news
    # fixme( need changed in win)
    classifier_2 = fasttext.load_model('../../Rank/FastText/Output/news10d.bin', label_prefix='__label__')
    #    print(classifier_2)
    # print(global_news)
    original_id = config[0]['newsId']

    # f = open("Australia_vocb.txt")
    Australian_list = []
    # for line in f:
    #     Australian_list.append(line.strip())
    # f.close()
    g = Goose()
    insert()

    # schedule.every(1).hour.do(insert)

    # while True:
    # schedule.run_pending()
    # time.sleep(1)

    # insert()
