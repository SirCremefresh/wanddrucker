import datetime

filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
Logfile = open("/home/pi/Desktop/donato ordnet stepper um/Log//" + filename1+".txt","w+")

Logfile.close
