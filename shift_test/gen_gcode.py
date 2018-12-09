#!/usr/bin/python

import sys

Pmin=10
Pmax=299


def P_speed(s):
    p = s*Pmax/5000.
    if p > Pmax: p = Pmax
    if p < Pmin: p = Pmin
    return int(p)

def strf(f):  return "%.2f" % f

def G(C=None,X=None,Y=None,F=None,S=None):
    s = ''
    if C is not None: s+= 'G'+str(C)
    if X is not None: s+=' X'+strf(X)
    if Y is not None: s+=' Y'+strf(Y)
    if F is not None: s+=' F'+str(F)
    if S is not None: s+=' S'+str(S)
    print s.strip()

def G1(X=None,Y=None,F=None,S=None): G(1,X,Y,F,S)
def G0(X=None,Y=None,F=None,S=None): G(0,X,Y,F,S)
def X(x): G(X=x)
def Y(y): G(Y=y)
def XS(x,s): G(X=x,S=s)


def gen_line(x=0.,y=0., dy=0.2, over_scan=10, length=0.50, speed=2000, lines = 10):
    print 'M3'
    G1(x,y,S=0)
    G1(F=speed)
    for i in range(lines):
        d=i*0.004
        X( x+over_scan-length/2+d)
        XS(x+over_scan+length/2+d, P_speed(speed))
        XS(x+over_scan*2+d, 0)
        y+=dy
        Y(y)
        X( x+over_scan+length/2-d)
        XS(x+over_scan-length/2-d, P_speed(speed))
        XS(x-d,0)
        y+=dy
        Y(y)
    print 'M5'

print 'G28'
print 'G1 F5000'
#gen_line(y=0.0,dy=0.1)
#gen_line(y=0.0)
#gen_line(y=0.0,speed=5000)
gen_line(y=0.0,dy=0.1,lines=20,speed=5000)
#gen_line(y=0.0,dy=0.08,lines=25,speed=5000)
print 'G0 X0Y0'
