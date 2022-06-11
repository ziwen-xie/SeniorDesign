import tkinter as tk
from tkinter.font import Font
import os
from record_start import record_start
from PIL import ImageTk, Image, ImageOps
from threading import Thread
from time import sleep
import picamera
from picamera import PiCamera
import RPi.GPIO as GPIO
import numpy as np
import skimage.color
import skimage.io
import matplotlib.pyplot as plt
import matplotlib.image as img
from matplotlib import image as mpimg
from threading import Thread
import io
import sys
import cv2
from record_start import record_start

from threading import Thread
import io
import sys
import cv2
from scipy import signal


def butter_lowpass(cutoff,fs,order):
    return butter(order,cutoff,fs=fs,btype='low',analog=False)

def butter_lowpass_filter(data,cutoff,fs,order):
    b,a = butter_lowpass(cutoff,fs,order = order)
    y = lfilter(b,a,data)
    return y

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    gray = 0.2989*r + 0.5870*g + 0.1140*b
    return gray

def ana4(r):
    count  = 0
    im = cv2.imread("red.jpg")
    
    
    #r = cv2.selectROI(im)
    #print(r)    
    current_dir = os.getcwd()
    red = "red.h264"
    nir = "nir.h264"
    red_v = os.path.join(current_dir,red)
    nir_v = os.path.join(current_dir,nir)
    #cv2.destroyAllWindows()
    
    #RED
    cap = cv2.VideoCapture(red)
    frameRate = cap.get(5)
    ret,frame = cap.read()

    yred = np.zeros(900)
    tred = np.arange(900)
    while ret:
            count = count +1
            crop_frame = frame[int(r[0]):int(r[0]+10),int(r[1]):int(r[1]+10)]
            img = Image.fromarray(crop_frame,'RGB')
            gray = img.convert('LA')
            yred[count] = np.mean(gray)
            ret,frame = cap.read()
    

    yred = yred[1:count]
    tred = tred[1:count]
    tred = tred/30
    b,a = signal.butter(2,2,fs=30)
    zred = signal.filtfilt(b,a,yred)
    
    maxredl = signal.argrelextrema(yred,np.greater)
    minredl = signal.argrelextrema(yred,np.less)
    length = min(maxredl[0].size,minredl[0].size)
    if (maxredl[0][0] < minredl[0][0]):
        maxred = yred[maxredl]
        minred = yred[minredl]
    else:
        maxred = yred[maxredl]
        minred = yred[minredl]
        maxred = maxred[1:maxred.size]
        
    lengthr = min(maxred.size,minred.size)
    maxred = maxred[1:lengthr]
    minred = minred[1:lengthr]
    ACDCred = abs(maxred-minred)/minred
    ACDCred = np.mean(ACDCred)
    
    
    #NIR
    count2 = 0
    cap2 = cv2.VideoCapture(nir)
    frameRate2 = cap2.get(5)
    ret2,frame2 = cap2.read()

    ynir = np.zeros(900)
    tnir = np.arange(900)
    while ret2:
            count2 = count2 +1
            crop_frame2 = frame2[int(r[0]):int(r[0]+10),int(r[1]):int(r[1]+10)]
            img2 = Image.fromarray(crop_frame2,'RGB')
            gray2 = img2.convert('LA')
            ynir[count2] = np.mean(gray2)
            ret2,frame2 = cap2.read()
    
    ylength = ynir.shape
    
    ynir = ynir[1:count2]
    tnir = tnir[1:count2]
    tnir = tnir/30
    b,a = signal.butter(2,2,fs=30)
    znir = signal.filtfilt(b,a,ynir)
   
    maxnirl = signal.argrelextrema(ynir,np.greater)
    minnirl = signal.argrelextrema(ynir,np.less)
    length = min(maxnirl[0].size,minnirl[0].size)
    if (maxnirl[0][0] < minnirl[0][0]):
        maxnir = ynir[maxnirl]
        minnir = ynir[minnirl]
    else:
        maxnir = ynir[maxnirl]
        minnir = ynir[minnirl]
        maxnir = maxnir[1:maxnir.size]
    length = min(maxnir.size,minnir.size)
    maxnir = maxnir[0:length]
    minnir = minnir[0:length]
    ACDCnir = abs(maxnir-minnir)/minnir
    ACDCnir = np.mean(ACDCnir)
    print(ACDCnir)
    print(ACDCred)
    R = ACDCnir/ACDCred
    return R

countx = 0
county = 0
R1 = np.zeros((300,300))

im = cv2.imread("red.jpg")
r = cv2.selectROI(im)
cv2.destroyAllWindows()
e624 = [774,5906.8]
e940 = [1214,693.44]
R = ana4(r)
R = R*0.98
SAO2 = (e624[1]-R*e940[1])/((R*e940[0]-R*e940[1])+(e624[1]-e624[0]))

        
print(r)
print(SAO2)
#fig = plt.figure()
#plt.imshow(R1,extent=[0,1,0,1])      
 



