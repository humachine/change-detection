# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 04:20:25 2014

@author: Home
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 02:30:41 2014

@author: Home
"""

from PIL import Image	
import cv2
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from binlabeller import bwlabel

import time
starttime = time.time() 

import pickle
import mylib


a=mylib.pickleload('a')
print a