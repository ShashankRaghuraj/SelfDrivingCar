import cv2
import RPi.GPIO as GPIO
from time import sleep
import time
#face cascade
stop_cascade = cv2.CascadeClassifier('classifiers/StopSign.xml')

cap = cv2.VideoCapture(0)
in1 = 24
in2 = 23
en = 25
temp1=1
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(75)
try:
    while cap.isOpened():
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        StopSigns = stop_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y , w, h) in StopSigns:
            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0,0), 2)
            strX = str(x)
            strY = str(y)

        intStop = int(len(StopSigns))
        strStop = str(len(StopSigns))
        font = cv2.FONT_HERSHEY_SIMPLEX
        if intStop >= 1:
            status = "stop"
        if intStop < 1:
            status = "go"
        if status == "go":
            cv2.putText(img , "Status: " + status, (30,30) , font, 0.5 ,(0,255,0),2,)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
        if status == "stop":
            cv2.putText(img , "Status: " + status, (30,30) , font, 0.5,(0,0,255),2,)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            time.sleep(5)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)


        cv2.imshow("Jeep Vision", img)

        k = cv2.waitKey(1)

except KeyboardInterrupt:
    cap.release()
