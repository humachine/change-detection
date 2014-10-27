# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 04:54:47 2014

@author: ipcv5
"""
import numpy as np
import pickle
from PIL import Image	
import cv2
import mylib
from mylib import pickleload, picklethis, show
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from binlabeller import bwlabel
from scipy import ndimage
import time
from binlabeller import bwlabel

starttime = time.time() 

class compstring:
    def __init__(self, listofcomps, direction, segment=None):
        self.listofcomps = listofcomps
        self.direction = direction
        self.segment= segment
    def __repr__(self):
        return repr(self.direction)

fname='15_b'


fname='5_b'
fname='6_a'
fname='8_a'

imname = 'Outputs\\labelinglinesremoved'+fname+'.png'

ccnum=pickleload('Outputs\\ccnum'+fname+'.pkl')
ccdict=pickleload('Outputs\\ccdict'+fname+'.pkl')
textcomplist=pickleload('Outputs\\textcomplist'+fname+'.pkl')
img1=np.asarray(imread(imname), dtype=bool)

assoclist=mylib.pickleload('Outputs\\assoclist'+fname+'.pkl')


images=[]
noofsegments=np.max(assoclist)
for i in range(noofsegments):
    images.append(np.zeros(img1.shape))
    
for i in range(1, ccnum+1):
    col=assoclist[i]
    
    if col >=1:
        for j in ccdict[i]:
            a,b=j
            images[col-1][b,a]=(col*255)/noofsegments


starttime = time.time() 
strmask=np.asarray(imread('Outputs\\stringmaskdil'+fname+'.png', 'r'), dtype=bool)
#show(strmask)
#            images[col-1][b,a]=(col*255)/noofsegments

for i in range(noofsegments):
    workimg=images[i]
    dylan=ndimage.binary_dilation(workimg, np.ones((3,3)))
    ans=np.bitwise_and(strmask, dylan)
    show(ans)
    print sum(ans)

orig=np.asarray(imread(fname+'.png'), dtype=bool)
a=open('Outputs\\getstrings'+fname+'.pkl', 'r')
list1=pickle.load(a)
list2=pickle.load(a)
hlist=pickle.load(a)
vlist=pickle.load(a)
a.close()

newimg=np.zeros((img1.shape))
for i in list1:
    j=i[0]
    j1=i[-1]
    
    print j, j1
    ul1=horlist[j].ul1
#    ul0=min(horlist[j].ul0, horlist[j1].ul0)
#    lr0=max(horlist[j].lr0, horlist[j1].lr0)
#    lr1=horlist[j1].lr1
#    
#    newimg[ul0:lr0+1, ul1:lr1+1]=orig[ul0:lr0+1, ul1:lr1+1]
    
    
        

##show(colorimg)
print time.time() - starttime, ' readfiles'
