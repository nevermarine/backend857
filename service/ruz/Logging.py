import logging
from Test import TestCase
class LogModule:
    def setUp(self):
        logger = logging.getLogger("RuzLogger")
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("RuzLog.log")
        formatter = logging.Formatter('%(asctime)s %(name)s :: %(levelname)s : %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        t = TestCase()
        t.setUp()
