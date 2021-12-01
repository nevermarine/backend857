import requests
import json


class Weather:
	@staticmethod
	def get_weather() -> dict:
		API = '8397aa1b69899690124619bad12a067e'
		id_Moscow = '524901'
		r = requests.get('http://api.openweathermap.org/data/2.5/weather?id='+id_Moscow+'&appid='+API +'&units=metric').json()
		# with open('weather_templates.json', 'w') as f:
		# 	json.dump(r, f)
		return r
