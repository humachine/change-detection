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
import numpy as np
from operator import itemgetter, attrgetter
import pytesser
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

import os
os.chdir('../../')

def centroid(ccdict, j):
#    print ccdict[j]
    zipdict=zip(*ccdict[j])
    ul0=min(zipdict[0])
    ul1=min(zipdict[1])
    lr0=max(zipdict[0])
    lr1=max(zipdict[1])
    
    return ul0, ul1, lr0, lr1


def process(string):
    string=string.replace('Z','2')
    string=string.replace('Z','2')
        
    if 'I-I' in string:
        string = string.replace('I-I', 'H')
    if '<' in string:
        string = string.replace('<', '(')
    if '>' in string:
        string = string.replace('>', ')')

    if '(bs' in string:
        string = string.replace('(bs','w')

    if 'B' in string:
        string = string.replace('B', '3')

    if 'O' in string:
        string=string.replace('O', '0')
    if 'o' in string:
        string=string.replace('o', '0')
    if 'Y' in string:
        string=string.replace('Y', '7')

    string=string.replace('S', '9')
    string=string.replace('I-{', 'H')
    string=string.replace('P', 'F')
    string=string.replace('U)', 'N)')
    string=string.replace('Q', '9')
    

    if 'j;' in string:
        string=string.replace('j;', 'i')
    if ')(' in string:
        string=string.replace(')(', 'X')
    if 'j:' in string:
        string=string.replace('j:', 'i')
    if '()' in string:
        string=string.replace('()','0')
    return string


def finale(fname=None):
    if fname==None:
        fname='6_b'
        fname='15_b'
        fname='5_b'
        fname='8_b'
        fname='8_a'
        fname='6_a'
        fname='5_a'
        fname='15_a'

    imname = 'Outputs\\labelinglinesremoved'+fname+'.png'
    
    ccnum=pickleload('Outputs\\ccnum'+fname+'.pkl')
    ccdict=pickleload('Outputs\\ccdict'+fname+'.pkl')
    textcomplist=pickleload('Outputs\\textcomplist'+fname+'.pkl')
    img=np.asarray(imread(imname), dtype=bool)
    height, width = img.shape
    assoclist=mylib.pickleload('Outputs\\assoclist'+fname+'.pkl')
    
    originalimage=np.asarray(imread('images_consolidated\\'+fname+'.png'), dtype=bool)
    
    
    #==============================================================================
    #  Load image 1 strings
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
        
        
    stringlist=mylib.pickleload('Outputs\\strprops'+fname)    
    stringlist1=mylib.pickleload('Outputs\\strprops1'+fname)    
    
    liststr=[x[5].rstrip('\n') for x in stringlist]
    euler=[x[4]-x[3] for x in stringlist]
    
    #==============================================================================
    #  Image 2
    #==============================================================================
    
    if fname[-1]=='a':
        fname1=fname[:-1]+'b'
    else:
        fname1=fname[:-1]+'a'
    
    imname1 = 'Outputs\\labelinglinesremoved'+fname1+'.png'
    
    ccnum1=pickleload('Outputs\\ccnum'+fname1+'.pkl')
    ccdict1=pickleload('Outputs\\ccdict'+fname1+'.pkl')
    textcomplist1=pickleload('Outputs\\textcomplist'+fname1+'.pkl')
    img1=np.asarray(imread(imname1), dtype=bool)
    height1, width1 = img1.shape
    assoclist1=mylib.pickleload('Outputs\\assoclist'+fname1+'.pkl')
    
    noofsegments=np.max(assoclist1)
    
    secondstringlist=mylib.pickleload('Outputs\\strprops'+fname1)    
    secondstringlist1=mylib.pickleload('Outputs\\strprops1'+fname1)    
    originalimage1=np.asarray(imread('images_consolidated\\'+fname1+'.png'), dtype=bool)
    #print len(secondstringlist), len(secondstringlist1), len(stringlist), len(stringlist1)
    
    #==============================================================================
    # SHUDDERS
    #==============================================================================
    for i in stringlist1:
        if i[5]=='':
            print 'alarm'
            i[5]=' '
    for i in secondstringlist1:
        if i[5]=='':
            print 'alarm'
            i[5]=' '
    
    
    for i in stringlist1:
        i[5]=i[5].rstrip('\n')
    for i in secondstringlist1:
        i[5]=i[5].rstrip('\n')
    
    work=list(stringlist1)
    work1=list(secondstringlist1)
    
    
    
    #work=sorted(L, key=itemgetter(1))
    #noofsegments=1
    notfound=[]
    alarm=False
    
    
    #data = np.zeros( (height,width,3), dtype=np.uint8)
    #data[256,256] = [255,0,0]
    #img = Image.fromarray(data, 'RGB')
    #img.save('my.png')
    
    #data=np.array([np.invert(originalimage), np.invert(originalimage), np.invert(originalimage)], dtype=np.uint8)
    #data1=np.array([np.invert(originalimage1), np.invert(originalimage1), np.invert(originalimage1)], dtype=np.uint8)
    #data1=[np.invert(originalimage1), np.invert(originalimage1), np.invert(originalimage1)]
    
    #noofsegments=1
    for i in range(1,noofsegments+1):
        lis=[x for x in work if x[1]==i]
        lis1=[x for x in work1 if x[1]==i]
    
    
        lizzy=[x[5].rstrip('\n') for x in lis]
        lizzy1=[x[5].rstrip('\n') for x in lis1]
    
