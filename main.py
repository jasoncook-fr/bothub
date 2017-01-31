"""
A simple Python script to receive messages from a client over
Bluetooth using Python sockets (with Python 3.3 or above).
"""

import socket
import RPi.GPIO as GPIO
from time import sleep
import threading

#no need for GPIO warnings
GPIO.setwarnings(False)

#GPIO values
flashLedPin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(flashLedPin, GPIO.OUT)

#define a global for blink speed:
speed = 1.0

hostMACAddress = 'B8:27:EB:29:03:7B' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3 # 3 is an arbitrary choice. However, it must match the port used by the client.
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)

# Toggle the flashing LED according to the speed global
def flash():
    global speed
    while True:
        GPIO.output(flashLedPin, not GPIO.input(flashLedPin))
        sleep(1.0/speed)

# This is called when the slider is updated:
def update_speed(obj, value):
    global speed
    print("Updating speed to:" + str(obj.value))
    speed = obj.value
    textNum = str(int(speed))
    btSocket.send(bytes(textNum, 'UTF-8'))

try:
    threading.Thread(target = flash).start()
    while True:
        client, address = s.accept()
        try:
            while 1:
                data = client.recv(size)
                if data:
                    print(data)
                    speed = int(data)
        except:	
            print("Connection lost")	

except (KeyboardInterrupt, SystemExit):
    client.close()
    s.close()
    print '\n! Received keyboard interrupt, quitting threads.\n'
