# -*- coding: utf-8 -*-
"""
THRESH=10000
ForSir - FIRST attempt at Thinning and getting segment masks
Created on Wed Apr 02 16:14:46 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 02 15:16:46 2014

@author: ipcv5
"""
import numpy as np
 
from PIL import Image	
import cv2
from mylib import pickleload, picklethis
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
import time
from scipy.ndimage import binary_dilation as dilate
from scipy.ndimage import binary_fill_holes as fill

def show(x):
    toimage(x).show()


    
starttime=time.time()
#def superb(fname=None):
if 1:
    fname=None
    if fname==None:
        fname='14_a'
        fname='9_a'
        fname='6_a'
        fname='15_a'
        fname='9_b'
        fname='7_a'
        fname='5_a'
        fname='16_a'
        fname='5_a'
        fname='8_a'
        fname='9_a'
        fname='10_a'
        fname='20_a'
        fname='26_b'

    print fname    
    fill2=np.asarray(imread('Outputs\\Restart\\'+fname+'tempfill'+'.png'), dtype=bool)

    print np.sum(fill2)
    print 'start'    

    ans=ndimage.morphology.distance_transform_cdt(fill2, metric='chessboard')    
    
    loc=np.where((ans<2) & (ans>0))

    
    fill2copy=fill2.copy()
    fill2copy[loc]=0

    

    curr=fill2copy
    curr=ndimage.grey_erosion(curr, size=(5,5))
    ccarr, ccnum=ndimage.label(curr, np.ones((3,3)))    
    ccarr=ccarr.astype(np.int16)
    temp=list(np.bincount(ccarr.flatten()))
    
    sortedtemp=sorted(temp, reverse=True)
    sortedtemp.remove(sortedtemp[0])    
    

    for index in range(len(sortedtemp)-1):
        now=sortedtemp[index]
        nxt=sortedtemp[index+1]
        if now - nxt < 200:
            thresh=now
            break
    
    thresh=10000
    for index, i in enumerate(temp):
        if i <= thresh:
            curr[ccarr==index]=0

    imsave('Outputs\\Restart\\Forsir1\\'+fname+'.png', curr)
    show(curr)
        


#lis=['5_a', '8_a', '14_a', '6_a', '15_a', '9_a']
#for i in lis:
##    print i
#    superb(i)
#    j=i[:-1]+'b'
##    print j
#    superb(j)

#lis=pickleload('Outputs\\fnamelist')
#for i in lis[::-1]:
#    print i
#    superb(i)
#    j=i[:-1]+'b'
#    print j
#    superb(j)


#lis=[2, 3, '4_1', '4_2', 7, 16]
#for i in lis:
#    j1=str(i)+'_a'
#    superb(j1)
#    j=j1[:-1]+'b'
#    superb(j)


print time.time()-starttime, 'seconds'