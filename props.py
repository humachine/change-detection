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
import mylib
from mylib import pickleload, picklethis, show, pickle
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
#import time
#from binlabeller import bwlabel
#starttime = time.time() 

#import os
#os.chdir('../../')
#
class component:
    def __init__(self, ul0, ul1, lr0, lr1, ccdictno, width=None, height=None, direction=None, top=None, bottom=None):
        self.ul0 = ul0
        self.top =top
        self.bottom=bottom
        self.ul1 = ul1
        self.lr0 = lr0   
        self.lr1 = lr1   
        self.ccdictno=ccdictno
  
        self.height = self.lr0-self.ul0
        self.width = self.lr1-self.ul1
        if(self.height < self.width):
            self.direction='v'
        else:
            self.direction='h'
            

    def __repr__(self):
        return repr((self.ccdictno))

class compstring:
    def __init__(self, listofcomps, direction):
        self.listofcomps = listofcomps
        self.direction = direction
    def __repr__(self):
        return repr(self.direction)

import cv2.cv as cv
import tesseract

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)

def conv(fname):
    image=cv.LoadImage(fname, cv.CV_LOAD_IMAGE_GRAYSCALE)
    #api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
    tesseract.SetCvImage(image,api)
    text=api.GetUTF8Text()
    conf=api.MeanTextConf()
    image=None
#    print text
    print text.rstrip('\n')
import config as cfg
#def stringprops(fname=None):
if 1:
    fname=None
    if fname==None:
        fname='6_b'
        fname='15_a'
        fname='8_a'
        fname='8_b'
        fname='6_a'
        fname='15_b'
        fname='5_b'
        fname='5_a'
        
    SAVE_DIR=cfg.OUT_DIR+'PGM/New/'
    strmaskhor=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname+'hor.png'), dtype=bool)
    strmaskvert=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname+'vert.png'), dtype=bool)
    originalimage=np.asarray(imread(cfg.IMG_DIR+fname+'.png'), dtype=bool)
    strmask=strmaskhor + strmaskvert    
    
    '''Horizontal Strings'''
    label_im, num = ndimage.label(strmaskhor)
    slices = ndimage.find_objects(label_im)
    
    for i, sl in enumerate(slices):
        b=strmaskhor[sl]*originalimage[sl]
        b=np.lib.pad(b, (50,50), 'constant')
        imsave(SAVE_DIR+fname+ str(i) + '.png', np.flipud(np.fliplr(b)) )

    cnt=i+1
    '''Vertical Strings'''        
    label_im, num = ndimage.label(strmaskvert)
    slices = ndimage.find_objects(label_im)

    for i, sl in enumerate(slices):
        b=strmaskvert[sl]*originalimage[sl]
        b=np.lib.pad(b, (50,50), 'constant')
        imsave(SAVE_DIR+fname+ str(cnt+i) + '.png', np.rot90(b,-1))
    cnt+=i+1