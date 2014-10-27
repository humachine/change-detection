# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 02:30:41 2014

@author: Home
"""

from PIL import Image	
import cv2
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from binlabeller import bwlabel

import time
starttime = time.time() 
 
imname = 'notext.png'
img = cv2.imread(imname,0)
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)
 
ret,img = cv2.threshold(img,127,255,0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
done = False
 
while( not done):
    eroded = cv2.erode(img,element)
    temp = cv2.dilate(eroded,element)
    temp = cv2.subtract(img,temp)
    skel = cv2.bitwise_or(skel,temp)
    img = eroded.copy()
 
    zeros = size - cv2.countNonZero(img)
    if zeros==size:
        done = True
 
cv2.imwrite('works.png', skel)

img1=np.asarray(imread(imname))
#print sum(img1)
newarr=np.subtract(img1, skel)
imsave('diff.png', newarr)
#toimage(newarr).show()
#print newarr
newarr1=np.asarray(imread('diff1.png'), dtype=bool)
newarr=np.asarray(imread('diff.png'), dtype=bool)
#print newarr
#print np.sum(newarr)
print np.sum(newarr1)
#print sum(newarr), sum(newarr1)

#if newarr[0,0]==False:
#    h, w =newarr.shape
#    if sum(newarr>=1)*2 > h*w:
#        newarr.


newimg = Image.open('skel.png')
newimg = newimg.convert('1')

#newdict, _, newcount, _ = bwlabel(newimg)
#print newcount
#    (ccdict, ccarr, count, output_img)

#show(skel)
#show(img)
#cv2.imshow("skel",skel)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
print time.time() - starttime, ' seconds'