import os
import sys
import json

from src.utils import Utils, Logger

class Parser:

    def __init__(self, json_path):
        self.args = {}
        self.json_path = json_path

    def parse_vars(self):
        f = open(self.json_path, "r")
        data = json.load(f)

        try:
            Utils.validateString(data['accl_path'])
            Utils.validateString(data['gyro_path'])
            Utils.validateString(data['magn_path'])
        except FileNotFoundError as fnf:
            Logger.logger.critical(fnf)
            sys.exit(-1)
        except ValueError as ve:
            Logger.logger.warning(ve)

        self.args['accl_path'] = data['accl_path']
        self.args['gyro_path'] = data['gyro_path']
        self.args['magn_path'] = data['magn_path']
        self.args['sampl_hz'] = data['sampl_hz']

        f.close()

        return self.args