# -*- coding: utf-8 -*-
"""
NO OVERLAP of stringmask and segmentmask

DENSITY = 0.05
Created on Fri Apr 04 15:43:57 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
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
dilate=ndimage.binary_dilation
fill=ndimage.binary_fill_holes
def show(x):
    toimage(x).show()

xor=np.logical_xor
def which(a,b):
    i=0
    while(1):
        try:
            if a[i] <= 10000:
                if b[i] <= 10000:
                    if np.sum(a[:i]) > np.sum(b[:i]):
                        return 2
                    else:
                        return 1
                else:
                    return 1
            else:
                if b[i] <=10000:
                    return 2
            i=i+1
        except IndexError:
            if a[i-1]<b[i-1]:
                return 1
            else:
                return 2
    
starttime=time.time()
#def superbcheck(fname=None):
if 1:
    fname=None
    if fname==None:
        fname='26_b'
        fname='22_a'
        fname='7_4_b'
        fname='1_a'
        fname='8_a'
        fname='6_a'
        fname='5_a'
        fname='15_a'
        fname='14_a'
        fname='4_6_a'
        fname='17_a'
        fname='7_5_b'
        fname='3_a'

    #Vital Constants
    TEXTBOX_DENSITY=0.05
    print fname    
    fill1=np.asarray(imread('Outputs\\Restart\\Forsir1\\'+fname+'.png'), dtype=bool)
    imgoriginal=np.asarray(imread('Outputs\\stringmask'+fname+'.png'), dtype=bool)
    img=imgoriginal.copy()
    original=np.asarray(imread('images_consolidated\\'+fname+'.png'), dtype=bool)
    
    z=np.logical_and(img, fill1)        
    fillcopy=fill1.copy()
    if np.sum(z)==0:    # I.e NO OVERLAP of stringmask and segmentmask
        print 'cool'
        imsave('Outputs\\SegmentMasks1\\'+fname+'fill.png', fill1)
        imsave('Outputs\\SegmentMasks1\\'+fname+'checking.png',xor(fill1, original))
    else:       #Stringmask and Segmentmasks overlap. Remains to be seen if the overlap is considerable enough to cause removal of a segment or two
        
#        show(z)
        
        
        ccfill, ccnumfill = ndimage.label(fill1, np.ones((3,3)))    
        ans=img*ccfill        
            
        ccfill=ccfill.astype(np.uint16)
        binfill=list(np.bincount(ccfill.flatten()))
        bfill=sorted(binfill, reverse=True)
        bfill.remove(bfill[0])

        ans=ans.astype(np.uint16)
        binans=list(np.bincount(ans.flatten()))
        
        print binans
        print binfill
        
        for i in range(1,len(binans)):
            if binans[i] > TEXTBOX_DENSITY*binfill[i]:
                print binans[i], binfill[i], (binans[i]/float(binfill[i])),'improved'
                fillcopy[ccfill==i]=False
#        show(xor(fillcopy, original))
#        show(fillcopy)
        imsave('Outputs\\SegmentMasks1\\'+fname+'checking.png', np.logical_xor(fillcopy, original))
        imsave('Outputs\\SegmentMasks1\\'+fname+'fill.png', fillcopy)

#flist=pickleload('Outputs\\fnamelist')
#for i in flist[::-1]:
#    superbcheck(i)
#    j=i[:-1]+'b'
#    superbcheck(j)
    







print time.time()-starttime, 'seconds'