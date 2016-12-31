#!/usr/bin/python
# -*- coding: utf-8 -*-

class statischeParameter:

	ServoGPIO = 18 #GPIO PIN Mit dindem der servo eingesteckt ist
	
	FaktorPixelZuMM = 3
	
	BildAbstandLinks = 180 * FaktorPixelZuMM #abstand von Links bis es zeichnet in pixel
	BildAbstandOben = 30 * FaktorPixelZuMM  #abstand von oben bis es zeichnet in pixel
	
	BildBreite = 270 #auf wie viele pixel grundweite es beim einlesen geendert werden soll. Canvas ist 270
	
	Speed = 30 #angabe in RPM gilt für die stepper motoren
	
	
	
	HalbeMotorAbstand = 234 # Halber abstand zwischen den motoren in Milimetern
	MotorBisNullPunkt = 100 # Abstand motoren zum oberen Nullpunkt in Milimetern