#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:08:31 2021

@author: quentin
"""
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button

omega = 2 * pi * 10
vl = lambda t : 0.3 * sin(omega * t)

def vc(vl, borne=0.05):
    vc = zeros(len(vl))
    for i in range(len(vl)):    
        if vl[i] < 0.1:
            vc[i] = 0.0
        else:
            vc[i] = 2.5 * 0.06
    return vc
        
def result(vl, vc):
    return vl + vc 

t = linspace(-0.1, 0.1, 1000)
VL = vl(t)
VC = vc(VL)
RESULT = result(VL, VC)

fig, ax = plt.subplots('Tensions de boucles')
plt.plot(t, RESULT, label='Résult')
plt.plot(t, VL, '--', label='$V_L$')
plt.plot(t, VC, label='$V_{int}$')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
plt.show()    
        