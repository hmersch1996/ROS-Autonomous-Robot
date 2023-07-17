#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

# LIBRERIAS PARA LOS PERIFERICOS
#PARA LOS ULTRASONICOS
import RPi.GPIO as GPIO 
import time
from time import sleep
import numpy as np
GPIO.setwarnings(False)

"""DEFINICIONES DE VARIABLES DEL ULTRASONIDO"""
TRIG1= 11 #gpio salida del sensor 1
ECHO1= 13 # gpio de entrada del sensor 1
TRIG2= 36 #gpio salida del sensor 2
ECHO2= 37 # gpio de entrada del sensor 2
TRIG3= 15 #gpio salida del sensor 3
ECHO3= 22 # gpio de entrada del sensor 3

# GPIO.setmode(GPIO.BOARD)
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

def separador(texto):
    x = texto.split(" ")
    return x



def sensores(data):
    
    # Lectura de los datos del IMU
    lista= separador(data.data)

    # Lectura de ultrasonicos
    ultrasonicos=[medidaUS(TRIG1,ECHO1),medidaUS(TRIG2,ECHO2) ,medidaUS(TRIG3,ECHO3)  ]

    # Redondeo de valores leidos
    ultrasonicos_r=[round(x,2) for x in ultrasonicos]

    #Aqui se carga los valores de los encoders
    encoders=[100,200]

    mediciones=ultrasonicos_r+lista+encoders

    mensaje=' '.join(mediciones)

    rospy.loginfo(mensaje)
    pub.publish(mensaje)
    rate.sleep()

        
        
rospy.init_node('pubsub_sensores')
sub = rospy.Subscriber('datos_imu', String, sensores)
pub = rospy.Publisher('datos_sensores',String,queue_size=10)
rate=rospy.Rate(2)

rospy.spin()
        
        
        