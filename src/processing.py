import sys
import numpy as np
import pandas as pd

from ahrs import Quaternion
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
        self.x = "SENSOR_X"
        self.y = "SENSOR_Y"
        self.z = "SENSOR_Z"

    def get_3axis(self):
        axes = {}
        
        for col in self.df.columns:
            for k, v in self.table.items():
                if col in v:
                    axes[k] = self.df[col].to_numpy()
                    break

        return axes

    def nx3_array(self):
        sensor_dict = self.get_3axis()
        return np.concatenate((sensor_dict[self.x].reshape(-1,1),
                                sensor_dict[self.y].reshape(-1,1), 
                                sensor_dict[self.z].reshape(-1,1)), axis=1)

    @staticmethod
    def moving_average(x, w, mode):
        return np.convolve(x, np.ones(w), mode) / w

    @staticmethod
    def get_rpy(orient):
        roll_list, pitch_list, yaw_list = [], [], []
        for i in range(orient.Q.shape[0]):
            q = Quaternion(orient.Q[i, :])
            roll, pitch, yaw = q.to_angles()
            roll_list.append(roll)
            pitch_list.append(pitch)
            yaw_list.append(yaw)

        return [np.rad2deg(np.array(roll_list)), np.rad2deg(np.array(pitch_list)), np.rad2deg(np.array(yaw_list))]


class Gyro(Sensor):

    table = {
        'GYRO_X': ['Gyroscope (x) [rad/s]'],
        'GYRO_Y': ['Gyroscope (y) [rad/s]'],
        'GYRO_Z': ['Gyroscope (z) [rad/s]']
    }
    
    def __init__(self, csv_path, sampl_hz):
        super().__init__(csv_path, sampl_hz)
        self.x = "GYRO_X"
        self.y = "GYRO_Y"
        self.z = "GYRO_Z"

    
class Accl(Sensor):

    table = {
        'ACCL_X': ['Accelerometer (x) [m/s2]', 'Accelerometer [m/s2]', 'Accelerometer (right/left) [m/s2]'],
        'ACCL_Y': ['Accelerometer (y) [m/s2]', 'Accelerometer (forward/back) [m/s2]'],
        'ACCL_Z': ['Accelerometer (z) [m/s2]', 'Accelerometer (up/down) [m/s2]']
    }
    
    def __init__(self, csv_path, sampl_hz):
        super().__init__(csv_path, sampl_hz)
        self.x = "ACCL_X"
        self.y = "ACCL_Y"
        self.z = "ACCL_Z"