#!/usr/bin/python

import sys

Pmin=10
Pmax=999


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


def gen_lines(x=0.,y=0., dy=0.2 , dy_group=0.5, over_scan=10, distance= 5, lines_per_speed=3, lines=[0.50,0.30,0.10], speeds = [8000,4000,2000,1000,500,250]):
    print 'M3'
    G1(x,y,S=0)
    for s in speeds:
        print >> sys.stderr, 'line speed:',s,'power:', P_speed(s)
        G1(F=s)
        for i in range(lines_per_speed):
            x+=over_scan-lines[0]/2
            X(x)
            for l in range(len(lines)):
                x+=lines[l]
                XS(x,P_speed(s))
                if l<len(lines)-1: 
                    x+=distance-(lines[l]+lines[l+1])/2.
                    XS(x,0)
            x+=over_scan-lines[-1]/2
            XS(x,0)
            y+=dy
            Y(y)
            x-=over_scan-lines[-1]/2
            X(x)
            for l in range(len(lines)-1,-1,-1):
                x-=lines[l]
                XS(x,P_speed(s))
                if l>0: 
                    x-=distance-(lines[l]+lines[l-1])/2.
                    XS(x,0)
            x-=over_scan-lines[0]/2
            XS(x,0)
            if i<lines_per_speed-1:
                y+=dy
                Y(y)

        y+=dy_group
        Y(y)
    print 'M5'

def gen_ruler(x=0.,y=0.,length=20, heigth=2, speed=500, dir=1):
    print >> sys.stderr, 'ruler speed:',speed,'power:', P_speed(speed), 'dir:',dir
    x-=(dir-1)/2*length
    for l in range(length+1):
        G0(x,y+heigth)
        print 'M3'
        h = heigth/2
        if l%10 == 0: h=0
        G1(x,y+h,S=P_speed(speed),F=speed)
        print 'M5'
        x+=dir

print 'G28'
print 'G1 F5000'
gen_lines(y=4.5)
gen_ruler(y=2,x=5)
gen_ruler(x=5,dir=-1)
print 'G0 X0Y0'
