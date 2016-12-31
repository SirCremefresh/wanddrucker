#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import stepper_steuerungen
from stepper import steppermotor
from threading import Timer
from threading import Thread
from threading import activeCount


def Motordreh(pMotor1dreh, pMotor2dreh):
	try:
		Motor1dreh = int(pMotor1dreh)
	except ValueError:
		Motor1dreh = 0
	try:
		Motor2dreh = int(pMotor2dreh)
	except ValueError:
		Motor2dreh = 0

	t = Thread(target=stepper_steuerungen.drehe2,args=(stepper1,Motor1dreh , stepper2,Motor2dreh))
	t.start()
	


def MotorCalibratorWin():
	
	MotorCalibrator = Tk()
	MotorCalibrator.geometry('640x320+0+0')
	MotorCalibrator.title('MotorCalibrator')
	
	#~
	#~ Title
	#~
	LMotorCalibrator = Label(MotorCalibrator,text="MotorCalibrator",bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=20,y=20, width=600,height=30)
	FMotorCalibratorBorder = Frame(MotorCalibrator,bg=BackGroundColor).place(x=20, y=50, width=600,height=253)
	FMotorCalibratorMain = Frame(MotorCalibrator).place(x=23, y=50, width=594,height=250)
	
	#~ title  Motor Left
	LMotorLeft = Label(MotorCalibrator,text="Motor Left",bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=40,y=70, width=270,height=30)
	FMotorLeftBorder = Frame(MotorCalibrator,bg=BackGroundColor).place(x=40, y=100, width=270,height=183)
	FMotorLeftMain = Frame(MotorCalibrator).place(x=43, y=100, width=264,height=180)
	
	#~ title  Motor Right
	LMotorRight = Label(MotorCalibrator,text="Motor Right",bg=BackGroundColor,fg="white",font=(Titlefont)).place(x=330,y=70, width=270,height=30)
	FMotorRightBorder = Frame(MotorCalibrator,bg=BackGroundColor).place(x=330, y=100, width=270,height=183)
	FMotorRightMain = Frame(MotorCalibrator).place(x=333, y=100, width=264,height=180)
	
	#~ Bridge betwen M1 and M2 
	FMotorLeftBorder = Frame(MotorCalibrator,bg=BackGroundColor).place(x=310, y=157, width=20,height=126)
	FMotorLeftMain = Frame(MotorCalibrator).place(x=43, y=160, width=350,height=120)
	
	#~  Motor Left
	BKalibratorMotor1L = Button(MotorCalibrator,text='Links', repeatinterval=10, repeatdelay=10 , command=lambda: stepper1.drehe(-1)).place(x=60,y=120,width=105,height=30)
	BKalibratorMotor1R = Button(MotorCalibrator,text='Rechts', repeatinterval=10, repeatdelay=10 , command=lambda: stepper1.drehe(1)).place(x=185,y=120,width=105,height=30)
	
	Motor1entry = Entry(MotorCalibrator) 
	Motor1entry.place(x=60,y=180,width=185,height=30)

	
	#~ Motor Right
	
	BKalibratorMotor2L = Button(MotorCalibrator,text='Links', repeatinterval=10, repeatdelay=10 , command=lambda: stepper2.drehe(-1)).place(x=350,y=120,width=105,height=30)
	BKalibratorMotor2R = Button(MotorCalibrator,text='Rechts', repeatinterval=10, repeatdelay=10 , command=lambda: stepper2.drehe(1)).place(x=475,y=120,width=105,height=30)
	
	Motor2entry = Entry(MotorCalibrator)
	Motor2entry.place(x=390,y=180,width=190,height=30)


	#~ submit m1 m2 in Grad
	Entrysubmit = Button(MotorCalibrator, text="Submit", bg="grey", command=lambda: Motordreh(Motor1entry.get(), Motor2entry.get())).place(x=265,y=180,width=105,height=30)
	
	#~ nur main windon wir geschlossen
	BQuit = Button(MotorCalibrator, text="Fertig", command=MotorCalibrator.destroy).place(x=60,y=230, width=520,height=30)
	
	
	
	
	
	MotorCalibrator.mainloop()

#~ holt die farben
def Farbenundschriften(pBackGroundColor,pTitlefont,pstepper1,pstepper2,*args):
	global BackGroundColor
	global Titlefont
	global stepper1
	global stepper2
	BackGroundColor = pBackGroundColor
	Titlefont = pTitlefont
	
	stepper1 = pstepper1
	stepper2 = pstepper2
	
	
if __name__ == "__main__":
	import Schoenes_GUI_teil_2
	BackGroundColor, Titlefont, stepper1, stepper2 = Schoenes_GUI_teil_2.FarbenundschriftenMain()
	MotorCalibratorWin()



