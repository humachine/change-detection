# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 05:56:23 2014

@author: Home
"""

from PIL import Image	
import cv2
from mylib import pickleload, picklethis, show
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage, imresize
from scipy import ndimage
import time
import config as cfg
#from SIFTbyDavidLowe import siftfn

import os
print os.getcwd()

SAVE_DIR='Outs/PGM/'

fname='5_a.png'
if 1:
#def siftdrive(fname):
    fname1=fname[:-4]
    fname2=fname[:-5]+ ['a','b'][fname[-5]=='a']
    print fname1, fname2
    
    imname1='../../Outputs/SegmentMasks1/'+fname1+'fill.png'
    imname2='../../Outputs/SegmentMasks1/'+fname2+'fill.png'

    im1=np.asarray(imread(imname1), dtype=bool)
    im2=np.asarray(imread(imname2), dtype=bool)

    SIG=3    
    
	'''The following piece of code takes the segment mask of an image. 
	It then saves each segment to a PGM file and tries to match it using SIFT
	The images are first blurred using a Gaussian filter and then scaled down to make it suitable for SIFT.
	'''
	
    label_im, num = ndimage.label(im1)
    slices = ndimage.find_objects(label_im)
    for i, slc in enumerate(slices):
        arr=np.lib.pad(im1[slc], (50,50), 'constant')
        arr=arr.astype(np.uint8)
        arr[arr==1]=255

        ratio=arr.shape[0]/400
        arr=imresize(arr, (400, int(arr.shape[1]/ratio)))
        imsave(SAVE_DIR + fname1 + str(i+1) + '.png', arr)

        conv = Image.open(SAVE_DIR + fname1 + str(i+1) + '.png')
        conv.save(SAVE_DIR + fname1 + str(i+1) + '.pgm')
    
#    centroids = ndimage.measurements.center_of_mass(im1, label_im, xrange(1,num+1))
#    cent1= [(int(x), int(y)) for (x,y) in centroids]
#
    label_im, num = ndimage.label(im2)
    slices = ndimage.find_objects(label_im)
    for i, slc in enumerate(slices):
        arr=np.lib.pad(im2[slc], (50,50), 'constant')
        arr=arr.astype(np.uint8)
        arr[arr==1]=255
        
        ratio=arr.shape[0]/400
        arr=imresize(arr, (400, int(arr.shape[1]/ratio)))
        imsave(SAVE_DIR + fname2 + str(i+1) + '.png', arr)
                
                
        
        conv = Image.open(SAVE_DIR + fname2 + str(i+1) + '.png')
        conv.save(SAVE_DIR + fname2 + str(i+1) + '.pgm')

#    centroids = ndimage.measurements.center_of_mass(im2, label_im, xrange(1,num+1))
#    cent2= [(int(x), int(y)) for (x,y) in centroids]

#    show(im2)

#siftdrive('5_a.png')