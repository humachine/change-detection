# -*- coding: utf-8 -*-
"""
Created on Fri May 16 05:58:29 2014

@author: Home
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 10:14:58 2014
Updates:

Progress thus far:

- Text and Graphics
`    Text extraction                             
`    Removing labeling lines, dashed lines, etc 
`    Grouping characters to strings
Segmentation and Matching
`    Segmentation
    Matching segments
Association of labels with segments
    Attaching labeling lines to segments
    Associating labels with segments
Image Comparison

@author: ipcv5
    """
from scipy.misc import toimage, imread, imshow, imsave
from scipy import ndimage
from PIL import Image
#from binlabelwithdict import bwlabel
from binlabeller import bwlabel
from itertools import product
import mylib
from mylib import show
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal

import time
start_time = time.time()

a=np.asarray(imread('images_consolidated\\5_a.png'), dtype=bool)
b=np.asarray(imread('Outputs\\Restart\\5_afill.png'), dtype=bool)

show(a*b)


    for i in range(1,ccnum+1):
        print i
        b*=0
        b[ccarr==i]=True
        bbb=np.invert(b)
        data = np.zeros( (aaa.shape[0],aaa.shape[1],3), dtype=np.uint8)
        data[::]=255
        data[:,:,1]=bbb*255
        data[:,:,2]=bbb*255
        
        imsave('Friday\\Vid2\\'+str(i)+'.png', data)

