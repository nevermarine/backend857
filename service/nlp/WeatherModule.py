import csv
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re
from service.weather.Weather import Weather as weatherModule
from pathlib import Path


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
        self.data = weatherModule.get_weather_date(self.city, 'ru', self.date)

    def read_data(self):
        if self.date == None:
          return None
        self.get_data()
        answer = 'На улице ' + self.data['text'] + '. '
        answer = answer + 'температура воздуха ' + str(self.data['temp']) + ' градусов, ощущается как ' + str(self.data['feels_like']) + '. '
        answer = answer + 'Влажность ' + str(self.data['humidity']) + ' процентов' + '.'
        return answer

    def parse_date_forweather(self, day_str, month_str, year_str):
        day = int(day_str)
        if month_str not in self.replace_months_forweather:
          raise Exception('Invalid month')
        month = self.replace_months_forweather[month_str]
        year = int(year_str)
        return date(year, month, day)

    def cities(self):
        cities = []
        with open(Path(__file__).parent.resolve() /'city.csv', 'r', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                cities.append(row[0].split(';')[3][1:-2])
        return cities

    def process(self, request):
        regex = r'какая погода будет в городе (.+?) (?:(\d{1,2}) (.+) (\d{4})|(завтра|послезавтра|сегодня))'
        match = re.search(regex, request, flags=re.IGNORECASE)
        if match is None:
            city = self.cities()
            rcity = None
            for i in city:
                if i in request:
                    rcity = i
                    break
            if rcity == None:
                rcity = 'Москва'
            if 'завтра' in request:
                return 'завтра', rcity
            if 'послезавтра' in request:
                return 'послезавтра', rcity
            return 'сегодня', rcity
        if match.groups()[4] is not None:
            text = match.groups()[4]
            if text == 'сегодня':
                parsed_date = str(date.today()).replace('-', '.')
            elif text == 'завтра':
                parsed_date = str(date.today() + relativedelta(days=1)).replace('-', '.')
            elif text == 'послезавтра':
                parsed_date = str(date.today() + relativedelta(days=2)).replace('-', '.')
            else:
                raise Exception()
        else:
            parsed_date = str(self.parse_date_forweather(match[2], match[3], match[4])).replace('-', '.')
        city = match[1]
        return parsed_date, city
