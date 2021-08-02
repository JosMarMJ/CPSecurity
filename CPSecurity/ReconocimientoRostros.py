import cv2
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import imutils
import urllib.request
import numpy as np
from urllib.request import urlopen


#Firebase
cred=credentials.Certificate('proyecto-ciber-sdk.json')
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://proyecto-ciber-default-rtdb.firebaseio.com/'  
})

dataPath = 'C:/Users/josel/Desktop/Reconocimiento Facial/Data'
imagePaths = os.listdir(dataPath)
print('imagePaths=',imagePaths)


#face_recognizer = cv2.face.EigenFaceRecognizer_create()
#face_recognizer = cv2.face.FisherFaceRecognizer_create()
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Leyendo el modelo
#face_recognizer.read('modeloEigenFace.xml')
#face_recognizer.read('modeloFisherFace.xml')
face_recognizer.read('modeloLBPHFace.xml')


###Modos de obtención de imagen

#cap = cv2.VideoCapture(0)  #Camara
#cap = cv2.VideoCapture('JoselynP.mp4')  #Video

#Descomentar solo para ESP32CAM
stream = urlopen('http://192.168.100.53/')
bytes = bytes()
#


faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

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
      #

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()

            faces = faceClassif.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:
                rostro = auxFrame[y:y+h,x:x+w]
                rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro)
                # print(result) #Numeros obtenidos

                cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
                
                # EigenFaces
                '''
                if result[1] < 5700:
                    cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                    nombre='{}'.format(imagePaths[result[0]])
                    
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
                    nombre='Desconocido'
                
                
                # FisherFace
                if result[1] < 500:
                    cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                    nombre='{}'.format(imagePaths[result[0]])
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
                    nombre='Desconocido'
                '''
                # LBPHFace
                if result[1] < 70:
                    cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                    nombre='{}'.format(imagePaths[result[0]])
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
                    nombre='Desconocido'
                

                print(nombre)
                #Mandar datos
                ref=db.reference('/')
                emp_ref=ref.child('Proyecto')
                emp_ref.update({
                 'Reconocimiento':nombre     
                })
                
                        
            cv2.imshow('frame',frame)
            k = cv2.waitKey(1)
            if k == 27:
                break

#cap.release()
cv2.destroyAllWindows()
