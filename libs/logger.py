import logging


class Logger(object):
    def __init__(self, name, **kwargs):
        level = kwargs.get('level', logging.ERROR)
        log_filename = kwargs.get('log_filename', 'app.log')
        log_formatter = kwargs.get(
            'log_formatter', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.logger = logging.getLogger(name)
        c_format = logging.Formatter(log_formatter)

        c_handler = logging.FileHandler(log_filename)
        c_handler.setFormatter(c_format)

        self.logger.setLevel(level)
        self.logger.addHandler(c_handler)

    @property
    def logger(self):
        return self.logger
