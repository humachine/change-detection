# -*- coding: utf-8 -*-
"""
- Takes Filled segments (often with labeling lines attached)
- Breaks labeling lines
- Now, analyzes segments based on size. Decides threshold. Removes the rest

THRESH=10000
ForSir - FIRST attempt at Thinning and getting segment masks
Created on Wed Apr 02 16:14:46 2014

Untitled6 -> Untitled7 -> extend


@author: ipcv5
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 02 15:16:46 2014

@author: ipcv5
"""
import numpy as np
 
from PIL import Image	
import cv2
from mylib import pickleload, picklethis
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
import time
from scipy.ndimage import binary_dilation as dilate
from scipy.ndimage import binary_fill_holes as fill
import config as cfg

def show(x):
    toimage(x).show()

def removelines(fname=None):
    starttime=time.time()
    if fname==None:
        print 'No file name assigned'
        return 0, time.time()-starttime

    if cfg.IMG_EXT in fname:
        fname=fname[:-4]
        
    print 'Removing labeling lines(Stage 1) for', fname
    fill2=np.asarray(imread(cfg.OUT_DIR+cfg.thinning.THINNING_DIR + fname + cfg.removelines.FILL_IMG_NAME + cfg.IMG_EXT), dtype=bool)


    ans=ndimage.morphology.distance_transform_cdt(fill2, metric='chessboard')    
    
    loc=np.where((ans<2) & (ans>0))
    
    fill2copy=fill2.copy()
    fill2copy[loc]=0

    curr=fill2copy
    curr=ndimage.grey_erosion(curr, size=(5,5))
    ccarr, ccnum=ndimage.label(curr, np.ones((3,3)))    
    ccarr=ccarr.astype(np.int16)
    temp=list(np.bincount(ccarr.flatten()))
    
    sortedtemp=sorted(temp, reverse=True)
    sortedtemp.remove(sortedtemp[0])    
    
    print 'Separating Segments from shaded boxes'    
    '''
    The below loop does this: There are several filled components with varying areas.
    The ones with smaller areas(less than 100-200) pixels are often shaded text boxes or so. 
    The actual segments are usually much larger than the remaining components. 
    So, we do a basic traversal of filled components from largest area->smallest area. 
    If at any point, the area of a component is 'SIGNIFICANTLY LARGER' than the area of the next smallest component, we break.
    The components smaller than the breakpoint are not segments and the ones larger are.
    '''
    thresh=cfg.removelines.STARTING_THRESH
    czlower=cfg.removelines.CHECK_ZONE_LOWER
    czupper=cfg.removelines.CHECK_ZONE_UPPER
    segvsnonseg=cfg.removelines.SEG_VS_NON_SEG_FACTOR
    
    for index in range(len(sortedtemp)-1):
        now=sortedtemp[index]
        nxt=sortedtemp[index+1]
        '''If Area of component > 10000 -> continue
        If area of component is >5000 & <10000, check if it's 'significantly' larger than the next component. If yes, threshold is at this component. If no, carry on
        If area of component < 5000, break and set threshold as the default(10000)
        '''
        if now > czlower and now < czupper:
            if now > nxt * segvsnonseg:
                thresh=now-1
                break
        if now<segvsnonseg:
            break
        
    for index, i in enumerate(temp):
        if i <= thresh:
            curr[ccarr==index]=0

    imsave(cfg.OUT_DIR + cfg.removelines.SAVE_DIR + fname+ cfg.IMG_EXT, curr)
    return 0, time.time()-starttime
