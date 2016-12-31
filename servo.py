#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO ## Import GPIO library
from time import sleep ## Import 'time' library. Allows us to use 'sleep'
from StaticParameters import statischeParameter


class servoClass:
	def __init__(self,pServoGPIOPin):
		ServoGPIOPin = pServoGPIOPin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(ServoGPIOPin,GPIO.OUT)

		self.pwm = GPIO.PWM(ServoGPIOPin,50)
		self.pwm.start(3.5)
			#~ #self.StiftHebenSenkenumrechnen(10)
		#~ sleep(0.5)
		#~ self.pwm.stop()

	def StiftHebenSenkenumrechnen(self,pangel):
		duty = float(pangel) / 10.0 + 2.5
		self.pwm.ChangeDutyCycle(duty)
		print("KX"+ str(duty))
	
#for i in range(170):
#	x = i + 10
#	UpdateDutyCycle(x)
#	sleep(0.1)

	def StiftHebenSenken(self,pz):
		if pz == 0:
			#~ self.pwm.start(3.5)
			self.StiftHebenSenkenumrechnen(10)
			sleep(0.5)
			#~ self.pwm.stop()
		elif pz == 1:
			#~ self.pwm.start(10.5)
			self.StiftHebenSenkenumrechnen(80)
			sleep(0.5) 
			#~ self.pwm.stop()

	
	def Cleanup(self):
		GPIO.cleanup()
		
if __name__ == "__main__":
	
	servo = servoClass(23)
	print ("instanziert")
	sleep(1)
	print("0")
	servo.StiftHebenSenken(0)
	
	sleep(0.4)
	print("1")
	servo.StiftHebenSenken(1)
	sleep(0.4)
	print("0")
	servo.StiftHebenSenken(0)
	sleep(0.4)
	print("1")
	servo.StiftHebenSenken(1)
	sleep(10)
