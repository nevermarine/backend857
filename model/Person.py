from peewee import *
from config.config import DATABASE_PATH


database = SqliteDatabase(DATABASE_PATH)


class BaseModel(Model):
    class Meta:
        database = database


class Person(BaseModel):
    face_data = BlobField(null=True)
    face_id = AutoField()
    first_name = TextField(null=True)
    last_name = TextField(null=True)
    patronymic = TextField(null=True)
    mail = TextField(null=True)
    position = TextField(null=True)
    filename = TextField(null=True)

    class Meta:
        table_name = 'faces'


# Person.create_table(safe=True)
