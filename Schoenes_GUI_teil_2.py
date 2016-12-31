#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *  #Lberary für GUI
from stepper import steppermotor #Class steppermotor für einzelne Steuerung der Motore
import stepper_steuerungen #
from threading import Timer
from threading import Thread
from threading import activeCount
from thread import start_new_thread
import sys
from time import sleep
from math import *
from Bildverarbeiter import Bildverarbeitung
from Zeichnungs_steuerung import Zeichnungssteuerung
import MotorCalibrator 
from MotorCalibrator import Farbenundschriften
import os
import datetime
import atexit
from servo import servoClass
from StaticParameters import statischeParameter

#~Variabeln 
Bildwidth = 270
Bildheight = 270

pGrad = 0
pRunden = 0

blackwhite_vorher = -1
pscale_vorher = 127

file_path_vorher = ""
erstesmal = True

CMotorGradsize = 103

IstKalibriert = False

ServoGPIO = statischeParameter.ServoGPIO

#~ Motoren initialisieren
stepper1 = stepper_steuerungen.machMotor1()
stepper2 = stepper_steuerungen.machMotor2() 

servo = servoClass(ServoGPIO)

bildverarbeiter1 = Bildverarbeitung()

zeichnungsSteuerung1 = Zeichnungssteuerung(stepper1,stepper2,servo)

#~farben und schrift im GUI 
#~Titel 
BackGroundColor = "#5B9BD5"
Titlefont = "bold",20

Logfilename = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
Logfile = open("Log//" + Logfilename+".txt","w+")

#~Alles Print in TTherminal umleiten 
class PrintToTTerminal(object):
	def write(self,s):
		#~TTerminal.insert(END,s)
		if s[0] == "I":
			Logfile.write(s)
		elif s[0] == "K":
			if s[1] == "X":
				TTerminal.insert(END,s)
				DruckPosX = X[3:]
			elif s[1] == "Y":
				DruckPosY = Y[3:]
def writeToTTerminal(s):
		#~TTerminal.insert(END,s)
		Logfile.write(s)
sys.stdout = PrintToTTerminal()


#~
#~
#~ Funktionen
#~
#~
 
def Motordreh(pMotor1dreh, pMotor2dreh):
	try:
		Motor1dreh = int(pMotor1dreh)
	except ValueError:
		Motor1dreh = 0
	try:
		Motor2dreh = int(pMotor2dreh)
	except ValueError:
		Motor2dreh = 0

	t = Thread(target=stepper_steuerungen.drehe2,args=(stepper1,Motor1dreh , stepper2,Motor2dreh)) # Definiert Thread mit der funktion drehe2 in der steppersteuerungen 
																								   # Parameter sind Classe motor1 dan Grad Dies kann - oder + sein das gleiche für den zweiten motor 
	t.start()

def stepperreset(pStepper):	
	t2 = Thread(target=pStepper.stepperreset, args=())
	t2.start()

def linemover(pline, pcan, pgrad):
	cx = CMotorGradsize / 2 + (CMotorGradsize / 2 - 8)* sin(radians(pgrad))
	cy = CMotorGradsize / 2 - (CMotorGradsize / 2 - 8) * cos(radians(pgrad))
	
	newcord= CMotorGradsize / 2 ,CMotorGradsize / 2, cx, cy
	pcan.coords(pline, newcord)
	
def changetext():
	pGrad = stepper1.stepperinfoGrad()
	pRunden = stepper1.stepperinfoRunden()
	LMotor1Runden.config(text=pRunden)
	
	linemover(CMotor1Gradline, CMotor1Grad, pGrad)
	
	pGrad = stepper2.stepperinfoGrad()
	pRunden = stepper2.stepperinfoRunden()
	LMotor2Runden.config(text=pRunden)
	
	linemover(CMotor2Gradline, CMotor2Grad, pGrad)
	
	pLThreads_open = activeCount() - threadsinitial
	
	if pLThreads_open == 0:
		colnumpLThreads_open = "green"
	else:
		colnumpLThreads_open = "red"
		
	LThreadsOpen.config(text=pLThreads_open, fg=colnumpLThreads_open)
	
	pImgPath= bildverarbeiter1.infoFilePath()
	LBildName.config(text=pImgPath)
	
	Timer(0.1, changetext).start()

