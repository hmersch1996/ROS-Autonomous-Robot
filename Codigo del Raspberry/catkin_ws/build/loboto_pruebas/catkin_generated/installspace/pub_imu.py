#!/usr/bin/env python3
import time
import board
import busio
import adafruit_lsm9ds1
#import <node pkg="loboto_pruebas" type="sensoresfull.py" name="lectura_sensores2" /> as GPIO 
import numpy as np
import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import String

# I2C connection:
# i2c = busio.I2C(board.SCL_1, board.SDA_1)
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

def read_data():
    pub = rospy.Publisher('datos_imu', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    while not rospy.is_shutdown():
        # Read acceleration, magnetometer, gyroscope, temperature.
        ax, ay, az = sensor.acceleration
        mx, my, mz = sensor.magnetic
        gx, gy, gz = sensor.gyro
        # temp = sensor.temperature
        
        # Anhadimos los valores de interes a una lista
        med_imu=[ax, ay, az, mx, my, mz, gx, gy, gz]

        # Redondeamos los valores leidos
        med_imu_r=[round(x,2) for x in med_imu]

        mensaje=str(med_imu_r)

        pub.publish(mensaje)
        rate.sleep()

        
if __name__ == '__main__':
    try:
        read_data()
    except rospy.ROSInterruptException:
        pass