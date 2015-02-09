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
import config as cfg

'''Component Class'''
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

#==============================================================================
#==============================================================================
# # Takes all the textual components and stringifies them (Turns them into strings)
#==============================================================================
#==============================================================================

def stringify(fname=None, kvs=[]):
    starttime=time.time()
    xor = np.logical_xor
    if fname==None:
        print 'No file name assigned'
        return 0, time.time()-starttime
    else:
        imname = cfg.IMG_DIR+fname
    print 'Stringifying text components from', imname

    if cfg.IMG_EXT in fname:
        fname=fname[:-4]
    
    #PRELIMINARIES - Loading Images and Text component list calculated in textextraction.py
    img=np.asarray(imread(imname), dtype=bool)
    height, width=img.shape
    
    textcomplist=pickleload(cfg.OUT_DIR+'textcomplist' + fname + '.pkl')
    ccdict=pickleload(cfg.OUT_DIR+'ccdict'+ fname)
    num=pickleload(cfg.OUT_DIR+'ccnum' + fname)
        
    imgoriginal = np.asarray(imread(imname), dtype=bool)
    
    height, width=img.shape
    img1=np.zeros(img.shape, dtype=bool)
    # IMG1 is the textonly Image
    
    MINTEXTAREA=cfg.stringify.MINTEXTAREA
    DILMASK=cfg.stringify.DILMASK
    TOLERANCE=cfg.stringify.TOLERANCE
    GAP=cfg.stringify.GAP
    TOL=cfg.stringify.TOL

    textcomplist= [x for x in textcomplist  if len(ccdict[x])>=MINTEXTAREA]     #Discard all textcomponents with less than 20 pixel points

    #Takes an image with only relevant textual components present
    for i in textcomplist:
        for j in ccdict[i]:
            a,b=j
            img1[b,a]=True
    
    noofcomponents=len(textcomplist)
    
    clslist=[]
    clscnt=1
    #Adds each textual 8-connected component to an instance of a component class
    for i in textcomplist:
        zipdict = zip(*ccdict[i])
    
        minr = min(zipdict[0])
        maxr = max(zipdict[0])
        minc = min(zipdict[1])
        maxc = max(zipdict[1])
    
        ul0, ul1 = (minc, minr)
        lr0, lr1= (maxc,maxr)
        
        clscnt+=1
        clslist.append(component(ul0, ul1, lr0, lr1, i))

#Text components that have larger height than width are classified as horizontal string components and vice versa
#There are a few cases of exception where like special characters which do not obey the above rule. They are specially dealt with below

    for i in clslist[:]:
        ratio=round((float(i.width)/float(i.height)), 4)
        work=img[i.ul0-1:i.lr0+1+1, i.ul1-1:i.lr1+1+1]
        _, num1=ndimage.label(work)
        if num1>1 and ratio>0.9 and ratio<1.1:
            #THe above searches for the M within a circle
            #The two conditions in the 'if' check for some SPECIFIC kind of shape viz. M (within a circle), PHI (slashed O, something like the Greek symbol phi)
            i.direction='v'
    
        _, num=ndimage.label(np.subtract(work, ndimage.binary_fill_holes(work)))
        if num>1 and (ratio<1.8) and ratio>0.8:
            i.direction='v'
            
#Horlist has the list of 'component' class instances that are horizontal in orientation            
    horlist=[clslist[i] for i in range(noofcomponents) if clslist[i].direction=='h']
    vertlist=[clslist[i] for i in range(noofcomponents) if clslist[i].direction=='v']
    
    hcount=len(horlist)
    vcount=len(vertlist)
    
    #FOr every element on vlist we later do a comparison between vlist[i] and vlist[i+1]. Hence we add a junk components at the far end of the image. The same idea is done for hlist as well
    vlist=sorted(vertlist, key=attrgetter('ul0'))
    vlist.append(component(height-2, width-2, height-1, width-1, 0))
    vlist[-1].direction='v'
    
    hlist=sorted(horlist, key=attrgetter('ul1'))
    hlist.append(component(height-4, width-4, height-3, width-3, 0))
    hlist[-1].direction='h'
    
    
    #==============================================================================
    #  STRINGING BEGINS
    #==============================================================================
    
    
    print 'Stringing together horizontal text components to get horizontal strings'