def Imgpathopen():
	LStatusbar.config(text="Working")
	bildverarbeiter1.ImgOpen()
	bildverarbeiter1.Imgconverter()
	imgdrawcanvasx()
	LStatusbar.config(text="Ready")
	
def imgdrawcanvasx(): #Diese Funktion schreibt Die Pixel ins canvas rein
	global blackwhite_vorher	#
	global Ivorschaubild		#  Macht diese variabeln Globale
	global file_path_vorher		# 
	global erstesmal			#

	FilePath = bildverarbeiter1.infoFilePath() #Holt den datei Pfad aus dem bildverarbeiter
	
	if FilePath != "": #Wenn der dateipfad nicht lehr ist
		blackwhite = bildverarbeiter1.infoblackwhite() #Holt die Schwarzweiss skala vom bildverarbeiter
		
		ischwarz = 0
		ischwarzneu = 0
		iweiss = 0
		iweissneu = 0
		
		im_x = bildverarbeiter1.infoBasewidht()    #Holt die werte fom Bild vom  bildverarbeiter
		im_y = bildverarbeiter1.infoBaseheight()
		im_array = bildverarbeiter1.infoImgArray()	
		Color = bildverarbeiter1.infoColor()
		
		if FilePath != file_path_vorher or blackwhite_vorher == -1: # WEnn ein neues bild Geladen Wurde
			#~ neuesBild = True
			CImgVorschau.delete(Ivorschaubild)
			Ivorschaubild = PhotoImage(width=bildverarbeiter1.infoBasewidht(),height= bildverarbeiter1.infoBaseheight())
			CImgVorschau.create_image(bildverarbeiter1.infoBasewidht() / 2, bildverarbeiter1.infoBaseheight()/ 2, image=Ivorschaubild)
			blackwhite_vorher = -1

		neuesBild = False
			
		if Color == "BW":
			ColorHex = "#000000"
		elif Color ==  "C":
			ColorHex = "#00ffff"
		elif Color ==  "M":
			ColorHex = "#ff00ff"
		elif Color ==  "Y":
			ColorHex = "#ffff00"
		else:
			ColorHex = "#000000"
			
		for iy in range (im_y):
			for ix in range(im_x):
				px = im_array[ix][iy]
				if px > blackwhite:  #255==schwarz  0==weiss
					iweiss = iweiss + 1
					if px < blackwhite_vorher or neuesBild:
						if erstesmal == False:
							iweissneu = iweissneu + 1
							Ivorschaubild.put("ffffff",(ix,iy)) #weiss
				else:
					ischwarz = ischwarz +1
					if px > blackwhite_vorher or neuesBild:
						ischwarzneu = ischwarzneu +1
						Ivorschaubild.put(ColorHex,(ix,iy)) #schwarz
						
		print(str(iweiss)+" iweiss")
		print(str(iweissneu)+" iweissneu")
		print(str(ischwarz)+" ischwarz")
		print(str(ischwarzneu)+" ischwarzneu")
		
		erstesmal = False
		blackwhite_vorher = blackwhite
		file_path_vorher = FilePath

def ZeichneBild(): # Diese Funktion started Die Zeichnungs Steuerung
	global IstKalibriert # Holt die Globale variabel IstKalibriert
	if IstKalibriert == True: # Wenn IstKalibriert Booleanischen wert True
		zeichnungsSteuerung1.MacheInstruktionsTabelle(bildverarbeiter1,IstKalibriert) #Sagt der zeichnungsSteuerung1 dass sie 
		zeichnungsSteuerung1.ZeicheBild(IstKalibriert)
	else:
		writeToTTerminal("Zuerst Kalibrieren")

