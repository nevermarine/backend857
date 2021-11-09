import requests
import datetime
from typing import Optional
import json


class Ruz:
    # def __init__(self):
    #     pass
    @classmethod
    def get_schedule_by_names(cls, last_name, first_name, patronymic: str) -> Optional[dict]:
        fio = " ".join(map(lambda s: s.strip().title(), [last_name, first_name, patronymic]))
        return cls.get_schedule_by_full_name(fio)

    @staticmethod
    def get_schedule_by_full_name(fio: str) -> Optional[dict]:
        type_ = 'student'
        date_ = datetime.datetime.now()
        date_str = str(date_).replace(' ', 'T')
        date_start = str(date_.date()).replace('-', '.')
        date_end = str(date_.date() + datetime.timedelta(days=7)).replace('-', '.')
        # date_start  = '2021.08.30'
        # date_end = '2021.09.03'
        r = requests.get('https://ruz.hse.ru/api/search?term=' + fio + '&type=' + type_).json()
        if not r:
            return None
        url = 'https://ruz.hse.ru/api/schedule/student/' + r[0][
            "id"] + '?start=' + date_start + '&finish=' + date_end + '&lng=1'
        syllabus = requests.get(url).json()
        schedule = None
        to_json = []
        if syllabus:
            for i in range(len(syllabus)):
                date_string = syllabus[i]['beginLesson']
                date_formatter = "%H:%M"
                if datetime.datetime.strptime(date_string, date_formatter).time() >= date_.time():
                    to_json.append(syllabus[i])
            return syllabus
        else:
            return None
        # with open('ruz_templates.json', 'w') as f:
        #     json.dump(to_json, f)


