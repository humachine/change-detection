# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:15:03 2014

@author: ipcv5
"""
#from untitled0.py import generateimage
from operator import itemgetter, attrgetter
from scipy import ndimage
import numpy as np
import scipy
from scipy.misc import imread, imsave, imshow, toimage
from PIL import Image
import numpy as np
import time
from mylib import picklethis, pickleload
import random
from numba import double, jit
import logging

class component:
    def __init__(self, ul0, ul1, lr0, lr1, ccdictno, width=None, height=None, direction=None, top=None, bottom=None):
        self.ul0 = ul0
        self.top =top
        self.bottom=bottom
        self.ul1 = ul1
        self.lr0 = lr0   
        self.lr1 = lr1   
        self.ccdictno=ccdictno
  
        self.height = self.lr0-self.ul0
        self.width = self.lr1-self.ul1
        if(self.height < self.width):
            self.direction='v'
        else:
            self.direction='v'
            

    def __repr__(self):
        return repr((self.ccdictno))

class compstring:
    def __init__(self, listofcomps, direction):
        self.listofcomps = listofcomps
        self.direction = direction
    def __repr__(self):
        return repr(self.direction)

def generateimage(componentslist, height, width, listofindices=None):
    img2=np.zeros((height, width), dtype=bool)

    if listofindices==None:
        for i in componentslist:
            img2[i.ul0:i.lr0, i.ul1:i.lr1]=True
    else:
        for i in listofindices:
            if isinstance(i, list):
                for char in i:
                    
                    j=componentslist[char]
                    img2[j.ul0:j.lr0, j.ul1:j.lr1]=True
            else:
                print type(i)
                j=componentslist[i]
                
                img2[j.ul0:j.lr0, j.ul1:j.lr1]=True
            
    return img2
    
    
    
starttime=time.time()

imname='ss.png'
imname='ok.png'
imname='bits.png'
imname='textonly.png'
imname='images_consolidated\\8_a.png'
imname='images_consolidated\\5_a.png'
imname='images_consolidated\\6_a.png'
fname = imname[-7:-4]
img=np.asarray(imread(imname), dtype=bool)
imm=img.copy()
height, width=img.shape



strel=np.ones((3,3), dtype=bool)
strel[0,0]=strel[0,2]=strel[2,0]=strel[2,2]=False

textcomplist=pickleload('textcomplist' + fname + '.pkl')
ccdict=pickleload('ccdict'+ fname)
num=pickleload('ccnum' + fname)
    

    
#print img[208, 3399], img[3399, 208]
clslist=[]

height, width=img.shape
img1=np.zeros(img.shape, dtype=bool)
for i in textcomplist:
    for j in ccdict[i]:
        a,b=j
        img1[b,a]=True
        imm[b,a]=False
#toimage(img1).show()
imsave('notext' + fname + '.png', imm)

noofcomponents=len(textcomplist)


for i in textcomplist:
    zipdict = zip(*ccdict[i])

    minr = min(zipdict[0])
    maxr = max(zipdict[0])
    minc = min(zipdict[1])
    maxc = max(zipdict[1])

    ul0, ul1 = (minc, minr)
    lr0, lr1= (maxc,maxr)
    
    clslist.append(component(ul0, ul1, lr0, lr1, i))

#==============================================================================
# 
#==============================================================================

sortedlistv=sorted(clslist, key=attrgetter('ul0'))
print len(sortedlistv)
sortedlistv.append(component(height-2, width-2, height-1, width-1, 0))
sortedlisth=sorted(clslist, key=attrgetter('ul1'))



strlist=[]
for i in range(noofcomponents):
    strlist.append([])

for i in range(noofcomponents):
#    print 
    curr=sortedlistv[i]
    if curr.direction == 'v':
        currdepth=curr.lr0
        
        j=i+1
        work=sortedlistv[j]
        while j<noofcomponents and abs(work.ul0-currdepth)<=30 :
            if work.direction=='v':
                if abs(work.ul1-curr.ul1)<=2 and abs(work.lr1-curr.lr1)<=2 :
                    curr.bottom=j
                    if curr.top==None:
                        sortedlistv[j].top=i
                        strlist[i].append(i)
                        strlist[i].append(j)
#                        print i, 'is new head'
                    else:
                        sortedlistv[j].top=curr.top
                        strlist[curr.top].append(j)
#                        print i, 'joins somewhere'
                    break
            j+=1
            work=sortedlistv[j]
for i in range(noofcomponents):
    curr=sortedlistv[i]
    if curr.top == None and curr.bottom==None:
        strlist[i].append(i)
            
list2 = [x for x in strlist if x]
print len(list2)

img2=generateimage(sortedlistv, height, width, strlist)
#toimage(img2).show()

img3=np.zeros(img2.shape, dtype=bool)
for i in list2:
    print i
    j=i[0]
    j1=i[-1]
    
    char=sortedlistv[j]
    char1=sortedlistv[j1]
    img3[char.ul0:char1.lr0, char.ul1:char.lr1]=True
toimage(img3).show()



print time.time()-starttime, ' seconds'


