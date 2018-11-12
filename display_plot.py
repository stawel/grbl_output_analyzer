#!/usr/bin/python

import sys
import os
import bitarray
import argparse
from bisect import *
import utils

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--pwm_cycle",        help="PWM cycle in samples, default 1024: 1MHz, 1ms cycle", type=int, default=1024)
parser.add_argument("-f", "--filter",           help="filter spikes of size, default 1", type=int, default=1)
parser.add_argument("-s", "--pwm_simple",       help="simple PWM value calculation (faster), default off", action="store_true")
parser.add_argument("-x", "--draw_x_speed",     help="draw x speed, default on", type=utils.str2bool, nargs='?', default='on')
parser.add_argument("-y", "--draw_y_speed",     help="draw y speed, default on", type=utils.str2bool, nargs='?', default='on')
parser.add_argument("-p", "--draw_pwm",         help="draw pwm, default on", type=utils.str2bool, nargs='?', default='on')
parser.add_argument("-o", "--output",           help='output filename, default "out.png"', default='')
parser.add_argument("-m", "--steps_mm",         help='steps per mm for X and Y axis, default 80', type=float, default=80.)
parser.add_argument("-w", "--sample_frequency", help='sample frequency, default 1000000 (1MHz)', type=float, default=1000000.)
parser.add_argument('filename',                 help='filename, default "out.bin"',nargs='?', default="out.bin")
args = parser.parse_args()


#read binary file
b = bitarray.bitarray()
with open(args.filename, 'rb') as fh:
    b.fromfile(fh)

#extract signal from bytestream (edit if necessary)
_,_,_,out,Y_step,Y_dir,X_step,X_dir = [ b[i::8] for i in range(8)]
#_,_,_,out,Y_dir,Y_step,X_step,X_dir = [ b[i::8] for i in range(8)]


#filter signals (remove spikes of size 2)
print 'filter signals:'
for s in [out, Y_step,Y_dir,X_step,X_dir]:
    utils.filter_signal(s, args.filter)

xp = utils.find_pulses(X_step, 'x')
yp = utils.find_pulses(Y_step, 'y')
p = xp + yp

if args.draw_pwm:
    if args.pwm_simple:
        p += utils.find_pulses(out, 's')
    else:
        print 'calculate PWM output integral'
        out_integral = utils.signal_integral(out)
        print 'integral calculation done'

p = sorted(p)

def draw(points, scycle):
    x,y,s,si=0,0,0,0
    xspeed, yspeed = 0.,0.
    step = 1./args.steps_mm                     # [mm]
    speed = step*args.sample_frequency*60       # [mm/min]
    out = []
    for i, tag, d1, d0 in points:
        if tag == 'x':
            if not X_dir[i]:    cdir = 1
            else:               cdir = -1
            if X_dir[i] != X_dir[i+d1+d0]:      xspeed = 0.
            else:                               xspeed = speed/(d0+d1)
            x += step * cdir
        if tag == 'y':
            if not Y_dir[i]: cdir = 1
            else:            cdir = -1
            if Y_dir[i] != Y_dir[i+d1+d0]:      yspeed = 0.
            else:                               yspeed = speed/(d0+d1)
            y += step * cdir
        if tag == 's':
            s = d1
            si = i
        if i-si > scycle:
            si += scycle
            s -= scycle
        if s < 0: s = 0

        if not args.pwm_simple and args.draw_pwm and i+scycle < len(out_integral): v = out_integral[i+scycle] - out_integral[i]
        else: v = s
        if v > scycle: v = scycle
        v = v*255/scycle

        out.append( (x,y,v,xspeed,yspeed) )
    return out



out = draw(p, args.pwm_cycle)
print 'out len:', len(out)
s=[0,1]
if args.draw_pwm:       s += [2]
if args.draw_x_speed:   s += [3]
if args.draw_y_speed:   s += [4]
out = utils.simplify_line(out,s, 0.0001)
print 'simplified out len:', len(out)


###### display 
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')


x,y,z,xspeed,yspeed = zip(*out)
#theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
#z = np.linspace(-2, 2, 100)
#r = z**2 + 1
#x = r * np.sin(theta)
#y = r * np.cos(theta)
if args.draw_pwm:
    ax.plot(x, y, z,        color='red',   label='PWM')

if args.draw_x_speed:
    ax.plot(x, y, xspeed,   color='blue',  label='x speed [mm/min]')

if args.draw_y_speed:
    ax.plot(x, y, yspeed,   color='green', label='y speed [mm/min]')

ax.legend()
plt.show()