def setbwscale(pbwscale):
	global pscale_vorher
	if pbwscale != pscale_vorher:
		bildverarbeiter1.setblackwhite(pbwscale)
		imgdrawcanvasx()
		pscale_vorher = pbwscale

def setCOL(pCOL):
	global blackwhite_vorher
	
	print(pCOL)
	bildverarbeiter1.setColor(pCOL)
	bildverarbeiter1.Imgconverter()
	blackwhite_vorher = -1
	imgdrawcanvasx()

#~ starte MotorCalibratorWindow und gibt schrift und farbe
def MotorCalibratorWinMain():
	MotorCalibrator.MotorCalibratorWin()
	
def MotorCalibratorWinFarbe():
	Farbenundschriften(BackGroundColor,Titlefont,stepper1,stepper2)
	MotorCalibratorWinMain()
	
#~ Returns schrift und farbe wen extern gestarted
def FarbenundschriftenMain():
	return (BackGroundColor, Titlefont,stepper1,stepper2)

	
def IstKalibriert(): 
	global IstKalibriert
	IstKalibriert = True
	
def savefile():
	Logfile.close
	servo.Cleanup()
	
	
	
#~
#~
#~
#~ Test Zone end Functionen
#~
#~
#~





#~
#~
#~ Test Zone end Functionen
#~
#~

atexit.register(savefile) # atexit macht dass wenn file geschlossen wird dass die funktion savefile aufgerufen wird


