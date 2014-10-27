#!/usr/bin/env python
"""
An animated image
"""
import sys
#sys.path.append("ffmpeg\ffmpeg-20140426-git-b217dc9-win32-static\bin")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image	
import cv2
from mylib import pickleload, picklethis
import numpy as np
from scipy.misc import imread, imsave, imshow, toimage
from scipy import ndimage
import time
import matplotlib
def show(x):
    toimage(x).show()

fig = plt.figure()
plt.rcParams['animation.ffmpeg_path'] = 'F:\\DDP\\ffmpeg\\ffmpeg-20140426-git-b217dc9-win32-static\\bin\\ffmpeg'
def f(x, y):
    return np.sin(x) + np.cos(y)

x = np.linspace(0, 2 * np.pi, 120)
y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)
# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame
aaa=np.asarray(imread('8_a.png'),dtype=bool)

#show(data)

#hoo=Image.open('horse.png')
#a=plt.imshow(hoo)

ims = []
for i in range(60):
    x += np.pi / 15.
    y += np.pi / 20.
    im = plt.imshow(f(x, y))
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=10, blit=True,
    repeat_delay=1000)
plt.show()
#ani.save('dynamic_images.mp4')

mywriter = animation.FFMpegWriter()
#ani.save('im.mp4', metadata={'artist':'Guido'}, writer=mywriter)
ani.save('mymovie.mp4',writer=mywriter)

