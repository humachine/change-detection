# -*- coding: utf-8 -*-
"""
Saves to Outputs\\Test : 
    - textmask OR imgoriginal (fname.png)
    - Dilttextmask OR imgoriginal (forviewing)
    - Stringmask
    - Stringmaskdiltry



img1 = Only Text
img - Full Original Image
Created on Wed Feb 19 10:15:03 2014

@author: ipcv5
"""
from operator import itemgetter, attrgetter
from scipy import ndimage
from scipy.misc import imread, imsave, imshow, toimage
from PIL import Image
import numpy as np
import time
import cPickle as pickle
from mylib import picklethis, pickleload, show

class component:
    def __init__(self, ul0, ul1, lr0, lr1, ccdictno, width=None, height=None, direction=None, top=None, bottom=None):
        self.ul0 = ul0
        self.top =top
        self.bottom=bottom
        self.ul1 = ul1
        self.lr0 = lr0   
        self.lr1 = lr1   
        self.ccdictno=ccdictno
  
        self.height = self.lr0-self.ul0+1
        self.width = self.lr1-self.ul1+1
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


def showcomp(img, ccdict, comp, complist=None):
    imgnew=np.zeros(img.shape, dtype=bool)
    if complist==None:
        for j in ccdict[comp]:
            a,b=j
            imgnew[b,a]=True
        return imgnew
    else:
        for i in complist:
            for j in ccdict[comp]:
                a,b=j
                imgnew[b,a]=True
        return imgnew


    
#==============================================================================
#==============================================================================
# # 
#==============================================================================
#==============================================================================
fname=None
flist=pickleload('Outputs\\fnamelist')

#def func(fname):
if 1:
    fname=None
    starttime=time.time()
    #def getstrings(fname=None):
    if fname==None:
    
        imname='images_consolidated\\9_b.png'
        imname='images_consolidated\\7_3_a.png'
        imname='images_consolidated\\15_a.png'
        imname='images_consolidated\\6_b.png'
        imname='images_consolidated\\8_a.png'
        imname='images_consolidated\\4_5_b.png'
        imname='images_consolidated\\15_b.png'
        imname='images_consolidated\\5_b.png'
        imname='images_consolidated\\8_b.png'
        imname='images_consolidated\\15_a.png'
        imname='images_consolidated\\6_a.png'
        imname='images_consolidated\\25_b.png'
        imname='images_consolidated\\5_a.png'
        imname='images_consolidated\\4_4_b.png'
        
        i=imname.rfind('\\')
        fname=imname[i+1:]
        fname=fname[:-4]
    else:
        imname='images_consolidated\\'+fname+'.png'
    
    #PRELIMINARIES
    img=np.asarray(imread(imname), dtype=bool)
    height, width=img.shape
    
    textcomplist=pickleload('Outputs\\textcomplist' + fname + '.pkl')
    ccdict=pickleload('Outputs\\ccdict'+ fname)
    num=pickleload('Outputs\\ccnum' + fname)
        
    
    imgoriginal = np.asarray(imread(imname), dtype=bool)
        
    #print img[208, 3399], img[3399, 208]
    
    height, width=img.shape
    img1=np.zeros(img.shape, dtype=bool)
    ccarrfake=np.zeros(img.shape, dtype=np.uint16)
    # IMG1 is the textonly Image
    #Discard all textcomponents with less than 20 pixel points
#VItal Constants    
    MINTEXTAREA=20
    textcomplist= [x for x in textcomplist  if len(ccdict[x])>=MINTEXTAREA]
    for i in textcomplist:
        for j in ccdict[i]:
            a,b=j
            img1[b,a]=True
            ccarrfake[b,a]=i
    
    noofcomponents=len(textcomplist)
    
    clslist=[]
    clscnt=1
    #ccarrfake=np.zeros(img.shape, dtype=np.uint16)
    textcomptoclslist={}
    cntr=0
    for i in textcomplist:
        zipdict = zip(*ccdict[i])
    
        minr = min(zipdict[0])
        maxr = max(zipdict[0])
        minc = min(zipdict[1])
        maxc = max(zipdict[1])
    
        ul0, ul1 = (minc, minr)
        lr0, lr1= (maxc,maxr)
        
    #    ccarrfake[zipdict[1], zipdict[0]]=clscnt
        clscnt+=1
        clslist.append(component(ul0, ul1, lr0, lr1, i))
    


    tessstrings=[]
    print fname
    for i in clslist[:]:
        ratio=round((float(i.width)/float(i.height)), 4)
        someval= float(np.sum(img[i.ul0:i.lr0+1, i.ul1:i.lr1+1]))
        dens=round(float(i.width*i.height)/float(np.sum(img[i.ul0:i.lr0+1, i.ul1:i.lr1+1])),4)
        
        work=img[i.ul0-1:i.lr0+1+1, i.ul1-1:i.lr1+1+1]
        _, num1=ndimage.label(work)
        if num1>1 and ratio>0.9 and ratio<1.1:
            #THe above searches for the M within a circle
            #I think these two ifs check for some SPECIFIC kind of shape viz. M (within a circle), PHI (slashed O, something like φ)
