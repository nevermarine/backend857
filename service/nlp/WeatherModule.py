import re
from service.weather.Weather import Weather as weatherModule
from deeppavlov import configs, build_model

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
        answer = answer + 'температура воздуха ' + str(self.data['temp']) + ' градусов, ощущается как ' + str(
            self.data['feels_like']) + '. '
        answer = answer + 'Влажность ' + str(self.data['humidity']) + ' процентов' + '.'
        return answer

    def multiple_replace(self, request, replace_values):
        for i, j in replace_values.items():
            if request.find(i) != -1:
                request = request.replace(i, j)
                break
        return request

    def process(self, request):
        regex = r'(\d{4})'
        dates = {}
        match = re.search(regex, request, flags=re.IGNORECASE)
        if match != None:
            dates['year'] = match[0]
            request = request.replace(match[0], '')
        else: dates['year'] = '2022'
        items = ner_model([request])
        for i in range(len(items[1][0])):
            if 'B-DATE' in items[1][0][i]: dates['day'] = items[0][0][i]
            if 'I-DATE' in items[1][0][i]: dates['month'] = items[0][0][i]
            if 'B-GPE' in items[1][0][i]: dates['city'] = items[0][0][i]
        d = dates['year'] + '.' + self.multiple_replace(dates['month'], self.replace_months_forweather) + '.' + dates['day']
        return d, dates['city']


ner_model = build_model(configs.ner.ner_ontonotes_bert_mult_torch, download=True)