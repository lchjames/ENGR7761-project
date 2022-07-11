# these imports let you use opencv
# An included library with Python install.
import ctypes  
import cv2,sys,os,dlib,glob,imutils,pylab,time,atexit
import numpy as np # matrix manipulations
from matplotlib import pyplot as plt
from skimage import io
# GUI
import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo
# fernet for encryption and decryption
from cryptography.fernet import Fernet, InvalidToken


cap = cv2.VideoCapture(0)
try_counter = 0 
face_find = False
too_many_face = False
able_to_access = False
encrypted = False
msg = ""
lname = ""
window = tk.Tk()
lname_var = tk.StringVar()
name_label = tk.Label(window, text = 'Please input your name: ')
name_entry = tk.Entry(window,textvariable = lname_var)

# lname = input("Please input your name: ")
# lname = lname.lower()
getusername = False
flag, img = cap.read() # get an initial frame
#cv2.namedWindow('Camera') # open a window for output
#cv2.imshow('Camera',img) # put the image in the output window
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
baseUrl = './To be encrypt'
test = baseUrl + "/" + "test.test"
keyname = baseUrl + "/" + "key.key"

def goodbye(): # make sure the file are encrypt when exit
    with open(test, 'rb') as infile:
            data = infile.read()
            try:
                f = Fernet(key)
                f.decrypt(data, None)
            except InvalidToken:
                print ("file is now encrypted")
                alist = next(os.walk(baseUrl))[2]
                for i in range(len(alist)):
                    afile = alist[i]
                    if afile[-4:] != '.key':
                        encryptFile(afile, key)

def popup_showinfo(msg):
    showinfo("Error", msg)
    
def load_key():
    return open(keyname, "rb").read()

def write_key():
    key = Fernet.generate_key()
    with open(keyname, "wb") as key_file:
        key_file.write(key)

def decryptFile(filename, key):
    f = Fernet(key)
    filename = baseUrl +"/"+ filename
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
        
def encryptFile(filename, key):
    f = Fernet(key)
    filename = baseUrl +"/"+ filename
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def detect_face(img):
    face_find = False
    too_many_face = False
    face_img = img.copy()
    grey = cv2.cvtColor(face_img,cv2.COLOR_BGR2GRAY)
    face_rects = []
    face_rects = face_cascade.detectMultiScale(grey)
    facenum = len(face_rects)
    if facenum == 0:
        face_find = False
    elif facenum >= 2:
        too_many_face = True
    for (x,y,w,h) in face_rects:
        re = cv2.rectangle(face_img, (x,y), (x+w, y+h), (255,255,255), 10)
        if 're' in locals():
            face_find = True
    return face_img, face_find, too_many_face, facenum

def face_crop(face_img):
    grey = cv2.cvtColor(face_img,cv2.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(grey)
    for (x,y,w,h) in face_rects:
        face = face_img[y:y + h, x:x + w]
    return face

def findface(img_name):
    faceimg = io.imread(img_name)
    dets = detector(faceimg, 1)
    dist = []
    os.remove(img_name)
    for k, d in enumerate(dets):
        shape = sp(faceimg, d)
        face_descriptor = facerec.compute_face_descriptor(faceimg, shape)
        d_test = np.array(face_descriptor)

        x1 = d.left()
        y1 = d.top()
        x2 = d.right()
        y2 = d.bottom()
        cv2.rectangle(faceimg, (x1, y1), (x2, y2), ( 0, 255, 0), 4, cv2. LINE_AA)
        for i in descriptors:
            dist_ = np.linalg.norm(i -d_test)
            dist.append(dist_)
    c_d = []
    c_d = dict(zip(candidate,dist))
    cd_sorted = sorted(c_d.items(), key = lambda d:d[1])
    print (cd_sorted)
    if cd_sorted != []:
        if cd_sorted[0][1] < 0.295:
            rec_name = cd_sorted[0][0]
            able_to_access = True
        else:
            rec_name = "Face not in database--"
            able_to_access = False
    else:
        rec_name = "There is no face--"
        able_to_access = False
    return rec_name

def get_username():
    global lname
    global getusername
    global encrypted,try_counter
    
    lname=lname_var.get().lower()
    print("The name is : " + lname)
    if lname != "" :
        getusername = True
    else :
        getusername = False
    while (getusername):
        try:
            #read a frame from the video capture obj
            flag, img = cap.read()
            face_img, face_find, too_many_face, facenum = detect_face(img)
            output_image=face_img.copy()
            img_name = "img/test.jpg"
            cv2.imwrite(img_name, output_image)
            name = findface(img_name)[:-2]
            print("This matchs with "+name) #show what user does the system detected

            if lname == name and encrypted == True:
                try_counter = 0
                if too_many_face == True:
                    msg = "There are people around you, program close: face count = " + str(facenum)
                    popup_showinfo(msg)
                with open(test, 'rb') as infile:
                    data = infile.read()
                    f = Fernet(key)
                    f.decrypt(data, None)
                    print ("file is now decrypted")
                    alist = next(os.walk(baseUrl))[2]
                    for i in range(len(alist)):
                        afile = alist[i]
                        if afile[-4:] != '.key':
                            decryptFile(afile, key)
                encrypted = False

            elif lname != name and encrypted == False:
                try_counter = try_counter + 1
                if face_find == False:
                    print ("The system can't find a face")
                msg = "Face not match"
                popup_showinfo(msg)
                with open(test, 'rb') as infile:
                    data = infile.read()
                    try:
                        f = Fernet(key)
                        f.decrypt(data, None)
                    except InvalidToken:
                        print ("file is now encrypted")
                        alist = next(os.walk(baseUrl))[2]
                        for i in range(len(alist)):
                            afile = alist[i]
                            if afile[-4:] != '.key':
                                encryptFile(afile, key)
                encrypted = True
            elif lname != name:
                msg = "Face not match"
                popup_showinfo(msg)
                try_counter = try_counter + 1
                print ("Error try: ", try_counter)    

            if try_counter >= 3:
                msg = "Too many error tries, program close"
                popup_showinfo(msg)
                break
            
            input("Press Enter to continue...")
            if 'normal' != window.state():
                break
            else :
                print("running")
        except Exception as e:
            print(e)
            break
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            break
        
    

predictor_path = "shape_predictor_68_face_landmarks.dat"
face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"
faces_folder_path = "./img"

#ensure the files are encrypted
if os.path.isfile(keyname) == False :
    write_key()
else:
    key = load_key()
with open(test, 'rb') as infile: #Ensure the file are encrypted
    data = infile.read()
    try:
        f = Fernet(key)
        f.decrypt(data, None)
    except InvalidToken:
        alist = next(os.walk(baseUrl))[2]
        for i in range(len(alist)):
            afile = alist[i]
            if afile[-4:] != '.key':
                encryptFile(afile, key)
    encrypted = True
    
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
descriptors = []
candidate = []

#load the image database
for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    base = os.path.basename(f)
    candidate.append(os.path.splitext(base)[ 0])
    img = io.imread(f)
    dets = detector(img, 1)
    for k, d in enumerate(dets):
        shape = sp(img, d)
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        v = np.array(face_descriptor)
        descriptors.append(v)
    
#main process
sub_btn=tk.Button(window,text = 'Submit', command = get_username)
name_label.grid(row=0,column=0)
name_entry.grid(row=1,column=0)
sub_btn.grid(row=2,column=0)

window.mainloop()
atexit.register(goodbye)
