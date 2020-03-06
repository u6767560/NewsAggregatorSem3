# -*- coding: utf-8 -*-
"""
Created on Sun Sept 22 18:26:24 2019

@author: geo
"""

import os
import schedule
import time
def RunUpload():
    os.system('python3 Upload_v0.py')
    # print('part 1 start')
    # time.sleep(3)
    # print('part 1 end')

RunUpload()

print("==========round 1 ends=========")
schedule.every(1).hour.do(lambda: RunUpload())



while True:
    schedule.run_pending()
    time.sleep(1)
