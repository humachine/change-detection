# -*- coding: utf-8 -*-
   #TODO-  Remove one of the below two save images. Most likely 'fill'. 'Tempfill' seems to do a good job.

"""
Takes Image. 
Creates Skeleton. 
Takes notext image. Fills it. Outputs it

Created on Tue Feb 25 15:50:45 2014
@author: Home
"""
 
from PIL import Image	
import cv2
from mylib import pickleload, picklethis
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
import time
from scipy.ndimage import binary_dilation as dilate
from scipy.ndimage import binary_fill_holes as fill

import config as cfg

def show(x):
    toimage(x).show()

def createskeleton(imname):
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
    return skel
    
def thinning(fname=None):
    starttime = time.time() 
    if fname==None:
        print 'No file name assigned'
        return 0, time.time()-starttime
    else:
        imname = cfg.IMG_DIR+fname

    print 'Thinning image: ', imname
    if cfg.IMG_EXT in fname:
        fname=fname[:-4]
        
    imname = cfg.OUT_DIR+'notext'+fname+cfg.IMG_EXT
    imgoriginal=np.asarray(imread(imname), dtype=bool)
    
    skel=createskeleton(imname)
    print 'Skeletonizing image. . .'
    
    img1=np.asarray(imread(imname))
    newarr1=np.subtract(img1, skel).astype(bool)
    imsave(cfg.OUT_DIR + cfg.thinning.SKEL_IMG_DIR + fname+'.png', skel)

    fill1=fill(newarr1)    
    
    if np.sum(fill1) < np.sum(imgoriginal):
        fill1=fill(imgoriginal)
    
    skel=skel.astype(bool)
    element=np.asarray([[0,1,0],[1,1,1],[0,1,0]], dtype=bool)

#Erode with the above element
    newarr=img1
    a = ndimage.binary_erosion(newarr, element)
#The skeleton image (computed earlier) is subtracted from the eroded image to remove the labeling lines
    z=(np.subtract( a.astype(int), skel.astype(int) ).astype(int))
    y=z
    y[y<0]=0
    z=y.copy().astype(bool)
    fill2=fill(z)
   
   #FIXME -  Remove one of the below two save images. Most likely 'fill'. 'Tempfill' seems to do a good job.
    imsave(cfg.OUT_DIR + cfg.thinning.THINNING_DIR + fname+'tempfill'+'.png', fill1)
    return 0, time.time()-starttime
       
#thinning('5_b.png')    