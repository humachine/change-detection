# -*- coding: utf-8 -*-
"""
@author: ipcv5
"""

from textextraction import textextraction
from stringify import stringify
import time

import config as cfg
start_time = time.time()


def main():
    fname='6_b.png'
    res, tim = textextraction(fname)
#    res,tim=-1,0
    if 0 > res:
        print 'Text Extraction Failed'
        return -1 
    else:
        print 'Text Extraction Done in', tim, 'seconds. . . \n\n'


    res, tim = stringify(fname)
#    res,tim=-1,0
    if 0 > res:
        print 'Stringify Text Failed'
        return -1 
    else:
        print 'Stringify Text Done in', tim, 'seconds. . . \n\n'
    return 0

if __name__ == "__main__":
    result=main()
    print 'Process ended in', ['failure', 'success'][result+1], 'in', time.time() - start_time, "seconds"
