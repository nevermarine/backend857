from RuzModule import RUZ
from WeatherModule import Weather
import json
from Model import *
import random
class VoiceAssistant:

    def understanding(self):
        return predict(self.speech)

    def start(self, quest):
        self.speech = quest
        self.id = self.understanding()
        if self.id in [0, 2, 3, 9]:
            return eval('self.' + answers[self.id]['intent'] + '()')
        else:
            return eval('self.standart_answer()')

    def personal_question(self):
        if 'хобби' in self.speech or 'заняти' in self.speech or 'увлечени' in self.speech or 'план' in self.speech:
            return answers[self.id]['customAnswers'][3]
        if 'счастлив' in self.speech or 'доволен' in self.speech:
            j = random.randint(0, len(answers[self.id]['customAnswers']) - 2)
            return answers[self.id]['customAnswers'][j]
        j = random.randint(0, len(answers[self.id]['customAnswers']) - 1)
        return answers[self.id]['customAnswers'][j]

    def greeting(self):
        if 'добр' in self.speech:
            return 'ну хоть у кого то'
        else:
            j = random.randint(0, len(answers[self.id]['customAnswers']) - 1)
            return answers[self.id]['customAnswers'][j]

    def standart_answer(self):
        j = random.randint(0, len(answers[self.id]['customAnswers']) - 1)
        return answers[self.id]['customAnswers'][j]

    def schedule(self):
        r = RUZ(self.speech)
        answer_ruz = r.read_data()
        return answer_ruz

    def weather(self):
        w = Weather(self.speech)
        answer_weather = w.read_data()
        return answer_weather

with open('talkTemplate.json', 'r', encoding='utf-8') as f:
    answers = json.load(f)