# Sample code to demonstrate Encoder class.  Prints the value every 5 seconds, and also whenever it changes.

import time
import RPi.GPIO as GPIO
#from encoder import Encoder
import Encoder

def valueChanged(value, direction):
    print("* New value: {}, Direction: {}".format(value, direction))

GPIO.setmode(GPIO.BCM)

e1 = Encoder.Encoder(38, 40)
e2 = Encoder.Encoder(21, 23)
try:
    while True:
        time.sleep(0.5)
        print("Encoder izquierdo {}".format(e1.getValue()))
        time.sleep(0.5)
        print("Encoder derecho  {}".format(e2.getValue()))
except Exception:
    pass

GPIO.cleanup()