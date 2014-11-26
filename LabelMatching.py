# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 00:32:50 2014

@author: Home
"""

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
from mylib import pickleload, picklethis, show, pickle
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
from scipy.spatial import distance
import time
from tifffile import TiffFile

import tesseract
import config as cfg

api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)

def findpagesize(path_to_file):    
    print path_to_file
    width=1
    length=1
    for page in TiffFile(path_to_file):
        for tag in page.tags.values():
            if tag.name=='image_width':
                width=tag.value
            if tag.name=='image_length':
                length=tag.value
    ratio=float(width)/float(length)
    if 1.5<ratio <1.6:
        return 4,4
    if 0.7<ratio <0.8 and length<6000:
        return 4,4
    if 0.7<ratio <0.8:
        return 8,8
    if 0.6<ratio<0.7:
        return 6,6
    
    return 4,4 


def process(string):
    string=string.replace('0','O')
    string=string.replace('Z','2')
    string=string.replace(':|:', 'i')   
    string=string.replace(':I:', 'i')   

    string=string.replace('j:', 'i')   
    string=string.replace('|', '1')
    string=string.replace('I', '1')
    string=string.replace('l', '1')
    string=string.replace('_', '.')
    string=string.replace('H:', '7i')
    string=string.replace('\xe2\x80\x94', '-')
    string=string.replace(':E', 'i')   
    string=string.replace('\xe2\x80\x98', 'T')
    string=string.replace('"', '7')
    return string

#fname='6_a.png'
#if 1:
def labelmatching(fname=None):
    starttime=time.time()
    if cfg.IMG_EXT in fname:
        fname=fname[:-4]        
    fname1=fname[:-1]+'a'        
    fname2=fname[:-1]+'b'        
        
    divl, divw=4,4
    if cfg.labelmatching.TIF_ON==True:
        divl, divw=findpagesize(cfg.IMG_DIR+fname1+'.tif')
        
        
    SAVE_DIR=cfg.OUT_DIR+cfg.properties.OUT_DIR

    '''Loading previously saved images and arrays
    '''
    strmaskhora=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname1+'hor.png'), dtype=bool)
    strmaskverta=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname1+'vert.png'), dtype=bool)
    
    originalimagea=np.asarray(imread(cfg.IMG_DIR+fname1+'.png'), dtype=bool)
    originalimageb=np.asarray(imread(cfg.IMG_DIR+fname2+'.png'), dtype=bool)

    strmaskhorb=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname2+'hor.png'), dtype=bool)
    strmaskvertb=np.asarray(imread(cfg.OUT_DIR+cfg.stringify.STRINGIFY_DIR+fname2+'vert.png'), dtype=bool)

    centa=pickleload(SAVE_DIR + fname1 + 'centroids.pkl')
    centb=pickleload(SAVE_DIR + fname2 + 'centroids.pkl')

    slia=pickleload(SAVE_DIR + fname1 + 'slices.pkl')
    slib=pickleload(SAVE_DIR + fname2 + 'slices.pkl')
 
    horstra=pickleload(SAVE_DIR + fname1 + 'hor.pkl')
    vertstra=pickleload(SAVE_DIR + fname1 + 'vert.pkl')
    texta=horstra+vertstra
    
    horstrb=pickleload(SAVE_DIR + fname2 + 'hor.pkl')
    vertstrb=pickleload(SAVE_DIR + fname2 + 'vert.pkl')
    textb=horstrb+vertstrb

#    texta=[process(i) for i in texta]
#    textb=[process(i) for i in textb]
    '''
    Comparing labels and label matching
    '''    
    
    for x in range(len(texta)):
        for y in range(len(textb)):
            p=texta[x]
            q=textb[y]
            
            if p!=q and p!=process(q) and q!=process(p) and process(q)!=process(p):            
#            if p!=q:
                continue

            sel=y            
            mindist=distance.euclidean(centa[x], centb[y])
            for z in range(y, len(textb)):
                if texta[x] == textb[z]:
                    if distance.euclidean(centa[x], centb[z]) < mindist:
                        sel=z
            texta[x]=''
            textb[sel]=''
    
    diffa=[x for x in texta if x!='']
    diffb=[x for x in textb if x!='']
    print 'Number of changes in Image 1: ', len(diffa)
    print 'Number of changes in Image 2: ', len(diffb)

    PADDING=cfg.labelmatching.PADDING
    THICKNESS=cfg.labelmatching.THICKNESS 
    
    f = open(cfg.OUT_DIR+cfg.RES_DIR+fname1+'changes.txt','w')
    f.write(str(len(diffa))+'\n')
#    resa=originalimagea*np.invert(strmaskhora)*np.invert(strmaskverta)
    resa=np.zeros((originalimagea.shape), dtype=bool)
    resa1=originalimagea.copy()
    length, width=resa.shape

    for x in range(len(texta)):
        if texta[x]!='':
            sll=slia[x]
            resa[sll[0].start-PADDING-2*THICKNESS: sll[0].start-PADDING,  sll[1].start-PADDING-2*THICKNESS:sll[1].stop+PADDING+2*THICKNESS]=True
            resa[sll[0].stop +PADDING: sll[0].stop +PADDING+2*THICKNESS,  sll[1].start-PADDING-2*THICKNESS:sll[1].stop+PADDING+2*THICKNESS]=True
            resa[sll[0].start-PADDING-2*THICKNESS:sll[0].stop+PADDING+2*THICKNESS, sll[1].start-PADDING-2*THICKNESS:sll[1].start-PADDING]=True
            resa[sll[0].start-PADDING-2*THICKNESS:sll[0].stop+PADDING+2*THICKNESS, sll[1].stop+PADDING:sll[1].stop+PADDING+2*THICKNESS]=True
            resa[slia[x]]=originalimagea[slia[x]]
            
            dival=int(centa[x][0]*divl/length)
            divaw=int(centa[x][1]*divw/width)
            
            f.write(chr(64+divl-dival)+ str(divw-divaw) + '\n')
    f.close()

                        
    resa1[:]=resa[:]
    resa=np.logical_or(originalimagea*np.invert(strmaskhora)*np.invert(strmaskverta), resa)
    '''
    Colorizing Output for A
    '''
    a=originalimagea.copy()
    a=np.invert(a)
    a=a.astype(np.uint8)
    a*=255
    b=a.copy()
    c=a.copy()
    b[resa1>0]=0
    c[resa1>0]=0
    imsave(cfg.OUT_DIR+cfg.RES_DIR+fname1+'colourized'+cfg.IMG_EXT, np.dstack((a,b,c)))    
    
    f = open(cfg.OUT_DIR+cfg.RES_DIR+fname2+'changes.txt','w')
    f.write(str(len(diffb))+'\n')
    
    resb=np.zeros((originalimageb.shape), dtype=bool)
    resb1=originalimageb.copy()
    for x in range(len(textb)):
        if textb[x]!='':
            sll=slib[x]
            resb[sll[0].start-PADDING-2*THICKNESS: sll[0].start-PADDING,  sll[1].start-PADDING-2*THICKNESS:sll[1].stop+PADDING+2*THICKNESS]=True
            resb[sll[0].stop +PADDING: sll[0].stop +PADDING+2*THICKNESS,  sll[1].start-PADDING-2*THICKNESS:sll[1].stop+PADDING+2*THICKNESS]=True
            resb[sll[0].start-PADDING-2*THICKNESS:sll[0].stop+PADDING+2*THICKNESS, sll[1].start-PADDING-2*THICKNESS:sll[1].start-PADDING]=True
            resb[sll[0].start-PADDING-2*THICKNESS:sll[0].stop+PADDING+2*THICKNESS, sll[1].stop+PADDING:sll[1].stop+PADDING+2*THICKNESS]=True
            resb[slib[x]]=originalimagea[slib[x]]

            divbl=int(centb[x][0]*divl/length)
            divbw=int(centb[x][1]*divw/width)
            
            f.write(chr(64+divl-divbl)+ str(divw-divbw) + '\n')

    f.close()
    resb1[:]=resb[:]
    resb=np.logical_or(originalimageb*np.invert(strmaskhorb)*np.invert(strmaskvertb), resb)

    '''
    Colorizing Output for B
    '''
    a=originalimageb.copy()
    a=np.invert(a)
    a=a.astype(np.uint8)
    a*=255
    b=a.copy()
    c=a.copy()
    b[resa1>0]=0
    c[resa1>0]=0
    imsave(cfg.OUT_DIR+cfg.RES_DIR+fname2+'colourized'+cfg.IMG_EXT, np.dstack((a,b,c)))    


    imsave(cfg.OUT_DIR+cfg.RES_DIR+fname1+cfg.IMG_EXT, np.invert(resa))    
    imsave(cfg.OUT_DIR+cfg.RES_DIR+fname2+cfg.IMG_EXT, np.invert(resb))    
    
    texta=[process(i) for i in texta]
    textb=[process(i) for i in textb]

#    print texta
#    print textb
    return 0, time.time()-starttime
labelmatching('5_a.png')