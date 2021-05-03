from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
   
camera = PiCamera()
camera.resolution =(320,240)
camera.framerate =32
rawCapture=PiRGBArray(camera,size=(320,240))
time.sleep(0.1)

model_sol=cv2.CascadeClassifier("sol/XML/cascade.xml")
model_geri=cv2.CascadeClassifier("geri/XML/cascade.xml")
model_sag=cv2.CascadeClassifier("sag/XML/cascade.xml")
model_ileri=cv2.CascadeClassifier("ileri/XML/cascade.xml")

for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
           
    img = frame.array
    tabela_sol = model_sol.detectMultiScale(img, 1.1, 1)
    tabela_sag = model_sag.detectMultiScale(img, 1.1, 1)
    tabela_geri = model_geri.detectMultiScale(img, 1.1, 1)
    tabela_ileri = model_ileri.detectMultiScale(img, 1.1, 1)
    for (x,y,w,h) in tabela_sol:
        cv2.putText(img, 'SOL', (x+10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255),2)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    
    for (x,y,w,h) in tabela_sag:
        cv2.putText(img, 'SAG', (x+10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255),2)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
     
    for (x,y,w,h) in tabela_geri:
        cv2.putText(img, 'GERI', (x+10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255),2)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        
    for (x,y,w,h) in tabela_ileri:
        cv2.putText(img, 'ILERI', (x+10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255),2)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        
    cv2.imshow("Ekran",img)
    key=cv2.waitKey(1)&0xFF
    
    rawCapture.truncate(0)
 
    if key==ord("q"):
        break
cv2.destroyAllWindows()
camera.close()
