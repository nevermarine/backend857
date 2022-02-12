import logging


class LogModule:
    def setUp(self):
        logger = logging.getLogger("LoggerController")
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("controller.log")
        formatter = logging.Formatter('%(asctime)s %(name)s :: %(levelname)s : %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
