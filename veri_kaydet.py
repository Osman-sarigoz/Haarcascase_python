from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import os
import math
from imutils.perspective import four_point_transform
camera = PiCamera()
camera.resolution =(320,240)
camera.framerate =32
rawCapture=PiRGBArray(camera,size=(320,240))
time.sleep(0.1)

def nothing(x):
    return
cv2.namedWindow("Ekran",cv2.WINDOW_AUTOSIZE)
genislik = 80
cv2.createTrackbar("Genislik_1","Ekran",genislik, 160 , nothing)
genislik1 = 80
cv2.createTrackbar("Genislik_2","Ekran",genislik1, 160, nothing)
yukseklik = 60
cv2.createTrackbar("Yukseklik_1","Ekran",yukseklik, 120, nothing)
yukseklik1 = 60
cv2.createTrackbar("Yukseklik_2","Ekran",yukseklik1, 120, nothing)
pozitif=open("pozitif.txt","w")
negatif=open("negatif.txt","w")
numPos=0
minHitRate=0.995
a=0
b=0
for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    frame= frame.array
    frame_img = np.copy(frame)
    genislik=cv2.getTrackbarPos("Genislik_1", "Ekran")
    genislik1=cv2.getTrackbarPos("Genislik_2", "Ekran")
    yukseklik=cv2.getTrackbarPos("Yukseklik_1", "Ekran")
    yukseklik1 =cv2.getTrackbarPos("Yukseklik_2", "Ekran")
    xeks1 = 50
    xeks2 = 110
    yeks1 = 30
    yeks2 = 90
    xeks1 = int((320 - (genislik * 2)) / 2)
    xeks2 = int(xeks1 + (genislik1 * 2))
    yeks1 = int((240 - (yukseklik * 2)) / 2)
    yeks2 = int(yeks1 + (yukseklik1 * 2))
    cv2.line(frame,(xeks1, 0),(xeks1, 240),(255, 255, 255), 1)
    cv2.line(frame,(xeks2, 0),(xeks2, 240),(255, 255, 255), 1)
    cv2.line(frame,(0, yeks1),(320, yeks1),(255, 255, 255), 1)
    cv2.line(frame,(0, yeks2),(320, yeks2),(255, 255, 255), 1)
    box=[[xeks1,yeks1],[xeks1,yeks2],[xeks2,yeks2],[xeks2,yeks1]]
    box = np.int0(box)
    cv2.drawContours(frame,[box],0,(255,255,255),1)
    warped = four_point_transform(frame, [box][0])
    cv2.imshow("istenilen alan",warped)
    
    height, width = warped.shape[:2]
    key=cv2.waitKey(1)&0xFF
 
    rawCapture.truncate(0)
    if key==ord("1"):
        a+=1
        cv2.imwrite("pozitif/"+str(a)+".jpg", frame_img)
        pozitif.write("pozitif/"+str(a) + ".jpg  " + str(1) + " " + str(xeks1) + " " + str(yeks1) +" " +str(xeks2-xeks1) + " " +str(yeks2-yeks1)+ "\n" )
    if key==ord("0"):
        b+=1
        cv2.imwrite('negatif/'+str(b)+'.jpg', frame_img)
        negatif.write("negatif/"+str(b) + ".jpg " + "\n" )
    
    if key==ord("2"):
        asamaSayisi = input("Asama sayisi kaç olsun? 17 olabilir...")
        print("\n")
        numPos=str(math.floor((a - b) / (1 + (int(asamaSayisi) - 1)*(1 - minHitRate))))
        print("Resimlerin Vec uzantılı dosya olusturmak için aşağıdaki kodu çalıştırın\n")
        print("opencv_createsamples -info pozitif.txt -num {0} -vec pozitifResim.vec -w 24 -h 24\n".format(a))
        print("Yapay zeka modeli oluşturmak için aşağıdaki kodu çalıştırın\n")
        print("opencv_traincascade -data XML -vec pozitifResim.vec -bg negatif.txt -numPos {0} ".format(int(numPos))+"-numNeg {0}".format(int(b))+" -numStages {0}".format(int(asamaSayisi))+" -minHitRate 0.995 -maxFalseAlarmRate 0.25 -mem 600 -w 24 -h 24\n")
        pozitif.close()
        negatif.close()
    if key==ord("q"):
        break
    font = cv2.FONT_HERSHEY_DUPLEX
    text = 'Pozitif Deger:' + '{0}'.format(a)
    cv2.putText(frame, text, (10,20), font, 0.5, (0,255,255), 1, cv2.LINE_AA)
    text1 = 'Negatif Deger:' + '{0}'.format(b)
    cv2.putText(frame, text1, (10,40), font, 0.5, (0,255,255), 1, cv2.LINE_AA)
    text2 = 'Pozitif icin [1] Negatif icin [0] basin... '
    cv2.putText(frame, text2, (10,210), font, 0.5, (0,255,255), 1, cv2.LINE_AA)
    text2 = 'Model bilgisi icin [2] basin...'
    cv2.putText(frame, text2, (10,230), font, 0.5, (0,255,255), 1, cv2.LINE_AA)
    cv2.imshow("Ekran",frame)
cv2.destroyAllWindows()
camera.close()
