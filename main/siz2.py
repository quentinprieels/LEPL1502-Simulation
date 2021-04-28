#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 12:52:36 2021

@author: quentin
"""

# === Components ===
# Bobine
N = 100  # Number of turns of the wire [#]
B_cst_val = 1.5  # Value en B near the magnet [mT]
r_int = 2.5  # [ohms]
v_l = 0.3  # [V]
# Pendule 250 mV


# AmplificationS
r_amp = 5600  # [ohms]
g = 10  # [#]

# Filter
r_f = 1200  # [ohms]
c_f = 0.000001  # [F]

# Comparator
r_c = 560  # [ohms]

# Interrupter
v_d = v_zk = 3.3  # [V]
beta = 375  # [#]
current = 0.3  # [A]

# Circuit
v_cc = 5  # [V]
v_ss = 0  # [V]


# === Optimisation functions ===
def find_prb():
    r_b = 4.3 * beta/current
    v_c = current * r_int
    return r_b, v_c


def find_pramp():
    p_r_amp = (g - 1) * r_amp
    return p_r_amp


def find_prref():
    lower_bound = 0
    upper_bound = v_l * g * 100000 / v_d
    vref_lower = 0
    vref_upper = v_d * upper_bound / 100000
    return lower_bound, upper_bound, vref_lower, vref_upper


# === Main program ===
if __name__ == '__main__':
    print('==== Dimensionnement - GR.71 ==== (les valeurs des potentiomètres sont arrondies à 2 centièmes près.)')

    print('\033[93m Sum of Rb : {:,.2f} ohms \033[0m'.format(find_prb()[0]))
    print('\t - Ic current : {:.2f} [mA]'.format(current))
    print('\t - Vc tension : {:.2f} [mV]'.format(find_prb()[1] * 1000))
    if current > 0.75:
        print('\t - \033[91mAttention, risque de surchauffe du transistor. \033[0m')
    if find_prb()[0] > 50000 or 0 > find_prb()[0]:
        print('\t - \033[91mAttention, cette valeur est impossible à obtenir. \033[0m')
    print()

    print('\033[93mpRamp : {:,.2f} ohms \033[0m'.format(find_pramp()))
    print('\t - Gain : {:.2%}'.format(g))
    print('\t - v_f tension (v_l)  : {:,.2f} [V]'.format(v_l * g))
    if find_pramp() > 100000:
        print('\t - \033[91mAttention, cette valeur est impossible à obtenir. \033[0m')
    if v_l * g > v_cc:
        print('\t - \033[91mAttention, pour cette valeur, l\'ampli-op va saturer. \033[0m')
    print()

    print('\033[93m{:,.2f} ohms < pRref < {:,.2f} ohms \033[0m'.format(find_prref()[0], find_prref()[1]))
    print('\t - Vref tension : {:.2f} [V] < Vref < {:.2f} [V]'.format(find_prref()[2], find_prref()[3]))
    print('\t - À positionner le plus bas possible.')
    if find_prref()[0] > 100000:
        print('\t - \033[91mAttention, la borne inférieur est impossible. \033[0m')
    if find_prref()[1] > 100000:
        print('\t - \033[91mAttention, la borne supérieur est impossible. \033[0m')