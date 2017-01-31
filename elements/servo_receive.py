"""
A simple Python script to receive messages from a client over
Bluetooth using Python sockets (with Python 3.3 or above).
"""

import socket
import RPi.GPIO as GPIO
from RPIO import PWM
from time import sleep
import threading

#no need for GPIO warnings
GPIO.setwarnings(False)

servo = PWM.Servo()

#GPIO values
flashLedPin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(flashLedPin, GPIO.OUT)

#define a global for blink position:
servo_pin = 18
position = 600 #600 to 2400 is our range (servo model MPX Nano-S)
last_position = 0

hostMACAddress = 'B8:27:EB:29:03:7B' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3 # 3 is an arbitrary choice. However, it must match the port used by the client.
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)

# Toggle the flashing LED according to the position global
def move_servo():
    global position
    global last_position
    while True:
        try:
            if position != last_position:
                finalPosition = int(round(position,-1))
                if finalPosition > last_position:
                    while finalPosition > last_position:
                        servo.set_servo(servo_pin, finalPosition)
                        finalPosition -= 10
                elif finalPosition < last_position:
                    while finalPosition < last_position:
                        servo.set_servo(servo_pin, finalPosition)
                        finalPosition += 10
                servo.set_servo(servo_pin, finalPosition)
                print("POSITON IS : " + str(finalPosition))
                last_position = position
        except (KeyboardInterrupt, SystemExit):
            client.close()
            s.close()

try:
    threading.Thread(target = move_servo).start()
    while True:
        client, address = s.accept()
        try:
            while 1:
                data = client.recv(size)
                if data:
                    numbers = data.split()
                    position = int(numbers[0])
                    #for x in range(0, len(numbers)):
                        #position = int(numbers[x])

        except:	
            print("Connection lost")	

except (KeyboardInterrupt, SystemExit):
    client.close()
    s.close()
    print '\n! Received keyboard interrupt, quitting threads.\n'
