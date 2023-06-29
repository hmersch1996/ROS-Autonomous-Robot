# Importamos la paquteria necesaria
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
TRIG1 = 11 #Variable que contiene el GPIO al cual conectamos la señal TRIG del sensor
ECHO1 = 13 #Variable que contiene el GPIO al cual conectamos la señal ECHO del sensor

TRIG2 = 36 #Variable que contiene el GPIO al cual conectamos la señal TRIG del sensor
ECHO2 = 37 #Variable que contiene el GPIO al cual conectamos la señal ECHO del sensor

TRIG3 = 15 #Variable que contiene el GPIO al cual conectamos la señal TRIG del sensor
ECHO3 = 22 #Variable que contiene el GPIO al cual conectamos la señal ECHO del sensor

GPIO.setmode(GPIO.BOARD)     #Establecemos el modo según el cual nos refiriremos a los GPIO de nuestra RPi            
GPIO.setup(TRIG1, GPIO.OUT) #Configuramos el pin TRIG como una salida 
GPIO.setup(ECHO1, GPIO.IN)  #Configuramos el pin ECHO como una salida 
GPIO.setup(TRIG2, GPIO.OUT) #Configuramos el pin TRIG como una salida 
GPIO.setup(ECHO2, GPIO.IN)  #Configuramos el pin ECHO como una salida
GPIO.setup(TRIG3, GPIO.OUT) #Configuramos el pin TRIG como una salida 
GPIO.setup(ECHO3, GPIO.IN)  #Configuramos el pin ECHO como una salida 

#Contenemos el código principal en un aestructura try para limpiar los GPIO al terminar o presentarse un error
try:
    #Implementamos un loop infinito
    while True:
#ULTRASONICO 1--------------------------------------------------
        # Ponemos en bajo el pin TRIG y después esperamos 0.5 seg para que el transductor se estabilice
        GPIO.output(TRIG1, GPIO.LOW)
        time.sleep(0.5)

        #Ponemos en alto el pin TRIG esperamos 10 uS antes de ponerlo en bajo
        GPIO.output(TRIG1, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG1, GPIO.LOW)

        # En este momento el sensor envía 8 pulsos ultrasónicos de 40kHz y coloca su pin ECHO en alto
        # Debemos detectar dicho evento para iniciar la medición del tiempo
        
        while True:
            pulso_inicio = time.time()
            if GPIO.input(ECHO1) == GPIO.HIGH:
                break

        # El pin ECHO se mantendrá en HIGH hasta recibir el eco rebotado por el obstáculo. 
        # En ese momento el sensor pondrá el pin ECHO en bajo.
	# Prodedemos a detectar dicho evento para terminar la medición del tiempo
        
        while True:
            pulso_fin = time.time()
            if GPIO.input(ECHO1) == GPIO.LOW:
                break

        # Tiempo medido en segundos
        duracion1 = pulso_fin - pulso_inicio

        #Obtenemos la distancia considerando que la señal recorre dos veces la distancia a medir y que la velocidad del sonido es 343m/s
        distancia1 = (34300 * duracion1) / 2
#ULTRASONICO 2------------------------------------------------------------------
        time.sleep(0.5)
        # Ponemos en bajo el pin TRIG y después esperamos 0.5 seg para que el transductor se estabilice
        GPIO.output(TRIG2, GPIO.LOW)
        time.sleep(0.5)

        #Ponemos en alto el pin TRIG esperamos 10 uS antes de ponerlo en bajo
        GPIO.output(TRIG2, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG2, GPIO.LOW)

        # En este momento el sensor envía 8 pulsos ultrasónicos de 40kHz y coloca su pin ECHO en alto
        # Debemos detectar dicho evento para iniciar la medición del tiempo
        
        while True:
            pulso_inicio = time.time()
            if GPIO.input(ECHO2) == GPIO.HIGH:
                break

        # El pin ECHO se mantendrá en HIGH hasta recibir el eco rebotado por el obstáculo. 
        # En ese momento el sensor pondrá el pin ECHO en bajo.
	# Prodedemos a detectar dicho evento para terminar la medición del tiempo
        
        while True:
            pulso_fin = time.time()
            if GPIO.input(ECHO2) == GPIO.LOW:
                break

        # Tiempo medido en segundos
        duracion2 = pulso_fin - pulso_inicio

        #Obtenemos la distancia considerando que la señal recorre dos veces la distancia a medir y que la velocidad del sonido es 343m/s
        distancia2 = (34300 * duracion2) / 2
        
#ULTRASONICO 3--------------------------------------------------------
            # Ponemos en bajo el pin TRIG y después esperamos 0.5 seg para que el transductor se estabilice
        time.sleep(0.5)
        GPIO.output(TRIG3, GPIO.LOW)
        time.sleep(0.5)

        #Ponemos en alto el pin TRIG esperamos 10 uS antes de ponerlo en bajo
        GPIO.output(TRIG3, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG3, GPIO.LOW)

        # En este momento el sensor envía 8 pulsos ultrasónicos de 40kHz y coloca su pin ECHO en alto
        # Debemos detectar dicho evento para iniciar la medición del tiempo
        
        while True:
            pulso_inicio = time.time()
            if GPIO.input(ECHO3) == GPIO.HIGH:
                break

        # El pin ECHO se mantendrá en HIGH hasta recibir el eco rebotado por el obstáculo. 
        # En ese momento el sensor pondrá el pin ECHO en bajo.
	# Prodedemos a detectar dicho evento para terminar la medición del tiempo
        
        while True:
            pulso_fin = time.time()
            if GPIO.input(ECHO3) == GPIO.LOW:
                break

        # Tiempo medido en segundos
        duracion3 = pulso_fin - pulso_inicio

        #Obtenemos la distancia considerando que la señal recorre dos veces la distancia a medir y que la velocidad del sonido es 343m/s
        distancia3 = (34300 * duracion3) / 2
#RESULTADOS ----------------------------------------------------------

        # Imprimimos resultado
        print( "Distancia 1: %.2f cm" % distancia1)
        # Imprimimos resultado
        print( "Distancia 2: %.2f cm" % distancia2)
        # Imprimimos resultado
        print( "Distancia 3: %.2f cm" % distancia3)
finally:
    # Reiniciamos todos los canales de GPIO.
    GPIO.cleanup()
