#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:08:31 2021

@author: quentin
"""
# Imports
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button

# Definition de Vl
omega = 2 * pi * 10
vl = lambda t : 0.3 * sin(omega * t)

# =========================================================================
#   1.1 Avec des simplifications
def vc(vl, borne=0.05):
    vc = zeros(len(vl))
    for i in range(len(vl)):    
        if vl[i] < 0.16:
            vc[i] = 0.0
        else:
            vc[i] = 2.5 * 0.06
    return vc

        
def result(vl, vc):
    return vl + vc 

#   1.2 Appel des functions
t = linspace(-0.1, 0.1, 1000)
VL = vl(t)
VC = vc(VL)
RESULT = result(VL, VC)

#   1.3 Plot simple
fig, ax = plt.subplots()
plt.plot(t, RESULT, label='Résult')
plt.plot(t, VL, '--', label='$V_L$')
plt.plot(t, VC, label='$V_{int}$')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

# =========================================================================
#   2. Sans simplifications
a = 0
vrefNotG = 0.2
def funct(vl, ic=0.06, rint=2.5):
    # Préallocation
    m = len(vl)
    vint = zeros(m)
    vsum = vl.copy()
    # Boucle
    for i in range(1, m):
        if vsum[i-1] > vrefNotG:
            vint[i] = ic * rint
            vsum[i] += vint[i]
            a = i
    # Return
    return vint, vsum, a

#   2.2 Appel des fonctions
VINT, VSUM, a = funct(VL)

#   2.3 Plot sans simplifications
fig, ax = plt.subplots()
plt.plot(t, VL, color='tomato', label='$V_L$')
plt.plot(t, VINT, color='gold', label='$V_{int}$')
plt.axvline(x = t[a], color='violet', label='Switch', ls='--')
plt.axhline(y = vrefNotG, color='yellowgreen' , label='$V_{ref}$', ls='--')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
plt.plot(t, VSUM, color='navy', label='Résult')
plt.legend()

plt.show()
