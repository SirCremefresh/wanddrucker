#!/usr/bin/python
# -*- coding: utf-8 -*-
import stepper_steuerungen
import sys
from time import sleep
from math import *
from servo import servoClass
from StaticParameters import statischeParameter


class ZeichnerClass:

	def __init__(self, pMotor1 , pMotor2,pservo): # DAS def __init__ wird immer aufgerufen wen eine classe definiert wird
		
		self.DistanzA = statischeParameter.HalbeMotorAbstand # Halber abstand zwischen den motoren in Milimetern
		self.DistanzB = statischeParameter.MotorBisNullPunkt # Abstand motoren zum oberen Nullpunkt in Milimetern
		self.DurchmesserAchse = 52 # durchemesser spule in Milimetern
		self.UmfangAchse = self.DurchmesserAchse * 3.1415296 # umfang achse in Milimetern
		
		# speicher den bekommen parameter in einer lokalen Variabel
		self.Motor1 = pMotor1 #Motoren Classe
		self.Motor2 = pMotor2 #Motoren Classe
		self.servo = pservo #Servo Classe
		
		self.Kalibriert = False 
		

		
	def RechePyti(self,pA,pB):
		C = sqrt(pA * pA + pB * pB) #berechnet die Die lenge der schnur mit dem pytagoras
		return C	#Gibt die vorhin berechnete hypotenuse zurück
		
	def StiftHebenSenken(self,pZ): #hebt und senkt den stift   pZ ist 1 oder 0
		if self.PosZ != pZ: # Schaut ob Pz und die aktuelle position ungleich sind
			self.servo.StiftHebenSenken(pZ) #sickt 1 oder 0 an server class 

	def Nullpunkt(self): # setzt die variabel auf die strecke vom nullpunkt
		self.PosX = self.DistanzA  #setzt self.PosX auf den halben abstand zwischen den motoren
		self.PosY = 0	# setzt die y position auf 0
		self.PosZ = 0	# setzt die z position auf 0
		
		self.Kalibriert = True 
		
		self.LangeM1alt = self.RechePyti(self.DistanzA, self.DistanzB)	#setzt self.LangeM1alt und LangeM2alt auf die lenge der ggrundstellung
		self.LangeM2alt = self.RechePyti(self.DistanzA, self.DistanzB)	#
		
		
	def GeheZu(self,pX,pY,pZ):# Bekommt die neue position und kann den stifft auf die kordinaten bewegen 
		if self.Kalibriert == True: # Schaut ob der drucker kalibriert geworden ist
			LangeM1 = self.RechePyti(pX / statischeParameter.FaktorPixelZuMM, self.DistanzB + pY / statischeParameter.FaktorPixelZuMM) #
			LangeM2 = self.RechePyti(self.DistanzA * 2 - pX / statischeParameter.FaktorPixelZuMM, self.DistanzB + pY / statischeParameter.FaktorPixelZuMM)

			differenzM1 = self.LangeM1alt - LangeM1
			differenzM2 = self.LangeM2alt - LangeM2
			
			GradM1 = differenzM1 / self.UmfangAchse * 360
			GradM2 = differenzM2 / self.UmfangAchse * 360
			print("I: pX = "+str(pX)+" pY = "+str(pY)+"\n")
			print ("I: GradM1 = "+str(GradM1)+" LangeM1 = "+str(LangeM1)+" LangeM1alt = "+str(self.LangeM1alt)+" differenzM1 = "+str(differenzM1)+"\n")
			print ("I: GradM2 = "+str(GradM2)+" LangeM2 = "+str(LangeM2)+" LangeM2alt = "+str(self.LangeM2alt)+" differenzM2 = "+str(differenzM2)+"\n")
			self.StiftHebenSenken(pZ)

			
			stepper_steuerungen.drehe2(self.Motor1, GradM1, self.Motor2, -GradM2)
			
			
			
			self.PosX = pX
			self.PosY = pY
			self.PosZ = pZ
			
			self.LangeM1alt = LangeM1
			self.LangeM2alt = LangeM2
		else:
			self.StiftHebenSenken(1)
			self.StiftHebenSenken(0)
			self.StiftHebenSenken(1)
			self.StiftHebenSenken(0)
	

		# drehe motor
#if __name__ == "__main__":
