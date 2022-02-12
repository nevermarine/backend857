# from sqlalchemy import Column, Text, Integer
from peewee import *
from config.config import DATABASE_PATH

# class Person:
# 	def __init__(self, first_name, last_name, patronymic):
# 		self.first_name = first_name
# 		self.last_name = last_name
# 		self.patronymic = patronymic
#
# 	id = Column('id', Integer, primary_key=True, nullable=False)
# 	first_name = Column('first_name', Text)
# 	last_name = Column('last_name', Text)
# 	patronymic = Column('patronymic', Text)
#db = SqliteDatabase('dao/people.db')


# class Person(Model):
#     id = IntegerField()
#     first_name = CharField()
#     last_name = CharField()
#     patronymic = CharField()


# 	static methods
#     def get_full_name(self):
#         return ' '.join([self.last_name, self.first_name, self.patronymic])

database = SqliteDatabase(DATABASE_PATH)


# class UnknownField(object):
#     def __init__(self, *_, **__): pass

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

    class Meta:
        table_name = 'faces'

