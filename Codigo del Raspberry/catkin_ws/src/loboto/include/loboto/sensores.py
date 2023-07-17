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
    
    
    while not rospy.is_shutdown():
        #LECTURA DE DATOS DE ULTRASONIDOS
        distancia1=medidaUS(TRIG1,ECHO1)        
        # time.sleep(0.5)
        distancia2=medidaUS(TRIG2,ECHO2)
        # time.sleep(0.5)
        distancia3=medidaUS(TRIG3,ECHO3)

        #Aqui se cargan los valores del magnetometro
        x=1
        y=2
        z=3
        
        #Aqui se cargan los valores de los ultrasonicos
        u1=np.around(distancia1,2)
        u2=np.around(distancia2,2)
        u3=np.around(distancia3,2)

        #Aqui se carga los valores de los encoders
        e1=100
        e2=200

        
        mensaje=str(str(x)+" "+str(y)+" "+str(z)+" "+str(u1)+" "+str(u2)+" "+str(u3)+" "+str(e1)+" "+str(e2))
        rospy.loginfo(mensaje)
        pub.publish(mensaje)
        rate.sleep()

        
        
if __name__ == '__main__':
    try:
        sensores()
    except rospy.ROSInterruptException:
        pass
        
        
        