#        for j in range(len(lis)):
#    #        if len(lizzy[j]) >=4:
#                print process(lizzy[j])
#        print
#        for j in range(len(lis1)):
#            print process(lizzy1[j])
        
    #==============================================================================
    #    imm=np.zeros(originalimage.shape, dtype=bool)
    #     for j in range(len(lis)):
    #         if lis[j][5]=='H-':
    #             for k in lis[j][0]:
    #                 ccchoose=ccdict[k]
    #                 for j0 in ccchoose:
    #                     a,b=j0
    #                     imm[b,a]=True
    #     for j in range(len(lis1)):
    #         if lis1[j][5]=='H-':
    #             for k in lis1[j][0]:
    #                 ccchoose=ccdict1[k]
    #                 for j0 in ccchoose:
    #                     a,b=j0
    #                     imm[b,a]=True
    #    show(imm)
    #==============================================================================
    
    
    
        for j in range(len(lis)):
            for k in range(len(lis1)):
                p=process(lizzy[j])
                q=process(lizzy1[k])
    #            print p, q
                if p==q or lizzy[j]==lizzy1[k] or p==lizzy1[k] or lizzy[j]==q:
                    if p!='H-':
                        lis[j][5]=''
                        lizzy[j]=''
                        lizzy1[k]=''
                        lis1[k][5]=''
                        break
            
            
    #    print
    #    for j in range(len(lis1)):
    #        if lis1[j][5]!='':
    #            print lis1[j][5]
    #        if lis[j][5]!='':
    #            print lis[j][5]
    
        try:
            image=np.asarray(imread('Outputs\\SegmentsWithLabels\\'+fname+str(i)+'.png'), dtype=bool)
        #    print
        #    print
            image=np.invert(image)
            for j in range(len(lis)):
        #        if lis[j][5]=='' or len(lis[j][5])<=3:
                if lis[j][5]=='':
        #            print lis[j][0]
                    for k in lis[j][0]:
                        ccchoose=ccdict[k]
                        for j0 in ccchoose:
                            a,b=j0
                            image[b,a]=False
        #                    data[b,a]=[255,0, 0]
                            
                else:
                    print process(lis[j][5].rstrip('\n'))
        except IOError:
            pass
    
    #    for j in range(len(lis)):
    #        if lis[j][5]=='H-':
    #            some=0
    #            if lis[j][2]=='v':
    #                if len(lis[j][0])==1:
    ##                    print lis[j][0][0], type(lis[j][0][0])
    #                    ul0, ul1, lr0, lr1=centroid(ccdict, lis[j][0][0])
    #                    some=np.sum(image[ul0:lr0, ul1-30:ul1])+np.sum(image[ul0:lr0, lr1:lr1+30])
    #            if lis[j][2]=='h':
    #                if len(lis[j][0])==1:
    ##                    print lis[j][0][0], type(lis[j][0][0])
    #                    ul0, ul1, lr0, lr1=centroid(ccdict, lis[j][0][0])
    #                    some= np.sum(image[ul0-30:ul0, ul1:lr1])+np.sum(image[lr0:lr0+30, ul1:lr1])
    #            print some
    #            if some <10:
    #                if len(lis[j][0])==1:
    #                    print 'enter'
    #                    for k in ccdict[lis[j][0][0]]:
    #                        a,b=k
    #                        image[b,a]=False
    #            else:
    #                if len(lis[j][0])==1:
    #                    for k in ccdict[lis[j][0][0]]:
    #                        a,b=k
    #                        image[b,a]=True
    
                    
                            
    
    #            if np.sum(origina)
    #    show(image)
    
        print 
        print
        try:
            image1=np.asarray(imread('Outputs\\SegmentsWithLabels\\'+fname1+str(i)+'.png'), dtype=bool)
            image1=np.invert(image1)
        
            for j in range(len(lis1)):
        #        if lis1[j][5]==''or len(lis1[j][5])<=3:
                if lis1[j][5]=='':
        
        #            print lis[j][0]
                    for k in lis1[j][0]:
                        ccchoose=ccdict1[k]
                        for j0 in ccchoose:
                            a,b=j0
                            image1[b,a]=False
        #                    data1[b,a]=[255,0, 0]
        
                else:
                    print process(lis1[j][5].rstrip('\n'))
        except IOError:
            pass
    
    #    for j in range(len(lis1)):
    #        if lis1[j][5]=='H-':
    #            some=0
    #            if lis1[j][2]=='v':
    #                if len(lis1[j][0])==1:
    ##                    print lis[j][0][0], type(lis[j][0][0])
    #                    ul0, ul1, lr0, lr1=centroid(ccdict1, lis1[j][0][0])
    #                    some=np.sum(image1[ul0:lr0, ul1-30:ul1])+np.sum(image1[ul0:lr0, lr1:lr1+30])
    #            if lis1[j][2]=='h':
    #                if len(lis1[j][0])==1:
    ##                    print lis[j][0][0], type(lis[j][0][0])
    #                    ul0, ul1, lr0, lr1=centroid(ccdict1, lis1[j][0][0])
    #                    some= np.sum(image1[ul0-30:ul0, ul1:lr1])+np.sum(image1[lr0:lr0+30, ul1:lr1])
    #            if some <10:
    #                if len(lis1[j][0])==1:
    #                    for k in ccdict1[lis1[j][0][0]]:
    #                        a,b=k
    #                        image1[b,a]=False
    #            else:
    #                if len(lis1[j][0])==1:
    #                    for k in ccdict1[lis1[j][0][0]]:
    #                        a,b=k
    #                        image1[b,a]=True
    #
    #    for j in range(len(lis1)):
    #        if lis1[j][5]=='H-':
    #            for k in ccdict1[lis1[j][0][0]]:
    #                a,b=k
    #                image1[b,a]=False
    
    
    
    #    show(image1)
        imsave('Outputs\\Results\\'+fname+str(i)+'.png', np.invert(image))
        imsave('Outputs\\Results\\'+fname1+str(i)+'.png', np.invert(image1))
        print

#==============================================================================
# 
#==============================================================================
if __name__ == "__main__":
    flist=[]

    fname='8_b'
    flist.append(fname)
    fname='8_a'
    flist.append(fname)
    fname='6_a'
    flist.append(fname)
    fname='5_a'
    flist.append(fname)
    fname='15_a'
    flist.append(fname)

    for i in flist: 
        finale(i)
    print time.time() - starttime, "seconds"

