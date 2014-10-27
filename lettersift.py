# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 15:28:45 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 14:09:13 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 15:50:45 2014
FINAL
@author: Home
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 02:30:41 2014

@author: Home
"""
import numpy as np
 
from PIL import Image	
import cv2
from mylib import pickleload, picklethis
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
import time

starttime = time.time() 
logor=np.logical_or
xor=np.logical_xor
label=ndimage.label
dilate=ndimage.grey_dilation
erode=ndimage.binary_erosion
fill=ndimage.binary_fill_holes
opening=ndimage.binary_opening

def show(x):
    toimage(x).show()

#a=np.asarray(imread('ETC\\ModHausdorffDist\\crop1.png'), dtype=bool)
#a=np.asarray(imread('fonts_test.png'), dtype=bool)
a=np.asarray(imread('ETC\\ModHausdorffDist\\begin.png'), dtype=bool)

#imsave('ETC\\ModHausdorffDist\\begin.png',np.invert(a))
#show(a)

ccarr, ccnum=ndimage.label(a, np.ones((3,3)))
print ccnum
PADDING=5

for i in range(1, ccnum+1):
    zipp=np.where(ccarr==i)
    zipp1=zip(*zipp)
    
    ul0=min(zipp[0])
    lr0=max(zipp[0])
    ul1=min(zipp[1])
    lr1=max(zipp[1])
    
    print ul0, lr0, ul1, lr1
    print

    zzz=ccarr[ul0-PADDING:lr0+PADDING+1, ul1-PADDING:lr1+PADDING+1].copy()
    zzz=zzz.astype(bool)
    zzz*=0
    zzz[PADDING:PADDING+lr0-ul0+1,PADDING:PADDING+lr1-ul1+1]=ccarr[ul0:lr0+1, ul1:lr1+1]

#    show(np.invert(zzz))
    imsave('ETC\\ModHausdorffDist\\test\\'+str(i)+'.png', np.invert(zzz))
