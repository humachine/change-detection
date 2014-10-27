
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
from scipy import ndimage

import time
starttime = time.time() 
 
def show(x):
    toimage(x).show()
 


imname1='511.png'
imname2='512.png'

imname2='diff1.png'
imname1='diff1.png'
im1=np.invert(np.asarray(imread(imname1), dtype=bool))
im2=np.invert(np.asarray(imread(imname2), dtype=bool))

im1=ndimage.binary_fill_holes(im1)
im2=ndimage.binary_fill_holes(im2)

imsave('fill1.png', im1)
imsave('fill2.png', im2)

print time.time() - starttime, ' seconds' 