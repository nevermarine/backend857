from service.PersonService import PersonService
from service.ruz import Ruz
from service.weather import Weather
from werkzeug.datastructures import FileStorage


class ActiveUser:
    def __init__(self, image):
        print(type(image))
        print(type(image) is FileStorage)
        if type(image) is FileStorage:
            user = PersonService.simpler_find_face(image)
        elif type(image) is bytes:
            user = PersonService.byte_find_face(image)
        else:
            print('fucked up types')
            user = None
        if user is None:
            print('fucked up database')
            self.id = None
        else:
            self.id = user.face_id
            self.first_name = user.first_name
            self.last_name = user.last_name
            self.patronymic = user.patronymic
            self.face_data = user.face_data

    def get_ruz(self):
        return Ruz.get_schedule_by_names(
            self.last_name, self.first_name, self.patronymic
        )

    @staticmethod
    def get_weather():
        return Weather.get_weather()
