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



""" Global variabels  """
Set_RPMd =80                            # SET RPM value
Set_RPMi =80                            # SET RPM value
feedbacki=0
feedbackd=0
previous_timed =0.0
previous_timei =0.0
previous_errori=0.0
previous_errord=0.0
Integrali=0.0
Integrald=0.0           
#D_cycal=80
vald=30
vali=30
Kp=50                                       # Proportional controller Gain (0 to 100)
Ki=50                                       # Integral controller Gain (0 to 100)
Kd=0                                       # Derivative controller Gain (0 to 100)
RunRPM=0
Loop_value=0
a=0
avr=0
i=0

Enc_Ai = 38 
GPIO.setup(Enc_Ai, GPIO.IN)
Enc_Ad = 21 
GPIO.setup(Enc_Ad, GPIO.IN)

""" PID control del motor derecho"""
def PID_functiond():
    
    global previous_timed
    global previous_errord
    global Integrald
    global vald
    global Kp
    global Ki
    global Kd
    
    error = int(Set_RPMd) -feedbackd                    # Differnce between expected RPM and run RPM
    
    if (previous_timed== 0):
         previous_timed =time.time()
         
    current_time = time.time()
    delta_time = current_time - previous_timed
    delta_error = error - previous_errord
    
    Pout = (Kp/10 * error)              
    
    Integrald += (error * delta_time)
    
    
    if Integrald>10:      
        Integrald=10
        
    if Integrald<-10:
        Integrald=-10
    
    Iout=((Ki/10) * Integrald)
    
    
    Derivative = (delta_error/delta_time)         #de/dt
    previous_timed = current_time
    previous_errord = error
    
    Dout=((Kd/1000 )* Derivative)
    
    output = Pout + Iout + Dout                  # PID controller output
    #print(output)
    if ((output>vald)&(vald<100)):           
        vald+=1
        
    if ((output<vald)&(vald>10)):           
        vald-=1
    
 
       
    return ()
"""PID motor izquierdo """
def PID_functioni():
    
    global previous_timei
    global previous_errori
    global Integrali
    global vali
    global Kp
    global Ki
    global Kd
    
    error = int(Set_RPMi) -feedbacki                    # Differnce between expected RPM and run RPM
    
    if (previous_timei== 0):
         previous_timei =time.time()
         
    current_time = time.time()
    delta_time = current_time - previous_timei
    delta_error = error - previous_errori
    
    Pout = (Kp/10 * error)              
    
    Integrali += (error * delta_time)
    
    
    if Integrali>10:      
        Integrali=10
        
    if Integrali<-10:
        Integrali=-10
    
    Iout=((Ki/10) * Integrali)
    
    
    Derivative = (delta_error/delta_time)         #de/dt
    previous_timei = current_time
    previous_errori = error
    
    Dout=((Kd/1000 )* Derivative)
    
    output = Pout + Iout + Dout                  # PID controller output
    print(output)
    if ((output>vali)&(vali<100)):           
        vali+=1
        
    if ((output<vali)&(vali>10)):           
        vali-=1
   
    
    
    return ()

"""   RPM del motor derecho   """
 
def RPM_functiond():      
    global feedbackd
    tc=time.time()
    
    
    while (GPIO.input(Enc_Ad )==False):               
        v=0
        ts=time.time()
        time_count=ts-tc
        
        if (time_count>3):
            print("Feedback failed, Please make proper feedback connection")
            feedbackd=0
            return ()         
               
    
    while (GPIO.input(Enc_Ad)==True):                  
        i=0
        ts=time.time()
        time_count=ts-tc
        if (time_count>7):
            print("Feedback failed, Please make proper feedback connection")
            feedbackd=0
            return ()
    
    v = time.time()                              # Stores the first pulse time
    while (GPIO.input(Enc_Ad)==False):               
        s=0                                     
    while (GPIO.input(Enc_Ad)==True):                  
        h=0                                            
    h=time.time()                                # Stores the next pulse time
    w=round(60/((h-v)*750)) #750                                # MOTOR speed in RPM  
    feedbackd = w
    
    return ()

"""   RPM del motor izquierdo  """
def RPM_functioni():      
    global feedbacki
    tc=time.time()
    
    
    while (GPIO.input(Enc_Ai)==False):               
        v=0
        ts=time.time()
        time_count=ts-tc
        
        if (time_count>7):
            print("Feedback failed, Please make proper feedback connection")
            feedbacki=0
            return ()         
               
    
    while (GPIO.input(Enc_Ai)==True):                  
        i=0
        ts=time.time()
        time_count=ts-tc
        if (time_count>7):
            print("Feedback failed, Please make proper feedback connection")
            feedbacki=0
            return ()
    
    v = time.time()                              # Stores the first pulse time
    while (GPIO.input(Enc_Ai )==False):               
        s=0                                     
    while (GPIO.input(Enc_Ai )==True):                  
        h=0                                            
    h=time.time()                                # Stores the next pulse time
    w=round(60/((h-v)*750)) #750                                # MOTOR speed in RPM  
    feedbacki = w
    
    return ()

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
F=70
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
        elif distancia1>50:
            F1=0           
        if distancia2<50:
            F2=k2*(1/distancia2)
        elif distancia2>50:
            F2=0
        if distancia3<50:
            F3=k3*(1/distancia3)
        elif distancia3 >50:
            F3=0
        
        Fx=F-F2-(F1*np.cos(np.deg2rad(30)))-(F3*np.cos(np.deg2rad(30)))
        Fy=(F3*np.sin(np.deg2rad(30)))-(F1*np.sin(np.deg2rad(30)))
        
        print("fx: %.2f"%Fx)
        print("fy: %.2f"%Fy)
#         if Fx>30:
#             val=(Fx/300)*100
#             
#         else:
            #val=3
        val=100
        vald=val
        vali=val    
        if(Fx<0): 
            x='f'
            xx='b'
            vali=40
            vald=40
            print("rotando")
        else: 
            x='f'
            xx='f'
            if Fy==0:
                vali=val
                vald=val
            elif Fy>0:
#                 if Fy>20:
#                     vali=((Fy/186))*val
#                     vald=(1-(Fy/186))*val
#                 else:
                vali=val
                vald=(1-(Fy/37))*val
            elif Fy<0:
#                 if (-Fy)>20:
#                     vald=((-Fy)/186)*val
#                     vali=(1-((-Fy)/186))*val
#                 else :
                vald=val
                vali=(1-(-Fy/37))*val
                    
        
#         print("vali: %.2f "% vali)
#         print("vald: %.2f "% vald)
        Set_RPMi=(200*vali)/100
        Set_RPMd=(200*vald)/100
        RPM_functiond()
        PID_functiond()
        RPM_functioni()
        PID_functioni()
#         print("Rpm requerido izq: %.2f "% Set_RPMi)
#         print("Rpm medido izq: %.2f"% feedbacki)
#         print("Rpm requerido der: %.2f "% Set_RPMd)
#         print("Rpm medido der: %.2f"% feedbackd)
        #print(D_cycal)
        print("vali: %.2f "% vali)
        print("vald: %.2f "% vald)
        controlL298N(x,vali,1) #izquierdo
        controlL298N(xx,vald,0) #derecho
        
        
finally:
    # Reiniciamos todos los canales de GPIO.
    GPIO.cleanup()