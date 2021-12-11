import os
import sys
import ahrs
import numpy as np
import pandas as pd

from abc import ABC, abstractmethod
from src.utils import Logger, Utils


class Sensor(ABC):

    table = {}

    def __init__(self, csv_path, sampl_hz):
        self.sampl_hz = sampl_hz
        
        try:
            self.csv_path = Utils.validateString(csv_path)
        except FileNotFoundError as fnf:
            Logger.logger.critical(fnf)
            sys.exit(-1)

        self.df = pd.read_csv(self.csv_path)

    def get_3axis(self):
        axes = {}
        
        for col in self.df.columns:
            for k, v in self.table.items():
                if col in v:
                    axes[k] = self.df[col].to_numpy()
                    break

        return axes

    def nx3_array(self, x, y, z):
        sensor_dict = self.get_3axis()
        return np.concatenate((sensor_dict[x].reshape(-1,1),
                                sensor_dict[y].reshape(-1,1), 
                                sensor_dict[z].reshape(-1,1)), axis=1)


class Gyro(Sensor):

    table = {
        'GYRO_X': ['Gyroscope (x) [rad/s]'],
        'GYRO_Y': ['Gyroscope (y) [rad/s]'],
        'GYRO_Z': ['Gyroscope (z) [rad/s]']
    }
    
    def __init__(self, csv_path, sampl_hz):
        super().__init__(csv_path, sampl_hz)

    
class Accl(Sensor):

    table = {
        'ACCL_X': ['Accelerometer (x) [m/s2]', 'Accelerometer [m/s2]', 'Accelerometer (right/left) [m/s2]'],
        'ACCL_Y': ['Accelerometer (y) [m/s2]', 'Accelerometer (forward/back) [m/s2]'],
        'ACCL_Z': ['Accelerometer (z) [m/s2]', 'Accelerometer (up/down) [m/s2]']
    }
    
    def __init__(self, csv_path, sampl_hz):
        super().__init__(csv_path, sampl_hz)