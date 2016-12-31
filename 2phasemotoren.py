#!/usr/bin/python from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperM$


from Adafruit_MotorHAT import *

 
import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr = 0x60)


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)


myStepper = mh.getStepper(200, 1)       # 200 steps/rev, motor port #1

myStepper.setSpeed(10)                  # 30 RPM


	#print("Single coil steps")
	#myStepper.step(200, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)
#~ myStepper.step(200, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	#print("Double coil steps")
	#myStepper.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
	#myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
#~ print("Interleaved coil steps")
#~ myStepper.step(400, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
	#~ myStepper.step(400, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
	#print("Microsteps")
#~ myStepper.step(200, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
#~ myStepper.step(7, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
myStepper.step(6, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
myStepper.setSpeed(1.32231)
myStepper.step(6, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)


