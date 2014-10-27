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
from itertools import product
import mylib
from mylib import show
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal


import time
start_time = time.time()

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

def textextraction(fname=None):
#if 1:
    fname=None
    print 'No file name assigned'
    
    if fname==None:
        imname='images_consolidated\\6_b.png'
        imname='images_consolidated\\8_a.png'
        imname='images_consolidated\\15_b.png'
        imname='images_consolidated\\6_a.png'

        imname='images_consolidated\\8_b.png'
        imname='images_consolidated\\5_b.png'
        imname='images_consolidated\\4_3_b.png'
        imname='images_consolidated\\4_7_a.png'
        imname='images_consolidated\\4_5_b.png'
        imname='images_consolidated\\4_6_b.png'
        imname='images_consolidated\\5_a.png'

        i=imname.rfind('\\')
        fname=imname[i+1:]
        fname=fname[:-4]
    else:
        imname='images_consolidated\\'+fname+'.png'

    print imname
#Opening Images, Preliminaries
    pilimg = Image.open(imname)
    pilimg = pilimg.convert('1')
#    pilimg.save('C:\\SwarunDocs\\im1.png')

    newimg=pilimg.copy()
    data=newimg.load()
    pilw, pilh=newimg.size
    BORDER=4
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
    im1 = np.zeros(img.shape)
    
    img.flags.writeable=True
    height, width = img.shape

       

#==============================================================================
# 
#==============================================================================

#Label matching
    (ccdict, _, num, output) = bwlabel(newimg)
    show(output)
    print 'Finding connected components. . . '
    print time.time() - start_time, 'seconds'
    print num, 'components found . . '
#    toimage(output).show()
    
    
    data = pilimg.load()
    complen=[]
    compwidth=[]
    for i in range(1,num+1):
#        print len(ccdict[i])
        ccchoose=i
        if len(ccdict[i])==0:
            ccdict[i]=[(1,1)]
#            del ccdict[i]
#            num-=1
#            complen.append(1)
#            compwidth.append(1)
#            continue
        aa=ccdict[ccchoose]
        c, d = zip(*aa)
        
        compmax=max(ccdict[ccchoose])
        compmin=min(ccdict[ccchoose])
        
       
        complen.append(max(c)-min(c)+1)
        compwidth.append(max(d)-min(d)+1)

#Vital Constants- EDITABLE        
    COMPWIDTH_L=55
    COMPLEN_L=55
    DASHEDLEN_U=25
    DASHEDWIDTH_U=25
    DOTSWIDTH_L=6
    DOTSLEN_L=6


#==============================================================================
#     for i in range(1,num+1):
#         ar=float((complen[i-1]*compwidth[i-1]) / len(ccdict[i]) )
#         if complen[i-1] < COMPLEN_L and compwidth[i-1]< COMPWIDTH_L : 
#             if ar>1:
#                 for j in ccdict[i]:
#                     
#                     a,b=j
#                     img[b,a]=False
#                 ccdict[i]=[]
#                 
#             if ar==1.0:
#                 if (complen[i-1]>DASHEDLEN_U or compwidth[i-1]>DASHEDWIDTH_U):
#                     for j in ccdict[i]:
#                         
#                         a,b=j
#                         img[b,a]=False
#                     ccdict[i]=[]
#                 if (complen[i-1]<DOTSLEN_L and compwidth[i-1]<DOTSWIDTH_L):
#                     for j in ccdict[i]:
#                         
#                         a,b=j
#                         img[b,a]=False
#                     ccdict[i]=[]
#     toimage(img).show()    
#==============================================================================
    
    textcomplist=[]    
    for i in range(1,num+1):
        ar=float((complen[i-1]*compwidth[i-1]) / len(ccdict[i]) )
        if complen[i-1] < COMPLEN_L and compwidth[i-1]< COMPWIDTH_L : 
            if ar>1:
                textcomplist.append(i)
#                ccdict[i]=[]
                
            elif ar==1.0:
                if (complen[i-1]>DASHEDLEN_U or compwidth[i-1]>DASHEDWIDTH_U):
                    textcomplist.append(i)
#                    ccdict[i]=[]
                if (complen[i-1]<DOTSLEN_L and compwidth[i-1]<DOTSWIDTH_L):
                    textcomplist.append(i)
#                    ccdict[i]=[]
    print
    print 'Extracting Text . . .'
    
    mylib.picklethis(ccdict, 'ccdict'+fname)
    mylib.picklethis(textcomplist, 'textcomplist'+fname)    
    mylib.picklethis(num, 'ccnum'+fname)
    

        
    for i in range(1, num+1):
        if i not in textcomplist:
            for j in ccdict[i]:
                a,b=j
                img[b,a]=False
            ccdict[i]=[]
    print 'Separating Text and Graphics. . .'


    imsave('Outputs\\textonly' + fname + '.png',img)
#    show(img)    
    img=img.astype(bool)
    img1=np.asarray(imread(imname), dtype=bool)
    img2=np.subtract(img, img1)
    imsave('Outputs\\notext' +fname+'.png', img2)
    
    print 'textonly and notext images generated. . '    
    print

textextraction('5_a')
if __name__ == "__main__":
#    flist=mylib.pickleload('Outputs\\fnamelist.pkl')
#    for i in flist:
#        textextraction(i)
#        j=i[:-1]+'b'
#        textextraction(j)
    print time.time() - start_time, "seconds"
