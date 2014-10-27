# -*- coding: utf-8 -*-
"""
Created on Fri Mar 07 16:14:16 2014

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
fname='8_a'
fname='5_a'
fname='15_a'
fname='5_b'
fname='8_b'
fname='6_b'

fname='15_b'
fname='19_a'
fname='10_a'

# 
imname = 'images_consolidated\\'+fname+'.png'


#img=Image.open(imname)
#img=img.convert('1')
#ccdict1, arr, ccnum, _ = bwlabel(img)
#print np.sum(np.where(arr>0))
#print ccnum
#print time.time() - starttime
#


#starttime=time.time()
#im=Image.open(imname)
#im=im.convert('1')
#ccdict, _, ccnum, _ = bwlabel(im)
#
#
#clen=[]
#for i in range(1, ccnum+1):
#    clen.append(len(ccdict[i]))
#print sorted(clen, reverse=True)[-1]
#
#print time.time() - starttime

starttime=time.time()

a=np.asarray(imread(imname), dtype=bool)
ccarr, num = ndimage.label(a, np.ones((3,3)))

ccdict={}
for j in range(1, num+1):
    ccdict[j]=[]
j=np.where(ccarr>0)
#clen1=[]
#for index, x in np.ndenumerate(j[0]):
##    ccdict[ccarr[x]].append(x)
#    ccdict[ccarr[x, j[1][index]]].append((x, j[1][index]))
#for i in range(1, num+1):
#    clen1.append(len(ccdict[i]))
#print sorted(clen1, reverse=True)[-1]
        
        


print time.time() - starttime


#==============================================================================
#   NO SPLITS
#==============================================================================
#==============================================================================
# starttime=time.time()
# 
# a=np.asarray(imread(imname), dtype=bool)
# height, width=a.shape
# ccarr, num=ndimage.label(a, np.ones((3,3)))
# ccdict={}
# j1=np.where(ccarr>0)
# 
# for i in range(1, num+1):
#     ccdict[i]=[]
# 
# 
# for i in range(1, num+1):
#     j2=np.where(ccarr[j1]==i)
#     for j in j2[0]:
#         ccdict[i].append((j1[1][j], j1[0][j]))
# 
# clen=[]
# for i in range(1, num+1):
#     clen.append(len(ccdict[i]))
# print sorted(clen, reverse=True)[-1]
#print time.time() - starttime
#==============================================================================



#==============================================================================
#   SPLIT INTO 4 PARTS
#==============================================================================
#==============================================================================
# 
# starttime=time.time()
# ccdict={}
# for i in range(1, num+1):
#     ccdict[i]=[]
# 
# j1=np.where((ccarr>0) & (ccarr<num/4))
# for i in range(1, num/4):
#     j2=np.where(ccarr[j1]==i)
#     for j in j2[0]:
#         ccdict[i].append((j1[1][j], j1[0][j]))
# 
# j1=np.where((ccarr>=num/4) & (ccarr<num/2))
# for i in range(num/4, num/2):
#     j2=np.where(ccarr[j1]==i)
#     for j in j2[0]:
#         ccdict[i].append((j1[1][j], j1[0][j]))
# 
# 
# j1=np.where((ccarr>=num/2) & (ccarr<(3*num)/4))
# for i in range(num/2, (3*num)/4):
#     j2=np.where(ccarr[j1]==i)
#     for j in j2[0]:
#         ccdict[i].append((j1[1][j], j1[0][j]))
# 
# j1=np.where((ccarr>=3*num/4))
# for i in range((3*num)/4, num+1):
#     j2=np.where(ccarr[j1]==i)
#     for j in j2[0]:
#        ccdict[i].append((j1[1][j], j1[0][j]))
# 
# clen=[]
# for i in range(1, num+1):
#     clen.append(len(ccdict[i]))
# print sorted(clen, reverse=True)[-1]
#print time.time() - starttime
#==============================================================================





#im=Image.open(imname)    
#im=im.convert('1')
#dict1, oldarr, num1, _ = bwlabel(im)
#print num1
#
#some1=0
#clen1=[]
#for i in range(1, 43):
#    clen1.append(len(dict1[i]))
#
#sort1=sorted(clen, reverse=True)
#sort2=sorted(clen1, reverse=True)
#for i in range(42):
#    print sort1[i], sort2[i]

    
#print np.sum(np.where(ccarr>0))
#print num




