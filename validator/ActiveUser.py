from service.PersonService import PersonService
from service.ruz import Ruz
from service.weather import Weather
from werkzeug.datastructures import FileStorage


class ActiveUser:
    id = None
    first_name = None
    last_name = None
    patronymic = None
    face_data = None

    @classmethod
    def __init__(cls, image):
        if type(image) is FileStorage:
            user = PersonService.simpler_find_face(image)
        elif type(image) is bytes:
            user = PersonService.byte_find_face(image)
        else:
            user = None

        #     cls.id = None
        # else:
        if user is not None:
            cls.id = user.face_id
            cls.first_name = user.first_name
            cls.last_name = user.last_name
            cls.patronymic = user.patronymic
            cls.face_data = user.face_data

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def __str__(cls):
        # return self.last_name + ' ' + self.first_name + ' ' + self.patronymic
        if cls:
            return f"{cls.last_name} {cls.first_name} {cls.patronymic}"
        else:
            return ''

    @classmethod
    def __bool__(cls):
        return cls.id is not None

    @classmethod
    def get_ruz(cls):
        return Ruz.get_schedule_by_names(
            cls.last_name, cls.first_name, cls.patronymic
        )

    @staticmethod
    def get_weather():
        return Weather.get_weather()


# CurrentUser = ActiveUser(None)
