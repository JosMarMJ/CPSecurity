import cv2
import os
import imutils
import urllib.request
import numpy as np
from urllib.request import urlopen

personName = 'Angie'
dataPath = 'C:/Proyecto de Ciberfisicos/Reconocimiento facial/Data' #Cambia a la ruta donde hayas almacenado Data
personPath = dataPath + '/' + personName

if not os.path.exists(personPath):
  print('Carpeta creada: ',personPath)
  os.makedirs(personPath)

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
count = 2100

#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#cap = cv2.VideoCapture('Joselyn.mp4')

#Descomentar solo para ESP32CAM
stream = urlopen('http://192.168.100.120')
bytes = bytes()
#

while True:

  '''
  #Camara y Video Normal
  ret, frame = cap.read()
  if ret == False: break
  #
  '''

  #Descomentar solo para ESP32CAM
  bytes += stream.read(1024)
  a = bytes.find(b'\xff\xd8')
  b = bytes.find(b'\xff\xd9')
  if a != -1 and b != -1:
    jpg = bytes[a:b+2]
    bytes = bytes[b+2:]
    if jpg :
      frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
  

      frame =  imutils.resize(frame, width=640)
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      auxFrame = frame.copy()

      faces = faceClassif.detectMultiScale(gray,1.3,5)

      for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(personPath + '/rotro_{}.jpg'.format(count),rostro)
        count = count + 1
      cv2.imshow('frame',frame)

      k =  cv2.waitKey(1)
      if k == 27 or count >= 2200:
        break

#cap.release()
cv2.destroyAllWindows()
