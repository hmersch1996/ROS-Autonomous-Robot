# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO          
from time import sleep

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
# print("\n")
# print("The default speed & direction of motor is LOW & Forward.....")
# print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
# print("\n")    

while(1):

    x='b'
    xx='b'
    
    if x=='f':
        print("run")
        if(temp1i==1):
         GPIO.output(in1i,GPIO.HIGH)
         GPIO.output(in2i,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1i,GPIO.LOW)
         GPIO.output(in2i,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1i,GPIO.LOW)
        GPIO.output(in2i,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1i,GPIO.HIGH)
        GPIO.output(in2i,GPIO.LOW)
        temp1i=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1i,GPIO.LOW)
        GPIO.output(in2i,GPIO.HIGH)
        temp1i=0
        x='z'

    elif x=='l':
        print("low")
        pi.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        pi.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        pi.ChangeDutyCycle(75)
        x='z'
    
    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break

#------ Derecha
    if xx=='f':
        print("run")
        if(temp1d==1):
         GPIO.output(in1d,GPIO.HIGH)
         GPIO.output(in2d,GPIO.LOW)
         print("forward")
         xx='z'
        else:
         GPIO.output(in1d,GPIO.LOW)
         GPIO.output(in2d,GPIO.HIGH)
         print("backward")
         xx='z'


    elif xx=='s':
        print("stop")
        GPIO.output(in1d,GPIO.LOW)
        GPIO.output(in2d,GPIO.LOW)
        xx='z'

    elif xx=='f':
        print("forward")
        GPIO.output(in1d,GPIO.HIGH)
        GPIO.output(in2d,GPIO.LOW)
        temp1d=1
        xx='z'

    elif xx=='b':
        print("backward")
        GPIO.output(in1d,GPIO.LOW)
        GPIO.output(in2d,GPIO.HIGH)
        temp1d=0
        xx='z'

    elif xx=='l':
        print("low")
        pd.ChangeDutyCycle(25)
        xx='z'

    elif xx=='m':
        print("medium")
        pd.ChangeDutyCycle(50)
        xx='z'

    elif xx=='h':
        print("high")
        pd.ChangeDutyCycle(75)
        xx='z'
    
    elif xx=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")