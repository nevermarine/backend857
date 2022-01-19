import binascii

import face_recognition as fr
from model.Person import Person
from dao.PersonDao import PersonDao
import uuid
import base64
import numpy as np
from typing import Optional
# from werkzeug.utils import secure_filename

from config.config import IMAGEPATH
from validator.validator import Validator


class PersonService:
    @staticmethod
    def find_face(frame):
        rgb_frame = fr.load_image_file(frame)
        # face_locations = fr.face_locations(rgb_frame)
        # if not rgb_frame:
        #     return None
        try:
            face_locations = fr.face_locations(rgb_frame)
            face_encodings = fr.face_encodings(rgb_frame, face_locations)
        except IndexError:
            return None
        query = PersonDao.get_all_persons_as_select()
        for person in query.iterator():
            # matches = fr.compare_faces(all_face_encodings, face_encoding)
            if not isinstance(person.face_data, type(None)):

                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    match = fr.compare_faces([np.frombuffer(person.face_data)], face_encoding)
                    print(match)
                    if match[0]:
                        return person

        return None

    @classmethod
    def simpler_find_face(cls, werkzeug_img):
        path = IMAGEPATH + str(uuid.uuid4())
        werkzeug_img.save(path)
        return cls.find_face(path)

    @classmethod
    def byte_find_face(cls, byte_img):
        path = IMAGEPATH + str(uuid.uuid4())
        with open(path, 'wb') as f:
            f.write(byte_img)
        return cls.find_face(path)

    @classmethod
    def convert_image_to_face_data(cls, img):  # Image must be valid!
        filename = cls.save_byte_image(img)
        loaded_image = fr.load_image_file(IMAGEPATH + filename)
        face_array = fr.face_encodings(loaded_image)
        if len(face_array) == 0:
            return None
        face_enq = face_array[0]
        print(type(face_enq))
        return face_enq

    @staticmethod
    def save_byte_image(byte_image):
        filename = str(uuid.uuid4().hex)
        with open(IMAGEPATH + filename, "wb") as f:
            f.write(byte_image)
        return filename

    @staticmethod
    def convert_str_to_img(hex_text: str) -> bytes:
        return base64.b64decode(hex_text)

    @classmethod
    def create_face(cls, person: dict) -> bool:
        try:
            face_embedding = cls.convert_image_to_face_data(
                cls.convert_str_to_img(person['face_data'])
            )
        except binascii.Error:
            return False
        if face_embedding is None:
            return False
        else:
            PersonDao.create_person(person['first_name'],
                                    person['last_name'],
                                    person['patronymic'],
                                    face_embedding)
            return True

    @staticmethod
    def delete_person_by_id(identity: int) -> bool:
        return PersonDao.delete_person_by_id(identity)

    @staticmethod
    def get_person_by_id(identity: int) -> Optional[Person]:
        return PersonDao.get_person_by_id(identity)

