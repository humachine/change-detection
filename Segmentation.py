# -*- coding: utf-8 -*-
"""
NO OVERLAP of stringmask and segmentmask

DENSITY = 0.05
Created on Fri Apr 04 15:43:57 2014

@author: ipcv5
"""

from PIL import Image	
import cv2
from mylib import pickleload, picklethis
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
import time
import config as cfg

dilate=ndimage.binary_dilation
fill=ndimage.binary_fill_holes
xor=np.logical_xor
def show(x):
    toimage(x).show()

starttime=time.time()
def segmentation(fname=None):
    if fname==None:
        print 'No file name assigned'
        return 0, time.time()-starttime
    
    print 'Attempting to segment image :', fname
    if cfg.IMG_EXT in fname:
        fname=fname[:-4]

    rmlinesfname = cfg.OUT_DIR + cfg.removelines.SAVE_DIR + fname + cfg.IMG_EXT
    strmaskfname = cfg.OUT_DIR + cfg.stringify.STRINGIFY_DIR + fname + 'strmask' +cfg.IMG_EXT
    
    fill1=np.asarray(imread(rmlinesfname), dtype=bool)
    img=np.asarray(imread(strmaskfname), dtype=bool)
    original=np.asarray(imread(cfg.IMG_DIR + fname + cfg.IMG_EXT), dtype=bool)
    
    z=np.logical_and(img, fill1)        
    fillcopy=fill1.copy()
    
    if np.sum(z)==0:    # I.e NO OVERLAP of stringmask and segmentmask
        print 'Saving Segment Masks to Disk'
        imsave(cfg.OUT_DIR + cfg.segmentation.OUT_DIR + fname + 'segmask.png', fill1)
        imsave(cfg.OUT_DIR + cfg.segmentation.DEBUG_DIR + fname+'forchecking.png',xor(fill1, original))
    
    else:       #Stringmask and Segmentmasks overlap. Remains to be seen if the overlap is considerable enough to cause removal of a segment or two
        print 'Separating textboxes from segments'
        ccfill, ccnumfill = ndimage.label(fill1, np.ones((3,3)))    
        ans=img*ccfill        #The string mask is ANDed with the label map of the removelines output image
            
        ccfill=ccfill.astype(np.uint16)             #Ccfill is an array that has each connected component labeled with a different sequence number (1,2,3 . . .)    
        binfill=list(np.bincount(ccfill.flatten())) #ccfill.flatten() flattens the array to get a vector. And Bincount creates a bin for each value and counts number of occurences of each value
        bfill=sorted(binfill, reverse=True)         #the bincount is then sorted in descending order (each element of binfill has the number of pixels that are present in connected component labeled i)
        bfill.remove(bfill[0])                      #Since, the number of background pixels ('0' pixels) is the usual maximum, we remove it from the list

        '''Now, ans is computed above by ANDing img & ccfill. The non-0 points of ans are just
        the points which are present in both the stringmask and the removelines image (the remove lines image consists of segments and shaded textboxes)
        Below, we attempt to differentiate between textboxes and segments. Textboxes ALWAYS must have a positive intersection with the stringmask (since they are supposed to contain strings)
        While segments may also contain text strings inside them, the ratio of area of text / area of segment is usually quite less < 0.05 
        '''
        ans=ans.astype(np.uint16)                   
        binans=list(np.bincount(ans.flatten()))
        
        for i in range(1,len(binans)):
            if binans[i] > cfg.segmentation.TEXTBOX_DENSITY *binfill[i]:
                fillcopy[ccfill==i]=False
#        show(xor(fillcopy, original))
#        show(fillcopy)
        imsave(cfg.OUT_DIR + cfg.segmentation.OUT_DIR + fname + 'segmask.png', fillcopy)
        imsave(cfg.OUT_DIR + cfg.segmentation.DEBUG_DIR + fname+'forchecking.png', np.logical_xor(fillcopy, original))
        
    return 0, time.time()-starttime