#!/usr/bin/python

import sys
import bitarray
from bisect import *

file_name = "out.bin"
if len(sys.argv)>1: file_name = sys.argv[1]

#read binary file
b = bitarray.bitarray()
with open(file_name, 'rb') as fh:
    b.fromfile(fh)

#extract signal from bytestream (edit if necessary)
_,_,_,out,Y_step,Y_dir,X_step,X_dir = [ b[i::8] for i in range(8)]


def filter_sig(sig,size):
    def filt2(sig,value, size):
        v = bitarray.bitarray([value]+[not value]*size+[value])
        l=sig.search(v)
        print 'spikes of', size, 'found:',l
        for i in l:
            for j in range(size):
                sig[i+j+1]=value
    if size<=0: return
    filter_sig(sig, size-1)
    filt2(sig, True, size)
    filt2(sig, False, size)


def find_pulses(signal, tag):
    w=[]
    i=0
    try:
        while i < len(signal):
            x = i = signal.index(True,i)
            y = i = signal.index(False,i)
            w.append((x,tag,y-x))
    except:
        pass
    return w

#filter signals (remove spikes of size 2)
print 'filter signals:'
for s in [out,Y_step,Y_dir,X_step,X_dir]:
    filter_sig(s, 2)


xp = find_pulses(X_step, 'x')
yp = find_pulses(Y_step, 'y')
sp = find_pulses(out   , 's')

p = sorted(xp + yp + sp)

def draw(points, x_off=0,y_off=0, sdist=0, img = None):
    x,y,s,sd,xmin,xmax,ymin,ymax,smax=x_off,y_off,0,0,100000,0,100000,0,0
    for i,tag,d in points:
        if tag == 'x':
            if not X_dir[i]: x+=1
            else: x-=1
        if tag == 'y':
            if Y_dir[i]: y+=1
            else: y-=1
        if tag == 's':
            s = d
            sd = i
        if i-sd > sdist:
            s = 0

        if img is not None:
            v = s*255/sdist
            b = 0
            if X_dir[i]: b = 30
            img[x,y] = (v,v,b)

        xmin,xmax = min(xmin, x), max(xmax, x)
        ymin,ymax = min(ymin, y), max(ymax, y)
        smax = max(s, smax)
    return xmin,xmax,ymin,ymax,smax

xmin,xmax,ymin,ymax,smax = draw(p)
print 'xm:',xmin,xmax
print 'ym:',ymin,ymax
print 'sm:',smax


###### display 
from PIL import Image

img = Image.new( 'RGB', (xmax-xmin+1,ymax-ymin+1), (10,10,0)) # create a new black image
pixels = img.load() # create the pixel map
draw(p, -xmin,-ymin, smax, pixels)

img.show()
