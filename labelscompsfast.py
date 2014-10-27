# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 18:47:26 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:27:43 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 15:50:45 2014

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
import mylib
from mylib import pickleload, picklethis, show
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from binlabeller import bwlabel
from scipy import ndimage
import time
from binlabeller import bwlabel

def whichcomp(a, b, ccdict, ccnum, ccarr=None):
    if ccarr==None:
        for i in range(1, ccnum+1):
            if (a,b) in ccdict[i]:
                return i
        return 0
    else:
        return ccarr[a,b]

def towhitebgd(numarr):
    a=np.sum(numarr)
    height, width=numarr.shape
    if (height*width) <= (2*a):
        return numarr
    else:
        return np.invert(numarr)


def toblackbgd(numarr):
    a=np.sum(numarr)
    height, width=numarr.shape
    if (height*width) > (2*a):
        return numarr
    else:
        return np.invert(numarr)

def genimage(img, ccdict, complist):
    for i in complist:
        for j in ccdict[i]:
            b,a =j
            img[a,b]=True
    return img

starttime = time.time() 

fname='6_a'
fname='5_b'
fname='8_a'
fname='15_b'

fname='6_b'
fname='5_a'

fname='8_b'
fname='15_a'

imname = 'Outputs\\labelinglinesremoved'+fname+'.png'

ccnum=pickleload('Outputs\\ccnum'+fname+'.pkl')
ccdict=pickleload('Outputs\\ccdict'+fname+'.pkl')
textcomplist=pickleload('Outputs\\textcomplist'+fname+'.pkl')
imgoriginal=np.asarray(imread(imname), dtype=bool)
print time.time() - starttime, ' readfiles'


img=imgoriginal.copy()
img=toblackbgd(img)


img=ndimage.binary_fill_holes(img)
img1=ndimage.binary_erosion(img, np.ones((5,5)))
img1=ndimage.binary_dilation(img1, np.ones((5,5)))

#print 'mega begins'
#img2=ndimage.binary_dilation(img1, np.ones((60,60)))
#imsave('Outputs\\megafill'+fname+'.png', img2)

bigdil=np.asarray(imread('Outputs\\megafill'+fname+'.png'), dtype=bool).astype(np.int8)
newarr=np.asarray(imread('Outputs\\'+fname+'.png'), dtype=bool).astype(np.int8)
print time.time() - starttime, ' bigdilate'

#imsave('tempfill.png', np.invert(bigdil))
#a=Image.open('tempfill.png')
#a=a.convert('1')
#bigdict, bigarr, bigcount, _ = bwlabel(a)
#bigarr=bigarr.astype(np.int8)

#mylib.picklethis(bigdict, )
bigarr,bigcount = ndimage.label(bigdil)
noofsegments=bigcount

print time.time() - starttime, ' assoc begins'


#def associate(ccnum, ccdict, textcomplist, bigcount, bigarr, start=180):
assoclist=[0]
t=np.zeros(newarr.shape, dtype=bool)
print 'entry'

start=160
for i in range(start, ccnum+1):
    if i in textcomplist:
        assoclist.append(-1)

    else:
        print 'iffy'

        zip1=zip(*ccdict[i])
        ul0=min(zip1[0])
        lr0=max(zip1[0])
        ul1=min(zip1[1])
        lr1=max(zip1[1])
        print np.sum(t)
#        show(t)
#        show(newarr[ul0:lr0+1, ul1:lr1+1])
        t[ul0:lr0+1, ul1:lr1+1]=False
        
#            print i            
        for j in ccdict[i]:
            a,b=j
            t[b,a]=True
        if sum(bigarr[ul0:lr0+1, ul1:lr1+1]) > 0:
            print np.sum(bigarr[ul0:lr0+1, ul1:lr1+1]), 
            print np.sum(t[ul0:lr0+1, ul1:lr1+1])
            
        finalans=bigarr[ul0:lr0+1, ul1:lr1+1] * t[ul0:lr0+1, ul1:lr1+1]
#            print np.max(finalans)
            
#            if np.max(finalans) >0 :
#                if np.min(finalans)==0:
#                    assoclist.append(np.max(finalans))
#            else:
#                assoclist.append(0)
            
#            ten=ccdict[i]
#            print type(ten)
#            appendflag=True
#            zipdict=zip(*ccdict[i])
#            for j in ccdict[i]:
#                a,b=
#        else:
#            appendflag=True
#            for j in ccdict[i]:
#                a,b=j
#                ans=whichcomp(a,b, bigdict, bigcount, bigarr) 
#                if ans > 0:
#                    assoclist.append(ans)
#                    appendflag=False
#                    break
#            else:
#                zipdict=zip(*ccdict[i])
##                ul0=min(zip1[0])
##                lr0=max(zip1[0])
##                ul1=min(zip1[1])
##                lr1=max(zip1[1])
##                
##                MASKWIDTH=1
##                finalans=0
##                while (np.max(finalans) ==0):
##                    finalans=strmask[ul0-MASKWIDTH:lr0+MASKWIDTH+1, ul1-MASKWIDTH:lr1+MASKWIDTH+1]*bigarr[ul0-MASKWIDTH:lr0+MASKWIDTH+1, ul1-MASKWIDTH:lr1+MASKWIDTH+1]
##                    MASKWIDTH+=1
##                print np.max(finalans)
##                stringbelongsto=np.max(finalans)
##                images[stringbelongsto-1][ul0:lr0+1, ul1:lr1+11]=imgoriginal[ul0:lr0+1, ul1:lr1+11]
#
#            if appendflag==True:
#                assoclist.append(0)
#
#    return assoclist
#
assoclist=associate(ccnum, ccdict, textcomplist, bigcount, bigarr, 50)
#print max(assoclist)
##mylib.picklethis(assoclist, 'Outputs\\assoclist'+fname+'.pkl')
#
##colorimg=np.zeros(img1.shape)
##for i in range(1, ccnum+1):
##    col=assoclist[i]
##    if col >=1:
##        for j in ccdict[i]:
##            a,b=j
##            colorimg[b,a]=(col*255)/noofsegments
##show(colorimg)
#
print time.time() - starttime, ' seconds'