"""Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы
получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько
страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:

   1) Наименование вакансии.
   2) Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
   3) Ссылку на саму вакансию.
   4) Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью
dataFrame через pandas. Сохраните в json либо csv.
"""

import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint
from pymongo import MongoClient

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
vacancy = input('Please input a desirable vacancy: ')
page = 1

client = MongoClient('localhost', 27017)
db = client['hh_vacancies']  # database
vacancies = db.vacancies  # collection

while True:

    url = f'https://hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true&ored_clusters=true&text={vacancy}&schedule=remote&from=cluster_schedule&hhtmFromLabel=cluster_schedule&page={page}&hhtmFrom=vacancy_search_list'
    response = requests.get(url, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    tags_span = dom.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_redesigned'})
    print(f'Parsing page #{page} of website')
    for tag in tags_span:
        name_vacancy = str(tag.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText())
        link_vacancy = tag.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}, href=True)['href']
        list_salary = []
        try:
            salary = tag.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
            if salary:
                if '-' in salary:
                    pat_min = re.compile(r'\d.+(?=\s–)')
                    min_salary = int(pat_min.search(salary).group().replace('\u202f', ''))  # '\u202f'
                    pat_max = re.compile(r'(?<=–.)[^a-zA-zа-яА-Я]+')
                    max_salary = int(pat_max.search(salary).group().replace('\u202f', ''))
                    pat_cur = re.compile(r'[a-zA-zа-яА-Я]+')
                    currency = pat_cur.search(salary).group()
                    list_salary = [min_salary, max_salary, currency]
                elif 'от' in salary:
                    pat_min = re.compile(r'[^a-zA-zа-яА-Я\.]+')
                    min_salary = int(pat_min.search(salary).group().replace('\u202f', ''))
                    pat_cur = re.compile(r'(?<=[^a-zA-zа-яА-Я\.]\s)[a-zA-zа-яА-Я]+')
                    currency = pat_cur.search(salary).group()
                    list_salary = [min_salary, None, currency]
                elif 'до' in salary:
                    pat_max = re.compile(r'[^a-zA-zа-яА-Я\.]+')
                    max_salary = int(pat_max.search(salary).group().replace('\u202f', ''))
                    pat_cur = re.compile(r'(?<=[^a-zA-zа-яА-Я\.]\s)[a-zA-zа-яА-Я]+')
                    currency = pat_cur.search(salary).group()
                    list_salary = [None, max_salary, currency]
        except:
            list_salary = [None, None, None]
        vacancy_value = {"vacancy_name": name_vacancy,
                         "vacancy_link": link_vacancy,
                         "salary": list_salary,
                         "web_link": "https://hh.ru"}
        vacancies.insert_one(vacancy_value)
    if tags_span != []:
        page += 1
    else:
        if page != 1:
            print('Script completed!')
            break
        else:
            print('Something wrong. Please check vacancy')
            break

find_salary = vacancies.find({"salary": {"$elemMatch": {"$gt": 400000}}})

for doc in list(find_salary):
    pprint(doc)

"""output

{'_id': ObjectId('620d9613fcd3e289fc560a99'),
 'salary': [None, 450000, 'руб'],
 'vacancy_link': 'https://khabarovsk.hh.ru/vacancy/51004272?from=vacancy_search_list&hhtmFrom=vacancy_search_list&query=python',
 'vacancy_name': 'Python разработчик (AWS)',
 'web_link': 'https://hh.ru'}

"""
