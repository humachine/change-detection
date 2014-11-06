# -*- coding: utf-8 -*-
"""
@author: ipcv5
"""

from TextExtraction import textextraction
from Stringify import stringify
from Thinning import thinning
import time

import config as cfg
start_time = time.time()


def main():
    fname='14_a.png'

    res, tim = textextraction(fname)
    res,tim=1,0
    if 0 > res:
        print 'Text Extraction Failed'
        return -1 
    else:
        print 'Text Extraction Done in', tim, 'seconds. . . \n\n'

    res, tim = stringify(fname)
    res,tim=1,0
    if 0 > res:
        print 'Stringify Text Failed'
        return -1 
    else:
        print 'Stringify Text Done in', tim, 'seconds. . . \n\n'

    res, tim = thinning(fname)
#    res,tim=1,0
    if 0 > res:
        print 'Thinning the image Failed'
        return -1 
    else:
        print 'Thinning of Image Done in', tim, 'seconds. . . \n\n'





    return 0

if __name__ == "__main__":
    result=main()
    print 'Process ended in', ['failure', 'success'][result+1], 'in', time.time() - start_time, "seconds"
