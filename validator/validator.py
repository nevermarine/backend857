import os
import imghdr
from config.config import UPLOAD_EXTENSIONS


class Validator:
    @staticmethod
    def is_text(s):
        return isinstance(s, str)

    @staticmethod
    def is_valid_filename(filename):
        file_ext = os.path.splitext(filename)[1]
        return filename != '' and file_ext in UPLOAD_EXTENSIONS

    @staticmethod
    def is_image(stream):
        header = stream.read(512)
        stream.seek(0)
        image_format = imghdr.what(None, header)
        if not image_format:
            return False
        return True

    @staticmethod
    def is_valid_person(person: dict) -> bool:
        for i in ('first_name', 'last_name', 'patronymic', 'face_data'):
            if i not in person:
                return False
        return True
