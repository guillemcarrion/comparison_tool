import logging


class CustomFormatter(logging.Formatter):
    FORMATS = {logging.DEBUG: "%(asctime) - DBG - %(module)s: %(lineno)d %(message)s",
               logging.ERROR: "%(asctime) - ERROR - %(module)s:%(lineno)d %(message)s",
               logging.INFO: "%(asctime) - INFO - %(message)s",
               'DEFAULT': "%(levelname)s: %(message)s"}

    def format(self, record):
        self._fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        return logging.Formatter.format(self, record)


def get_custom_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger

