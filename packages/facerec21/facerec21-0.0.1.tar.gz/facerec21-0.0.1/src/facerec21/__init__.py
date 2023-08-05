#!/usr/bin/env python
import smbus2
from smbus2 import SMBus
from mlx90614 import MLX90614
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
from myemail import sendEmail




def FindEncodings(images):
    encodeList=[]
    for i in images:
        i = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(i)[0]
        encodeList.append(encode)
    return encodeList




# print(encodeKnownList)
def countdown(t):
    while t: # while t > 0 for clarity
      mins = t // 60
      secs = t % 60
      timer = '{:02d}:{:02d}'.format(mins, secs)
      #print("The temperature will be measured in: ")
      print(timer, end="\r") # overwrite previous line
      time.sleep(1)
      t -= 1

#def tempMonitor():


def Attendancesystem(name):
     with open('/home/pi/Desktop/MyPythonFiles/FaceRec/attendance.csv','r+') as f:
         myDataList= f.readlines()
         nameList=[]
         for line in myDataList:
             entry= line.split(',')
             nameList.append(entry[0])
         if name not in nameList:
             now= datetime.now()
             today=datetime.today()
             dtString = now.strftime('%I:%M %p')
             dateStr=today.strftime('%d/%m/%Y')

             bus = SMBus(1)
             sensor = MLX90614(bus, address=0x5A)
             print("The temperature will be measured in: ")
             countdown(5)
             temp = sensor.get_object_1()
             temp=round(temp,2)
             print("The temperature is successfully monitored!")
             if temp<40:
                 status="NORMAL"
             else:
                 status="HIGH"
             f.writelines(f'{name},{dtString},{temp},{status},{dateStr}\n')





def facerec():
    path =  '/home/pi/Desktop/MyPythonFiles/FaceRec/Images'

    images=[]
    classNames=[]
    myList = os.listdir(path)
    print(myList)

    for img in myList:
        CurImg = cv2.imread(f'{path}/{img}')
        images.append(CurImg)
        classNames.append(os.path.splitext(img)[0])

    print(classNames)

    encodeKnownList = FindEncodings(images)

    print('Creation of embeddings completed')

    video = cv2.VideoCapture(0)

    while True:
        success,pic = video.read()
        imgS = cv2.resize(pic,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

        faceLocPerFrame = face_recognition.face_locations(imgS)

        encodeVideoPerFrame = face_recognition.face_encodings(imgS,faceLocPerFrame)

        for eachEncode,faceLoc in zip(encodeVideoPerFrame,faceLocPerFrame):
            compare = face_recognition.compare_faces(encodeKnownList,eachEncode)
            faceDis = face_recognition.face_distance(encodeKnownList,eachEncode)
            #print(faceDis)

            matchIndex = np.argmin(faceDis)

            if compare[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)
                Attendancesystem(name)
                y1,x2,y2,x1= faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(pic,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(pic,(x1,y1-35),(x2,y2),(0,255,0),2)
                cv2.putText(pic,name,(x1+6,y1-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)

        cv2.imshow('Live Webcam',pic)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    sendEmail()