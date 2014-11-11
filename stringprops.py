# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 16:08:59 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 04:54:47 2014
LIST1 - VERTLIST
LIST2 - HORLIST
@author: ipcv5
"""
#import pytesser

from PIL import Image	
from operator import itemgetter, attrgetter
import mylib
from mylib import pickleload, picklethis, show, pickle
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
#import time
#from binlabeller import bwlabel
#starttime = time.time() 

import os
os.chdir('../../')

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

import cv2.cv as cv
import tesseract

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)

def conv(fname):
    image=cv.LoadImage(fname+'.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
    #api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
    tesseract.SetCvImage(image,api)
    text=api.GetUTF8Text()
    conf=api.MeanTextConf()
    image=None
#    print text
    print text.rstrip('\n')
    
#def stringprops(fname=None):
if 1:
    fname=None
    if fname==None:
        fname='6_b'
        fname='15_a'
        fname='8_a'
        fname='8_b'
        fname='6_a'
        fname='15_b'
        fname='5_b'
        fname='5_a'

  
    imname = 'Outputs\\labelinglinesremoved'+fname+'.png'
    
    ccdict=pickleload('Outputs\\ccdict'+fname+'.pkl')
    textcomplist=pickleload('Outputs\\textcomplist'+fname+'.pkl')
    img1=np.asarray(imread(imname), dtype=bool)
    height, width = img1.shape
    assoclist=mylib.pickleload('Outputs\\assoclist'+fname+'.pkl')
    
    stringlist=mylib.pickleload('Outputs\\strassoc'+fname)    
    stringlist1=mylib.pickleload('Outputs\\strassoc1'+fname)    
    originalimage=np.asarray(imread('images_consolidated\\'+fname+'.png'), dtype=bool)
    
    print len(stringlist1), len(stringlist)
    
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
    
    work=np.zeros((500,500), dtype=bool)
    counter=0
    intt=0
    for i in list2:
        print 'list'        
        j=i[0]
        j1=i[-1]
        
        ul0=min(hlist[j].ul0, hlist[j1].ul0)
        ul1=hlist[j].ul1
        
        lr0=max(hlist[j].lr0, hlist[j1].lr0)
        lr1=hlist[j1].lr1
    
        b=(originalimage[ul0-5:lr0+5, ul1-5:lr1+5])
        b=np.flipud(originalimage[ul0-5:lr0+5, ul1-5:lr1+5])
        b=np.fliplr(b)
    
        b=np.lib.pad(b, (50,50), 'constant')
        imsave('OCR/'+fname+str(intt)+'.png', np.uint8((b)*255))
#        im = Image.fromarray(np.uint8((b)*255))
#        im.save('OCR/'+str(intt)+'.png')        
        text='ha'    
        
#        conv('OCR/'+str(intt))        
        intt+=1
        print text
        textstring=text
        print textstring
        
        work=(originalimage[ul0-5:lr0+5, ul1-5:lr1+5]).copy()
        work=ndimage.binary_dilation(work)
        _, n=ndimage.label(work)
        difference=np.subtract(ndimage.binary_fill_holes(work), work)
        if np.sum(difference) > 10:
            _, n1=ndimage.label(difference)
        else:
            n1=0
    
    
        stringlist1[counter].append(n)
        stringlist1[counter].append(n1)
        stringlist1[counter].append(textstring)
        
        stringlist[counter].append(n)
        stringlist[counter].append(n1)
        stringlist[counter].append(textstring)
    
        counter+=1
    
    
    print
    
    for i in list1:
        j=i[0]
        j1=i[-1]
        
        ul1=min(vlist[j].ul1, vlist[j1].ul1)
        ul0=vlist[j].ul0
        
        lr1=max(vlist[j].lr1, vlist[j1].lr1)
        lr0=vlist[j1].lr0
    
        b=(originalimage[ul0-5:lr0+5, ul1-5:lr1+5])
        b=np.transpose(b)
        b=np.fliplr(b)
    
        b=np.lib.pad(b, (50,50), 'constant')
        im = Image.fromarray(np.uint8((b)*255))
        im.save('OCR/'+str(intt)+'.png')        
#        conv('OCR/'+str(intt))

        intt+=1
        textstring=''
        print textstring
    
    
        work=(originalimage[ul0-5:lr0+5, ul1-5:lr1+5]).copy()
        work=ndimage.binary_dilation(work)
        _, n=ndimage.label(work)
        
        
        difference=np.subtract(ndimage.binary_fill_holes(work), work)
    #    print sum(difference)
        if np.sum(difference) >=10:
            _, n1=ndimage.label(difference)
        else:
            n1=0
    #    print n, n1
        stringlist1[counter].append(n)
        stringlist1[counter].append(n1)
        stringlist1[counter].append(textstring)
        
        
        stringlist[counter].append(n)
        stringlist[counter].append(n1)
        stringlist[counter].append(textstring)
        counter+=1
    
        
    mylib.picklethis(stringlist, 'Outputs\\strprops'+fname)    
    mylib.picklethis(stringlist1, 'Outputs\\strprops1'+fname)    
    print len(stringlist1), len(stringlist)
