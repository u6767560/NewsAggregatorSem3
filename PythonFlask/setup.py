from flask import Flask,render_template
import json
from flask import request
from pymongo import IndexModel, ASCENDING, DESCENDING
from flask_pymongo import PyMongo
import pymongo
import re
from pymongo import MongoClient

from flask import request


app = Flask(__name__)

app.config.update(
    MONGO_URI='mongodb://localhost:27017/NewsAggregator',
    MONGO_USERNAME='user',
    MONGO_PASSWORD='1234'
)
mongo = PyMongo(app)
client = MongoClient('mongodb://user:1234@localhost:27017')
client = MongoClient()
db = client.NewsAggregator


@app.route('/')
def hello():
    return render_template('jkl_index.html')


@app.route('/index', methods=["GET"])
def index():
    return render_template('jkl_index.html')


@app.route('/Australia.html')
def Australia():
    return render_template('Australia.html')

@app.route('/Global.html')
def Global():
    return render_template('Global.html')

@app.route('/Canberra.html')
def Canberra():
    return render_template('Canberra.html')

# the load of the news with the highest score
@app.route('/test_get', methods=['GET'])
def test_get():
    result = []
    ids = request.args.get("page")
    cate = request.args.get("cate")
    t_max = db.news.find({"category":cate}).count()
    t = db.news.find({"category":cate}).sort("timerank", DESCENDING).limit(20).skip(20*int(ids)-20)
    result.append(t_max)
    for news in t:
        del news['_id']
        del news['cleaned_text']
        del news['meta_description']
        result.append(news)
    return json.dumps(result)


# the function of get the newest news regardless of the score
@app.route('/test_get_latest', methods=['GET'])
def test_get_latest():
    result = []
    t = db.news.find().sort("publish_date", DESCENDING).limit(10)
    for news in t:
        del news['_id']
        del news['cleaned_text']
        del news['meta_description']
        result.append(news)
    return json.dumps(result)


# the function of approve and disapprove
@app.route('/comment', methods=['GET'])
def comment():
    ip = request.remote_addr
    t = list(db.approveRecord.find({"ip":ip,"news_id":request.args.get("news_id")}))
    news_raw = db.news.find({"news_id": int(request.args.get("news_id"))})
    news = news_raw[0]
    news['status'] = 0
    # print(t)
    # print(news)
    if t is None or len(t) == 0:
        news['status'] = 1
    db.approveRecord.insert_one({"news_id": request.args.get("news_id"),
                                 "ip": ip,
                                 "approve_type": request.args.get("comment_type")
                                 })
    if news['status'] == 1:
        news['approve'] = news['approve'] + 1
        news['status'] = 0
        myquery = {"news_id": int(request.args.get("news_id"))}
        newvalues = {"$set": {"approve": news['approve']}}
        db.news.update_one(myquery, newvalues)
    else:
        news['approve'] = news['approve'] + 1
        news['status'] = 1
        myquery = {"news_id": int(request.args.get("news_id"))}
        newvalues = {"$set": {"approve": news['approve']}}
        db.news.update_one(myquery, newvalues)
        # else:
        #     news['disapprove'] = news['disapprove'] + 1
        #     myquery = {"news_id": int(request.args.get("news_id"))}
        #     newvalues = {"$set": {"disapprove": news['disapprove']}}
        #     db.news.update_one(myquery, newvalues)
    del news['_id']
    return json.dumps(news)

@app.route('/comment_canberra', methods=['GET'])
def comment_canberra():
    ip = request.remote_addr
    t = list(db.approveRecord.find({"ip":ip,"news_id":request.args.get("news_id")}))
    news_raw = db.news.find({"news_id": int(request.args.get("news_id"))})
    news = news_raw[0]
    news['status'] = 0
    # print(t)
    # print(news)
    if t is None or len(t) == 0:
        news['status'] = 1
    db.approveRecord.insert_one({"news_id": request.args.get("news_id"),
                                 "ip": ip,
                                 "approve_type": request.args.get("comment_type")
                                 })
    if news['status'] == 1:
        news['approve'] = news['approve'] + 1
        news['status'] = 0
        if news['approve']<=100:
            news['timerank'] += 0.003
        print(news['timerank'])
        myquery = {"news_id": int(request.args.get("news_id"))}
        newvalues = {"$set": {"approve": news['approve']}}
        db.news.update_one(myquery, newvalues)
        newvalues = {"$set": {"timerank": news['timerank']}}
        db.news.update_one(myquery, newvalues)
    else:
        news['approve'] = news['approve'] + 1
        news['status'] = 1
        if news['approve']<=100:
            news['timerank'] += 0.003
        print(news['timerank'])
        myquery = {"news_id": int(request.args.get("news_id"))}
        newvalues = {"$set": {"approve": news['approve']}}
        db.news.update_one(myquery, newvalues)
        newvalues = {"$set": {"timerank": news['timerank']}}
        db.news.update_one(myquery, newvalues)
        # else:
        #     news['disapprove'] = news['disapprove'] + 1
        #     myquery = {"news_id": int(request.args.get("news_id"))}
        #     newvalues = {"$set": {"disapprove": news['disapprove']}}
        #     db.news.update_one(myquery, newvalues)
    del news['_id']
    return json.dumps(news)



@app.route('/news_details/<news_id>', methods=['GET'])
def news_details(news_id):
    news2 = db.news.find({"news_id": int(news_id)})
    result = []

    for news in news2:
        del news['_id']
        news['top_image'] = str(news['top_image'], encoding='utf-8')
        result.append(news)
    return_entity = result[0]

    return render_template('news_details.html', return_entity=return_entity)


# the search function
@app.route('/search_news', methods=['GET'])
def search_news():
    # this part is just for trial, it will be replaced by the elastic search
    keyword = request.args.get("keyword")
    ids = request.args.get("page")
    cate = request.args.get("cate")
    keyword.strip()
    rexExp = re.compile('.*' + keyword + '.*', re.IGNORECASE)
    news_accurate_max = db.news.find({"cleaned_text":rexExp}).count()
    news_accurate = db.news.find({"cleaned_text":rexExp}).sort("timerank", DESCENDING).limit(10).skip(10*int(ids)-10)
    news_list = []
    news_list.append(news_accurate_max)
    for news in news_accurate:
        del news['_id']
        news_list.append(news)
    return json.dumps(news_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
#    app.run()
