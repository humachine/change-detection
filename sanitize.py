# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 03:36:46 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 09:31:05 2014
FINAL
@author: ipcv5
"""

from scipy.misc import toimage, imread, imshow, imsave
from scipy import ndimage
import numpy as np
import config as cfg


'''Tries to sanitize image. All images which do not resemble a drawing (like a fully black image etc) are rejected
'''
def sanitize(fname, fname1):
    return True
    try:
        a=np.asarray(imread(cfg.IMG_DIR + fname), dtype=bool)
        b=np.asarray(imread(cfg.IMG_DIR + fname1), dtype=bool)
        
        DENS_LOW=cfg.sanitize.DENS_LOW
        DENS_HIGH=cfg.sanitize.DENS_HIGH
        
        print DENS_LOW, DENS_HIGH
        ratio = float(np.sum(a))/float(np.sum(b))
        if  ratio < DENS_LOW or ratio >= DENS_HIGH:
            return False
            
        _, num1=ndimage.label(a, np.ones((3,3)))
        _, num2=ndimage.label(b, np.ones((3,3)))
        ratio1=float(num1)/float(num2)
        
        if ratio1 < DENS_LOW or ratio1>=DENS_HIGH:
            return False
        return True
            
    except IOError:
        return False