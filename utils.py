#!/usr/bin/python

import bitarray
from bisect import *



def filter_signal(sig,size):
    def filt2(sig,value, size):
        v = bitarray.bitarray([value]+[not value]*size+[value])
        l=sig.search(v)
        print 'spikes of size:', size, 'found:',l
        for i in l:
            for j in range(size):
                sig[i+j+1]=value
    if size<=0: return
    filter_signal(sig, size-1)
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



def signal_integral(signal):
    s = 0
    out_integral = []
    for v in signal:
        if v: s+=1
        out_integral.append(s)
    return out_integral


