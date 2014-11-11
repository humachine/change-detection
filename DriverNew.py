# -*- coding: utf-8 -*-
"""
@author: ipcv5
"""
from Setup import setup
from Sanitize import sanitize
from TextExtraction import textextraction
from Stringify import stringify
from Thinning import thinning
from RemoveLines import removelines
from Segmentation import segmentation
from LabelToSegment import labeltosegment
from StringProperties import stringproperties
from LabelMatching import labelmatching

import time
import config as cfg

start_time = time.time()


def drive(fname):
    '''Text Extraction'''
    res, tim = textextraction(fname)
    res,tim=1,0
    if 0 > res:
        print 'Text Extraction Failed'
        return -1 
    else:
        print 'Text Extraction Done in', tim, 'seconds. . . \n\n'

    '''Stringify Textual Components'''
    res, tim = stringify(fname)
    res,tim=1,0
    if 0 > res:
        print 'Stringify Text Failed'
        return -1 
    else:
        print 'Stringify Text Done in', tim, 'seconds. . . \n\n'

    '''Thinning labeling lines'''
    res, tim = thinning(fname)
#    res,tim=1,0
    if 0 > res:
        print 'Thinning the image Failed'
        return -1 
    else:
        print 'Thinning of Image Done in', tim, 'seconds. . . \n\n'


    '''Removing labeling lines'''
    res, tim = removelines(fname)
#    res,tim=1,0
    if 0 > res:
        print 'Removing labeling lines Failed ! '
        return -1 
    else:
        print 'Removed all the labeling lines in', tim, 'seconds. . . \n\n'


    '''Segmentation of Image'''
    res, tim = segmentation(fname)
#    res,tim=1,0
    if 0 > res:
        print 'Segmentation Failed ! Segmentation Fault ! '
        return -1 
    else:
        print 'Image segmentation completed in', tim, 'seconds. . . \n\n'
    return 0


    '''Attaching Labels to Segments'''
    res, tim = labeltosegment(fname)
#    res,tim=1,0
    if 0 > res:
        print 'Attaching labels to segments failed'
        return -1 
    else:
        print 'Attaching labels to segments completed in', tim, 'seconds. . . \n\n'
    return 0


    '''Calculating String Properties'''
    res, tim = stringproperties(fname)
#    res,tim=1,0
    if 0 > res:
        print 'OCR Failed'
        return -1 
    else:
        print 'OCR Engine recognition completed in', tim, 'seconds. . . \n\n'
    return 0


def main():
    print 'Creating Directories. . .'
    print 'Preparing Environment. . .'
    setup()
    
    fname='5_a.png'
    
    '''Sanitization'''    
    fname1=fname
    fname1=fname[:-5]+ ['a','b'][fname[-5]=='a']  +fname[-4:]
    print fname, fname1
#    if not sanitize(fname, fname1):
#        print 'Images are not suitable for comparison. Quitting'
#        return -1
    print 'Images are suitable for comparison. \nChange Detection begins. . .'
    
    print 'Precomputing for Image1'
    drive(fname)
    print 'Precomputing for Image2'
    drive(fname1)

    '''Label Matching'''
    res, tim = labelmatching(fname)
    if 0 > res:
        print 'Label Matching Failed'
        return -1 
    else:
        print 'Label Matching completed in', tim, 'seconds. . . \n\n'
    return 0

if __name__ == "__main__":
    result=main()
    print 'Process ended in', ['failure', 'success'][result+1], 'in', time.time() - start_time, "seconds"
