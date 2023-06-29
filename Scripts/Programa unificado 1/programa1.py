"""librerias para ultrasonido """
import RPi.GPIO as GPIO
import time         
from time import sleep
import numpy as np
GPIO.setwarnings(False)

"""DEFINICIONES VARIABLES DE ULTRASONIDO"""

TRIG1 = 11 #Variable que contiene el GPIO al cual conectamos la señal TRIG del sensor
ECHO1 = 13 #Variable que contiene el GPIO al cual conectamos la señal ECHO del sensor

TRIG2 = 36 #Variable que contiene el GPIO al cual conectamos la señal TRIG del sensor
ECHO2 = 37 #Variable que contiene el GPIO al cual conectamos la señal ECHO del sensor

TRIG3 = 15 #Variable que contiene el GPIO al cual conectamos la señal TRIG del sensor
ECHO3 = 22 #Variable que contiene el GPIO al cual conectamos la señal ECHO del sensor

GPIO.setmode(GPIO.BOARD)    #Establecemos el modo según el cual nos refiriremos a los GPIO de nuestra RPi            
GPIO.setup(TRIG1, GPIO.OUT) #Configuramos el pin TRIG como una salida 
GPIO.setup(ECHO1, GPIO.IN)  #Configuramos el pin ECHO como una salida 
GPIO.setup(TRIG2, GPIO.OUT) #Configuramos el pin TRIG como una salida 
GPIO.setup(ECHO2, GPIO.IN)  #Configuramos el pin ECHO como una salida
GPIO.setup(TRIG3, GPIO.OUT) #Configuramos el pin TRIG como una salida 
GPIO.setup(ECHO3, GPIO.IN)  #Configuramos el pin ECHO como una salida 

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


""" Definiciones para campo potencial"""
F=300
F1=0  # Valor de fuerza teórica calculado a partir del ultrasonico1
F2=0  # Valor de fuerza teórica calculado a partir del ultrasonico2
F3=0  # Valor de fuerza teórica calculado a partir del ultrasonico3
k1=1000
k2=1000
k3=1000
Fx=0
Fy=0

"""FUNCIONES DE ULTRASONIDO"""
def medidaUS(trig,echo):
    GPIO.output(trig, GPIO.LOW)
    time.sleep(0.1)

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
    




#Contenemos el código principal en un aestructura try para limpiar los GPIO al terminar o presentarse un error
try:
    #Implementamos un loop infinito
    while True:
        
        """"LECTURA DE DATOS DE ULTRASONIDOS"""
        distancia1=medidaUS(TRIG1,ECHO1)        
        # time.sleep(0.5)
        distancia2=medidaUS(TRIG2,ECHO2)
        # time.sleep(0.5)
        distancia3=medidaUS(TRIG3,ECHO3)

        # Imprimimos resultado
        print( "Distancia 1: %.2f cm" % distancia1)
        # Imprimimos resultado
        print( "Distancia 2: %.2f cm" % distancia2)
        # Imprimimos resultado
        print( "Distancia 3: %.2f cm" % distancia3)
        
   # """ Tomamos como distancia valida valores menores a 50 cm """
        if distancia1<50:
            F1=k1*(1/distancia1)
        elif distancia1>52:
            F1=0           
        if distancia2<50:
            F2=k2*(1/distancia2)
        elif distancia2>55:
            F2=0
        if distancia3<50:
            F3=k3*(1/distancia3)
        elif distancia3 >55:
            F3=0
        
        Fx=F-F2-(F1*np.cos(np.deg2rad(30)))-(F3*np.cos(np.deg2rad(30)))
        Fy=(F3*np.sin(np.deg2rad(30)))-(F1*np.sin(np.deg2rad(30)))
        
        print("fx: %.2f"%Fx)
        print("fy: %.2f"%Fy)
#         if Fx>30:
#             val=(Fx/300)*100
#             
#         else:
            #val=30
        val=100
        vald=val
        vali=val    
        
        if Fy==0:
            vali=val
            vald=val
        elif Fy>0:
            if Fy>93:
                vali=((Fy/186))*val
                vald=(1-(Fy/186))*val
            else:
                vald=((Fy/186))*val
                vali=(1-(Fy/186))*val
        elif Fy<0:
             if (-Fy)>93:
                vald=((-Fy)/186)*val
                vali=(1-((-Fy)/186))*val
             else :
                vali=(-Fy/186)*val
                vald=(1-(-Fy/186))*val
        x='f'
        xx='f'
        
        print("vali: %.2f "% vali )
        print("vald: %.2f "% vald )
        controlL298N(x,vali,1) #izquierdo
        controlL298N(xx,vald,0) #derecho
        
        
finally:
    # Reiniciamos todos los canales de GPIO.
    GPIO.cleanup()