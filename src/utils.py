import os
import re
import sys
import logging

class Utils:

    @staticmethod
    def str2bool(s):
        return s.lower() in ("true", "yes", "y")

    @staticmethod
    def str2lst(s):
        return re.findall(r"[\w']+", s)

    @staticmethod
    def validateString(s):

        if not s:
            raise ValueError(f"Empty path.")
        else:
            s = os.path.abspath(os.path.realpath(s))
            if not os.path.exists(s):
                raise FileNotFoundError(f"Path {s} does not exist. Quitting...")

        return s

    @staticmethod
    def checkInstance(val, type):

        if isinstance(val, type):
            return val
        else:
            raise ValueError(f"Value must be {str(type)}. Quitting...")

    @staticmethod
    def checkBool(val):
        return val if isinstance(val, bool) else Utils.str2bool(val)


def singleton(cls):
    # alternative https://code.activestate.com/recipes/578103-singleton-parameter-based/
    instances = {}

    def get_instances():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instances()

@singleton
class Logger:

    def __init__(self, formatter='%(asctime)-2s # %(levelname)-2s # %(message)s'):
        log_file_path = os.path.join(os.getcwd(), "log.log")

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(formatter)

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)

        out_handler = logging.StreamHandler(sys.stdout)
        out_handler.setLevel(logging.INFO)
        out_handler.addFilter(lambda record: record.levelno == logging.INFO)
        out_handler.setFormatter(formatter)

        err_handler = logging.StreamHandler(sys.stderr)
        err_handler.setLevel(logging.WARNING)
        err_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(out_handler)
        self.logger.addHandler(err_handler)


