#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time         
from time import sleep
import numpy as np
import math
GPIO.setwarnings(False)

""" DEFINICIONES PARA L298N """
in1i = 18
in2i = 16
eni = 12
in1d = 29
in2d = 31
end = 33
temp1i=1
temp1d=1
GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1i,GPIO.OUT)
GPIO.setup(in2i,GPIO.OUT)
GPIO.setup(eni,GPIO.OUT)
GPIO.output(in1i,GPIO.LOW)
GPIO.output(in2i,GPIO.LOW)
pi=GPIO.PWM(eni,1000)


GPIO.setup(in1d,GPIO.OUT)
GPIO.setup(in2d,GPIO.OUT)
GPIO.setup(end,GPIO.OUT)
GPIO.output(in1d,GPIO.LOW)
GPIO.output(in2d,GPIO.LOW)
pd=GPIO.PWM(end,1000)

pi.start(10)
pd.start(10)

""" Funciones de L298N """
def controlL298N(x,valu,p):
    if p==1:
        if x=='s':
            #print("stop")
            GPIO.output(in1i,GPIO.LOW)
            GPIO.output(in2i,GPIO.LOW)
            pi.ChangeDutyCycle(valu)
            x='z'
        elif x=='f':
            #print("forward")
            GPIO.output(in1i,GPIO.HIGH)
            GPIO.output(in2i,GPIO.LOW)
            pi.ChangeDutyCycle(valu)
            x='z'
        elif x=='b':
            #print("backward")
            GPIO.output(in1i,GPIO.LOW)
            GPIO.output(in2i,GPIO.HIGH)
            pi.ChangeDutyCycle(valu)
            x='z'
        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")
    else:
        if x=='s':
            #print("stop")
            GPIO.output(in1d,GPIO.LOW)
            GPIO.output(in2d,GPIO.LOW)
            pd.ChangeDutyCycle(valu)
            x='z'
        elif x=='f':
            #print("forward")
            GPIO.output(in1d,GPIO.HIGH)
            GPIO.output(in2d,GPIO.LOW)
            pd.ChangeDutyCycle(valu)
            x='z'
        elif x=='b':
            #print("backward")
            GPIO.output(in1d,GPIO.LOW)
            GPIO.output(in2d,GPIO.HIGH)
            pd.ChangeDutyCycle(valu)
            x='z'
        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")
    



def chatter_callback(message):
    datoss=str(message.data)
    print(datoss)

    datos=datoss.split()

    print("\n====================")
   # print("Motor 1:"+datos[0])
   # print("Motor 2:"+datos[1])
    #val=100
    vald=math.trunc(int(datos[0]))   # primer valor un numero de 0 a 100 para el motor
    vali=math.trunc(int(datos[1]))   # segundo, de 0 a 100 para el motor izquierdo
    print(vald)
    print(vali)
    x= datos[2]       # si es f o b, adelante o atras izquierda
    xx=datos[3]       # si es f o b, adelante o atras derecha
    controlL298N(x,vali,1) #izquierdo
    controlL298N(xx,vald,0) #derecho


def instrucciones():
    rospy.init_node('kuka',anonymous=True)

    rospy.Subscriber("chatter2",String, chatter_callback)

    rospy.spin()

if __name__ == '__main__':
    instrucciones()