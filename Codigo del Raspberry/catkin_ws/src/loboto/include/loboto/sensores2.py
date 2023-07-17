#!/usr/bin/env python3
import rospy
import random
from std_msgs.msg import String
# LIBRERIAS PARA LOS PERIFERICOS
#PARA LOS ULTRASONICOS
import RPi.GPIO as GPIO 
import time
from time import sleep
import numpy as np
GPIO.setwarnings(False)

"""Definiciones para el acelerometro/giroscopio/magnetometro"""
#!/usr/bin/env python
#coding: utf-8

#import ctypes
#import time
from ctypes import *

path = "../../../../../../LSM9DS1_RaspberryPi_Library/lib/liblsm9ds1cwrapper.so"
lib = cdll.LoadLibrary(path)

lib.lsm9ds1_create.argtypes = []
lib.lsm9ds1_create.restype = c_void_p

lib.lsm9ds1_begin.argtypes = [c_void_p]
lib.lsm9ds1_begin.restype = None

lib.lsm9ds1_calibrate.argtypes = [c_void_p]
lib.lsm9ds1_calibrate.restype = None

lib.lsm9ds1_gyroAvailable.argtypes = [c_void_p]
lib.lsm9ds1_gyroAvailable.restype = c_int
lib.lsm9ds1_accelAvailable.argtypes = [c_void_p]
lib.lsm9ds1_accelAvailable.restype = c_int
lib.lsm9ds1_magAvailable.argtypes = [c_void_p]
lib.lsm9ds1_magAvailable.restype = c_int

lib.lsm9ds1_readGyro.argtypes = [c_void_p]
lib.lsm9ds1_readGyro.restype = c_int
lib.lsm9ds1_readAccel.argtypes = [c_void_p]
lib.lsm9ds1_readAccel.restype = c_int
lib.lsm9ds1_readMag.argtypes = [c_void_p]
lib.lsm9ds1_readMag.restype = c_int

lib.lsm9ds1_getGyroX.argtypes = [c_void_p]
lib.lsm9ds1_getGyroX.restype = c_float
lib.lsm9ds1_getGyroY.argtypes = [c_void_p]
lib.lsm9ds1_getGyroY.restype = c_float
lib.lsm9ds1_getGyroZ.argtypes = [c_void_p]
lib.lsm9ds1_getGyroZ.restype = c_float

lib.lsm9ds1_getAccelX.argtypes = [c_void_p]
lib.lsm9ds1_getAccelX.restype = c_float
lib.lsm9ds1_getAccelY.argtypes = [c_void_p]
lib.lsm9ds1_getAccelY.restype = c_float
lib.lsm9ds1_getAccelZ.argtypes = [c_void_p]
lib.lsm9ds1_getAccelZ.restype = c_float

lib.lsm9ds1_getMagX.argtypes = [c_void_p]
lib.lsm9ds1_getMagX.restype = c_float
lib.lsm9ds1_getMagY.argtypes = [c_void_p]
lib.lsm9ds1_getMagY.restype = c_float
lib.lsm9ds1_getMagZ.argtypes = [c_void_p]
lib.lsm9ds1_getMagZ.restype = c_float

lib.lsm9ds1_calcGyro.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcGyro.restype = c_float
lib.lsm9ds1_calcAccel.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcAccel.restype = c_float
lib.lsm9ds1_calcMag.argtypes = [c_void_p, c_float]
lib.lsm9ds1_calcMag.restype = c_float


"""DEFINICIONES DE VARIABLES DEL ULTRASONIDO"""
TRIG1= 11 #gpio salida del sensor 1
ECHO1= 13 # gpio de entrada del sensor 1
TRIG2= 36 #gpio salida del sensor 2
ECHO2= 37 # gpio de entrada del sensor 2
TRIG3= 15 #gpio salida del sensor 3
ECHO3= 22 # gpio de entrada del sensor 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)
"""FUNCIONES DE ULTRASONIDO"""
def medidaUS(trig,echo):
    GPIO.output(trig, GPIO.LOW)
    time.sleep(0.2)
    #Ponemos en alto el pin TRIG esperamos 10 uS antes de ponerlo en bajo
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)
    # En este momento el sensor envía 8 pulsos ultrasónicos de 40kHz y coloca su pin ECHO en alto
    # Debemos detectar dicho evento para iniciar la medición del tiempo
    while True:
        pulso_inicio = time.time()
        if GPIO.input(echo) == GPIO.HIGH:
            break
    # El pin ECHO se mantendrá en HIGH hasta recibir el eco rebotado por el obstáculo. 
    # En ese momento el sensor pondrá el pin ECHO en bajo. 
    # Prodedemos a detectar dicho evento para terminar la medición del tiempo
    while True:
        pulso_fin = time.time()
        if GPIO.input(echo) == GPIO.LOW:
            break
    # Tiempo medido en segundos
    duracion = pulso_fin - pulso_inicio
    # Obtenemos la distancia considerando que la señal recorre dos veces la 
    # distancia a medir y que la velocidad del sonido es 343m/s
    distancia = (34300 * duracion) / 2
    return distancia

