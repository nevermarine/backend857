import datetime
import logging
from typing import Optional

import requests

import ruz

logg = logging.getLogger("RuzLogger.WorkLogger")
logg.debug("Initialize Ruz")


class Ruz:
    @classmethod
    def get_schedule_by_names(cls, last_name, first_name, patronymic: str) -> Optional[dict]:
        fio = " ".join(map(lambda s: s.strip().title(), [last_name, first_name, patronymic]))
        return cls.get_schedule_by_full_name(fio)

    def check_mail(mail, FIO):  # не доработана!!!
        schedule = ruz.person_lessons("mymail@edu.hse.ru")
        print(schedule)
        fields = ['auditorium', 'auditoriumAmount', 'beginLesson', 'building', 'dayOfWeekString', 'discipline',
                  'endLesson', 'group', 'lecturer', 'url1']
        for i in schedule:
            for key, value in list(i.items()):
                if key not in fields:
                    del i[key]
        print(schedule)
        return True

    def get_mail(f: str, i: str, o: str, type_: str):
        ch = {'Й': 'y', 'Ц': 'ts', 'У': 'u', 'К': 'k', 'Е': 'e', 'Н': 'n', 'Г': 'g', 'Ш': 'sh', 'Щ': 'sch', 'З': 'z',
              'Х': 'h', 'Ф': 'f', 'Ы': 'y', 'В': 'v', 'А': 'a', 'П': 'p', 'Р': 'r', 'О': 'o', 'Л': 'l', 'Д': 'd',
              'ь': '', 'ъ': '', 'Ж': 'zh', 'Э': 'e', 'Я': 'ya', 'Ч': 'ch', 'С': 's', 'М': 'm', 'И': 'i', 'Т': 't',
              'Б': 'b'}
        mail = ''
        mail = mail + ch[i[0]]
        mail = mail + ch[o[0]]
        for i in f:
            mail = mail + ch[i.upper()]
        if type_ == 'student':
            mail = mail + '.edu.hse.ru'
        else:
            mail = mail + '.hse.ru'
        return mail

    @staticmethod
    def get_schedule_by_name_and_date(fio: str, date: str, type_='student') -> Optional[dict]:
        logg.info('Try to get schedule by name and date...')
        logg.info('Initialize the type of person...')
        # type_ = 'student'
        if type_ == 'teacher':
            type_ = 'lecturer'
        logg.info('Start work with date...')
        date_start = date
        if date == '':
            logg.error('The date is empty string!')
            return None
        if fio == '':
            logg.error('The name is empty string!')
            return None
        date_ = datetime.datetime.strptime(date, '%Y.%m.%d')
        date_end = str(date_.date() + datetime.timedelta(days=7)).replace('-', '.')
        if datetime.datetime.now() > datetime.datetime.strptime(date_end, '%Y.%m.%d'):
            logg.error('The date has already passed!')
            return None
        logg.info('Date is correct!')
        logg.info('Start work with ruz.hse.ru...')
        r = requests.get('https://ruz.hse.ru/api/search?term=' + fio + '&type=' + type_).json()
        if not r:
            logg.error('The empty answer from ruz!')
            return None
        logg.info('Get id from ruz! Continue working...')
        url = 'https://ruz.hse.ru/api/schedule/' + type_ + '/' + r[0][
            "id"] + '?start=' + date_start + '&finish=' + date_end + '&lng=1'
        logg.info('Try to get schedule from ruz...')
        syllabus = requests.get(url).json()
        to_json = []
        fields = ['auditorium', 'auditoriumAmount', 'beginLesson', 'building', 'dayOfWeekString', 'discipline',
                  'endLesson', 'group', 'lecturer', 'url1']
        logg.info('Processing a response from ruz.hse.ru...')
        if syllabus:
            for i in range(len(syllabus)):
                date_string = syllabus[i]['beginLesson']
                date_formatter = "%H:%M"
                if datetime.datetime.strptime(date_string, date_formatter).time() >= date_.time():
                    to_json.append(syllabus[i])
            for i in syllabus:
                for key, value in list(i.items()):
                    if key not in fields:
                        del i[key]
            logg.info('I get a correct answer and send it!')
            return syllabus
        else:
            logg.error('The empty answer from ruz!')
            return None

    @staticmethod
    def get_schedule_by_full_name(fio: str) -> Optional[dict]:
        logg.info('Try to get schedule by name...')
        if fio == '':
            logg.error('Empty name!')
            return None
        logg.info('Initialize the type of person...')
        type_ = 'student'
        logg.info('Start work with date...')
        date_ = datetime.datetime.now()
        date_str = str(date_).replace(' ', 'T')
        date_start = str(date_.date()).replace('-', '.')
        date_end = str(date_.date() + datetime.timedelta(days=1)).replace('-', '.')
        # date_start  = '2022.01.10'
        # date_end = '2022.01.17'
        logg.info('Start work with ruz.hse.ru...')
        r = requests.get('https://ruz.hse.ru/api/search?term=' + fio + '&type=' + type_).json()
        if not r:
            logg.error('The empty answer from ruz!')
            return None
        logg.info('Get id from ruz! Continue working...')
        url = 'https://ruz.hse.ru/api/schedule/student/' + r[0][
            "id"] + '?start=' + date_start + '&finish=' + date_end + '&lng=1'
        logg.info('Try to get schedule from ruz...')
        syllabus = requests.get(url).json()
        to_json = []
        fields = ['auditorium', 'auditoriumAmount', 'beginLesson', 'building', 'dayOfWeekString', 'discipline',
                  'endLesson', 'group', 'lecturer', 'url1']
        logg.info('Processing a response from ruz.hse.ru...')
        if syllabus:
            for i in range(len(syllabus)):
                date_string = syllabus[i]['beginLesson']
                date_formatter = "%H:%M"
                if datetime.datetime.strptime(date_string, date_formatter).time() >= date_.time():
                    to_json.append(syllabus[i])
            for i in syllabus:
                for key, value in list(i.items()):
                    if key not in fields:
                        del i[key]
            logg.info('I get a correct answer and send it!')
            return syllabus
        else:
            logg.error('The empty answer from ruz!')
            return None
