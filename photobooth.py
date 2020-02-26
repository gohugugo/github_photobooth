from PIL import Image as im
from Adafruit_Thermal import *
import RPi.GPIO as gp
import os


def shootAndPrint():
    os.system("sudo fswebcam -r 640x480 --no-banner /home/pi/photobooth/photo1.png")
    pt = Adafruit_Thermal("/dev/serial0",19200,timeout=5)
    #pt.println("test")
    pic = im.open("/home/pi/photobooth/photo1.png")
    pic2=pic.rotate(-90).resize((384,512), im.ANTIALIAS).convert("1")
    pic2.save("photo2.bmp")
    data = list(pic2.getdata())
    echauffement = [170]*9600
    print(len(data))
    L = []
    for x in data:
        if x==0:
            L.append(1)
        else:
            L.append(0)
    print("done")
    M = []
    i = 0
    while i < 196608:
        oct = 0
        for k in range(7,-1,-1):
            #print(i)
            #print(k)
            oct += L[i]*(2**k)
            i += 1
        M.append(oct)
    print(len(M))
    #pt.printBitmap(384,200, echauffement)
    #pt.feed(2)
    pt.printBitmap(384,512,M, True)

gp.setmode(gp.BOARD)
gp.setup(11, gp.IN, gp.PUD_UP)

while 1:
    print("Programme photobooth lance avec python, attente d'un appui suur le bouton")
    gp.wait_for_edge(11, gp.FALLING)
    shootAndPrint()
    
   

    
