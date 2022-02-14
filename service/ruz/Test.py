import unittest
import logging
from RUZ import Ruz

class TestCase(unittest.TestCase):
    def setUp(self):
        self.logg = logging.getLogger("RuzLogger.TesterRuzLogger")
        self.logg.debug("Initialize TestCase")
        self.r = Ruz()
        self.test_start()

    def test_start(self):
        self.logg.info("Start testing module RUZ")
        self.test_system()
        self.test_empty_name_send()
        self.test_empty_time_send()
        self.test_wrong_send()
        self.test_wrong_time()
        self.logg.info('All test passed!')

    def test_system(self):
        self.logg.info("Checking the testing system ...")
        self.assertEqual(True, True)
        self.logg.info("The testing system has been verified!")

    def test_wrong_send(self):
        self.logg.info('Checking for incorrect data entry ...')
        a = self.r.get_schedule_by_full_name('рпрпрпр')
        self.assertIsNone(a)
        self.logg.info('No errors found!')

    def test_empty_name_send(self):
        self.logg.info('Checking for empty name entry ...')
        b = self.r.get_schedule_by_full_name('')
        self.assertIsNone(b)
        self.logg.info('No errors found!')

    def test_wrong_time(self):
        self.logg.info('Checking the incorrect date input ...')
        c = self.r.get_schedule_by_name_and_date('Кофанова Мария Александровна', '2021.01.10')
        self.assertIsNone(c)
        self.logg.info('No errors found!')

    def test_empty_time_send(self):
        self.logg.info('Checking for empty date entry ...')
        d = self.r.get_schedule_by_name_and_date('Кофанова Мария Александровна', '')
        self.assertIsNone(d)
        self.logg.info('No errors found!')

#TestCase.test_something()
