import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
vacancy = input('Please input a desirable vacancy: ')
page = 1
num = 1

vacancy_dict = {}

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
                    currency = str(pat_cur.search(salary).group())
                    list_salary = [min_salary, max_salary, currency]
                elif 'от' in salary:
                    pat_min = re.compile(r'[^a-zA-zа-яА-Я\.]+')
                    min_salary = int(pat_min.search(salary).group().replace('\u202f', ''))
                    pat_cur = re.compile(r'(?<=[^a-zA-zа-яА-Я\.]\s)[a-zA-zа-яА-Я]+')
                    currency = str(pat_cur.search(salary).group())
                    list_salary = [min_salary, None, currency]
                elif 'до' in salary:
                    pat_max = re.compile(r'[^a-zA-zа-яА-Я\.]+')
                    max_salary = int(pat_max.search(salary).group().replace('\u202f', ''))
                    pat_cur = re.compile(r'(?<=[^a-zA-zа-яА-Я\.]\s)[a-zA-zа-яА-Я]+')
                    currency = str(pat_cur.search(salary).group())
                    list_salary = [None, max_salary, currency]
        except:
            list_salary = [None, None, None]
        vacancy_value = {num: {"vacancy_name": name_vacancy,
                               "vacancy_link": link_vacancy,
                               "salary": list_salary,
                               "web_link": "https://hh.ru"}}
        vacancy_dict.update(vacancy_value)
        num += 1
    if tags_span != []:
        page += 1
    else:
        if page != 1:
            print('Script completed!')
            break
        else:
            print('Something wrong. Please check vacancy')
            break

with open('vacancy_dict.json', 'w') as json_file:
    json.dump(vacancy_dict, json_file, ensure_ascii=False)
