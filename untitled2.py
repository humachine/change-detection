# -*- coding: utf-8 -*-
"""
Created on Fri May 16 06:20:56 2014

@author: Home
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 02:59:12 2014

@author: Home
"""

import sys
#sys.path.append("ffmpeg\ffmpeg-20140426-git-b217dc9-win32-static\bin")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image	
import cv2
from mylib import pickleload, picklethis
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
import time
import matplotlib

def show(x):
    toimage(x).show()

#fig = plt.figure()
#plt.rcParams['animation.ffmpeg_path'] = 'F:\\DDP\\ffmpeg\\ffmpeg-20140426-git-b217dc9-win32-static\\bin\\ffmpeg'
 
starttime = time.time() 
logor=np.logical_or
xor=np.logical_xor
label=ndimage.label
dilate=ndimage.grey_dilation
erode=ndimage.binary_erosion
fill=ndimage.binary_fill_holes
opening=ndimage.binary_opening


#def extend(fname):
if 1:
    fname=None
    if fname==None:
        fname='14_a'
        fname='1_2_b'
        fname='9_a'
        fname='15_b'
        fname='4_5_b'
        fname='15_a'
        fname='6_b'
        fname='8_b'
        fname='5_b'
        fname='6_a'
        fname='4_6_a'
        fname='5_a'
        fname='8_a'
        
        
    imname = 'images_consolidated\\'+fname+'.png'
    a=np.asarray(imread(imname), dtype=bool)

    
    b=a.copy()
    aaa=a

    b*=0
#    b[ccarr==i]=True
    b=a
    bbb=np.invert(b)
    bbb=b
    data = np.zeros( (aaa.shape[0],aaa.shape[1],3), dtype=np.uint8)
    data[::]=255
#    data[:,:,1]=bbb*
#    data[:,:,2]=bbb*255

#    data[:,:,0]=bbb*27
    data[:,:,1]=bbb*7
#    data[:,:,2]=bbb*53

#rgb 27 8 53
    show(data)    
#    imsave('Friday\\Vid2\\'+str(i)+'.png', data)


