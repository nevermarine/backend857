from model.Person import Person, database
from typing import Union, Optional
from peewee import *
import numpy as np


class PersonDao:
    # CREATE
    @staticmethod
    def create_person_by_model(person):
        person.save()

    @staticmethod
    def create_person(first_name=None,
                      last_name=None,
                      patronymic=None,
                      face_data=None,
                      position=None,
                      mail=None,
                      filename=None) \
            -> Optional[Person]:
        person = Person(position=position,
                        last_name=last_name,
                        first_name=first_name,
                        patronymic=patronymic,
                        face_data=face_data,
                        mail=mail,
                        filename=filename)
        person.save()
        return person

    # READ
    @staticmethod
    def get_person_by_id(identity: int) -> Optional[Person]:
        try:
            person = Person.get_by_id(identity)
            return person
        except DoesNotExist:
            return None

    @staticmethod
    def get_person_by_lastname(lastname: str) -> Optional[list]:
        try:
            person_list = Person.select().where(Person.last_name == lastname).get()
            if isinstance(person_list, list):
                return person_list
            else:
                return [person_list]
        except DoesNotExist:
            return None

    @staticmethod
    def get_person_by_fullname(fullname: str) -> Optional[list]:
        try:
            lastname, firstname, patronymic = fullname.split(' ')
            person_list = Person.select().where(Person.last_name == lastname,
                                                Person.first_name == firstname,
                                                Person.patronymic == patronymic).get()
            if not isinstance(person_list, list):
                person_list = [person_list]
            return person_list
        except DoesNotExist:
            return None

    @staticmethod
    def get_all_persons_as_select():  # -> Optional[ModelSelect]
        return Person.select()

    @staticmethod
    def get_all_person_as_cursor():
        query = Person.select()
        return database.execute(query)

    # @staticmethod
    # def get_all_persons_as_dict() -> dict:
    # 	return Person.select().dicts()

    # UPDATE
    # @staticmethod
    # def update_person_face_by_id(identity: int, **params):
    #     try:
    #         person = Person.get_by_id(identity)

    # DELETE
    @staticmethod
    def delete_person_by_id(i: int) -> bool:
        try:
            person = Person.get(Person.face_id == i)
            person.delete_instance()
            return True
        except DoesNotExist:
            return False