def sensores():
    pub = rospy.Publisher('chatter',String,queue_size=10)
    rospy.init_node('sensores',anonymous=True)
    
    rate=rospy.Rate(50000)
    
    
    
    #while not rospy.is_shutdown():
    while True:
        #LECTURA DE DATOS DE ULTRASONIDOS
        distancia1=medidaUS(TRIG1,ECHO1)        
        # time.sleep(0.5)
        distancia2=medidaUS(TRIG2,ECHO2)
        # time.sleep(0.5)
        distancia3=medidaUS(TRIG3,ECHO3)

        #Aqui se cargan los valores del giroscopio
        while lib.lsm9ds1_gyroAvailable(imu) == 0:
            pass
        lib.lsm9ds1_readGyro(imu)
        while lib.lsm9ds1_accelAvailable(imu) == 0:
            pass
        lib.lsm9ds1_readAccel(imu)
        while lib.lsm9ds1_magAvailable(imu) == 0:
            pass
        lib.lsm9ds1_readMag(imu)

        gx = lib.lsm9ds1_getGyroX(imu)
        gy = lib.lsm9ds1_getGyroY(imu)
        gz = lib.lsm9ds1_getGyroZ(imu)

        ax = lib.lsm9ds1_getAccelX(imu)
        ay = lib.lsm9ds1_getAccelY(imu)
        az = lib.lsm9ds1_getAccelZ(imu)

        mx = lib.lsm9ds1_getMagX(imu)
        my = lib.lsm9ds1_getMagY(imu)
        mz = lib.lsm9ds1_getMagZ(imu)

        cgx = lib.lsm9ds1_calcGyro(imu, gx)
        cgy = lib.lsm9ds1_calcGyro(imu, gy)
        cgz = lib.lsm9ds1_calcGyro(imu, gz)

        


        #print ("------------------------------------")
        #print("Gyro: %f, %f, %f [deg/s]" % (cgx, cgy, cgz))
        #print ("------------------------------------")
        #print("Accel: %f, %f, %f [Gs]" % (cax, cay, caz))
        #print ("------------------------------------")
        #print("Mag: %f, %f, %f [gauss]" % (cmx, cmy, cmz))
        #time.sleep(0)

        #Aqui se cargan los valores del magnetometro
        cmx = lib.lsm9ds1_calcMag(imu, mx)
        cmy = lib.lsm9ds1_calcMag(imu, my)
        cmz = lib.lsm9ds1_calcMag(imu, mz)

        #Aqui se cargan los valores del acelerometro
        cax = lib.lsm9ds1_calcAccel(imu, ax)
        cay = lib.lsm9ds1_calcAccel(imu, ay)
        caz = lib.lsm9ds1_calcAccel(imu, az)

        #Aqui se cargan los valores de los ultrasonicos
        u1=np.around(distancia1,2)
        u2=np.around(distancia2,2)
        u3=np.around(distancia3,2)

        #Aqui se carga los valores de los encoders
        e1=100
        e2=200

        
        mensaje=str(str(cmx)+" "+str(cmy)+" "+str(cmz)+" "+str(u1)+" "+str(u2)+" "+str(u3)+" "+str(e1)+" "+str(e2)+" "+str(cgx)+" "+str(cgy)+" "+str(cgz))
        rospy.loginfo(mensaje)
        pub.publish(mensaje)
        rate.sleep()

        
        
if __name__ == '__main__':
   
    try:
        imu = lib.lsm9ds1_create()
        lib.lsm9ds1_begin(imu)
        if lib.lsm9ds1_begin(imu) == 0:
              print("Failed to communicate with LSM9DS1.")
              quit()
        lib.lsm9ds1_calibrate(imu)
        sensores()
    except rospy.ROSInterruptException:
        pass
        
        
        