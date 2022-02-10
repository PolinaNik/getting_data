import requests
import json

appid = 'b6907d289e10d714a6e88b30761fae22'
service = 'https://samples.openweathermap.org/data/2.5/weather'
req = requests.get(f'{service}?q=London,uk&appid={appid}')
data = json.loads(req.text)

print(f"В городе {data['name']} {data['main']['temp']} "
      f"градусов по Кельвину")


