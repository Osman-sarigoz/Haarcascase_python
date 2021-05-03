import math
import numpy as np
numPos=0
a = input("pozitif değer kaç...")
print("\n")
b = input("negatif deger kaç...")
print("\n")
asamaSayisi = input("Asama sayisi kaç olsun? 17 olabilir...")
print("\n")

numPos=str(math.floor((int(a) - int(b)) / (1 + (int(asamaSayisi) - 1)*(1 - 0.995))))
print("Resimlerin Vec uzantılı dosya olusturmak için aşağıdaki kodu çalıştırın\n")
print("opencv_createsamples -info pozitif.txt -num {0} -vec pozitifResim.vec -w 24 -h 24\n".format(a))
print("Yapay zeka modeli oluşturmak için aşağıdaki kodu çalıştırın\n")
print("opencv_traincascade -data XML -vec pozitifResim.vec -bg negatif.txt -numPos {0} ".format(int(numPos))+"-numNeg {0}".format(int(b))+" -numStages {0}".format(int(asamaSayisi))+" -minHitRate 0.995 -maxFalseAlarmRate 0.25 -mem 600 -w 24 -h 24\n")
        
