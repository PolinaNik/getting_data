from pprint import pprint
import requests
from lxml import html
import re
from pymongo import MongoClient

url = 'https://lenta.ru/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

top_news = dom.xpath("//div[@class='topnews']")[0]

news = []

# Работа со всеми новостями, кроме главной
elem = top_news.xpath("//a[@class='card-mini _topnews']")
for new in elem:
    title = {}
    new_title = new.xpath(".//span[@class='card-mini__title']/text()")[0]
    new_link = new.xpath(".//@href")[0]
    new_time = new.xpath(".//time[@class='card-mini__date']/text()")[0]
    year = re.findall('\d+', new_link)[0]
    month = re.findall('\d+', new_link)[1]
    day = re.findall('\d+', new_link)[2]
    title['name'] = new_title
    title['source'] = url
    title['link'] = 'https://lenta.ru' + new_link
    title['data'] = f'{year}/{month}/{day} ' + new_time
    news.append(title)

# Работа с главной новостью
big_news = top_news.xpath("//div[@class='topnews__first-topic']")[0]
title = {}
new_title = big_news.xpath(".//h3[@class='card-big__title']/text()")[0]
new_link = big_news.xpath(".//@href")[0]
year = re.findall('\d+', new_link)[0]
month = re.findall('\d+', new_link)[1]
day = re.findall('\d+', new_link)[2]
title['name'] = new_title
title['source'] = url
title['link'] = 'https://lenta.ru' + new_link
title['data'] = f'{year}/{month}/{day} ' + new_time

news.append(title)
pprint(news)

"""Вставка значений в базу данных
с прокеркой на уникальность ссылки новости
"""

client = MongoClient('localhost', 27017)
db = client['news']  # database
news_db = db.vacancies  # collection

for item in news:
    link_news = item['link']
    if news_db.count_documents({"link": link_news}) == 0:
        news_db.insert_one(item)
