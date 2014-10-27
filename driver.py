# -*- coding: utf-8 -*-
"""

5
6
8
15
17
19
25
26
4_7


FINAL
@author: ipcv5
"""

from scipy.misc import toimage, imread, imshow, imsave
from scipy import ndimage
from PIL import Image
from without_textanddashes_withclass import textextraction
from binlabeller import bwlabel
from itertools import product
import mylib
import numpy as np
from getthem import getstrings
import time
from actualthinningondrugs import thinning
from labelstocomps import labels2comps
from associationsrev import associations
from stringprops import stringprops
from finale import finale
start_time = time.time()



fname='20_a'

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


def drive(fname):
    textextraction(fname)
    print 'textextraction done'
    getstrings(fname)
    print 'getstrings done'
    thinning(fname)
    print 'thinning done'
    #
    labels2comps(fname, True)
#    labels2comps(fname, False)
    
    print 'label2comps (MEGAFILL) done'
    ##
    #
    associations(fname)
    print 'assoc done'
    stringprops(fname)
    print 'stringprops done'
    
    
    if fname[-1]=='a':
        fname=fname[:-1]+'b'
    else:
        fname=fname[:-1]+'a'
    textextraction(fname)
    print 'textextraction done1'
    getstrings(fname)
    print 'getstrings done1'
    thinning(fname)
    print 'thinning done1'
    #
    labels2comps(fname, True)
#    labels2comps(fname, False)
    
    print 'label2comps (MEGAFILL) done1'
    ##
    #
    associations(fname)
    print 'assoc done1'
    stringprops(fname)
    print 'stringprops done1'
    
    
    
    #
    if fname[-1]=='b':
        fname=fname[:-1]+'a'
    finale(fname)
    print 'Phew!'
    #
    #    
    #StringProps - String Properties, Euler number, Text Extraction . . . 
    #Finale - Result Generation
    
#for i in flist: 
#    drive(i)

drive('8_a')
print time.time() - start_time, 'seconds'