import os
import schedule
import time


def RunUploadRSS():
    os.system('python3 UploadRSS_v0.py')
    # print('part 2 start')
    # time.sleep(5)
    # print('part 2 end')


RunUploadRSS()

print("==========round 1 ends=========")

schedule.every(1).hour.do(lambda: RunUploadRSS())

while True:
    schedule.run_pending()
    time.sleep(1)