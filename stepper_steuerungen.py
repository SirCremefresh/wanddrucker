#!/usr/bin/python
# -*- coding: utf-8 -*-
from stepper import steppermotor
from time import sleep ## Import 'time' library. Allows us to use 'sleep'
#from threading import Thread
#import thread 
from threading import *
from StaticParameters import statischeParameter



def machMotor1():
	stepper1 = steppermotor(1)#
	return stepper1
	
	
def machMotor2():
	stepper2 = steppermotor(2)
	return stepper2
	
def stepperclean(pMotor):
	pMotor.stepperclean()

Maxspeed = statischeParameter.Speed * 360 / 60 #grad in Minute
AnzStepps = 200	
	
	
def drehe2(pMotor1,pGradM1, pMotor2, pGradM2):
	#~ pGradM1 , pGradM2 drehen ingrad -+
	
	if abs(int(pGradM1)) < abs(int(pGradM2)):
		MotorKleinGrad = pGradM1
		MotorGrossGrad = pGradM2
		steppermk = pMotor1
		steppermg = pMotor2
	else:
		MotorGrossGrad = pGradM1
		MotorKleinGrad = pGradM2
		steppermg = pMotor1
		steppermk = pMotor2

	if not MotorGrossGrad == 0:
		
		if MotorKleinGrad == 0:
			
			MotorGrossThread = Thread(target=steppermg.drehe,args=(MotorGrossGrad , Maxspeed)) 
			MotorGrossThread.start()
			MotorGrossThread.join()
		
		else:
			#MotorGrossLaufzeit = MotorGrossGrad / Maxspeed # 
			
			difference = abs(MotorGrossGrad) / abs(MotorKleinGrad)
			
			MotorKleinLaufspeed = Maxspeed / difference
			
			
			MotorGrossThread = Thread(target=steppermg.drehe,args=(MotorGrossGrad , Maxspeed)) 
			MotorKleinThread = Thread(target=steppermk.drehe,args=(MotorKleinGrad , MotorKleinLaufspeed)) 
			
			MotorGrossThread.start()
			MotorKleinThread.start()
			
			MotorGrossThread.join()
			MotorKleinThread.join()






