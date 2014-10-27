# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 15:50:45 2014

@author: Home
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 02:30:41 2014

@author: Home
"""

from PIL import Image	
import cv2
from mylib import pickleload, picklethis, iswhitebg
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from binlabeller import bwlabel
from scipy import ndimage
import time
from binlabeller import bwlabel

starttime = time.time() 

def show(x):
    toimage(x).show()
 
fname='5_b.png'
fname='6_a.png'
fname='8_a.png'

imname = 'notext'+fname[-7:-4]+'.png'
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
newarr=np.subtract(img1, skel)
skel=skel.astype(bool)
#
newarr=img1
if iswhitebg(newarr):
    newarr=np.invert(newarr)



a = ndimage.binary_erosion(newarr, element)
print sum(skel), np.max(skel), sum(a), np.max(a)
#show(a)
#z=(np.subtract(a.astype(int)),skel.astype(int)).astype(int)
z=(np.subtract( a.astype(int), skel.astype(int) ).astype(int))
y=z
y[y<0]=0
show(y)
#z[z<0]=0
#z = ndimage.binary_dilation(z, element)
#z = ndimage.binary_erosion(z, element)
#show(z)
#
#imsave('temptemp.png', np.invert(a))
#imgforlabelling=Image.open('temptemp.png')
#imgforlabelling=imgforlabelling.convert('1')
#skeldict, _, skelcount, out=bwlabel(imgforlabelling)

#show(a)
#solid=np.subtract(a, skel)
#imsave('labelinglinesremoved'+fname[-7:-4]+'.png', solid)




print time.time() - starttime, ' seconds'