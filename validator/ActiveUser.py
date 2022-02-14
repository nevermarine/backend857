from service.PersonService import PersonService
from werkzeug.datastructures import FileStorage
from model.Singleton import Singleton
from service.ruz.ruz import Ruz
from typing import Optional


class ActiveUser(metaclass=Singleton):
    id = None
    first_name = None
    last_name = None
    patronymic = None
    face_data = None
    mail = None
    position = None

    # @classmethod
    # def __init__(cls, image):
    #     pass

    @classmethod
    def update(cls, image):
        if type(image) is FileStorage:
            user = PersonService.simpler_find_face(image)
        elif type(image) is bytes:
            user = PersonService.byte_find_face(image)
        else:
            user = None

        if user is not None:
            cls.id = user.face_id
            cls.first_name = user.first_name
            cls.last_name = user.last_name
            cls.patronymic = user.patronymic
            cls.face_data = user.face_data
            cls.mail = user.mail

    @classmethod
    def update_by_id(cls, i: int) -> Optional[str]:
        user = PersonService.get_person_by_id(i)
        if user is not None:
            cls.id = user.face_id
            cls.first_name = user.first_name
            cls.last_name = user.last_name
            cls.patronymic = user.patronymic
            cls.face_data = user.face_data
            cls.mail = user.mail
            cls.position = user.position
            return str(cls)
        return None

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def __str__(cls):
        if cls:
            # return f"{cls.last_name} {cls.first_name} {cls.patronymic}"
            return cls.last_name + ' ' + cls.first_name + ' ' + cls.patronymic
        else:
            return ''

    @classmethod
    def __bool__(cls):
        return cls.id is not None

    @classmethod
    def get_schedule(cls):
        return Ruz.get_schedule_by_names(
            cls.last_name, cls.first_name, cls.patronymic
        )


CurrentUser = ActiveUser()
