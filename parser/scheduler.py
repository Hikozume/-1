import schedule
import time
import os


def job():
    os.system('python main.py')


schedule.every().day.at("14:54").do(job) #парсинг по расписанию в 14:54 каждого дня будет запускаться скрипт main,py


while 1:
    schedule.run_pending()
    time.sleep(1)
