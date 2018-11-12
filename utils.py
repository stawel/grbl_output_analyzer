#!/usr/bin/python

import bitarray
from bisect import *


# signals

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
            z     = signal.index(True,i)
            w.append((x,tag,y-x, z-x))
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


# lines

def simplify_line(line, pos, eps):
    last = line[0]
    r = [last]
    for i in range(1,len(line)-1):
        curr = line[i]
        next = line[i+1]
        ok = True
        t,d = 0, 0
        for k in pos:
            if abs(next[k] - last[k]) > eps:
                t = (curr[k] - last[k])*1./(next[k] - last[k])

        for k in pos:
            d = abs((curr[k] - last[k]) - t*(next[k] - last[k]))
            if d > eps:
                ok = False
                break

        if not ok:
#            print t,d
            r.append(curr)
            last = curr

    r.append(line[-1])
    return r

# others

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1', 'on'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0','off'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
