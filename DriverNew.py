# -*- coding: utf-8 -*-
"""
@author: ipcv5
"""

from TextExtraction import textextraction
from Stringify import stringify
from Thinning import thinning
from RemoveLines import removelines
from Segmentation import segmentation
import time

import config as cfg
start_time = time.time()

def main():
    fname='14_a.png'

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


    '''Segmentation of Image - Stage 1'''
    res, tim = segmentation(fname)
#    res,tim=1,0
    if 0 > res:
        print 'Segmentation Failed ! Segmentation Fault ! '
        return -1 
    else:
        print 'Image segmentation completed in', tim, 'seconds. . . \n\n'
    return 0

if __name__ == "__main__":
    result=main()
    print 'Process ended in', ['failure', 'success'][result+1], 'in', time.time() - start_time, "seconds"