if __name__ == "__main__": #Wen __name__ == "__main__" dass heist dass wen der name gleich ist wie der name der datei die gestarted wurde 

	#~Screen 
	root = Tk()
	root.geometry('1280x800+0+0') #Legt die grösse des Bildes fesst und wie viel von oben links weg es gespawnt werden soll
	root.title('motor calibrator')

	#~ 
	#~
	#~	Bildverarbeiter 
	#~ 
	#~ 

	#~Title 
	LBildverarbeiter = Label(root,text='Bildverarbeiter',bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=20,y=20, width=600,height=30)
	FBildverarbeiterBorder = Frame(root,bg=BackGroundColor).place(x=20, y=50, width=600,height=453)
	FBiwriteldverarbeiterMain = Frame(root).place(x=23, y=50, width=594,height=450)

	#~Line1
	BBlidLaden = Button(root,text="Bild Laden", command=Imgpathopen).place(x=40, y=70, width=180,height=30)
	LBildName = Label(root,text="")
	LBildName.place(x=240, y=70,height=30)

	#~Line2 
	BFarbwahlBW = Button(root,text="BW",command=lambda:setCOL("BW")).place(x=40,y=120, width=80,height=30)
	BFarbwahlY = Button(root,text="Y",command=lambda:setCOL("Y")).place(x=140,y=120, width=80,height=30)
	BFarbwahlM = Button(root,text="M",command=lambda:setCOL("M")).place(x=240,y=120, width=80,height=30)
	BFarbwahlC = Button(root,text="C",command=lambda:setCOL("C")).place(x=340,y=120, width=80,height=30)

	EFarbauswahl = Entry(root).place(x=460,y=120, width=100,height=30)
	BSubmitEFarbauswahl = Button(root,text="OK").place(x=560,y=120, width=40,height=30)

	#~Line3
	BZeichnen = Button(root,text="Zeichenen", command=ZeichneBild).place(x=40,y=170, width=140,height=30)
	LStatusbar = Label(root,text="ready",bg=BackGroundColor)
	LStatusbar.place(x=200,y=170, width=400,height=30)

	#~Line4
	CImgVorschau = Canvas(root,bg= "white")
	CImgVorschau.place(x=40,y=220,width=Bildwidth,height=Bildwidth)

	Ivorschaubild = PhotoImage(width=bildverarbeiter1.infoBasewidht(),height= bildverarbeiter1.infoBaseheight())
	CImgVorschau.create_image(bildverarbeiter1.infoBasewidht() / 2, bildverarbeiter1.infoBaseheight()/ 2, image=Ivorschaubild)

	CImgZeichenenVorschau = Canvas(root,bg= "white")
	CImgZeichenenVorschau.place(x=330,y=220,width=Bildwidth,height=Bildwidth)

	#~ 
	#~
	#~	Kalibrator 
	#~ 
	#~
	 
	#~Title 
	LKalibrator = Label(root,text='Kalibrator',bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=660,y=20, width=600,height=30)
	FBildverarbeiterBorder = Frame(root,bg=BackGroundColor).place(x=660, y=50, width=600,height=193)
	FBildverarbeiterMain = Frame(root).place(x=663, y=50, width=594,height=190)

	#~Line1
	#~Motor1
	LKalibratorMotor1 = Label(root,text='Motor1',bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=680,y=70, width=270,height=30)
	FKalibratorMotor1Border = Frame(root,bg=BackGroundColor).place(x=680, y=100, width=270,height=73)
	FKalibratorMotor1Main = Frame(root).place(x=683, y=100, width=264,height=70) 

	BKalibratorMotor1L = Button(root,text='Links', repeatinterval=10, repeatdelay=10 , command=lambda: stepper1.drehe(-1,30)).place(x=700,y=120,width=105,height=30)
	BKalibratorMotor1R = Button(root,text='Rechts', repeatinterval=10, repeatdelay=10 , command=lambda: stepper1.drehe(1,30)).place(x=825,y=120,width=105,height=30)

	#~Motor2
	LKalibratorMotor2 = Label(root,text='Motor2',bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=970,y=70, width=270,height=30)
	FKalibratorMotor2Border = Frame(root,bg=BackGroundColor).place(x=970, y=100, width=270,height=73)
	FKalibratorMotor2Main = Frame(root).place(x=973, y=100, width=264,height=70) 

	BKalibratorMotor2L = Button(root,text='Links', repeatinterval=10, repeatdelay=10 , command=lambda: stepper2.drehe(-1,30)).place(x=990,y=120,width=105,height=30)
	BKalibratorMotor2R = Button(root,text='Rechts', repeatinterval=10, repeatdelay=10 , command=lambda: stepper2.drehe(1,30)).place(x=1115,y=120,width=105,height=30)

	#~Line 2
	BSetPrintHead0o0 = Button(root,text="Print Head isch oben Mitte", command= IstKalibriert).place(x=680,y=190,width=270,height=30)

	BSetPrintHead100o100 = Button(root,text="Print Head Is Bottom right Corner",command=zeichnungsSteuerung1.GeheZuNull).place(x=970,y=190,width=270,height=30)

	#~ 
	#~
	#~  Info
	#~ 
	#~ 

	#~ Titel 
	LInfo = Label(root,text='Info',bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=660,y=280, width=600,height=30)
	FInfoBorder = Frame(root,bg=BackGroundColor).place(x=660, y=310, width=600,height=473)
	FInfoMain = Frame(root).place(x=663, y=310, width=594,height=470)

	#~Rechts
	#~Terminal
	LTerminal = Label(root,text="Terminal",bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=906,y=330, width=334,height=30)
	TTerminal = Text(root,bg="black",fg="white")
	TTerminal.place(x=906,y=360, width=334,height=400)

	#~Links 
	#~ Drucker Info 
	LTerminal = Label(root,text="Drucker Info ",bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=680,y=330, width=206,height=30)
	FTerminalBorder = Frame(root,bg=BackGroundColor).place(x=680,y=360, width=206,height=403)
	FTerminalMain = Frame(root).place(x=683,y=360, width=200,height=400)

	#~ Position Druckkopf 
	LDruckerPosLabel = Label(root,text="Drucker Position :").place(x=700,y=380,height=30)
	LDruckerPos = Label(root,text="x/y")
	LDruckerPos.place(x=820,y=380,height=30)

	#~Threads Open
	LThreadsOpenLabel = Label(root,text="Threads Open :").place(x=700,y=430,height=30)
	LThreadsOpen = Label(root,text="0")
	LThreadsOpen.place(x=820,y=430,height=30)

	#~ 
	#~
	#~  Info Motoren
	#~ 
	#~ 
	 
	#~ Titel 
	LInfoMotoren = Label(root,text='Info Motoren',bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=20,y=540, width=600,height=30)
	FInfoMotorenBorder = Frame(root,bg=BackGroundColor).place(x=20, y=570, width=600,height=213)
	FInfoMotorenMain = Frame(root).place(x=23, y=570, width=594,height=210)

	#~ 
	#~Motor1
	#~ 
	LInfoMotorenMotor1 = Label(root,text='Motor 1',bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=40,y=590, width=270,height=30)
	LInfoMotorenMotor1Border = Frame(root,bg=BackGroundColor).place(x=40, y=620, width=270,height=143)
	LInfoMotorenMotor1Main = Frame(root).place(x=43, y=620, width=264,height=140)

	#~Motor1 Grad
	CMotor1Grad = Canvas(root) 
	CMotor1Grad.place(x=59,y=639,width=CMotorGradsize,height=CMotorGradsize)
	CMotor1Grad.create_oval(1,1,100,100,fill=BackGroundColor)

	CMotor1Gradline = CMotor1Grad.create_line(CMotorGradsize / 2,CMotorGradsize / 2,CMotorGradsize / 2,0, fill="red", width=2)

	#~Motor 1 Runden
	LMotor1LabelRunden = Label(root,text="Runden :").place(x=179,y=639)
	LMotor1Runden = Label(root,text="0")
	LMotor1Runden.place(x=239,y=639)

	#~ 
	#~Motor2
	#~  
	LInfoMotorenMotor2 = Label(root,text='Motor 2',bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=330,y=590, width=270,height=30)
	LInfoMotorenMotor2Border = Frame(root,bg=BackGroundColor).place(x=330, y=620, width=270,height=143)
	LInfoMotorenMotor2Main = Frame(root).place(x=333, y=620, width=264,height=140)

	#~Motor2 Grad
	CMotor2Grad = Canvas(root) 
	CMotor2Grad.place(x=349,y=639,width=CMotorGradsize,height=CMotorGradsize)
	CMotor2Grad.create_oval(1,1,100,100,fill=BackGroundColor)

	CMotor2Gradline = CMotor2Grad.create_line(CMotorGradsize / 2,CMotorGradsize / 2,CMotorGradsize / 2,0, fill="red", width=2)

	#~Motor 2 Runden
	LMotor2LabelRunden = Label(root,text="Runden :").place(x=469,y=639)
	LMotor2Runden = Label(root,text="0")
	LMotor2Runden.place(x=529,y=639)


	#~
	#~
	#~ menubar
	#~
	#~

	menubar = Menu(root)

	# create a pulldown menu, and add it to the menu bar
	filemenu = Menu(menubar, tearoff=0)

	#~Open motor calibrator window
	filemenu.add_command(label="Motor Calibrator", command=MotorCalibratorWinFarbe)
	menubar.add_cascade(label="Tools", menu=filemenu)

	# display the menu
	root.config(menu=menubar)

	#~
	#~
	#~
	#~ Test Zone end Tkinter
	#~
	#~
	#~



	#~
	#~
	#~ Test Zone end Tkinter
	#~
	#~

	#~anzahl standart Threads 
	threadsinitial = activeCount() + 1
	#~text wechser
	changetext() 

	root.mainloop()


stepper_steuerungen.stepperclean(stepper1)
stepper_steuerungen.stepperclean(stepper2)

