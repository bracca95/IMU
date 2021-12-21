import matplotlib.pyplot as plt

from scipy.signal import savgol_filter
from ahrs.filters.madgwick import Madgwick

from src.parser import Parser
from src.processing import Sensor, Gyro, Accl
from src.utils import Plotter


if __name__=="__main__":
    parser = Parser("config/config.json")
    args = parser.parse_vars()

    sensor_accl = Accl(args['accl_path'], args['sampl_hz'])
    sensor_gyro = Gyro(args['gyro_path'], args['sampl_hz'])

    orient = Madgwick(sensor_gyro.nx3_array(), sensor_accl.nx3_array(), frequency=args['sampl_hz'])
    orient_filt = [savgol_filter(orient.Q[:, i], 301, 3) for i in range(4)]
    rpy = Sensor.get_rpy(orient)
    rpy_filt = [savgol_filter(angle, 301, 3) for angle in rpy]

    Plotter.plot(orient.Q[:, 0], orient.Q[:, 1], orient.Q[:, 2], orient.Q[:, 3], a='qw', b='qx', c='qy', d='qz', fps=args['sampl_hz'])
    Plotter.plot(rpy[0], rpy[1], rpy[2], a='roll', b='pitch', c='yaw', fps=args['sampl_hz'])
