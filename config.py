# -*- coding: utf-8 -*-
"""
@author: ipcv5
"""
IMG_DIR = '../../images_consolidated/'
OUT_DIR = 'Outs/'
IMG_EXT = '.png'

class textextractioncfg:
    BORDER=4        #Make border to 0 so that components near border do not create array-boundary errors
    COMPWIDTH_L=55
    COMPLEN_L=55
    DASHEDLEN_U=25
    DASHEDWIDTH_U=25
    DOTSWIDTH_L=6
    DOTSLEN_L=6

class stringify:
    MINTEXTAREA=20
    STRINGIFY_DIR='GetStrings/'
    DILMASK=30
    TOLERANCE= 16
    GAP=52
    TOL=0

class thinning:
    SKEL_IMG_DIR='Skeletons/'
    THINNING_DIR='Thinning/'

class removelines:
    FILL_IMG_DIR='../../Outputs/Restart/'
    FILL_IMG_NAME='tempfill'
    '''Below constants are empirical. Play around as is necessary'''
    STARTING_THRESH=10000
    CHECK_ZONE_LOWER=5000
    CHECK_ZONE_UPPER=1000
    SEG_VS_NON_SEG_FACTOR=5
    SAVE_DIR='Segments/Intermediates/'
    
class segmentation:
    TEXTBOX_DENSITY=0.05    #Refers to the density of text pixels in a shaded textbox i.e No of text pixels / Total pixels of a shaded textbox > 0.05
    OUT_DIR='Segments/'
    DEBUG_DIR='Segments/Debug/'

class labeltosegment:
    OUT_DIR = 'LabelToSegment/'
    GREY_DIL_SIZE=(50,50)
    STD_DIL_SIZE=(3,3)
    SKEL_DIL_SIZE=(5,5)
    