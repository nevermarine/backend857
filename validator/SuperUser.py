from ActiveUser import ActiveUser
from service.ruz import Ruz
from service.weather import Weather


class SuperUser(ActiveUser):
    @classmethod
    def get_ruz(cls):
        return Ruz.get_schedule_by_names(
            cls.last_name, cls.first_name, cls.patronymic
        )

    @staticmethod
    def get_weather():
        return Weather.get_weather()


CurrentSuperUser = SuperUser()
CurrentSuperUser.id = 4
