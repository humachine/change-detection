# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 00:20:52 2014

@author: ipcv5
"""
from scipy.misc import toimage
import cv2
import numpy as np
import itertools
import sys
import time
start_time=time.time()
def findKeyPoints(img, template, distance=200):
    detector = cv2.FeatureDetector_create("SIFT")
    descriptor = cv2.DescriptorExtractor_create("SIFT")

    skp = detector.detect(img)
    skp, sd = descriptor.compute(img, skp)

    tkp = detector.detect(template)
    tkp, td = descriptor.compute(template, tkp)

    flann_params = dict(algorithm=1, trees=4)
    flann = cv2.flann_Index(sd, flann_params)
    idx, dist = flann.knnSearch(td, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    skp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            skp_final.append(skp[i])

    flann = cv2.flann_Index(td, flann_params)
    idx, dist = flann.knnSearch(sd, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    tkp_final = []
#    print len(dist)
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            tkp_final.append(tkp[i])
#    print len(tkp_final)
    return skp_final, tkp_final, len(dist), len(tkp_final)

def drawKeyPoints(img, template, skp, tkp, num=-1):
    h1, w1 = img.shape[:2]
    h2, w2 = template.shape[:2]
    nWidth = w1+w2
    nHeight = max(h1, h2)
    hdif = (h1-h2)/2
    newimg = np.zeros((nHeight, nWidth, 3), np.uint8)
    newimg[hdif:hdif+h2, :w2] = template
    newimg[:h1, w2:w1+w2] = img
    maxlen = min(len(skp), len(tkp))
    if num < 0 or num > maxlen:
        num = maxlen
    for i in range(num):
        pt_a = (int(tkp[i].pt[0]), int(tkp[i].pt[1]+hdif))
        pt_b = (int(skp[i].pt[0]+w2), int(skp[i].pt[1]))
        cv2.line(newimg, pt_a, pt_b, (255, 255, 0))
    return newimg


def match(imname1, imname2):
    img = cv2.imread(imname1)
    temp = cv2.imread(imname2)
    try:
    	dist = int(sys.argv[3])
    except IndexError:
    	dist = 30
    try:
    	num = int(sys.argv[4])
    except IndexError:
    	num = -1
    dist=10
    skp, tkp, totalkp, noofkpmatched = findKeyPoints(img, temp, dist)
    newimg = drawKeyPoints(img, temp, skp, tkp, num)
#    toimage(newimg).show()
#    cv2.imshow("image", newimg)
#    cv2.waitKey(0)
    return totalkp, noofkpmatched
    
if __name__ == "__main__":
    imname1='barca.jpg'
    imname2='boot.jpg'
    
    imname1='ETC\\ModHausdorffDist\\nf\\1.png'
#    imname2='ETC\\ModHausdorffDist\\sift2.png'
    imname2='ETC\\ModHausdorffDist\\nf\\2.png'
#    imname2='boot.jpg'
    for i in range(1, 6):
        for j in range(1, 6):
            imname1='ETC\\ModHausdorffDist\\'+str(i)+'.png'
            imname1='ETC\\ModHausdorffDist\\'+str(j)+'.png'
            
            total, noofmatches=match(imname1, imname2)
            print i, j, ':', total, noofmatches
    print time.time() - start_time, "seconds"