#            print ratio, dens, num1, i.direction, 'tag'
            i.direction='v'
    
        _, num=ndimage.label(np.subtract(work, ndimage.binary_fill_holes(work)))
        if num>1 and (ratio<1.8) and ratio>0.8:
    #        imgnew[i.ul0:i.lr0+1, i.ul1:i.lr1+1]=True
#            print ratio, dens, num, i.direction
            i.direction='v'
    horlist=[clslist[i] for i in range(noofcomponents) if clslist[i].direction=='h']
    vertlist=[clslist[i] for i in range(noofcomponents) if clslist[i].direction=='v']
    
    hcount=len(horlist)
    vcount=len(vertlist)
    
    #FOr every element on vlist we do a comparison between vlist[i] and vlist[i+1]. Hence we add two new components at the far end of the image.
    vlist=sorted(vertlist, key=attrgetter('ul0'))
    vlist.append(component(height-2, width-2, height-1, width-1, 0))
    vlist[-1].direction='v'
    
    hlist=sorted(horlist, key=attrgetter('ul1'))
    hlist.append(component(height-4, width-4, height-3, width-3, 0))
    hlist[-1].direction='h'
#    

#        
#        
        
    
    #==============================================================================
    #  STRINGING BEGINS
    #==============================================================================
    
    print 'horstart'
    
    hstrlist=[]
    for i in range(hcount):
        hstrlist.append([])
#    hstrlist=[[]]*hcount
    vstrlist=[[]]*vcount
    #VITAL CONSTANTS
    DILMASK=30
    TOLERANCE= 16
    GAP=52
    TOL=0

    xor = np.logical_xor
    
    swarimg=np.zeros(img1.shape, dtype=bool)
    swarun=np.zeros(img1.shape, dtype=bool)

    for i in range(hcount):
        curr=hlist[i]
        swarimg[curr.ul0-TOL:curr.lr0+1+TOL, curr.ul1:curr.lr1+GAP+1]=True
#    show(xor(swarimg, imgoriginal))

    ccarr, ccnum=ndimage.label(swarimg)
    print ccnum
    hortemp=[0]*hcount
    for i in range(hcount):
        curr=hlist[i]
        a,b=ccdict[curr.ccdictno][0]
        hortemp[i]=ccarr[b,a]
    swarimgcopy=swarimg.copy()

    dilans=np.zeros(img1.shape, bool)    
    finalans=np.zeros(img1.shape, bool)    
    hstrings=[]
    for i in np.unique(hortemp):
        loc=[jj for jj in range(hcount) if hortemp[jj]==i]
#        print loc, i
        minul1=min([hlist[jj].ul1 for jj in loc])
        maxlr1=max([hlist[jj].lr1 for jj in loc])

        minul0=min([hlist[jj].ul0 for jj in loc])
        maxlr0=max([hlist[jj].lr0 for jj in loc])
        finalans[minul0:maxlr0+1, minul1:maxlr1+1]=True
        dilans[minul0-DILMASK:maxlr0+DILMASK+1, minul1-DILMASK:maxlr1+DILMASK+1]=True
        hstrings.append((minul0, minul1, maxlr0, maxlr1))        

    finals=np.zeros(img1.shape, bool)    
#==============================================================================
# #vertical attempt
#==============================================================================
    swarimg=np.zeros(img1.shape, dtype=bool)

    for i in range(vcount):
        curr=vlist[i]
        swarimg[curr.ul0:curr.lr0+1+GAP, curr.ul1-TOL:curr.lr1+TOL+1]=True
    show(xor(swarimg, imgoriginal))
    ccarr, ccnum=ndimage.label(swarimg)
    print ccnum
    vertemp=[0]*vcount
    for i in range(vcount):
        curr=vlist[i]
        a,b=ccdict[curr.ccdictno][0]
        vertemp[i]=ccarr[b,a]

    vstrings=[]
    for i in np.unique(vertemp):
        loc=[jj for jj in range(vcount) if vertemp[jj]==i]
#        print loc, i
        minul1=min([vlist[jj].ul1 for jj in loc])
        maxlr1=max([vlist[jj].lr1 for jj in loc])
        minul0=min([vlist[jj].ul0 for jj in loc])
        maxlr0=max([vlist[jj].lr0 for jj in loc])
        
        vstrings.append((minul0, minul1, maxlr0, maxlr1))        

        dilans[minul0-DILMASK:maxlr0+DILMASK+1, minul1-DILMASK:maxlr1+DILMASK+1]=True
        finals[minul0:maxlr0+1, minul1:maxlr1+1]=True

    
    save=True
    if save==False:
        show(xor(finals+finalans, imgoriginal))
    else:
        imsave('Outputs\\GetStrings\\'+fname+'strmask'+'.png',(finals+finalans))
        imsave('Outputs\\GetStrings\\'+fname+'strmaskdil'+'.png',dilans)
        imsave('Outputs\\GetStrings\\'+fname+'check'+'.png',xor(finals+finalans, imgoriginal))
        a=open('Outputs\\GetStrings\\getstrings'+fname+'.pkl', 'w')
        pickle.dump(hstrings, a)
        pickle.dump(vstrings, a)
        a.close()


print time.time() - starttime, "seconds"


