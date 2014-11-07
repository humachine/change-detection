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
from PIL import Image
import mylib
import numpy as np
import time

start_time = time.time()


def sanitized(fname, fname1):
    
    try:
        a=np.asarray(imread('images_consolidated\\'+fname+'.png'), dtype=bool)
        b=np.asarray(imread('images_consolidated\\'+fname1+'.png'), dtype=bool)
        
#        print np.sum(a), np.sum(b)
        ratio = float(np.sum(a))/float(np.sum(b))
#        print type(ratio), ratio
        if  ratio < 0.4 or ratio >= 2:
            return False
            
        _, num1=ndimage.label(a, np.ones((3,3)))
        _, num2=ndimage.label(b, np.ones((3,3)))
        ratio1=float(num1)/float(num2)
#        print ratio1, num1, num2
        
        if ratio1 < 0.4 or ratio1>=2:
            return False
        return True
            
    except IOError:
        return False
        
    return False

fname='8_a'
fname1='8_e'


#print time.time() - start_time, 'seconds'