# -*- coding: utf-8 -*-
"""
FINAL 
Created on Thu Feb 27 14:27:43 2014

@author: ipcv5
"""

from PIL import Image	
import mylib
from mylib import pickleload, picklethis, show
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from binlabeller import bwlabel
from scipy import ndimage
import time
import config as cfg

def whichcomp(a, b, ccdict, ccnum, ccarr=None):
    if ccarr==None:
        for i in range(1, ccnum+1):
            if (a,b) in ccdict[i]:
                return i
        return 0
    else:
        return ccarr[a,b]

'''
Certain images are inherently on a black background instead of the default white background. 
This function (and the one below it) inverts such images based on black pixel density.'''
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

'''Given a list of components and the points comprising each component it generates an image'''
def genimage(img, ccdict, complist):
    for i in complist:
        for j in ccdict[i]:
            b,a =j
            img[a,b]=True
    return img


def associate(ccnum, ccdict, textcomplist, bigdict, bigcount, bigarr, start=100):
        assoclist = [0]
        
        for i in xrange(start, ccnum+1):
            if i in textcomplist:
                assoclist.append(-1)
            else:
                appendflag=True
                for j in ccdict[i]:
                    a,b=j
                    ans=whichcomp(a,b, bigdict, bigcount, bigarr) 
                    if ans > 0:
                        assoclist.append(ans)
                        appendflag=False
                        break
                    
                if appendflag==True:
                    assoclist.append(0)
        return assoclist
    
import os
os.chdir('../../')
    

starttime = time.time() 
def labels2comps(fname=None, flag=True):
    if fname==None:
        print 'No file name assigned'
#        return 0, time.time()-starttime

#    imname = cfg.IMG_DIR+fname
    fname='5_a.png'
    if cfg.IMG_EXT in fname:
        fname=fname[:-4]
        
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
    
    if flag==False:
        print 'Mega Dilation Begins. Take a break. . '
        img2=ndimage.binary_dilation(img1, np.ones((60,60)))
        imsave('Outputs\\megafill'+fname+'.png', img2)
    
    bigdil=np.asarray(imread('Outputs\\megafill'+fname+'.png'), dtype=bool).astype(np.int8)
    print time.time() - starttime, ' bigdilate'
    
    imsave('tempfill.png', np.invert(bigdil))
    a=Image.open('tempfill.png')
    a=a.convert('1')
    bigdict, bigarr, bigcount, bigout = bwlabel(a)
    bigarr=bigarr.astype(np.int8)
    
    #mylib.picklethis(bigdict, )
    noofsegments=bigcount
    
    print time.time() - starttime, ' assoc begins'
    
    assoclist=associate(ccnum, ccdict, textcomplist, bigdict, bigcount, bigarr, 1)
    print np.max(assoclist)
    mylib.picklethis(assoclist, 'Outputs\\assoclist'+fname+'.pkl')
    
    colorimg=np.zeros(img1.shape)
    for i in range(1, ccnum+1):
        col=assoclist[i]
        if col >=1:
            for j in ccdict[i]:
                a,b=j
                colorimg[b,a]=(col*255)/noofsegments
    
    show(colorimg)
    return colorimg
#
if __name__ == "__main__":
    img=labels2comps()
    print time.time() - starttime, "seconds"
