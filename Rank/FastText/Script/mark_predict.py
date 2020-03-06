import random
import codecs
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import os
import fasttext
import json
import sklearn
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import auc
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import spacy
import pickle

'''
mark predict is used for test returned mark for specific input format
'''

modelpath = '../Output/news10d.bin'
stri = 'Here is a selection of photos sent in by audience members from around Australia. If you have any photos that youd like to share, send them in via the upload page. You can take a look at more photos from across the country on our Instagram, and share your own photos with us by using #ABCmyphoto on Instagram.'

def generate_result(datapath,classifier):# use fasttext to predict the mails into spam or ham
    labels_predict = []
    spam_rate = []  # store the result into the dict spam_rate

    with open (datapath) as fr:
       lines = fr.readlines()
    for line in lines:

        labels_predict.append(classifier.predict_proba(line)[0][0])
        predict_value = 1 if classifier.predict_proba([line[0:-10]])[0][0][0] == '1' else 0
        if predict_value == 1:
            spam_rate.append(classifier.predict_proba([line[0:-10]])[0][0][1])
        else:
            spam_rate.append(round(1.0-float(classifier.predict_proba([line[0:-10]])[0][0][1]),6))
        print(spam_rate)

def generate_result_str(stri,classifier):# use fasttext to predict the mails into spam or ham
    spam_rate = 0.0  # store the result into the dict spam_rate
    predict_value = 1 if classifier.predict_proba([stri])[0][0][0] == '1' else 0
    if predict_value == 1:
        spam_rate = classifier.predict_proba([stri])[0][0][1]
    else:
        spam_rate = round(1.0-float(classifier.predict_proba([stri])[0][0][1]),6)
    return spam_rate


classifier = fasttext.load_model(modelpath, label_prefix='__label__')

#generate_result(datapath,classifier)
print(type(generate_result_str(stri,classifier)))
print(generate_result_str(stri,classifier))

i = 1
j = 1
s = str(i)+','+str(j)
print(s)
print(type(s))