# -*- coding: utf-8 -*-
"""
@author: ipcv5
"""

from textextraction import textextraction
import time
#from actualthinningondrugs import thinning
#from labelstocomps import labels2comps
#from associationsrev import associations
#from stringprops import stringprops

import config as cfg
start_time = time.time()


def main():
    print cfg.IMG_DIR
    fname='8_a'
    #res, tim = textextraction(fname)
    res,tim=-1,0
    print res, tim
    if 0 > res:
        print 'Text Extraction Failed'
        return -1 
    else:
        print 'Text Extraction Done . . . \n\n'

#
#
#fname='20_a'
#
#flist=[]
#
#fname='8_b'
#flist.append(fname)
#fname='8_a'
#flist.append(fname)
#fname='6_a'
#flist.append(fname)
#fname='5_a'
#flist.append(fname)
#fname='15_a'
#flist.append(fname)
#
#
def drive(fname):
    res, time=textextraction(fname)
    getstrings(fname)
    print 'getstrings done'
#    thinning(fname)
#    print 'thinning done'
#    #
#    labels2comps(fname, True)
##    labels2comps(fname, False)
#    
#    print 'label2comps (MEGAFILL) done'
#    ##
#    #
#    associations(fname)
#    print 'assoc done'
#    stringprops(fname)
#    print 'stringprops done'
#    
#    
#    if fname[-1]=='a':
#        fname=fname[:-1]+'b'
#    else:
#        fname=fname[:-1]+'a'
#    textextraction(fname)
#    print 'textextraction done1'
#    getstrings(fname)
#    print 'getstrings done1'
#    thinning(fname)
#    print 'thinning done1'
#    #
#    labels2comps(fname, True)
##    labels2comps(fname, False)
#    
#    print 'label2comps (MEGAFILL) done1'
#    ##
#    #
#    associations(fname)
#    print 'assoc done1'
#    stringprops(fname)
#    print 'stringprops done1'
#    
#    
#    
#    #
#    if fname[-1]=='b':
#        fname=fname[:-1]+'a'
#    finale(fname)
#    print 'Phew!'
#    #
#    #    
#    #StringProps - String Properties, Euler number, Text Extraction . . . 
#    #Finale - Result Generation
#    
##for i in flist: 
##    drive(i)
#
#drive('8_a')
#print time.time() - start_time, 'seconds'
    
    
if __name__ == "__main__":
    main()
    print time.time() - start_time, "seconds"
