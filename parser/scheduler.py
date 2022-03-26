import schedule
import time
import os


def job():
    os.system('python main.py')


schedule.every().day.at("10:30").do(job)


while 1:
    schedule.run_pending()
    time.sleep(1)
