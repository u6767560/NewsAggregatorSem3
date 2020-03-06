# -*- coding: utf-8 -*-
"""
Created on Sun Sept 22 18:26:24 2019

@author: geo

RepeatUpload.py is used for repeat Goose and RSS upload every 1 hour.
"""

import os
import schedule
import time
import threading

def RunUpload():
    os.system('python3 Upload_v0.py')
    # print('part 1 start')
    # time.sleep(3)
    # print('part 1 end')

def RunUploadRSS():
    os.system('python3 RSSTextualExtraction.py')
    # print('part 2 start')
    # time.sleep(5)
    # print('part 2 end')
 

# upload in one function
def RunUploadAll():
    os.system('python3 Upload_v0.py')
    time.sleep(120)
    os.system('python3 UploadRSS_v0.py')

def run_threaded(func):
    job_thread = threading.Thread(target=func)
    job_thread.start()

RunUpload()
RunUploadRSS()

print("==========round 1 ends=========")
# How to allocate the minute to run depends on which file can be executed faster.
# if RunUpload runs faster which last less than 15 min, then RunUploadRSS can set :20
# Not sure the exact time writing to DB, it might not work well if they overlap
# schedule.every().hour.at(':15').do(run_threaded, RunUpload)
# schedule.every().hour.at(':45').do(run_threaded, RunUploadRSS)


# Can uncomment and try this if the above doesn't work well
schedule.every(2).hours.do(RunUploadAll)



while True:
    schedule.run_pending()
    time.sleep(1)
