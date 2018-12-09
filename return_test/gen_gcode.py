#!/usr/bin/python

import sys

Pmin=50
Pmax=999

swap_xy=True
swap_xy=False


XX=' X'
YY=' Y'
if swap_xy:
    XX=' Y'
    YY=' X'


def P_speed(s):
    p = s*Pmax/5000.
    if p > Pmax: p = Pmax
    if p < Pmin: p = Pmin
    return int(p)

def strf(f):  return "%.2f" % f

def G(C=None,X=None,Y=None,F=None,S=None):
    s = ''
    if C is not None: s+= 'G'+str(C)
    if X is not None: s+= XX +strf(X)
    if Y is not None: s+= YY +strf(Y)
    if F is not None: s+=' F'+str(F)
    if S is not None: s+=' S'+str(S)
    print s.strip()

def G1(X=None,Y=None,F=None,S=None): G(1,X,Y,F,S)
def G0(X=None,Y=None,F=None,S=None): G(0,X,Y,F,S)
def X(x): G(X=x)
def Y(y): G(Y=y)
def XS(x,s): G(X=x,S=s)



def gen_ruler(x=0.,y=0.,length=4, dist=[], heigth=1, speed=500, dir=1):
    print >> sys.stderr, 'ruler speed:',speed,'power:', P_speed(speed), 'dir:',dir
    x-=(dir-1)/2*sum(dist)
    if dir < 0: dist = list(reversed(dist))
    dist = dist+[0]
    for d in dist:
        G0(x,y+heigth)
        print 'M3'
        G1(x,y,S=P_speed(speed),F=speed)
        print 'M5'
        x+=dir*d
    x+=dir*5
    G0(x,y)

print 'G28'
print 'G1 F5000'
d = [1.1,1.15,1.17]
gen_ruler(y=1,x=5.83,dist=d)
gen_ruler(x=5.83,dir=-1, dist=d)
print 'G0 X0Y0'
