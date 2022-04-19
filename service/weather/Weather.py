import requests
import logging
from typing import Optional

logg = logging.getLogger("WeatherLogger.WorkLogger")
logg.debug("Initialize Weather")


class Weather:
    @staticmethod
    def get_weather(city="Москва", lang="ru") -> Optional[dict]:
        logg.info('Try to get current weather by name of the city and language...')
        logg.info('Initialize API for openweathermap.org...')
        API = '8397aa1b69899690124619bad12a067e'
        logg.info('Start work with openweathermap.org...')
        logg.info('Try to get data from the openweathermap.org...')
        data = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&lang={lang}&units=metric&appid={API}').json()
        if data:
            logg.info('Processing a response from openweathermap.org...')
            weather = {
            'description': data['weather'][0]['main'],
            'text': data['weather'][0]['description'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'windSpeed': data['wind']['speed']
            }
            logg.info('I get a correct answer and send it!')
            return weather
        else:
            logg.error('The empty answer from openweathermap.org!')
            return None

    @staticmethod
    def get_weather_date(city="Москва", lang="ru", date = "") -> Optional[dict]:
        logg.info('Try to get current weather by name of the city, language and date...')
        logg.info('Initialize API for openweathermap.org...')
        API = '8397aa1b69899690124619bad12a067e'
        logg.info('Start work with openweathermap.org...')
        logg.info('Try to get data from the openweathermap.org...')
        data = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?q={city}&lang={lang}&units=metric&appid={API}').json()
        if data:
            logg.info('Processing a response from openweathermap.org...')
            finded = None
            print(data)
            for i in data['list']:
                if (i['dt_txt'][:10]).replace('-', '.') == date and i['dt_txt'][10:-3] ==' 12:00':
                    print(i['dt_txt'])#[:10])
                    finded = i
            data = finded
            weather = {
                'description': data['weather'][0]['main'],
                'text': data['weather'][0]['description'],
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'windSpeed': data['wind']['speed']}
            logg.info('I get a correct answer and send it!')
            return weather
        else:
            logg.error('The empty answer from openweathermap.org!')
            return None
