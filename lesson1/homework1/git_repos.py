"""1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
для конкретного пользователя, сохранить JSON-вывод в файле *.json."""


import requests
import json

user = "PolinaNik"

url = f'https://api.github.com/users/{user}/repos'
response = requests.get(url)

j_data = response.json()

repos = []
for repo in j_data:
    name = repo.get("name")
    repos.append(name)

for repo_name in repos:
    print(repo_name)

with open('repo_names.json', 'w') as json_file:
    json.dump(repos, json_file)