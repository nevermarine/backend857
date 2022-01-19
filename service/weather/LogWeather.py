import logging
from TestWeather import TestCase
class LogModule:
    def setUp(self):
        logger = logging.getLogger("WeatherLogger")
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("WeatherLog.log")
        formatter = logging.Formatter('%(asctime)s %(name)s :: %(levelname)s : %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        t = TestCase()
        t.setUp()
