"""
A simple Python script to receive messages from a client over
Bluetooth using Python sockets (with Python 3.3 or above).
"""

import socket
import RPi.GPIO as GPIO
from time import sleep

#no need for GPIO warnings
GPIO.setwarnings(False)

#GPIO values
flashLedPin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(flashLedPin, GPIO.OUT)

def flash(dt):
    global speed
    GPIO.output(flashLedPin, not GPIO.input(flashLedPin))
    Clock.schedule_once(flash, 1.0/speed)

hostMACAddress = 'B8:27:EB:29:03:7B' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3 # 3 is an arbitrary choice. However, it must match the port used by the client.
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    while True:
        client, address = s.accept()
        try:
            while 1:
                data = client.recv(size)
                if data:
                    print(data)
                    client.send(data)
		    num = int(data)
                    for x in range(0, num):
                     GPIO.output(flashLedPin, GPIO.HIGH)
                     sleep(.3)
                     GPIO.output(flashLedPin, GPIO.LOW)
                     sleep(.3)
        except:	
            print("Connection lost")	

except (KeyboardInterrupt, SystemExit):
    client.close()
    s.close()
    print '\n! Received keyboard interrupt, quitting threads.\n'
