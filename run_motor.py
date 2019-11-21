import RPi.GPIO as GPIO
import time

#a couple of delay constants
dispense_time = 2

#Pin Layout
STBY = 15 #STBY BCM22
AIN1 = 13 #AIN1 BCM27
AIN2 = 7  #AIN2 BCM4
PWMA = 11 #PWMA BCM17

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
    print("Dispensing...")
    dispense(dispense_time)
    print("Enjoy your candy")
    GPIO.cleanup()

except KeyboardInterrupt:
    print("Error")
    GPIO.cleanup()