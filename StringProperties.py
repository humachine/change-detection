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
import time

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)

def conv(fname):
    image=cv.LoadImage(fname, cv.CV_LOAD_IMAGE_GRAYSCALE)
    #api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
    tesseract.SetCvImage(image,api)
    text=api.GetUTF8Text()
    conf=api.MeanTextConf()
    text=text.rstrip('\n')
    return text, conf

fname=None
import config as cfg
def stringproperties(fname=None):
#if 1:
    starttime=time.time()
    if fname==None:
        fname='6_b'
        fname='15_a'
        fname='8_a'
        fname='6_a'
        fname='15_b'
        fname='5_a'
        fname='5_b'
        fname='8_b'
    if cfg.IMG_EXT in fname:
        fname=fname[:-4]        
        
    SAVE_DIR=cfg.OUT_DIR+cfg.properties.OUT_DIR
    strmaskhor=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname+'hor.png'), dtype=bool)
    strmaskvert=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname+'vert.png'), dtype=bool)
    originalimage=np.asarray(imread(cfg.IMG_DIR+fname+'.png'), dtype=bool)

    print 'Character Recognition begins.. .' 
    
    '''Takes up Horizontal Strings. Saves each string to a separate image and runs the OCR engine on it.
    The OCR output(horstr), the string centroid(centr) and the string bounding box boundaries(slia) are saved.    
    '''
    label_im, num = ndimage.label(strmaskhor)
    slices = ndimage.find_objects(label_im)
    centroids=ndimage.measurements.center_of_mass(strmaskhor, label_im, xrange(1, num+1))

    confidence = []
    horstr=[]
    centr=[]
    sli=[]
    cnt=0
    for i, sl in enumerate(slices):
        if (np.sum(strmaskvert[sl]*strmaskhor[sl]) == np.sum(strmaskhor[sl])):
            continue
        b=strmaskhor[sl]*originalimage[sl]
        b=np.lib.pad(b, (50,50), 'constant')
        imsave(SAVE_DIR+fname+ str(cnt) + '.png', np.flipud(np.fliplr(b)) )
        text, conf = conv(SAVE_DIR+fname+ str(cnt) + '.png')
        if text=='':
            continue
        
        cnt+=1
        confidence.append(conf)
        centr.append(centroids[i])
        horstr.append(text)
        sli.append(sl)

    '''A similar process is done for Vertical Strings'''        
    label_im, num = ndimage.label(strmaskvert)
    slices = ndimage.find_objects(label_im)
    centroids=ndimage.measurements.center_of_mass(strmaskvert, label_im, xrange(1, num+1))
    
    vertstr=[]
    for i, sl in enumerate(slices):
        if (np.sum(strmaskvert[sl]*strmaskhor[sl]) == np.sum(strmaskvert[sl])):
            continue
        b=strmaskvert[sl]*originalimage[sl]
        b=np.lib.pad(b, (50,50), 'constant')
        imsave(SAVE_DIR+fname+ str(cnt) + '.png', np.rot90(b,-1))

        text, conf = conv(SAVE_DIR+fname+ str(cnt) + '.png')
        if text=='':
            continue

        confidence.append(conf)
        vertstr.append(text)
        centr.append(centroids[i])
        sli.append(sl)
        cnt+=1
        
    print 'OCR completed with a percentage confidence of', np.mean(confidence)
    
    picklethis(sli,  SAVE_DIR + fname + 'slices.pkl')
    picklethis(centr,  SAVE_DIR + fname + 'centroids.pkl')
    picklethis(horstr, SAVE_DIR + fname + 'hor.pkl')
    picklethis(vertstr, SAVE_DIR + fname + 'vert.pkl')
    
    return 0, time.time()-starttime
stringproperties('5_a.png')