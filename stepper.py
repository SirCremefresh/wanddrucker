#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO ## Import GPIO library
from time import sleep ## Import 'time' library. Allows us to use 'sleep'
from Adafruit_MotorHAT import * ## import Shield Liberary
import atexit
from StaticParameters import statischeParameter


anzStepper = -1
Speed = statischeParameter.Speed       # 30 RPM 


class steppermotor:
	# # A=0
	# # B=0
	# # C=0
	# # D=0

	def __init__(self,pMNum): #pMPos bekommt die motor position auf dem Shiel 1 oder 2
		
		global anzStepper # Nicht mehr notwendig
		global mh
		
		if anzStepper == -1:
			mh = Adafruit_MotorHAT(addr = 0x60)
			anzStepper = 0
		
		anzStepper = anzStepper + 1
		
		

		
		
		self.MNum=pMNum
		
		self.myStepper = mh.getStepper(200, self.MNum)              # 200 steps/rev, motor port 1 odre 2
		self.myStepper.setSpeed(Speed)      		#speed festlegen
		
		
		self.SteppArt = Adafruit_MotorHAT.INTERLEAVE
		
		if self.SteppArt == Adafruit_MotorHAT.INTERLEAVE:
			self.step360 = 400
		else:
			self.step360 = 200
		
		self.rundung = 0
		self.gradstellung = 0
		self.rundeningrad = 0
		
		atexit.register(self.stepperclean)




	# grad = raw_input("wie viel grad: ")
	def nullstellung(self):
		self.gradstellung = 0
	
	def stepperinfoGrad(self):
		self.gradstellung = self.gradstellung  % 360
		
		return self.gradstellung
		
	def stepperinfoRunden(self):
		return self.rundeningrad / 360
		
	def stepperreset(self):
		if self.stepperinfoGrad() <= 180:
			grad = -self.stepperinfoGrad()
			gradrich = -1
		else:
			grad =  360 - self.stepperinfoGrad()
			gradrich = 1
		for i in range (abs(grad)):
			self.drehe(gradrich)
		
		
	
	
	def drehe(self, grad, pSpeed):
		tempgradstellung = self.gradstellung
		self.rundeningrad = self.rundeningrad + abs(grad)
		
		self.MotorTempo = pSpeed / float(360) * 60
		
		self.myStepper.setSpeed(self.MotorTempo) 
		
		if grad != 0:    
			steps  = float(grad) * self.step360 / float(360)
			
			steps = steps + self.rundung
			self.rundung = steps - int(steps)
			print ("I: steps = "+ str(steps) + " / int(steps) = "+str(int(abs(steps))))
			
			if steps != 0:	
				if grad < 0:  
					self.myStepper.step(int(abs(steps)), Adafruit_MotorHAT.BACKWARD, self.SteppArt)
				else:
					self.myStepper.step(int(abs(steps)), Adafruit_MotorHAT.FORWARD, self.SteppArt)
					
				
		self.gradstellung = tempgradstellung + grad

	def stepperclean(self):  
		global anzStepper
		anzStepper = anzStepper - 1  
		mh.getMotor(self.MNum).run(Adafruit_MotorHAT.RELEASE) #Motor Cleanen
		


if __name__ == "__main__":
	stepper1 = steppermotor(1)
	stepper2 = steppermotor(2)
	#~ atexit.register(stepper1.stepperclean)
	#~ atexit.register(stepper2.stepperclean)
	
	stepper1.drehe(360)
	stepper1.drehe(-360)
	stepper2.drehe(360)
	stepper2.drehe(-360)
	stepper1.stepperclean()
	stepper2.stepperclean()


		


