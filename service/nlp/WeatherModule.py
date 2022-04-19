import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from service.weather.Weather import Weather as weatherModule
import json

class Weather:
    def __init__(self, quest):
        self.date, self.city = self.process(quest)
        self.replace_months_forweather = {
          "января": 1,
          "февраля": 2,
          "марта": 3,
          "апреля": 4,
          "мая": 5,
          "июня": 6,
          "июля": 7,
          "августа": 8,
          "сентября": 9,
          "октября": 10,
          "ноября": 11,
          "декабря": 12
        }

    def get_data(self):
        print(self.city, self.date)
        self.data = weatherModule.get_weather_date(self.city, 'ru', self.date)

    def read_data(self):
        if self.date == None:
            return 'я не понял вас'
        self.get_data()
        answer = 'На улице ' + self.data['text'] + '. '
        answer = answer + 'температура воздуха ' + str(self.data['temp']) + ' градусов, ощущается как ' + str(
            self.data['feels_like']) + '. '
        answer = answer + 'Влажность ' + str(self.data['humidity']) + ' процентов' + '.'
        return answer

    def parse_date_forweather(self, day_str, month_str, year_str):
        day = int(day_str)
        if month_str not in self.replace_months_forweather:
          raise Exception('Invalid month')
        month = self.replace_months_forweather[month_str]
        year = int(year_str)
        return date(year, month, day)

    def process(self, request):
        regex = r'в (.+)'
        reg_date = '(?:(\d{1,2}) (.+) (\d{4}))'
        reg_day = r'(завтра|послезавтра|сегодня)'
        match_day = re.search(reg_day, request, flags=re.IGNORECASE)
        match_city = re.search(regex, request, flags=re.IGNORECASE)
        match_date = re.search(reg_date, request, flags=re.IGNORECASE)
        if match_day is not None:
            text = match_day[0]
            print(text)
            if text == 'сегодня':
                parsed_date = str(date.today()).replace('-', '.')
            elif text == 'завтра':
                parsed_date = str(date.today() + relativedelta(days=1)).replace('-', '.')
            elif text == 'послезавтра':
                parsed_date = str(date.today() + relativedelta(days=2)).replace('-', '.')
            else:
                raise Exception
        else:
            if match_date is not None:
                match = match_date
                parsed_date = str(self.parse_date_forweather(match[0], match[1], match[2])).replace('-', '.')
            else:
                parsed_date = str(date.today()).replace('-', '.')
        if match_city is not None:
            city = match_city[0][2:]
            with open('/app/service/nlp/cities.json', 'r') as f:
                cities = json.load(f)
            city = [i['name'] for i in cities['city'] if city.lower()[:-1] in i['name'].lower()]
            if len(city)>0:
                city = city[0]
            else:
                city = 'москва'
        else:
            city = 'москва'

        return parsed_date, city
