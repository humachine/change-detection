# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 04:54:47 2014
FINAL
LIST1 - VERTLIST
LIST2 - HORLIST
@author: ipcv5
"""
import numpy as np
from operator import itemgetter, attrgetter
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


def associations(fname=None):
    if fname==None:
        fname='6_b'
        fname='15_a'
        fname='8_a'
        fname='8_b'
        fname='6_a'
        fname='15_b'
        fname='5_a'
        fname='5_b'

    imname = 'Outputs\\labelinglinesremoved'+fname+'.png'
    
    ccnum=pickleload('Outputs\\ccnum'+fname+'.pkl')
    ccdict=pickleload('Outputs\\ccdict'+fname+'.pkl')
    textcomplist=pickleload('Outputs\\textcomplist'+fname+'.pkl')
    img1=np.asarray(imread(imname), dtype=bool)
    height, width = img1.shape
    assoclist=mylib.pickleload('Outputs\\assoclist'+fname+'.pkl')
    
    imgoriginal=np.asarray(imread('images_consolidated\\'+fname+'.png'), dtype=bool)
    
    images=[]
    for i in range(np.max(assoclist)):
        images.append(np.zeros((img1.shape), dtype=bool))
        
    noofsegments=np.max(assoclist)
    allseg=np.zeros(img1.shape, dtype=np.int8)
    for i in range(1, ccnum+1):
        col=assoclist[i]
        
        if col >=1:
            for j in ccdict[i]:
                a,b=j
                allseg[b,a]=col
                images[col-1][b,a]=True
    
    workimg=images[0]
    
    strmask=np.asarray(imread('Outputs\\stringmaskdil'+fname+'.png', 'r'), dtype=bool)
    #show(strmask)
    #            images[col-1][b,a]=(col*255)/noofsegments
    #show(ans)
    
    #==============================================================================
    #  HORLIST , VLIST GENERATION STARTS
    #==============================================================================
    
    a=open('Outputs\\getstrings'+fname+'.pkl', 'r')
    list1=pickle.load(a)
    list2=pickle.load(a)
    a.close()
    
    
    textcomplist= [x for x in textcomplist  if len(ccdict[x])>=20]
    noofcomponents=len(textcomplist)
    
    clslist=[]
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
    
    vlist=sorted(vertlist, key=attrgetter('ul0'))
    vlist.append(component(height-2, width-2, height-1, width-1, 0))
    vlist[-1].direction='v'
    
    hlist=sorted(horlist, key=attrgetter('ul1'))
    hlist.append(component(height-4, width-4, height-3, width-3, 0))
    hlist[-1].direction='h'
    
    
    #==============================================================================
    # HORLIST , VLIST GENERATION ENDS
    #==============================================================================
    
    stringlist=[]
    stringlist1=[]  
    newnewimg=np.zeros((img1.shape), dtype=bool)
    for i in list2:
        j=i[0]
        j1=i[-1]
        
        ul0=min(hlist[j].ul0, hlist[j1].ul0)
        ul1=hlist[j].ul1
        
        lr0=max(hlist[j].lr0, hlist[j1].lr0)
        lr1=hlist[j1].lr1
    
    #    print ul0, lr0, ul1, lr1   
        try:   
            newnewimg[ul0-30:lr0+31, ul1-30:lr1+31]=True
            finalans=strmask[ul0-30:lr0+31, ul1-30:lr1+31]*allseg[ul0-30:lr0+31, ul1-30:lr1+31]
            stringbelongsto=np.max(finalans)

        except ValueError:
            ll0=ul0-30
            rl0=lr0+31
            ll1=ul1-30
            rl1=lr1+31
            
            if ul0<30:
                ll0=0
            if lr0+32 >= height:
                rl0=height-1
            if ul1<30:
                ll1=0
            if lr1+32 >=width:
                rl1=width-1
            finalans=strmask[ll0:rl0+1, ll1:rl1+1]*allseg[ll0:rl0+1, ll1:rl1+1]
            stringbelongsto=np.max(finalans)
 

        
        if np.min(finalans)!= np.max(finalans):
            if np.min(finalans)>0:
                print 'Boom', np.min(finalans), np.max(finalans)
                
                
    
        if stringbelongsto>0:
            images[stringbelongsto-1][ul0:lr0+1, ul1:lr1+11]=imgoriginal[ul0:lr0+1, ul1:lr1+11]
    
        else:
            if stringbelongsto==0:
                MASKWIDTH=31
                MASKLIM=150
                finalans=0
                while (np.max(finalans)==0) and MASKWIDTH<MASKLIM:
#                    print 
                    mask=np.ones((lr0-ul0+MASKWIDTH+MASKWIDTH+1,lr1-ul1+MASKWIDTH+MASKWIDTH+1),dtype=bool)
                    if(ul1<=MASKWIDTH+1):
                        break
                    if lr1+MASKWIDTH+2 >= width:
                        break
                    if lr0+MASKWIDTH+2 >=height:
                        break
                    if ul0<=MASKWIDTH+1:
                        break
                    
#                    print -(ul1-MASKWIDTH)+lr1+MASKWIDTH+1
#                    print ul1-MASKWIDTH, lr1+MASKWIDTH+1
#                    print allseg[ul0-MASKWIDTH:lr0+MASKWIDTH+1, ul1-MASKWIDTH:lr1+MASKWIDTH+1].shape
#                    print mask.shape
                    
#                    print ul1, lr1, ul0, lr0, MASKWIDTH
#                    print mask.shape, allseg[ul0-MASKWIDTH:lr0+MASKWIDTH+1, ul1-MASKWIDTH:lr1+MASKWIDTH+1].shape
#                    
#                    print ul1, lr1, MASKWIDTH                    
                    finalans=mask*allseg[ul0-MASKWIDTH:lr0+MASKWIDTH+1, ul1-MASKWIDTH:lr1+MASKWIDTH+1]
                    MASKWIDTH+=1
                    
                    
                if MASKWIDTH==MASKLIM:
                    stringbelongsto=0
    
    #            print np.max(finalans)
                stringbelongsto=np.max(finalans)
                images[stringbelongsto-1][ul0:lr0+1, ul1:lr1+11]=imgoriginal[ul0:lr0+1, ul1:lr1+11]
    #            
        cclist=[]
        for k in i:
            if hlist[k].ccdictno > 0:
                cclist.append(hlist[k].ccdictno)
            
        stringlist1.append([cclist, stringbelongsto, 'h'])
        stringlist.append([i, stringbelongsto, 'h'])
    
    print len(stringlist1), len(stringlist)
    
    #==============================================================================
    #     Vlist Begins
    #==============================================================================
    
    
    for i in list1:
        j=i[0]
        j1=i[-1]
        
        ul1=min(vlist[j].ul1, vlist[j1].ul1)
        ul0=vlist[j].ul0
        
        lr1=max(vlist[j].lr1, vlist[j1].lr1)
        lr0=vlist[j1].lr0
            
        try:
            newnewimg[ul0-30:lr0+31, ul1-30:lr1+31]=True
            finalans=strmask[ul0-30:lr0+31, ul1-30:lr1+31]*allseg[ul0-30:lr0+31, ul1-30:lr1+31]
            stringbelongsto=np.max(finalans)
#            print ul1-30, lr1+31
#            print strmask[ul0-30:lr0+31, ul1-30:lr1+31].shape, allseg[ul0-30:lr0+31, ul1-30:lr1+31].shape
#            print finalans.shape   
        except ValueError:
            ll0=ul0-30
            rl0=lr0+31
            ll1=ul1-30
            rl1=lr1+31
            
            if ul0<30:
                ll0=0
            if lr0+32 >= height:
                rl0=height-1
            if ul1<30:
                ll1=0
            if lr1+32 >=width:
                rl1=width-1
            finalans=strmask[ll0:rl0+1, ll1:rl1+1]*allseg[ll0:rl0+1, ll1:rl1+1]
            stringbelongsto=np.max(finalans)
        
        
    
        if np.min(finalans)!= np.max(finalans):
            if np.min(finalans)>0:
                print 'Boom', np.min(finalans), np.max(finalans)
        
    
        if stringbelongsto>0:
            images[stringbelongsto-1][ul0:lr0+1, ul1:lr1+11]=imgoriginal[ul0:lr0+1, ul1:lr1+11]
        else:
            if stringbelongsto ==0:
                MASKWIDTH=31
                MASKLIM=150
                while (np.max(finalans) ==0) and MASKWIDTH<MASKLIM:
                    if(ul1<=MASKWIDTH+1):
                        break
                    if lr1+MASKWIDTH+2 >= width:
                        break
                    if lr0+MASKWIDTH+2 >=height:
                        break
                    if ul0<=MASKWIDTH+1:
                        break
                    
                    mask=np.ones((lr0-ul0+MASKWIDTH+MASKWIDTH+1,lr1-ul1+MASKWIDTH+MASKWIDTH+1),dtype=bool)
                    
                    finalans=mask*allseg[ul0-MASKWIDTH:lr0+MASKWIDTH+1, ul1-MASKWIDTH:lr1+MASKWIDTH+1]

                    MASKWIDTH+=1

                if MASKWIDTH==MASKLIM:
                    stringbelongsto=0
                else:
                    stringbelongsto=np.max(finalans)
                    images[stringbelongsto-1][ul0:lr0+1, ul1:lr1+11]=imgoriginal[ul0:lr0+1, ul1:lr1+11]
    
        cclist=[]
        for k in i:
            if vlist[k].ccdictno > 0:
                cclist.append(vlist[k].ccdictno)
        
        stringlist1.append([cclist, stringbelongsto, 'v'])
        stringlist.append([i, stringbelongsto, 'v'])
    
    print len(stringlist1), len(stringlist)
    
    
    for i in range(noofsegments):
        imsave('Outputs\\SegmentsWithLabels\\'+fname+str(i+1)+'.png', np.invert(images[i]))
    #    show(images[i])
    
    print len(stringlist), len(stringlist1)
    mylib.picklethis(stringlist1, 'Outputs\\strassoc1'+fname)    
    mylib.picklethis(stringlist, 'Outputs\\strassoc'+fname)    

#==============================================================================
# fname='6_b'
# f(fname)
# fname='15_a'
# f(fname)
# fname='8_a'
# f(fname)
# fname='8_b'
# f(fname)
# fname='5_a'
# f(fname)
# fname='5_b'
# f(fname)
# fname='6_a'
# f(fname)
# fname='15_b'
# f(fname)
#==============================================================================
    
#==============================================================================
# mig=np.zeros(img1.shape, dtype=bool)
# for i in stringlist:
#     k=i[0]
#     for cc in k:
#         for j in ccdict[cc]:
#             a,b=j
#             mig[b,a]=True
#==============================================================================
            


if __name__ == "__main__":
    associations('4_2_b')
    print time.time() - starttime, "seconds"
