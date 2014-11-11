# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 00:32:50 2014

@author: Home
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 16:08:59 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 04:54:47 2014
LIST1 - VERTLIST
LIST2 - HORLIST
@author: ipcv5
"""
#import pytesser

from PIL import Image	
from operator import itemgetter, attrgetter
from mylib import pickleload, picklethis, show, pickle
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage

import cv2.cv as cv
import tesseract
import config as cfg

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)

def process(string):
    string=string.replace('0','O')
    string=string.replace('Z','2')
    string=string.replace(':|:', 'i')   
    string=string.replace('|', '1')

    return string


            


fname='6_a.png'
if 1:
#def grandfinale(fname=None):
    if cfg.IMG_EXT in fname:
        fname=fname[:-4]        
    fname1=fname[:-1]+'a'        
    fname2=fname[:-1]+'b'        
        
    SAVE_DIR=cfg.OUT_DIR+'PGM/New/'

    #Loading Images
    strmaskhora=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname1+'hor.png'), dtype=bool)
    strmaskverta=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname1+'vert.png'), dtype=bool)
    originalimage=np.asarray(imread(cfg.IMG_DIR+fname+'.png'), dtype=bool)
    strmaskhorb=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname2+'hor.png'), dtype=bool)
    strmaskvertb=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname2+'vert.png'), dtype=bool)
 
#    
#    label_im1, num = ndimage.label(strmaskhora)
#    centroids = ndimage.measurements.center_of_mass(strmaskhora, label_im1, xrange(1,num+1))
#    cent1= [(int(x), int(y)) for (x,y) in centroids]
#    label_im1, num = ndimage.label(strmaskverta)
#    centroids = ndimage.measurements.center_of_mass(strmaskverta, label_im1, xrange(1,num+1))
#    cent2= [(int(x), int(y)) for (x,y) in centroids]
#    centa=cent1+cent2
#
#    label_im1, num = ndimage.label(strmaskhorb)
#    centroids = ndimage.measurements.center_of_mass(strmaskhorb, label_im1, xrange(1,num+1))
#    cent1= [(int(x), int(y)) for (x,y) in centroids]
#    label_im1, num = ndimage.label(strmaskvertb)
#    centroids = ndimage.measurements.center_of_mass(strmaskvertb, label_im1, xrange(1,num+1))
#    cent2= [(int(x), int(y)) for (x,y) in centroids]
#    centb=cent1+cent2


    horstra=pickleload(SAVE_DIR + fname1 + 'hor.pkl')
    horlima=len(horstra)
    vertstra=pickleload(SAVE_DIR + fname1 + 'vert.pkl')
    texta=horstra+vertstra
    
    horstrb=pickleload(SAVE_DIR + fname2 + 'hor.pkl')
    horlimb=len(horstrb)
    vertstrb=pickleload(SAVE_DIR + fname2 + 'vert.pkl')
    textb=horstrb+vertstrb

    texta=[process(i) for i in texta]
    textb=[process(i) for i in textb]
#    diff(texta, textb, horlima, horlimb)

    print 'Differences are:', set(texta) ^ set(textb)    
#    print len(texta), len(textb), len(centa), len(centb)
#        
#    for x in range(len(texta)):
#        for y in range(len(textb)):
#            p=texta[x]
#            q=textb[y]
#            
#            if p!=q:
#                continue
