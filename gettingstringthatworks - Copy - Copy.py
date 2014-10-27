# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:15:03 2014

@author: ipcv5
"""
from operator import itemgetter, attrgetter
import pickle
from scipy import ndimage
from scipy.misc import imread, imsave, imshow, toimage
from PIL import Image
import numpy as np
import time
from mylib import picklethis, pickleload
import random

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
            self.direction='h'
            

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
                try:
                    j=componentslist[i]
                    img2[j.ul0:j.lr0, j.ul1:j.lr1]=True
                except IndexError, e:
                    print i, e
            
    return img2

def show(x):
    toimage(x).show()    
    
    
starttime=time.time()

imname='ss.png'
imname='ok.png'
imname='bits.png'
imname='textonly.png'
imname='images_consolidated\\5_b.png'
imname='images_consolidated\\6_a.png'
imname='images_consolidated\\15_b.png'
imname='images_consolidated\\8_a.png'

i=imname.rfind('\\')
fname=imname[i+1:]
fname=fname[:-4]
    

img=np.asarray(imread(imname), dtype=bool)
imm=img.copy()
height, width=img.shape



strel=np.ones((3,3), dtype=bool)
strel[0,0]=strel[0,2]=strel[2,0]=strel[2,2]=False

textcomplist=pickleload('Outputs\\textcomplist' + fname + '.pkl')
ccdict=pickleload('Outputs\\ccdict'+ fname)
num=pickleload('Outputs\\ccnum' + fname)
    

    
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
imsave('Outputs\\notext' + fname + '.png', imm)


textcomplist= [x for x in textcomplist  if len(ccdict[x])>=20]
            

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

horlist=[]
vertlist=[]
for i in range(noofcomponents):
    curr=clslist[i]
    if curr.direction=='h':
        horlist.append(curr)
    elif curr.direction=='v':
        vertlist.append(curr)
    
hcount=len(horlist)
vcount=len(vertlist)

vlist=sorted(vertlist, key=attrgetter('ul0'))
vlist.append(component(height-2, width-2, height-1, width-1, 0))
vlist[-1].direction='v'

hlist=sorted(horlist, key=attrgetter('ul1'))
hlist.append(component(height-4, width-4, height-3, width-3, 0))
hlist[-1].direction='h'


#==============================================================================
# 
#==============================================================================


    
    

hstrlist=[]
for i in range(hcount):
    hstrlist.append([])
vstrlist=[[]]*vcount

PADDING = 60
TOLERANCE=5

for i in range(hcount):
    
    curr=hlist[i]
    currdepth=curr.lr1
    
    j=i+1
    work=hlist[j]

    while j<hcount and abs(work.ul1-currdepth)<=PADDING :

        if abs(work.ul0-curr.ul0)<=TOLERANCE and abs(work.lr0-curr.lr0)<=TOLERANCE :
            curr.bottom=j
            
            if curr.top==None:
                hlist[j].top=i
                hstrlist[i].append(i)
                hstrlist[i].append(j)
            else:
                hlist[j].top=curr.top
                hstrlist[curr.top].append(j)
            break
        j+=1
        work=hlist[j]

for i in range(hcount):
    curr=hlist[i]
    if curr.top == None and curr.bottom==None:
        hstrlist[i].append(i)

list2 = [x for x in hstrlist if x]

img3=np.zeros(img1.shape, dtype=bool)
for i in list2:
    j=i[0]
    j1=i[-1]
    
    char=hlist[j]
    char1=hlist[j1]

    img3[char.ul0:char.lr0, char.ul1:char1.lr1]=True
#toimage(img3).show()


#==============================================================================
# 
#==============================================================================


vstrlist=[]
for i in range(vcount):
    vstrlist.append([])



for i in range(vcount):
    
    curr=vlist[i]
    currdepth=curr.lr0
    
    j=i+1
    work=vlist[j]

    while j<vcount and abs(work.ul0-currdepth)<=PADDING :
#        print abs(work.ul0-curr.ul0), abs(work.lr0-curr.lr0)

        if abs(work.ul1-curr.ul1)<=TOLERANCE and abs(work.lr1-curr.lr1)<=TOLERANCE :
            curr.bottom=j
            
            if curr.top==None:
                vlist[j].top=i
                vstrlist[i].append(i)
                vstrlist[i].append(j)
            else:
                vlist[j].top=curr.top
                vstrlist[curr.top].append(j)
            break
        j+=1
        work=vlist[j]

for i in range(vcount):
    curr=vlist[i]
    if curr.top == None and curr.bottom==None:
        vstrlist[i].append(i)

list1 = [x for x in vstrlist if x]

img2=img3
#img2=np.zeros(img1.shape, dtype=bool)
for i in list1:
    
    j=i[0]
    j1=i[-1]
    
    char=vlist[j]
    char1=vlist[j1]
#    print char.ul0, char1.lr0
    
    img2[char.ul0:char1.lr0, char.ul1:char.lr1]=True
#toimage(img2).show()
imsave('Outputs\\stringmask'+fname+'.png', img2)

a=open('Outputs\\getstrings'+fname+'.pkl', 'w')
pickle.dump(list1, a)
pickle.dump(list2, a)
pickle.dump(horlist, a)
pickle.dump(vertlist, a)
a.close()


print time.time()-starttime, ' seconds'


