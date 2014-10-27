

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


def zerofunc(x):
    return 0

def show(x):
    toimage(x).show()

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
        fname='8_a'
        fname='5_b'
        fname='6_a'
        fname='4_6_a'
        fname='5_a'
        
        
    print fname
    imname = 'Outputs\\Skeletons\\'+fname+'.png'
    skel=np.asarray(imread(imname), dtype=bool)
    original=skel.copy()
    
    fill1=np.asarray(imread('Outputs\\SegmentMasks\\'+fname+'fill.png'), dtype=bool)
    fillarr, noofsegments=ndimage.label(fill1, np.ones((3,3)))
    
    segexamplelist=[]
    for i in range(1,noofsegments+1):
        zipp=np.where(fillarr==i)
        segexamplelist.append((zipp[0][0], zipp[1][0]))
    fill1=ndimage.grey_dilation(fill1, size=(50,50))
    
    skelfillorg=fill(skel)
    skelfill=xor(skelfillorg, skel)
    skelfill=dilate(skelfill, size=(3,3))
    
    skel=(xor(skelfill, skelfillorg))    

#    ccarr, ccnum=label(skel, np.ones((3,3)))
#    
#    ccarr=ccarr.astype(np.uint16)
#    binfill=list(np.bincount(ccarr.flatten()))
#    bfill=sorted(binfill, reverse=True)
#    bfill.remove(bfill[0])
#    
#    structure=np.zeros((3,3), dtype=bool)
#    structure[1,1]=True
#    show(ndimage.bin)
#    for i in range(len(binfill)):
#        if binfill[i]<=5:
#            ccarr[ccarr==i]=0
        

    
#==============================================================================
#     
#==============================================================================
    mins=np.logical_and(fill1, skel)
    minmin=np.logical_xor(skel, mins)
    
    skeldil=dilate(skel, size=(5,5))
    

    SIZE=35

    bigelement=np.zeros((SIZE, SIZE), dtype=bool)
    bigelement[(SIZE-1)/2, :]=True

    element=np.array([[False, False, False], [True, True, True], [False, False, False]])
    min1 = (ndimage.binary_erosion(minmin, element))
    minmin1=ndimage.binary_dilation(min1, bigelement)
    print np.sum(min1), np.sum(minmin1)

    bigelementv=np.zeros((SIZE, SIZE), dtype=bool)
    bigelementv[:, (SIZE-1)/2]=True
    element1=np.array([[False, True, False], [False, True, False], [False, True, False]])
    min2 = (ndimage.binary_erosion(minmin, element1))
    minmin2=ndimage.binary_dilation(min2, bigelementv)
    print np.sum(min2), np.sum(minmin2)


    slants=xor(minmin, min2)
    slants=xor(slants, min1)
    slantsdil=dilate(slants, size=(5,5))

    slantsarr, slantsnum =label(slantsdil, np.ones((3,3)))
    slantsarr=slantsarr.astype(np.uint16)
    binfill=list(np.bincount(slantsarr.flatten()))
    bfill=sorted(binfill, reverse=True)
    bfill.remove(bfill[0])
    
    for i in range(len(binfill)):
        if binfill[i]<=100:
            slantsdil[slantsarr==i]=False


#Obtain MinMinz
    minminz=np.zeros(minmin2.shape, dtype=bool)
    minminz=(np.logical_or(skeldil, minmin1))
    minminz=(np.logical_or(slantsdil, minmin1))
    minminz=(np.logical_or(minminz, minmin2))
    minminz=(np.logical_or(minminz, fill1))
    
    ccarr, ccnum=label(minminz, np.ones((3,3)))
    print ccnum
    
    ccarr=ccarr.astype(np.uint16)
    binfill=list(np.bincount(ccarr.flatten()))
    bfill=sorted(binfill, reverse=True)
    bfill.remove(bfill[0])
    
#    show(minminz)
    for i in range(len(binfill)):
        if binfill[i]<=500:
            minminz[ccarr==i]=False
        
    ccarr1, ccnum1=label(minminz, np.ones((3,3)))
    print ccnum1
#    show(minminz)
    
    ansans=logor(original, minmin1)
    ansans=logor(ansans, minmin2)
    ansans=logor(ansans, slantsdil)    

    z1=np.asarray(imread('Outputs\\GetStrings\\'+fname+'strmaskdil.png'), dtype=bool)
    final=logor(z1, minminz)
    farr, fnum=ndimage.label(final, np.ones((3,3)))

    actualsegments=[]
    for i in segexamplelist:
        a,b=i
        actualsegments.append(farr[a,b])
        
#    for i in fnum:
#        if i not in actualsegments:
#            zipp=np.where(farr==i)
#            zipp1=zip(*zipp)
#            a=min
    
    if fnum != noofsegments:
        print 'Oh No', fnum, noofsegments
    else:
        print 'Good work! '
    imsave('Outputs\\Assoc\\'+fname+'withtext.png', final)
    imsave('Outputs\\Assoc\\'+fname+'check.png', minminz)
    imsave('Outputs\\Assoc\\'+fname+'.png', ansans)
    

#    show(logor(minminz, skel))
#    minminz=np.logical_or(minminz, fill1)


#flist=['6_a', '8_a']
#flist=pickleload('Outputs\\fnamelist')
#for i in flist[::-1]:
#    print i
#    extend(i)
#    
#    j=i[:-1]+'b'
#    print j
#    extend(j)
#
    print time.time() - starttime, "seconds"

