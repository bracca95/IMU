import ahrs
import matplotlib.pyplot as plt

from src.parser import Parser
from src.processing import Gyro, Accl

if __name__=="__main__":
    parser = Parser("config/config.json")
    args = parser.parse_vars()

    sensor_accl = Accl(args['accl_path'], args['sampl_hz'])
    sensor_gyro = Gyro(args['gyro_path'], args['sampl_hz'])
    
    accl_arr = sensor_accl.nx3_array('ACCL_X', 'ACCL_Y', 'ACCL_Z')
    gyro_arr = sensor_gyro.nx3_array('GYRO_X', 'GYRO_Y', 'GYRO_Z')

    filter = ahrs.filters.madgwick.Madgwick(gyro_arr, accl_arr, frequency=args['sampl_hz'])

    plt.plot(range(len(filter.Q[:, 0])), filter.Q[:, 0])
    plt.plot(range(len(filter.Q[:, 0])), filter.Q[:, 1])
    plt.plot(range(len(filter.Q[:, 0])), filter.Q[:, 2])
    plt.plot(range(len(filter.Q[:, 0])), filter.Q[:, 3])
    plt.show()

    print(args)