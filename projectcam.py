# these imports let you use opencv
import cv2 #opencv itself
import numpy as np # matrix manipulations
from matplotlib import pyplot as plt
import pylab
pylab.rcParams['figure.figsize'] = (10.0, 8.0)
import ctypes  # An included library with Python install.


cap = cv2.VideoCapture(0)
img_counter = 0 
face_find = False
flag, img = cap.read() # get an initial frame
cv2.namedWindow('Camera') # open a window for output
cv2.imshow('Camera',img) # put the image in the output window

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def detect_face(img):
    face_img = img.copy()
    grey = cv2.cvtColor(face_img,cv2.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(grey)
    if len(face_rects) == 0:
        face_find = False
    for (x,y,w,h) in face_rects:
        re = cv2.rectangle(face_img, (x,y), (x+w, y+h), (255,255,255), 10)
        if 're' in locals():
            face_find = True
    return face_img, face_find

def face_crop(face_img):
    grey = cv2.cvtColor(face_img,cv2.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(grey)
    for (x,y,w,h) in face_rects:
        face = face_img[y:y + h, x:x + w]
    return face
    

while True:

    #read a frame from the video capture obj
    flag, img = cap.read()
    face_img, face_find = detect_face(img)
    output_image=face_img.copy()
    cv2.imshow('Camera',face_img) # put the image in the output window
    key = cv2.waitKey(1)
    # wait for someone to press escape then destroy the output window 
    if key%256  == 27:
        # esc pressed
        cv2.destroyAllWindows()
        break
    elif key%256  == 32:
        # SPACE pressed
        if face_find == True:
            img_name = "img/Face_{}.jpg".format(img_counter)
            img = face_crop(face_img)
            cv2.imwrite(img_name, img)
            print("{} written!".format(img_name))
            img_counter += 1
