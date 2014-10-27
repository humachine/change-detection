# -*- coding: utf-8 -*-
"""
Created on Thu Mar 06 15:01:51 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 05 14:50:16 2014

@author: ipcv5
"""

import numpy as np
import pytesser
from PIL import Image	, ImageFilter
import cv2
import mylib
from mylib import pickleload, picklethis, show
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from binlabeller import bwlabel
from scipy import ndimage
import time
import os

from without_textanddashes_withclass import textextraction
from actualthinningondrugs import thinning


starttime=time.time()

fname='6_a'
fname='5_b'
fname='8_a'
fname='15_b'
fname='6_b'
fname='5_a'
fname='15_a'
fname='8_b'
fname='10_a'




def megadilfn(fname):      
    return 1


starttime=time.time()
print fname
imname = 'Outputs\\labelinglinesremoved'+fname+'.png'
 
a=np.asarray(imread(imname), dtype=bool)
height, width=a.shape

a=np.invert(a)
    
a=ndimage.binary_fill_holes(a)
ccarr, num=ndimage.label(a)

print 'labels'    
for i in range(1, num+1):
    j1, j2=np.where(ccarr==i)
    if len(j1)>1:
        if len(j1)<1000:
            for k in xrange(len(j1)):
                a[j1[k], j2[k]]=False
    elif len(j1)==1:
        a[j1, j2]=False

    
print 'finding edges'
imsave('temp.png', a)
image = Image.open('temp.png')
image = image.filter(ImageFilter.FIND_EDGES)

b=np.asarray(image, dtype=bool)

print 'dilating'
j1, j2=np.where(b==True)
strel=30
for i in xrange(len(j1)):
    j, k=j1[i], j2[i]
    if b[j,k]:
        if np.sum(b[j-strel:j+strel+1,k-strel:k+strel+1])>1:
            b[j-strel:j+strel+1,k-strel:k+strel+1]=True
print 'holefilling'
b=ndimage.binary_fill_holes(b)

imsave('Outputs\\megadilfill'+fname+'.png',b)
#return time.time()-starttime






def newfunc():

    timelist=[0]*86
    filelist=os.listdir('images_consolidated')
    
    thinningtimes=[0]*len(filelist)
    textextractiontimes=[0]*len(filelist)
    dilfilltime=[0]*len(filelist)
    
    for i in os.listdir('images_consolidated'):
        fname=i[0:-4]
    #    if not os.path.isfile('Outputs\\labelinglinesremoved'+fname+'.png'):
    #        print fname
    #        starttime=time.time()
    #        textextraction(fname)
    #        textextractiontimes.append(time.time()-starttime)
    #        print time.time()-starttime
    #
    #        starttime=time.time()
    #        thinning(fname)
    #        thinningtimes.append(time.time()-starttime)
    #        print time.time()-starttime
    #        
    #    else:
    #        textextractiontimes.append(0)
    #        thinningtimes.append(0)
    #        dilfilltime.append(0)
            
        if os.path.isfile('Outputs\\labelinglinesremoved'+fname+'.png'):
        
            print fname
            timetaken=megadilfn(fname)
            timelist.append(timetaken)
            print fname, timetaken 
    
megadilfn(fname)

print time.time() - starttime