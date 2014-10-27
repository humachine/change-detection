# -*- coding: utf-8 -*-
"""
FINAL 
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
from skimage import filter


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

#==============================================================================
# 
# def whichcomp(a, b, ccdict, ccnum, ccarr=None):
#     if ccarr==None:
#         for i in range(1, ccnum+1):
#             if (a,b) in ccdict[i]:
#                 return i
#         return 0
#     else:
#         return ccarr[a,b]
# 
# def associate(ccnum, ccdict, textcomplist, bigdict, bigcount, bigarr, start=100):
#         assoclist = [0]
#         
#         for i in xrange(start, ccnum+1):
#             if i in textcomplist:
#                 assoclist.append(-1)
#             else:
#                 appendflag=True
#                 for j in ccdict[i]:
#                     a,b=j
#                     ans=whichcomp(a,b, bigdict, bigcount, bigarr) 
#                     if ans > 0:
#                         assoclist.append(ans)
#                         appendflag=False
#                         break
#     #==============================================================================
#     #             else:
#     #                 zip1=zip(*ccdict[i])
#     #                 ul0=min(zip1[0])
#     #                 lr0=max(zip1[0])
#     #                 ul1=min(zip1[1])
#     #                 lr1=max(zip1[1])
#     #                 
#     #                 MASKWIDTH=1
#     #                 finalans=0
#     #                 while (np.max(finalans) ==0):
#     #                     finalans=strmask[ul0-MASKWIDTH:lr0+MASKWIDTH+1, ul1-MASKWIDTH:lr1+MASKWIDTH+1]*allseg[ul0-MASKWIDTH:lr0+MASKWIDTH+1, ul1-MASKWIDTH:lr1+MASKWIDTH+1]
#     #                     MASKWIDTH+=1
#     #                 print np.max(finalans)
#     #                 stringbelongsto=np.max(finalans)
#     #                 images[stringbelongsto-1][ul0:lr0+1, ul1:lr1+11]=imgoriginal[ul0:lr0+1, ul1:lr1+11]
#     #==============================================================================
#     
#                 if appendflag==True:
#                    assoclist.append(0)
#        return assoclist
#==============================================================================
    

#def labels2comps(fname=None, flag=True):
if 1:
    fname=None; 
    flag=True
    if fname==None:
        fname='6_a'
        fname='5_b'
        fname='15_b'
        
        
        fname='8_b'
        fname='6_b'
        fname='5_a'
        fname='8_a'
        fname='15_a'
        
        
    imname = 'Outputs\\labelinglinesremoved'+fname+'.png'
    
    ccnum=pickleload('Outputs\\ccnum'+fname+'.pkl')
    ccdict=pickleload('Outputs\\ccdict'+fname+'.pkl')
    textcomplist=pickleload('Outputs\\textcomplist'+fname+'.pkl')
    img=np.asarray(imread(imname), dtype=bool)
    print time.time() - starttime, ' readfiles'
    
    
    img=toblackbgd(img)
    
    
    img=ndimage.binary_fill_holes(img)
    img1=ndimage.binary_erosion(img, np.ones((5,5)))
    img1=ndimage.binary_dilation(img1, np.ones((5,5)))

#    flag=False
    if flag==False:
        print 'Mega Dilation Begins. Take a break. . ', time.time()-starttime
        imm=ndimage.grey_dilation(img1, size=(60,60))
#        img2=ndimage.binary_dilation(img1, np.ones((60,60)))
        imsave('Outputs\\megafill'+fname+'.png', imm)




#    bigdil=np.asarray(imread('Outputs\\megafill'+fname+'.png'), dtype=bool).astype(np.int8)
    bigdil=np.asarray(imread('Outputs\\megafill'+fname+'.png'), dtype=bool)

    imgoriginal=np.asarray(imread('images_consolidated\\'+fname+'.png'), dtype=bool)
    newarr=imgoriginal.copy().astype(np.int8)



    print time.time() - starttime, ' bigdilate'
    show(np.logical_or(bigdil, imgoriginal))
#
#    bigarr, bigcount=ndimage.label(bigdil)
#    bigarr=bigarr.astype(np.int8)
#    noofsegments=bigcount
#    
#    assoclist = [0]
#    start=1
#    for i in xrange(start, ccnum+1):
#        if i in textcomplist:
#            assoclist.append(-1)
#        else:
#            zipdict=zip(*ccdict[i])
#            ans=np.max(bigarr[zipdict[1], zipdict[0]])
#            assoclist.append(ans)
#
#    
#    
#    
#    
#    
#    images=[]
#    for i in range(noofsegments):
#        images.append(np.zeros(img1.shape, dtype=bool))
#    
#    for i in range(1, ccnum+1):
#        col=assoclist[i]
#        if col >=1:
#            zipdict=zip(*ccdict[i])
#                
#            images[col-1][zipdict[1], zipdict[0]]=True
#
#    for index, i in enumerate(images):
#        imsave('Outputs\\LabelsToComps\\'+fname+str(index+1)+'.png', np.invert(i))

if __name__ == "__main__":
#    labels2comps()
    print time.time() - starttime, "seconds"
