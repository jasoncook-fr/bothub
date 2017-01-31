from RPIO import PWM
from time import sleep

servo = PWM.Servo()

try:
	while True:
		for x in range(600, 2400, 10):
			servo.set_servo(18, x)
			sleep(.05)
			print x

		for x in range(2400, 600, -10):
			servo.set_servo(18, x)
			sleep(.05)
			print x
			
except (KeyboardInterrupt, SystemExit):
	servo.stop_servo(18)