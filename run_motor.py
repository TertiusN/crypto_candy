import RPi.GPIO as GPIO
import time

#a couple of delay constants
dispense_time = 5

#Pin Layout
STBY = 22
AIN1 = 27
AIN2 = 4
PWMA = 17

GPIO.setmode(GPIO.BOARD) #use board pin numbers

#Set GPIO outputs
GPIO.setup(STBY, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)

#Initialise
GPIO.output(STBY, GPIO.LOW)
GPIO.output(AIN1, GPIO.HIGH)
GPIO.output(AIN2, GPIO.LOW)
GPIO.output(PWMA, GPIO.HIGH)

#Dispense Candy
def dispense(run_time):
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)

    GPIO.output(STBY, GPIO.HIGH) #start
    time.sleep(run_time)
    GPIO.output(STBY, GPIO.LOW) #stop

try:
    while True:
        dispense(dispense_time)

except KeyboardInterrupt:

    GPIO.cleanup()