from PIL import Image, ImageDraw
import time
start_time = time.time()
import sys
import math, random
from itertools import product, chain
from ufarray import *
import numpy as np

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
    mmax=8
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
##            ccdict[labelswap[lab]].append((a,b))
    
#ccarr is returned instead of labels
    return (ccdict, ccarr, count, output_img)
import json

def main():
    img = Image.open('images_consolidated\\8_a.png')

    # Threshold the image, this implementation is designed to process b+w
    # images only
    #img = img.point(lambda p: p > 190 and 255)
    img = img.convert('1')

    (ccdict, ccarr, count, output_img) = bwlabel(img1)
    output_img.show()
    print count


## -----------------------------------------------------------------------------------------------------------------------------------------
        

    
if __name__ == "__main__":
    main()
    print time.time() - start_time, "seconds"
