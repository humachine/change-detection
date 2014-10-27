from PIL import Image, ImageDraw
import time
from scipy import ndimage
from mylib import pickleload, picklethis, show
start_time = time.time()
import sys
import math, random
from itertools import product, chain
from ufarray import *
import numpy as np
from scipy.misc import imread, imsave, imshow

def bwlabel(img):
    data = img.load()
    width, height = img.size
 
    # Union find data structure
    uf = UFarray()
  
    #
    # First pass
    #
 
    # Dictionary of point:label pairs
    labels = {}
 
    for y, x in product(range(height), range(width)):
 
        #
        # Pixel names were chosen as shown:
        #
        #   -------------
        #   | a | b | c |
        #   -------------
        #   | d | e |   |
        #   -------------
        #   |   |   |   |
        #   -------------
        #
        # The current pixel is e
        # a, b, c, and d are its neighbors of interest
        #
        # 255 is white, 0 is black
        # White pixels part of the background, so they are ignored
        # If a pixel lies outside the bounds of the image, it default to white
        #
 
        # If the current pixel is white, it's obviously not a component...
        if data[x, y] == 255:
            pass
 
        # If pixel b is in the image and black:
        #    a, d, and c are its neighbors, so they are all part of the same component
        #    Therefore, there is no reason to check their labels
        #    so simply assign b's label to e
        elif y > 0 and data[x, y-1] == 0:
            labels[x, y] = labels[(x, y-1)]
 
        # If pixel c is in the image and black:
        #    b is its neighbor, but a and d are not
        #    Therefore, we must check a and d's labels
        elif x+1 < width and y > 0 and data[x+1, y-1] == 0:
 
            c = labels[(x+1, y-1)]
            labels[x, y] = c
 
            # If pixel a is in the image and black:
            #    Then a and c are connected through e
            #    Therefore, we must union their sets
            if x > 0 and data[x-1, y-1] == 0:
                a = labels[(x-1, y-1)]
                uf.union(c, a)
 
            # If pixel d is in the image and black:
            #    Then d and c are connected through e
            #    Therefore we must union their sets
            elif x > 0 and data[x-1, y] == 0:
                d = labels[(x-1, y)]
                uf.union(c, d)
 
        # If pixel a is in the image and black:
        #    We already know b and c are white
        #    d is a's neighbor, so they already have the same label
        #    So simply assign a's label to e
        elif x > 0 and y > 0 and data[x-1, y-1] == 0:
            labels[x, y] = labels[(x-1, y-1)]

        # If pixel d is in the image and black
        #    We already know a, b, and c are white
        #    so simpy assign d's label to e
        elif x > 0 and data[x-1, y] == 0:
            labels[x, y] = labels[(x-1, y)]
 
        # All the neighboring pixels are white,
        # Therefore the current pixel is a new component
        else: 
            labels[x, y] = uf.makeLabel()
 
    #
    # Second pass
    #
 
    uf.flatten()
    
 
    colors = {}

    # Image to display the components in a nice, colorful way
    output_img = Image.new("RGB", (width, height))
    outdata = output_img.load()

    count=0
    for (x, y) in labels:
 
        # Name of the component the current point belongs to
        component = uf.find(labels[(x, y)])

        # Update the labels with correct information
        labels[(x, y)] = component
 
        # Associate a random color with this component 
        if component not in colors: 
            colors[component] = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
            count=count+1

        # Colorize the image
        outdata[x, y] = colors[component]

#Creating a 2D numpy array(of size width*height)
#Checks if there are more 1s than 0s and vice versa. It creates an array filled with zeros/ones appropriately
    if((len(labels)*2) > width*height):
        ccarr = np.ones((width, height))
    else:
        ccarr = np.zeros((width, height))
#    ccarr=0

#The labeling that is done above has a disjoint sequence of integers
#Eg: Components with labels 1, 2, 5 may exist. But there may be no components with labels 3 or 4.
#This is because in the second pass, components are combined and hence certain labels are lost

#Suppose there are 'N' components with labels c1, c2, ...,cN (where c1..cN is an arbitrary sequence of integers)
#Labelswap associates the above sequence {c1...cN} to {1....N}
#Also ccarr is now an array such that
#       ccarr[i,j]=0                            , if the pixel was originally zero.
#       ccarr[i,j]=some label between 1 & N     , if the pixel was originally part of a component

    labelswap = {}
    labelcount=1
    ccdict = {}
    for i in range(1, count+1):
        ccdict[i]=[]
