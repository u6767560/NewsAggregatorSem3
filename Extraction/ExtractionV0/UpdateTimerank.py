import schedule
from pymongo import MongoClient
import math
import time

'''
UpdateTimerank is to update the scores in the database according to the time difference from their publish time.
Canberra news, specially, considers upvote number.
'''

def update_time_rank():
    update_time = int(time.time())
    client = MongoClient()
    db = client.NewsAggregator
    max_id = db.news.count()
    for i in range(1,max_id+1):
        myquery = {"news_id": i}
        news = db.news.find_one(myquery)
        publish_date = news['publish_date']
        category = news['category']
        score = news['rank']
        approve = news['approve']
        if category != "Canberra":
            timerank = score * math.pow(0.9, (update_time - publish_date) / 86400)
        else:
            timerank = ((0.4 * score + 0.3) * math.pow(0.9, (update_time - publish_date) / 86400)+0.003*approve)* math.pow(0.9, (update_time - publish_date) / 86400)
        newvalues = {"$set": {"timerank": timerank}}
        db.news.update_one(myquery, newvalues)
    print("finished updating!")

update_time_rank()

schedule.every(1).hours.do(update_time_rank)

while True:
    schedule.run_pending()
    time.sleep(1)