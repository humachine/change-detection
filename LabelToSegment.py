

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 14:09:13 2014

@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 15:50:45 2014
FINAL
@author: Home
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 02:30:41 2014

@author: Home
"""
 
from PIL import Image	
import cv2
from mylib import pickleload, picklethis
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
import time

import config as cfg

logor=np.logical_or
xor=np.logical_xor
label=ndimage.label
dilate=ndimage.grey_dilation
erode=ndimage.binary_erosion
fill=ndimage.binary_fill_holes
opening=ndimage.binary_opening

def show(x):
    toimage(x).show()

starttime = time.time() 

def labeltosegment(fname):
    if fname==None:
        print 'No file name assigned'
        return 0, time.time()-starttime
    
    print 'Attempting to attach labels to segments', fname
    if cfg.IMG_EXT in fname:
        fname=fname[:-4]
        
    skelname = cfg.OUT_DIR + cfg.thinning.SKEL_IMG_DIR +fname+ cfg.IMG_EXT
    skel=np.asarray(imread(skelname), dtype=bool)
    original=skel.copy()
    
    rmlinesfname = cfg.OUT_DIR + cfg.removelines.SAVE_DIR + fname + cfg.IMG_EXT
    fill1=np.asarray(imread(rmlinesfname), dtype=bool)
    fillarr, noofsegments=ndimage.label(fill1, np.ones((3,3)))
    
    segexamplelist=[]
    for i in range(1,noofsegments+1):
        zipp=np.where(fillarr==i)
        segexamplelist.append((zipp[0][0], zipp[1][0]))
        
    print 'Dilating Segments... . .'
    fill1=ndimage.grey_dilation(fill1, size=cfg.labeltosegment.GREY_DIL_SIZE)
    
    '''
    We attempt to associate labeling lines to particular segments. We erode with a horizontal element
    to remove all vertical labeling lines. We also erode the skeleton image with a vertical element to get only
    the horizontal lines.
    We then extend (dilation using an appropriate mask) these lines along their direction. The slanting lines are dilated using a standard mask to extend them
    
    These images (horlines, vertlines & slantsdil) are nothing but the labeling lines extended in order to meet the nearby segments
    '''    
    
    skelfillorg=fill(skel)
    skelfill=xor(skelfillorg, skel)
    skelfill=dilate(skelfill, size=cfg.labeltosegment.STD_DIL_SIZE)
    
    skel=(xor(skelfill, skelfillorg))    

    mins=np.logical_and(fill1, skel)
    minmin=np.logical_xor(skel, mins)
    
    skeldil=dilate(skel, size=cfg.labeltosegment.SKEL_DIL_SIZE)
    
    SIZE=cfg.labeltosegment.BIG_ELEMENT_SIZE
    bigelement=np.zeros((SIZE, SIZE), dtype=bool)
    bigelement[(SIZE-1)/2, :]=True

    print 'Extending labeling lines to meet segments. . '
    element=cfg.labeltosegment.HOR_ELEMENT
    hor1 = (ndimage.binary_erosion(minmin, element))
    horlines=ndimage.binary_dilation(hor1, bigelement)

    bigelementv=np.zeros((SIZE, SIZE), dtype=bool)
    bigelementv[:, (SIZE-1)/2]=True
    element1=cfg.labeltosegment.VERT_ELEMENT
    vert1 = (ndimage.binary_erosion(minmin, element1))
    vertlines=ndimage.binary_dilation(vert1, bigelementv)

    slants=xor(minmin, vert1)
    slants=xor(slants, hor1)
    slantsdil=dilate(slants, size= cfg.labeltosegment.SKEL_DIL_SIZE)

    slantsarr, slantsnum =label(slantsdil, np.ones(cfg.labeltosegment.STD_DIL_SIZE))
    slantsarr=slantsarr.astype(np.uint16)
    binfill=list(np.bincount(slantsarr.flatten()))
    bfill=sorted(binfill, reverse=True)
    bfill.remove(bfill[0])
    
    '''
    Here, all slant components which are lesser than COMP_MIN_SIZE pixels are discarded since they are usually insignificant noise
    '''
    for i in range(len(binfill)):
        if binfill[i]<=cfg.labeltosegment.COMP_MIN_SIZE:
            slantsdil[slantsarr==i]=False

#Obtain Horizontal + VertLines + Slantlines + Dilated Segmasks
    horvertslant=np.zeros(vertlines.shape, dtype=bool)
    horvertslant=(np.logical_or(skeldil, horlines))
    horvertslant=(np.logical_or(slantsdil, horlines))
    horvertslant=(np.logical_or(horvertslant, vertlines))
    horvertslant=(np.logical_or(horvertslant, fill1))
    
    ccarr, ccnum=label(horvertslant, np.ones((3,3)))
    
    ccarr=ccarr.astype(np.uint16)
    binfill=list(np.bincount(ccarr.flatten()))
    bfill=sorted(binfill, reverse=True)
    bfill.remove(bfill[0])
    
    for i in range(len(binfill)):
        if binfill[i]<=cfg.labeltosegment.COMP_MIN_SIZE:
            horvertslant[ccarr==i]=False
        
    ccarr1, ccnum1=label(horvertslant, np.ones(cfg.labeltosegment.STD_DIL_SIZE))
    print 'Number of segments is', ccnum1
    
    ansans=logor(original, horlines)
    ansans=logor(ansans, vertlines)
    ansans=logor(ansans, slantsdil)    

    strmaskdilname = cfg.OUT_DIR + cfg.stringify.STRINGIFY_DIR + fname + 'strmaskdil' +cfg.IMG_EXT
    z1=np.asarray(imread(strmaskdilname), dtype=bool)
    final=logor(z1, horvertslant)
    farr, fnum=ndimage.label(final, np.ones(cfg.labeltosegment.STD_DIL_SIZE))

    actualsegments=[]
    for i in segexamplelist:
        a,b=i
        actualsegments.append(farr[a,b])
        
    imsave(cfg.OUT_DIR + cfg.labeltosegment.OUT_DIR + fname + 'withtext.png', final)
    imsave(cfg.OUT_DIR + cfg.labeltosegment.OUT_DIR + fname + 'check.png', horvertslant)
    imsave(cfg.OUT_DIR + cfg.labeltosegment.OUT_DIR + fname + '.png', ansans)
    
#    if fnum != noofsegments:
#        print 'Number of segments calculated incorrectly. . '
#        return -1, time.time()-starttime

    return 0, time.time()-starttime
    