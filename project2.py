import numpy as np
import cv2
import pickle


# for serial port
import serial
import time
 
#############################################
 
frameWidth= 640         # CAMERA RESOLUTION
frameHeight = 480
brightness = 180
threshold = 0.90         # PROBABLITY THRESHOLD
font = cv2.FONT_HERSHEY_SIMPLEX
# initializing arduino
arduino = serial.Serial(port='COM3',  baudrate=115200, timeout=.1)
##############################################
 
# SETUP THE VIDEO CAMERA
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, brightness)
# IMPORT THE TRANNIED MODEL
pickle_in=open("model_trained.p","rb")  ## rb = READ BYTE
model=pickle.load(pickle_in)
 
def grayscale(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return img


def equalize(img):
    img =cv2.equalizeHist(img)
    return img


def preprocessing(img):
    img = grayscale(img)
    img = equalize(img)
    img = img/255
    return img


def getClassName(classNo):
    if   classNo == 0: return '20'
    elif classNo == 1: return '30'
    elif classNo == 2: return '50'
    elif classNo == 3: return '60'
    elif classNo == 4: return '70'
    elif classNo == 5: return '80'
    elif classNo == 6: return '90'
    elif classNo == 7: return '100'
    elif classNo == 8: return '120'


# to send signal in arduino
def write_read(x):
    arduino.write(bytes(x,  'utf-8'))
    time.sleep(0.05)
    # data = arduino.readline()
    # return data
 
while True:
 
    # READ IMAGE
    success, imgOrignal = cap.read()
    
    # PROCESS IMAGE
    img = np.asarray(imgOrignal)
    img = cv2.resize(img, (32, 32))
    img = preprocessing(img)
    cv2.imshow("Processed Image", img)
    img = img.reshape(1, 32, 32, 1)
    cv2.putText(imgOrignal, "CLASS: " , (20, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(imgOrignal, "PROBABILITY: ", (20, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
    # PREDICT IMAGE
    predictions = model.predict(img)
    classIndex = np.argmax(predictions, axis=-1)[0]
    probabilityValue =np.amax(predictions)
    if probabilityValue > threshold:

        cv2.putText(imgOrignal,str(classIndex)+" "+str(getClassName(classIndex)), (120, 35), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(imgOrignal, str(round(probabilityValue*100,2) )+"%", (180, 75), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

        write_read(getClassName(classIndex))
        # time.sleep(3)
    cv2.imshow("Result", imgOrignal)
    
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()