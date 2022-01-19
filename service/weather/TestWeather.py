import unittest
from Weather import Weather
import logging


class TestCase(unittest.TestCase):
    def setUp(self):
        self.logg = logging.getLogger("WeatherLogger.TesterWeatherLogger")
        self.logg.debug("Initialize TestCase...")
        self.weather = Weather
        self.start_test()

    def start_test(self):
        self.logg.info("Start testing module Weather...")
        self.test_system()
        self.test_wrong_data_send()
        self.test_empty_data_send()
        self.logg.info('All test passed!')

    def test_system(self):
        self.logg.info("Checking the testing system ...")
        self.assertEqual(True, True)
        self.logg.info("The testing system has been verified!")

    def test_wrong_data_send(self):
        self.logg.info('Checking for incorrect data entry:')
        self.logg.info('Checking for incorrect city entry ...')
        a = self.weather.get_weather_date(city='Мffjif', lang='ru', date='2022.01.07')
        self.assertIsNone(a)
        self.logg.info('No errors found!')
        self.logg.info('Checking for incorrect language entry ...')
        b = self.weather.get_weather_date(city='Москва', lang='jko', date='2022.01.07')
        self.assertIsNone(b)
        self.logg.info('No errors found!')
        self.logg.info('Checking for incorrect date entry ...')
        c = self.weather.get_weather_date(city='Москва', lang='ru', date='2021.01.07')
        self.assertIsNone(c)
        self.logg.info('No errors found!')

    def test_empty_data_send(self):
        self.logg.info('Checking for empty data entry ...')
        self.logg.info('Checking for empty city entry ...')
        b = self.weather.get_weather_date(city='', lang='ru', date='2022.01.07')
        self.assertIsNone(b)
        self.logg.info('No errors found!')
        self.logg.info('Checking for empty language entry ...')
        c = self.weather.get_weather_date(city='Москва', lang='', date='2022.01.07')
        self.assertIsNone(c)
        self.logg.info('No errors found!')
        self.logg.info('Checking for empty date entry ...')
        d = self.weather.get_weather_date(city='Москва', lang='ru', date='')
        self.assertIsNone(d)
        self.logg.info('No errors found!')
        self.logg.info('Checking for another function empty city entry ...')
        e = self.weather.get_weather(city='', lang='ru')
        self.assertIsNone(d)
        self.logg.info('No errors found!')
        self.logg.info('Checking for another function empty language entry ...')
        f = self.weather.get_weather(city='Москва', lang='')
        self.assertIsNone(f)
        self.logg.info('No errors found!')
