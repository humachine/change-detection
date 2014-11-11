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
from mylib import pickleload, picklethis, show, pickle
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
from scipy.spatial import distance
import time

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
    string=string.replace('\xe2\x80\x94', '-')
    return string

def labelmatching(fname=None):
    starttime=time.time()
    if cfg.IMG_EXT in fname:
        fname=fname[:-4]        
    fname1=fname[:-1]+'a'        
    fname2=fname[:-1]+'b'        
        
    SAVE_DIR=cfg.OUT_DIR+cfg.properties.OUT_DIR

    '''Loading previously saved images and arrays
    '''
    strmaskhora=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname1+'hor.png'), dtype=bool)
    strmaskverta=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname1+'vert.png'), dtype=bool)
    
    originalimagea=np.asarray(imread(cfg.IMG_DIR+fname1+'.png'), dtype=bool)
    originalimageb=np.asarray(imread(cfg.IMG_DIR+fname2+'.png'), dtype=bool)

    strmaskhorb=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname2+'hor.png'), dtype=bool)
    strmaskvertb=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname2+'vert.png'), dtype=bool)

    centa=pickleload(SAVE_DIR + fname1 + 'centroids.pkl')
    centb=pickleload(SAVE_DIR + fname2 + 'centroids.pkl')

    slia=pickleload(SAVE_DIR + fname1 + 'slices.pkl')
    slib=pickleload(SAVE_DIR + fname2 + 'slices.pkl')
 
    horstra=pickleload(SAVE_DIR + fname1 + 'hor.pkl')
    vertstra=pickleload(SAVE_DIR + fname1 + 'vert.pkl')
    texta=horstra+vertstra
    
    horstrb=pickleload(SAVE_DIR + fname2 + 'hor.pkl')
    vertstrb=pickleload(SAVE_DIR + fname2 + 'vert.pkl')
    textb=horstrb+vertstrb

    texta=[process(i) for i in texta]
    textb=[process(i) for i in textb]

    for x in range(len(texta)):
        for y in range(len(textb)):
            p=texta[x]
            q=textb[y]
            
            if p!=q:
                continue

            sel=y            
            mindist=distance.euclidean(centa[x], centb[y])
            for z in range(y, len(textb)):
                if texta[x] == textb[z]:
                    if distance.euclidean(centa[x], centb[z]) < mindist:
                        sel=z
            texta[x]=''
            textb[sel]=''
    
    diffa=[x for x in texta if x!='']
    diffb=[x for x in textb if x!='']
    print 'Number of changes in Image 1: ', len(diffa)
    print 'Number of changes in Image 2: ', len(diffb)
    
    resa=originalimagea*np.invert(strmaskhora)*np.invert(strmaskverta)
    for x in range(len(texta)):
        if texta[x]!='':
            resa[slia[x]]=originalimagea[slia[x]]

    resb=originalimageb*np.invert(strmaskhorb)*np.invert(strmaskvertb)
    for x in range(len(textb)):
        if textb[x]!='':
            resb[slib[x]]=originalimageb[slib[x]]

    imsave(cfg.OUT_DIR+cfg.RES_DIR+fname1+cfg.IMG_EXT, np.invert(resa))    
    imsave(cfg.OUT_DIR+cfg.RES_DIR+fname2+cfg.IMG_EXT, np.invert(resb))    
    
    return 0, time.time()-starttime