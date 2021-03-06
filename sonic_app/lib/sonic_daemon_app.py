import logging

import abc


class SonicDaemonApp:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_timeout = 5
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.fh = logging.FileHandler(self.log_path, "w")
        self.fh.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)

    @abc.abstractmethod
    def run(self):
        pass
