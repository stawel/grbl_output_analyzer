#!/usr/bin/python

import sys

Pmax = 400
speed = 2000
lines = 20

P0 = 400


def strf(f):  return "%.2f" % f
def stri(i):  return "%03d" % i

def G(C=None,X=None,Y=None,F=None,S=None):
    s = ''
    if C is not None: s+= 'G'+str(C)
    if X is not None: s+=' X'+strf(X)
    if Y is not None: s+=' Y'+strf(Y)
    if F is not None: s+=' F'+str(F)
    if S is not None: s+=' S'+stri(S)
    print s.strip()

def G1(X=None,Y=None,F=None,S=None): G(1,X,Y,F,S)
def G0(X=None,Y=None,F=None,S=None): G(0,X,Y,F,S)
def X(x): G(X=x)
def Y(y): G(Y=y)
def XS(x,s): G(X=x,S=s)


def gen_line(x=0.,y=0., dy=0.4, over_scan=10, length=5.0, speed=2000, lines = 40):
    print 'M3'
    G1(x,y,S=0)
    G1(F=speed)

    for i in range(lines):
        p1=i*Pmax/lines
        if p1 == 0: p1 = P0
        X( x+over_scan-length/2)
        XS(x+over_scan+length/2, p1)
        XS(x+over_scan*2, 0)
        y+=dy
        Y(y)
        X( x+over_scan+length/2)
        XS(x+over_scan-length/2, p1)
        XS(x,0)
        y+=dy
        Y(y)
    print 'M5'

print 'G28'
print 'G1 F5000'
gen_line(speed=speed, lines=lines)
print 'G0 X0Y0'
