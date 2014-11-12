# -*- coding: utf-8 -*-
"""
Created on Sun Jun 01 02:03:09 2014

@author: Home
"""

from PIL import Image
from numpy import *
from mylib import show
import pylab
import sift
from scipy.spatial import distance
import time

starttime=time.time()
dist=distance.euclidean

def angle(u, v):
    if array_equal(u,v):
        return 0
    c = dot(u,v)/norm(u)/norm(v) # -> cosine of the angle
    vectorangle = arccos(c)
    print u, v, vectorangle*57.2957795131
    return vectorangle*57.2957795131


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return 360
    return angle*57.2957795131


def siftfn(fname1=[], fname2=[]):
    if fname1==[]:
            
    
        fname1='c1'
        fname2='c2'
        
        fname1='d1'
        fname2='d2'
        
        fname1='d1blur'
        fname2='d2blur'
        
        
        fname1='barca'
        fname2='boot'
        
        fname1='c2'
        fname2='c22'
    print fname1, fname2
    
    sift.process_image(fname1+'.pgm', fname1+'.key')    
    
    l1,d1 = sift.read_features_from_file(fname1+'.key')
    im1 = array(Image.open(fname1+'.pgm'))
    
    sift.plot_features(im1,l1)
    
    sift.process_image(fname2+'.pgm', fname2+'.key')    
    l2,d2 = sift.read_features_from_file(fname2+'.key')
    im2 = array(Image.open(fname2+'.pgm'))
    sift.plot_features(im2,l2)
    
    matchscores=sift.match(d1, d2)
    cnt=sift.plot_matches(im1,im2,l1,l2,matchscores)
    
    #(822, 567) (390, 820)
    coord1=np.zeros((cnt,2))
    coord2=np.zeros((cnt,2))
    
    ct=0
    for i in range(len(matchscores)):
        if matchscores[i]>0:
            coord1[ct,1]=(l1[i,1])
            coord1[ct,0]=(l1[i,0])
            ct+=1
    
    ct=0
    angles1=[]
    angles2=[]
    anglesr=[]
    for i in range(len(matchscores)):
        if matchscores[i]>0:
            coord2[ct,1]=(l2[int(matchscores[i]),1])
            coord2[ct,0]=(l2[int(matchscores[i]),0])
            ct+=1
            angles1.append(l1[i,3])
            angles2.append(l2[int(matchscores[i]),3])
            anglesr.append(np.abs(float((l2[int(matchscores[i]),3]/l1[i, 3]))))
    #        print l1[i,2], l1[i, 3], l2[int(matchscores[i]),2], l2[int(matchscores[i]),3], np.abs(float((l2[int(matchscores[i]),3]/l1[i, 3])))
    
    
    ratio=[]
    for i in range(ct-1):
        dist1=dist(coord1[i], coord1[i+1])
        dist2=dist(coord2[i], coord2[i+1])
        if abs(dist2)>=0.000001:
            ratio.append(float(dist1/dist2))
        ang1=angle_between(coord1[i]-coord1[i+1], coord1[i+1])
        ang2=angle_between(coord2[i]-coord2[i+1], coord2[i+1])
        ang3=angle_between(coord2[i],coord1[i])
    #    print ang1, ang2, ang3
    #        print float(dist1/dist2)
    
    
    print 
    print
    sortedratio=sorted(ratio)
    ratio1=-1
    if len(ratio)>10:
        ratio1=sortedratio[3:-3]
        
    
    print time.time()-starttime, 'seconds'
    y0,x0=coord1[0]
    deg1=[]
    for i in range(1, cnt):
        y1, x1=coord1[i]
        if x1-x0 >=0:
            deg1.append(angle_between([x1-x0, y1-y0], [-1,0]))
        else:
            deg1.append(angle_between([x1-x0, y1-y0], [1,0]))
        
    
    y0,x0=coord2[0]
    deg2=[]
    for i in range(1, cnt):
        y1, x1=coord2[i]
        if x1-x0 >=0:
            deg2.append(angle_between([x1-x0, y1-y0], [-1,0]))
        else:
            deg2.append(angle_between([x1-x0, y1-y0], [1,0]))
    
    #TODO Write code for interquartile mean as a function
    
    anglediff=[deg2[i]-deg1[i] for i in range(ct-1)]
    quart1=percentile(anglediff, 25)
    quart2=median(anglediff)
    quart3=percentile(anglediff, 75)
    interquart=quart3-quart1
    
    srtanglediff=sorted(anglediff)
    anglediffstart=searchsorted(srtanglediff, quart1-3*interquart)
    anglediffend=searchsorted(srtanglediff, quart3+3*interquart, 'right')
    
    print mean(srtanglediff[anglediffstart:anglediffend]), 'degrees shifted from image 1'
    print 'scaling is', mean(ratio1), median(ratio)
    #
    
    #    print x-p2[0], y-p2[1]
    
    #    print dist1, dist2
    #    print ratio[i], dist1, dist2
            
    #sift.plot_features(im1, coord1)
    #sift.plot_features(im2, coord2)
#import os
#os.chdir('../../')
#print os.getcwd()
#SAVE_DIR='Outs/PGM/'
#SAVE_DIR=''
#fname1='8_a1'
#fname2='8_b1'

fname1='5_a1'
fname2='5_b1'

#siftfn(SAVE_DIR+fname1, SAVE_DIR+fname2)
#
#print time.time()-starttime, 'seconds'
#
siftfn(fname1, fname2)