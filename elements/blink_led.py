import RPi.GPIO as GPIO
from time import sleep

#my values
flashLedPin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(flashLedPin, GPIO.OUT)

for x in range(0, 30):
    GPIO.output(flashLedPin, GPIO.HIGH)
    sleep(.1)
    GPIO.output(flashLedPin, GPIO.LOW)
    sleep(.1)
