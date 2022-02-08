import random
import nltk
import json
from RuzModule import RUZ
from WeatherModule import Weather


class VoiceAssistant:
    def __init__(self, question):
        # self.model = build_model(configs.classifiers.paraphraser_rubert, download=True)
        self.flag = True
        self.quest = question

    def main_words(self, speech):
        tokenizer = nltk.tokenize.RegexpTokenizer('\w+|\$[\d\.]+|\S+')
        word_list = tokenizer.tokenize(speech)
        nltk_words = list(nltk.corpus.stopwords.words('russian'))
        output = ''
        for w in word_list:
            if not w in nltk_words:
                output = output + w + ' '
        return output

    def start(self):
        ans = self.answer(self.quest)
        return ans


    def same(self, one, two):  # сократить 100
        k = self.model([one], [two])
        return k[0]

    def speech_writer(self):
        '''
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as audio_file:
            r.adjust_for_ambient_noise(audio_file)
            print("говорите")
            audio = r.listen(audio_file)
            try:
                input_text = r.recognize_google(audio,  language="ru")

            except:
                input_text = ''
        '''
        input_text = input('Человек: ')
        return input_text.lower()

    def answer(self, question):
        f = 'C:/Users/' + 'Maria Kofanova'+'/PycharmProjects/VAParts/talk_template.json'
        with open(f, 'r', encoding='utf-8') as f:
            answers = json.load(f)
        if question == "замолчи" or question == "отстань" or question == "стоп":
            self.flag = False
            return 'Хорошо. Больше не мешаю'
        for i in range(len(answers)):
            for m in range(len(answers[i]['action'])):
                if question == answers[i]['action'][m]:
                    j = random.randint(0, len(answers[i]['customAnswers']) - 1)
                    if answers[i]['customAnswers'][j] == 'open_RUZ':
                        ruz = RUZ(question)
                        schedule = ruz.read_data()
                        if schedule:
                            return schedule
                    elif answers[i]['customAnswers'][j] == 'open_Weather':
                        w = Weather(question)
                        description = w.read_data()
                        if description:
                            return description
                    elif answers[i]['customAnswers'][j] == 'pass':
                        return ''
                    else:
                        return answers[i]['customAnswers'][j]
        question = ''.join(self.main_words(question))
        for i in range(len(answers)):
            for m in range(len(answers[i]['action'])):
                if question == answers[i]['action'][m]:
                    j = random.randint(0, len(answers[i]['customAnswers']) - 1)
                    if answers[i]['customAnswers'][j] == 'open_RUZ':
                        ruz = RUZ(question)
                        schedule = ruz.read_data()
                        if schedule:
                            return schedule
                    elif answers[i]['customAnswers'][j] == 'open_Weather':
                        w = Weather(question)
                        description = w.read_data()
                        if description:
                            return description
                    elif answers[i]['customAnswers'][j] == 'pass':
                        return ''
                    else:
                        return answers[i]['customAnswers'][j]
        return 'Мне аж интересно стало что вы имеете в виду'

    def answer_NEW(self, question):
        with open('C:/Users/Maria Kofanova/PycharmProjects/VAParts/talk_template.json', 'r') as f:
            answers = json.load(f)
        for i in answers:
            if self.same(question, i['action']):
                if i['customAnswers'][0] == 'open_RUZ':
                    ruz = RUZ(question)
                    schedule = ruz.read_data()
                    if schedule:
                        return schedule
                elif i['customAnswers'][0] == 'openWeather':
                    w = Weather(question)
                    description = w.read_data()
                    if description:
                        return description
                elif i['customAnswers'][0] == 'close':
                    self.flag = False
                    return 'Больше не мешаю'
                else:
                    j = random.randint(0, len(i['customAnswers']) - 1)
                    return i['customAnswers'][j]
        return 'мне аж интересно стало что вы имеете в виду'

    def voice_sintes(self, answer):
        '''tts = pyttsx3.init()
        tts.setProperty('voice', 'ru')  # Наш голос по умолчанию
        tts.setProperty('rate', 190)    # Скорость в % (может быть > 100)
        tts.setProperty('volume', 0.8)  # Громкость (значение от 0 до 1)
        tts.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0')
        tts.say(answer)
        tts.runAndWait()'''
        print('Помощник: ' + answer)

