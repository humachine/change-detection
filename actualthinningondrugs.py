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
from binlabeller import bwlabel
from scipy import ndimage
import time
from binlabeller import bwlabel

starttime = time.time() 

def circular_structure(radius):
    size = radius*2+1
    i,j = np.mgrid[0:size, 0:size]
    i -= (size/2)
    j -= (size/2)
    return np.sqrt(i**2+j**2) <= radius

def show(x):
    toimage(x).show()
 
def thinning(fname=None):
#if 1:
#    fname=None
    if fname==None:
        fname='8_a'
        fname='6_a'
        fname='5_b'
        fname='15_b'
        
        fname='5_a'
        
        fname='8_b'
        fname='6_b'
        fname='15_a'
        fname='14_a'


    imname = 'Outputs\\notext'+fname+'.png'
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
     
    cv2.imwrite('Outputs\\works.png', skel)
    
    img1=np.asarray(imread(imname))
    newarr=np.subtract(img1, skel)
    skel=skel.astype(bool)
    #
    newarr=img1
    #if iswhitebg(newarr):
    #    newarr=np.invert(newarr)
    
    print 'reached'
    
    a = ndimage.binary_erosion(newarr, element)
    z=(np.subtract( a.astype(int), skel.astype(int) ).astype(int))
    y=z
    y[y<0]=0
    z=y.copy()
    
    print time.time() - starttime, ' after removal'
    z=ndimage.binary_closing(z, np.ones((15,15)))
    print time.time() - starttime, ' after closing'
    #z=(ndimage.binary_fill_holes(z))
    print time.time() - starttime, ' after filling'
    imsave('Outputs\\tempfill.png', np.invert(z))
    
    a=Image.open('Outputs\\tempfill.png')
    a=a.convert('1')
    ccdict, _, count, out = bwlabel(a)
    print count
    
    complen=[]
    complen.append(0)
    for i in range(1, count+1):
        complen.append(len(ccdict[i]))
    
    prev=complen[0]
    i=1
    threshold=complen[0]/10
    a=sorted(complen, reverse=True)
    while(i<len(complen)):
        curr=a[i]
        if curr*2 < prev:
            threshold=curr+10
            break
        if curr < 500:
            threshold = 500
            break
        i=i+1
        prev=curr
    
    print threshold
    
    im2=z.copy()
    #labellist=[]
    for i in range(1, count+1):
        if len(ccdict[i])<threshold:
    #        labellist.append(i)
            for j in ccdict[i]:
                a,b=j
                im2[b,a]=False
    #picklethis(labellist, 'Outputs\\labellist'+fname)
    filled=(ndimage.binary_fill_holes(im2))
    #show(filled)
    
    im3=z.copy()
    im3=np.ones(z.shape)
    dens=[0]
    for i in range(1, count+1):
        density=0
        for j in ccdict[i]:
            a,b=j
            if filled[b,a]==True:
                density+=1
        dens.append(density)
    
    im2=z.copy()
    casual=[]
    for i in range(1, count+1):
        if len(ccdict[i])<threshold and complen[i]>dens[i]:
            for j in ccdict[i]:
                a,b=j
                im2[b,a]=False
            casual.append(i)
        else:
            if len(ccdict[i])<500:
                for j in ccdict[i]:
                    a,b=j
                    im2[b,a]=False
            casual.append(i)
        
                
    #show(im2)
    
    #show(im3)
    
    
    
    imsave('Outputs\\zzlabelinglinesremoved'+fname+'.png', np.invert(im2))
       
    
    #imsave('temptemp.png', np.invert(a))
    #imgforlabelling=Image.open('temptemp.png')
    #imgforlabelling=imgforlabelling.convert('1')
    #skeldict, _, skelcount, out=bwlabel(imgforlabelling)
    
    #show(a)
    #solid=np.subtract(a, skel)
    #imsave('labelinglinesremoved'+fname[-7:-4]+'.png', solid)
    
    
if __name__ == "__main__":
    flist=pickleload('Outputs\\fnamelist')
    for i in flist[::-1]:
        print i
        thinning(i)
        j=i[:-1]+'b'
        print j
        thinning(j)
        print 
#    thinning()
    print time.time() - starttime, "seconds"

