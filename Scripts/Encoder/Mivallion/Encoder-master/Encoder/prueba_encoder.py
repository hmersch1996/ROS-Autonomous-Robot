import Encoder
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)

enc = Encoder.Encoder(38,40)

while True:
    


    lectura=enc.read()

    print( "Lectura: %.2f" % lectura)
    
    time.sleep(0.5)
    
GPIO.cleanup()