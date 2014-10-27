# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 02:30:41 2014

@author: Home
"""

from PIL import Image	
import cv2
from mylib import pickleload, picklethis
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from binlabeller import bwlabel

import time
starttime = time.time() 
 
fname='8_a.png'
imname = 'notext'+fname[-7:-4]+'.png'
img = cv2.imread(imname,0)
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)
 
ret,img = cv2.threshold(img,127,255,0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
done = False
 
print 'begin loop'
while( not done):
    eroded = cv2.erode(img,element)
    temp = cv2.dilate(eroded,element)
    temp = cv2.subtract(img,temp)
    skel = cv2.bitwise_or(skel,temp)
    img = eroded.copy()
 
    zeros = size - cv2.countNonZero(img)
    if zeros==size:
        done = True
 
print 'loop over'
cv2.imwrite('works.png', skel)

img1=np.asarray(imread(imname))
newarr=np.subtract(img1, skel)
#toimage(newarr).show()

imsave('diff.png', newarr)
imsave('diff1.png', np.invert(newarr))


newimg = Image.open('diff.png')
newimg = newimg.convert('1')
data = newimg.load()

newimg1 = Image.open('diff1.png')
newimg1 = newimg1.convert('1')
data1= newimg1.load()

if data[0,0]<data1[0,0]:
    newarr=np.invert(newarr)
    imsave('diff1.png', newarr)
    

b=toimage(newarr)
b=b.convert('1')


print 'start label'

textcomps=pickleload('textcomplist'+fname[-7:-4])
dict1=pickleload('ccdict'+fname[-7:-4])
count=pickleload('ccnum'+fname[-7:-4])




complen=[]
complen.append(0)
for i in range(1, count+1):
    complen.append(len(dict1[i]))
complen1=sorted(complen, reverse=True)

dboundary=1500
i=0
while complen1[i] > 1500:
    if complen1[i]>complen1[i+1]*2:
        dboundary = complen1[i+1]+10
        break
    i+=1




solid=np.asarray(imread('diff1.png'),dtype=bool)
print 'label over'

for i in range(1, count+1):
    if len(dict1[i])<dboundary :
#        print len(dict1[i])
        for j in dict1[i]:
            a,b =j
#            solid[b,a]=False
            solid[b,a]=True
toimage(solid).show()
imsave('labelinglinesremoved'+fname[-7:-4]+'.png', solid)


print time.time() - starttime, ' seconds'