#Takes one horizontal component at a time. Sees in a neighbourhood of DILMASK if there's another such component. If yes, it dilates to touch that component too. Similar method employed for vertical strings.    
    hstrlist=[]
    for i in range(hcount):
        hstrlist.append([])

    imgtmp=np.zeros(img1.shape, dtype=bool)
    for i in range(hcount):
        curr=hlist[i]
        imgtmp[curr.ul0-TOL:curr.lr0+1+TOL, curr.ul1:curr.lr1+GAP+1]=True
#    show(xor(imgtmp, imgoriginal))

    ccarr, ccnum=ndimage.label(imgtmp)
    hortemp=[0]*hcount
    for i in range(hcount):
        curr=hlist[i]
        a,b=ccdict[curr.ccdictno][0]
        hortemp[i]=ccarr[b,a]

    dilans=np.zeros(img1.shape, bool)    
    finalans=np.zeros(img1.shape, bool)    
    hstrings=[]
    for i in np.unique(hortemp):
        loc=[jj for jj in range(hcount) if hortemp[jj]==i]
        minul1=min([hlist[jj].ul1 for jj in loc])
        maxlr1=max([hlist[jj].lr1 for jj in loc])

        minul0=min([hlist[jj].ul0 for jj in loc])
        maxlr0=max([hlist[jj].lr0 for jj in loc])
        finalans[minul0:maxlr0+1, minul1:maxlr1+1]=True
        dilans[minul0-DILMASK:maxlr0+DILMASK+1, minul1-DILMASK:maxlr1+DILMASK+1]=True
        hstrings.append((minul0, minul1, maxlr0, maxlr1))        

    finals=np.zeros(img1.shape, bool)    
#==============================================================================
# STringify Strings vertically
#==============================================================================
    imgtmp=np.zeros(img1.shape, dtype=bool)

    print 'Stringing together vertical text components to get vertical strings'

    for i in range(vcount):
        curr=vlist[i]
        imgtmp[curr.ul0:curr.lr0+1+GAP, curr.ul1-TOL:curr.lr1+TOL+1]=True
#    show(xor(imgtmp, imgoriginal))

    ccarr, ccnum=ndimage.label(imgtmp)
    vertemp=[0]*vcount
    for i in range(vcount):
        curr=vlist[i]
        a,b=ccdict[curr.ccdictno][0]
        vertemp[i]=ccarr[b,a]

    vstrings=[]
    for i in np.unique(vertemp):
        loc=[jj for jj in range(vcount) if vertemp[jj]==i]
        minul1=min([vlist[jj].ul1 for jj in loc])
        maxlr1=max([vlist[jj].lr1 for jj in loc])
        minul0=min([vlist[jj].ul0 for jj in loc])
        maxlr0=max([vlist[jj].lr0 for jj in loc])
        
        vstrings.append((minul0, minul1, maxlr0, maxlr1))        

        dilans[minul0-DILMASK:maxlr0+DILMASK+1, minul1-DILMASK:maxlr1+DILMASK+1]=True
        finals[minul0:maxlr0+1, minul1:maxlr1+1]=True

    save=True
    if 'nosave' in kvs:
        save=False
    
    if save==False:
        show(xor(finals+finalans, imgoriginal))
    else:
        imsave(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname+'vert'+'.png',finals)
        imsave(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname+'hor'+'.png',finalans)
        imsave(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR + fname+'strmask'+'.png',(finals+finalans))
        imsave(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname+'strmaskdil'+'.png',dilans)
        imsave(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname+'check'+'.png',xor(finals+finalans, imgoriginal))
        
        a=open(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+'getstrings'+fname+'.pkl', 'w')
        pickle.dump(hstrings, a)
        pickle.dump(vstrings, a)
        a.close()

    return 0, time.time() - starttime

import os
l=os.listdir(cfg.IMG_DIR)
for i in l:
    stringify(i)