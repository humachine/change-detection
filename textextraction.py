# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 10:14:58 2014
Updates:

Progress thus far:

- Text and Graphics
`    Text extraction                             
`    Removing labeling lines, dashed lines, etc 
`    Grouping characters to strings
Segmentation and Matching
`    Segmentation
    Matching segments
Association of labels with segments
    Attaching labeling lines to segments
    Associating labels with segments
Image Comparison

@author: ipcv5
    """
from scipy.misc import toimage, imread, imshow, imsave
from scipy import ndimage
from PIL import Image
from binlabeller import bwlabel
from mylib import show
import numpy as np
import time

import mylib
import config as cfg

"""The Component Class
"""
class component:
    def __init__(self, text, length, width, corners, centroid, category):
        self.text = text
        self.length = length
        self.width = width
        self.corners = corners
        self.centroid = centroid
        self.category = category

    def __repr__(self):
        return str(self.category)

#------------------------------------------------------------------------
'''Main Textextraction Routine
'''

def textextraction(fname=None, kvs=[]):
    start_time = time.time()

    if fname==None:
        print 'No file name assigned'
        return 0, time.time()-start_time
    else:
        imname = cfg.IMG_DIR+fname
    print 'Extracting text from', imname
    if cfg.IMG_EXT in fname:
        fname=fname[:-4]

    #Initializing all vital constants
    BORDER=cfg.textextractioncfg.BORDER
    COMPWIDTH_L=cfg.textextractioncfg.COMPWIDTH_L
    COMPLEN_L=cfg.textextractioncfg.COMPLEN_L
    DASHEDLEN_U=cfg.textextractioncfg.DASHEDLEN_U
    DASHEDWIDTH_U=cfg.textextractioncfg.DASHEDWIDTH_U
    DOTSWIDTH_L=cfg.textextractioncfg.DOTSWIDTH_L
    DOTSLEN_L=cfg.textextractioncfg.DOTSLEN_L

#Opening Images and Preliminaries
    pilimg = Image.open(imname)
    pilimg = pilimg.convert('1')

    newimg=pilimg.copy()
    data=newimg.load()
    pilw, pilh=newimg.size
    
    for i in range(pilw):
        for j in range(BORDER):
            data[i,j]=255

    for i in range(pilw):
        for j in range(pilh-BORDER, pilh):
            data[i,j]=255

    for i in range(BORDER):
        for j in range(pilh):
            data[i,j]=255

    for i in range(pilw-BORDER,pilw):
        for j in range(pilh):
            data[i,j]=255


    img=np.asarray(Image.open(imname), dtype=bool)    
    
    img.flags.writeable=True
    height, width = img.shape

#==============================================================================
#   Image-Text Extraction using 8-connected component labeling
#==============================================================================

#Label matching
    print 'Finding connected components. . . '
    (ccdict, _, num, output) = bwlabel(newimg)  #ccdict has a dictionary containing: ccdict[i] has all the point pairs  (x,y) that belong to component number i

    if ('displayoutputs=True' in kvs):  #If output mode is true, then show intermediate screens, else carry on processing images
        show(output)
    
    print time.time() - start_time, 'seconds taken'
    print num, 'components found . . '
    
    
    data = pilimg.load()
    complen=[]
    compwidth=[]
    
    #Finding component dimensions. Complen and compwidth have the pixel 
    for i in range(1,num+1):
        ccchoose=i
        if len(ccdict[i])==0:
            ccdict[i]=[(1,1)]

        aa=ccdict[ccchoose]
        c, d = zip(*aa)
        
        complen.append(max(c)-min(c)+1)
        compwidth.append(max(d)-min(d)+1)

    textcomplist=[]    

#ar refers to the pixel density of the component being considered. ar=1.0 denotes a completely shaded rectangle
    for i in range(1,num+1):
        ar=float((complen[i-1]*compwidth[i-1]) / len(ccdict[i]) )   #Complen * Compwidth = Area of component; Len(ccdict) = Number of points in component
        if complen[i-1] < COMPLEN_L and compwidth[i-1]< COMPWIDTH_L : #If the component lengths and widths are not within the thresholds, the component is not considered to be that of text
            if ar>1:    #If ar>1, it's not a dashed line or a dot and is hence added to textcomplist
                textcomplist.append(i)
                
            elif ar==1.0:   #ar==1.0 means that it's either a dashed line or a dot. Both cases are dealt with below
                if (complen[i-1]>DASHEDLEN_U or compwidth[i-1]>DASHEDWIDTH_U):
                    textcomplist.append(i) 
                if (complen[i-1]<DOTSLEN_L and compwidth[i-1]<DOTSWIDTH_L):
                    textcomplist.append(i)
    print
    print 'Extracting Text . . .'
    
    #Pickles all the data and saves it to separate files
    mylib.picklethis(ccdict, cfg.OUT_DIR+'ccdict'+fname)
    mylib.picklethis(textcomplist, cfg.OUT_DIR+'textcomplist'+fname)    
    mylib.picklethis(num, cfg.OUT_DIR+'ccnum'+fname)
    

    print 'Separating Text and Graphics. . .'
    #The below loop removes all the components that are not text giving us the TEXTONLY image
    for i in range(1, num+1):
        if i not in textcomplist:
            for j in ccdict[i]:
                a,b=j
                img[b,a]=False
            ccdict[i]=[]


    imsave(cfg.OUT_DIR+'textonly' + fname + cfg.IMG_EXT,img)
    img=img.astype(bool)
    img1=np.asarray(imread(imname), dtype=bool)
    img2=np.subtract(img, img1)
    imsave(cfg.OUT_DIR+'notext' + fname+cfg.IMG_EXT, img2)
    
    print 'Text_only and No_text images generated. . '    
    print
    print time.time() - start_time, 'seconds taken'
    return 0, time.time()-start_time

#textextraction('5_a.png')
