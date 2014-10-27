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
from scipy.ndimage import binary_dilation as dilate
from scipy.ndimage import binary_fill_holes as fill

starttime = time.time() 

def circular_structure(radius):
    size = radius*2+1
    i,j = np.mgrid[0:size, 0:size]
    i -= (size/2)
    j -= (size/2)
    return np.sqrt(i**2+j**2) <= radius

def show(x):
    toimage(x).show()
 
def sk(i, r=None): 
    x = ndimage.distance_transform_edt(i) 
    if r==None:
        y = ndimage.morphological_laplace(x) 
    else:
        y = ndimage.morphological_laplace(x, (r, r)) 
        #r=5 , TYPICALLY
    return y < y.min()/2  

def thinfast(fname=None, r=5):
#def sk(i, r=None): 
    timestart=time.time()
    i=np.asarray(imread('Outputs\\notext'+fname+'.png'), dtype=bool)
#    r=5
    x = ndimage.distance_transform_edt(i) 
    if r==None:
        y = ndimage.morphological_laplace(x) 
    else:
        y = ndimage.morphological_laplace(x, (r, r)) 
        #r=5 , TYPICALLY
    print time.time()-timestart
#    ans=y < y.min()/2  
#    imsave('Outputs\\Laplace\\zzlabelinglinesremoved'+fname+'.png', np.invert(ans))
    return y < y.min()/2  
 
def allimgs():
    flist=pickleload('Outputs\\fnamelist')
    for i in flist[::-1]:
        print i
        thinfast(i)
        j=i[:-1]+'b'
        print j
        thinfast(j)
        print
    
 
def createskeleton(imname):
    img = cv2.imread(imname,0)
    size = np.size(img)
    skel = np.zeros(img.shape,np.uint8)
     
    ret,img = cv2.threshold(img,127,255,0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
    
    
    while( not done):
        eroded = cv2.erode(img,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(img,temp)
        skel = cv2.bitwise_or(skel,temp)
        img = eroded.copy()
   
        zeros = size - cv2.countNonZero(img)
        if zeros==size:
            done = True
    return skel
def thinning(fname=None):
#if 1:
#    fname=None
    if fname==None:
        fname='8_b'
        fname='5_b'
        fname='6_b'
        fname='1_2_b'
        fname='9_a'
        fname='15_b'
        fname='4_5_b'
        fname='4_1_a'
        fname='5_a'
        fname='8_a'
        fname='6_a'
        fname='15_a'
        fname='14_a'
        
        
    print fname
    imname = 'Outputs\\notext'+fname+'.png'
    imgoriginal=np.asarray(imread(imname), dtype=bool)
    
    skel=createskeleton(imname)
#    cv2.imwrite('Outputs\\works.png', skel)
    
    img1=np.asarray(imread(imname))
    newarr1=np.subtract(img1, skel).astype(bool)
#    show(skel)
    imsave('Outputs\\Skeletons\\'+fname+'.png', skel)

#        fill1=fill(newarr1)    
#        print np.sum(fill1)
#    #    skel=skel.astype(bool)
#    #
#    #
#        newarr=img1
#        a = ndimage.binary_erosion(newarr, element)
#        z=(np.subtract( a.astype(int), skel.astype(int) ).astype(int))
#        y=z
#        y[y<0]=0
#        z=y.copy().astype(bool)
#        fill2=fill(z)
#        print np.sum(fill2)
#    #    diff=(np.subtract(fill1, fill2))
#    #    imsave('Outputs\\Restart\\'+'tempfill'+fname+'.png', fill(diff))
#    
#    #    show(fill(z))
#    
#    #    imsave('Outputs\\Restart\\'+fname+'tempfill'+'.png', fill1)
#        imsave('Outputs\\Restart\\'+fname+'fill'+'.png', fill2)
#    #    show(fill1)
#    #    show(fill2)
#    
#       
#    
#    
#    #    
#    #    print time.time() - starttime, ' after removal'
#    #    
#    
       
    
    
if __name__ == "__main__":
#    lis=['5_a', '8_a', '14_a', '6_a', '15_a', '9_a']
#    for i in lis:
##        j1=str(i)+'_a'
#        j1=i
#        thinning(j1)
#        j=j1[:-1]+'b'
#        thinning(j)

    flist=pickleload('Outputs\\fnamelist')
    for i in flist[::-1]:
        print i
        thinning(i)
        j=i[:-1]+'b'
        print j
        thinning(j)
        print 
#   

#    lis=[2, 3, '4_1', '4_2', 7, 16]
#    for i in lis:
#        j1=str(i)+'_a'
#        thinning(j1)
#        j=j1[:-1]+'b'
#        thinning(j)

        
#    zz=thinfast('5_a')
#    zz=ndimage.grey_dilation(zz, size=(10, 10))
#    show(fill(zz))

#    thinning()
#    allimgs()
#    thinning()
    print time.time() - starttime, "seconds"

