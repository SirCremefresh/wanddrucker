#!/usr/bin/python
# -*- coding: utf-8 -*-
from Bildverarbeiter import Bildverarbeitung
from Zeichner import ZeichnerClass
from time import sleep
from servo import servoClass
from StaticParameters import statischeParameter
import sys

sys.setrecursionlimit(10000) # 10000 is an example, try with different values

class Zeichnungssteuerung:
	def __init__(self,pstepper1,pstepper2,pservo):
		# self.instrX = []
		# self.instrY = []
		# self.instrRunden = []
		# self.instrZeile = -1
		
		self.stepper1 = pstepper1
		self.stepper2 = pstepper2
		self.servo = pservo
		
		self.ZeichnerClass = ZeichnerClass(self.stepper1, self.stepper2,self.servo)
		
		self.abstandx = statischeParameter.BildAbstandLinks
		self.abstandy = statischeParameter.BildAbstandOben
		
	def MacheInstruktionsTabelle(self,pbildverarbeiter,IstKalibriert):
		im_x = pbildverarbeiter.infoBasewidht()
		im_y = pbildverarbeiter.infoBaseheight()
		im_array = pbildverarbeiter.infoImgArray()	
		blackwhite = pbildverarbeiter.infoblackwhite()
		Blackpx = 0
		runde = 0
		self.instrX = []
		self.instrY = []
		self.instrRunden = []
		self.instrZeile = -1
		

		
		print("MacheInstruktionsTabelle")
		#~ print(im_x + " " + im_y)
		
		def fillinstr(pix,piy):
			global instrZeile
			
			self.instrZeile = self.instrZeile +1
			
			if self.instrZeile == 0:
				runde = 1
				diffy = 0
				diffx = 0
			else:
				diffx = abs(self.instrX[self.instrZeile-1]-(pix + self.abstandx))
				diffy = abs(self.instrY[self.instrZeile-1]-piy)
				
				if diffx <= 1 and diffy <= 1:
					runde = self.instrRunden[self.instrZeile-1]
				else:
					runde = self.instrRunden[self.instrZeile-1] + 1
			
			print ("I: self.instrZeile = "+str(self.instrZeile)+" / pix = "+str(pix)+" / piy = "+str(piy)+" / runde = "+str(runde)+" / diffx"+str(diffx)+" / diffy"+str(diffy)+"\n")
			im_array[pix][piy] = runde	
			self.instrX.append(pix + self.abstandx)
			self.instrY.append(piy)
			self.instrRunden.append(runde)
			
			
			
			#print ("runden= ",runde," x= ",pix + 180," y= ",piy)
			print "self.ZeichnerClass.GeheZu(" + str(pix + self.abstandx) + "," + str(piy) + ",0)"
			
		def FindeNachbar(pix,piy):
			
			
			#~ print(str(runde) + " " + str(pix) + " " + str(piy))         [self.instrZeile]
			def PixelZuZeichen(pix,piy):
				
				if pix < 0 or piy < 0 or piy > im_y -1 or pix > im_x - 1: #ist pixel auserhalb des bildes
					return False
				
				elif im_array[pix][piy] == 9999: 
					return True

				else:
					
					return False
				
					
			for i in range(1,5):
				for ix in range(2*i+1):
					for iy in range(2*i+1):
					#	print("I: pix = "+str(pix)+" / piy = "+str(piy)+" / i = "+str(i)+" / ix = "+str(ix-i)+" / iy = "+str(iy-i)+" / istneu"+str("")+"\n")
						if abs(ix-i) == i or abs(iy-i) == i:
							istneu = PixelZuZeichen(pix+ix-i,piy+iy-i)
							
							if istneu:
								fillinstr(pix+ix-i, piy+iy-i)
								FindeNachbar(pix+ix-i, piy+iy-i)
								
			
		
		#alle Pixel die man malen muss auf 9999 setzen
 		for iy in range (im_y):
			for ix in range(im_x):
				if im_array[ix][iy] <= blackwhite:  #255==schwarz  0==weiss
					im_array[ix][iy] = 9999
					Blackpx = Blackpx +1
				else:
					im_array[ix][iy] = 0
					
						
		for iy in range (im_y):
			for ix in range(im_x):
				if im_array[ix][iy] == 9999:
					fillinstr(ix,iy)
					FindeNachbar(ix,iy)	
					
		for iy in range (im_y):
			zeile = ""
			for ix in range(im_x):
				px = im_array[ix][iy]
				zeile = zeile + "-" + str(px)
			print("I:" + str(zeile)+"\n")	
		
		
			
	def ZeicheBild(self,pIstKalibriert):
		if pIstKalibriert == True:
			self.ZeichnerClass.Nullpunkt()
		
		self.ZeichnerClass.GeheZu(self.abstandx,0,0)
		LetzteRundenNummer = -1
		
		for iy in range (len(self.instrX)):
			#print("I:"+str(self.instrRunden[iy]) + " " + str(self.instrX[iy]) + " " + str(self.instrY[iy]))
			if LetzteRundenNummer == self.instrRunden[iy]:
				stift = 1
			else:
				stift = 0
			
			
			self.ZeichnerClass.GeheZu(self.instrX[iy],self.instrY[iy],stift)
	
			LetzteRundenNummer = self.instrRunden[iy]
			
		self.ZeichnerClass.GeheZu(self.abstandx,0,0) #~ Zurueck zum nullpunkt
		
	def GeheZuNull(self):
		self.ZeichnerClass.Nullpunkt()
		self.ZeichnerClass.GeheZu(209,0,0)
		self.ZeichnerClass.GeheZu(209,34,0)
		self.ZeichnerClass.GeheZu(243,34,0)
		self.ZeichnerClass.GeheZu(180,34,0)
		self.ZeichnerClass.GeheZu(209,34,0)
		self.ZeichnerClass.GeheZu(209,62,0)
		
		self.ZeichnerClass.GeheZu(234,0,0)
