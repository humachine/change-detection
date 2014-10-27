# -*- coding: utf-8 -*-
"""
NOT WORKING. REJECTED
Attempt to pick between the two different fills for Thinning
Created on Wed Apr 02 15:16:46 2014

@author: ipcv5
"""
import numpy as np
 
from PIL import Image	
import cv2
from mylib import pickleload, picklethis
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from binlabeller import bwlabel
from scipy import ndimage
import time
from binlabeller import bwlabel
from scipy.ndimage import binary_dilation as dilate
from scipy.ndimage import binary_fill_holes as fill

def show(x):
    toimage(x).show()

def which(a,b):
    i=0
    while(1):
        try:
            if a[i] <= 10000:
                if b[i] <= 10000:
                    #Both images simultaenously go below 10000. Which probably means they are very similar
                    if np.sum(a[:i]) > np.sum(b[:i]):
                        return 2
                    else:
                        return 1
                else:
                    return 1
            else:
                #If B crosses 10000 first, it probably means it has more compact components whereas A has random structures
                if b[i] <=10000:
                    return 2
            i=i+1
        except IndexError:
            if a[i-1]<b[i-1]:
                return 1
            else:
                return 2
    

#def superb(fname=None):
if 1:
    fname=None
    if fname==None:
        fname='14_a'
        fname='5_a'
        fname='6_a'
        fname='15_a'
        fname='9_b'
        fname='8_a'
        fname='7_a'
        fname='9_a'
    
    fill1=np.asarray(imread('Outputs\\Restart\\'+fname+'fill.png'), dtype=bool)
    fill2=np.asarray(imread('Outputs\\Restart\\'+fname+'tempfill.png'), dtype=bool)
    
    
#    diff=np.subtract(fill1.astype(int), fill2.astype(int))    
    #imsave('Outputs\\Restart\\'+'diff'+fname+'.png', fill(diff))
    
    ccarr, ccnum=ndimage.label(fill1, np.ones((3,3)))
    ccarr1, ccnum1=ndimage.label(fill2, np.ones((3,3)))
    
    ccarr=ccarr.astype(np.uint16)
    ccarr1=ccarr1.astype(np.uint16)
    
    bin1=list(np.bincount(ccarr.flatten()))
    bin2=list(np.bincount(ccarr1.flatten()))
    
    a=sorted(bin1, reverse=True)
    b=sorted(bin2, reverse=True)
    
    a.remove(a[0])
    b.remove(b[0])
    
    print a[:10]
    print
    print b[:10]
    
    result=which(a,b)
    print result, fname
    
#    if result==0:
#        if ccnum > ccnum1:
#            imsave('Outputs\\Restart\\Perf\\'+fname+'.png', fill2)
#        else:
#            imsave('Outputs\\Restart\\Perf\\'+fname+'.png', fill1)
#
#    elif result==1:
#            imsave('Outputs\\Restart\\Perf\\'+fname+'.png', fill1)
#    elif result==2:
#            imsave('Outputs\\Restart\\Perf\\'+fname+'.png', fill2)





#lis=['5_a', '8_a', '14_a', '6_a', '15_a', '9_a']
#for i in lis:
##    print i
#    superb(i)
#    j=i[:-1]+'b'
##    print j
#    superb(j)

#lis=[2, 3, '4_1', '4_2', 7, 16]
#for i in lis:
#    j1=str(i)+'_a'
#    superb(j1)
#    j=j1[:-1]+'b'
#    superb(j)



#ccarr=ccarr.astype(bool)
#ccarr1=ccarr1.astype(bool)

#ccarr=ccarr.fl