##    print ccdict
    for i in labels.keys():
        lab = int(labels[i])
        (a,b)=i
            
        if lab in labelswap:
            ccarr[a,b]=labelswap[lab]
            tmp=labelswap[lab]
            
            ccdict[tmp].append((a,b))
            
##            ccdict[labelswap[lab]].append((a,b))
            
            

        else:
            labelswap[lab]=labelcount
            labelcount+=1
            ccarr[a,b]=labelswap[lab]
            ccdict[labelswap[lab]].append((a,b))
    
#ccarr is returned instead of labels
    return (ccdict, ccarr, count, output_img)


def fslow(imname):
    img = Image.open(imname)
    img = img.convert('1')

    (ccdict1, ccarr, count, output_img) = bwlabel(img)
    actuallen= [len(ccdict1[i]) for i in xrange(1, count+1)]
#    print sum(actuallen)
    return count
#    return ccdict1, ccarr, count, output_img, actuallen
    
def ffast(imname):
    a=np.asarray(imread(imname), dtype=bool)
    b, num = ndimage.label(a, np.ones((3,3)))
    b=b.astype(int)
#    print num
    b2=Image.fromarray(b)

    width, height = b2.size
    data=b2.load()
    
    ccdict={}
    for i in xrange(1, num+1):
        ccdict[i]=[]
    xxx=np.where(b>0)        
    for i in xrange(len(xxx[0])):
        y, x=int(xxx[0][i]), int(xxx[1][i])
        if data[x,y]>0:
            ccdict[data[x,y]].append((y,x))
    complen = [len(ccdict[i]) for i in xrange(1, num+1)]
#    print sum(complen)
    return num
#    return num, ccdict, complen
    

#def main():
if __name__ == "__main__":
    fname='8_a'
    fname='6_a'
    fname='26_a'
    fname=flist[20]
    flist=pickleload('Outputs\\fnamelist')
#[0, 2, 3, 30, 33, 34, 35, 39, 41, 42, 84]

    answer=[]
    imname='images_consolidated\\'+fname+'.png'
    cnt=0
    
#    for i in flist:
#        imname='images_consolidated\\'+i+'.png'
#        print i, round(((41-cnt)*100/42), 2)
#        starttime=time.time()
#        count1=fslow(imname)
#        t1=time.time() - starttime
#        
#        starttime=time.time()
#        count2=ffast(imname)
#        t2=time.time() - starttime
#        answer.append([t1, t2, count1, count2, i])
#        
#        j=i[:-1]+'b'
#        imname='images_consolidated\\'+j+'.png'
#        print j
#        starttime=time.time()
#        count1=fslow(imname)
#        t1=time.time() - starttime
#        
#        starttime=time.time()
#        count2=ffast(imname)
#        t2=time.time() - starttime
#        answer.append([t1, t2, count1, count2, j])
#        
#        cnt+=1
#    picklethis(answer, 'speedcomp.pkl')
#
    img = Image.open(imname)
    img = img.convert('1')

    (ccdict1, ccarr, count, output_img) = bwlabel(img)
    actuallen= [len(ccdict1[i]) for i in xrange(1, count+1)]
#    print sum(actuallen)
#    return ccdict1, ccarr, count, output_img, actuallen



    a=np.asarray(imread(imname), dtype=bool)
    original=a.copy()
    b, num = ndimage.label(a, np.ones((3,3)))
    b=b.astype(int)
    barr=b.copy()
#    print num
    b2=Image.fromarray(b)

    width, height = b2.size
    data=b2.load()
    
    ccdict={}
    for i in xrange(1, num+1):
        ccdict[i]=[]
    xxx=np.where(b>0)        
    for i in xrange(len(xxx[0])):
        y, x=int(xxx[0][i]), int(xxx[1][i])
        if data[x,y]>0:
            ccdict[data[x,y]].append((y,x))
    complen = [len(ccdict[i]) for i in xrange(1, num+1)]

    lis1=[]
    lis2=[]
    for i in range(1, num+1):
        t1, t2=ccdict[i][0]
        temp=int(ccarr[t2, t1])
        
        if len(ccdict[i]) != len(ccdict1[temp]):
            print i, temp
            lis1.append(i)
            lis2.append(temp)

    new1=np.zeros(original.shape)
    new2=np.zeros(original.shape, dtype=bool)
#    2622, 5534 50 50
    cnt=1
    length=len(lis1)
    for j in lis1:
        new=np.zeros(original.shape)
        for i in ccdict[j]:
            a, b=i
#            new[a,b]=255/cnt
            new[a,b]=255
        show(new)
        new1=np.add(new1, new)
        cnt+=1
        
    for j in lis2:
        for i in ccdict1[j]:
            a, b=i
            new2[b,a]=True




