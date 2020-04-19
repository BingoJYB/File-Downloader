import logging
import os

from libs.defaults import ROOT_DIR


class Logger(object):
    def __init__(self, name, **kwargs):
        level = kwargs.get('level', logging.ERROR)
        log_filename = kwargs.get(
            'log_filename', os.path.join(ROOT_DIR, 'app.log'))
        log_formatter = kwargs.get(
            'log_formatter', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self._logger = logging.getLogger(name)
        c_format = logging.Formatter(log_formatter)

        c_handler = logging.FileHandler(log_filename)
        c_handler.setFormatter(c_format)

        self.logger.setLevel(level)
        self.logger.addHandler(c_handler)

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, logger):
        self._logger = logger
