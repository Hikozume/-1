import time

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pyodbc


connection_to_db = pyodbc.connect(r'Driver={SQL Server};Server=DESKTOP-SI0JD8G;Database=Auto;Trusted_Connection=yes;')
cursor = connection_to_db.cursor()
links = []


def update_main_page():
    url = 'https://www.autonews.ru/tags/?tag=%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8'
    request = requests.get(url)
    print(request.status_code)
    soup = BeautifulSoup(request.text, 'lxml')
    news = []
    try:
        temp = soup.find_all('div', 'js-exclude-block')
        for el in temp:
            if el.find('a', 'item-big__category').text == 'Новости':
                link = el.find('a', 'item-big__link')['href']
                if link in links:
                    continue
                links.append(link)
                title = el.find('span', 'item-big__title').text
                news.append({'title': title,
                             'link': link})
    except:
        pass
    return news


def parse_page(news):
    for el in news:
        request = requests.get(el['link'])
        print(request.status_code)
        soup = BeautifulSoup(request.text, 'lxml')
        anons = soup.find('div', 'article__header__anons').text
        main_image = soup.find('div', 'article__main-image__image').find('img')['src']
        all_base_cols = soup.find_all('div', 'l-base__col__main')
        all_p = all_base_cols[1].find_all('p')
        text = ''
        for p in all_p:
            if p.text != ', ':
                text += p.text
        query = 'INSERT INTO dbo.News (link, title, anons, image, text, date) VALUES (?,?,?,?,?,?);'
        values = el['link'], el['title'], anons, main_image, text, datetime.now()
        cursor.execute(query, values)
        connection_to_db.commit()


while True:
    time.sleep(60)
    parse_page(update_main_page())