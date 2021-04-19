# import numpy as np

# === Components ===
# Bobine
N = 100  # Number of turns of the wire [#]
B_cst_val = 1.5  # Value en B near the magnet [mT]
r_int = 4  # [ohms]
v_l = 0.25  # [V]
margin = 0.8  # [#]

# Amplification
r_amp = 5600  # [ohms]
g = 10  # [#]

# Filter
r_f = 1200  # [ohms]
c_f = 0.000001  # [F]

# Comparator
r_c = 560  # [ohms]

# Interrupter
r_b = 10000  # [ohms]
v_d = v_zk = 3.3  # [V]
beta = 375  # [#]

# Circuit
v_cc = 5  # [V]
v_ss = 0  # [V]


# === Optimisation functions ===
def find_prb():
    p_r_b = (4.3 * beta * r_int) / (margin * v_l) - r_b
    v_c = margin * v_l
    i_c = v_c / r_int
    return p_r_b, v_c, i_c


def find_pramp():
    p_r_amp = (g - 1) * r_amp
    return p_r_amp


def find_prref():
    lower_bound = find_prb()[1] * g * 100000 / v_d
    upper_bound = v_l * g * 100000 / v_d
    vref_lower = v_d * lower_bound / 100000
    vref_upper = v_d * upper_bound / 100000
    return lower_bound, upper_bound, vref_lower, vref_upper


# === Main program ===
if __name__ == '__main__':
    print('==== Dimensionnement - GR.71 ==== (les valeurs des potentiomètres sont arrondies à l\'unité)')

    print('\033[93mpRb : {:,.0f} ohms \033[0m'.format(find_prb()[0]))
    print('\t - Marge : {:.2%}'.format(1 - margin))
    print('\t - Ic current : {:.3f} [A]'.format(find_prb()[2]))
    print('\t - Vc tension : {:.3f} [V]'.format(find_prb()[1]))
    print('\t - Vl tension : {:.3f} [V]'.format(v_l))
    if find_prb()[2] > 0.75:
        print('\t - \033[91mAttention, risque de surchauffe du transistor. \033[0m')
    if find_prb()[0] > 50000 or 0 > find_prb()[0]:
        print('\t - \033[91mAttention, cette valeur est impossible à obtenir. \033[0m')
    print()

    print('\033[93mpRamp : {:,.0f} ohms \033[0m'.format(find_pramp()))
    print('\t - Gain : {:.2%}'.format(g))
    print('\t - v_f tension (v_l)  : {:,.2f} [V]'.format(v_l * g))
    print('\t - v_f tension (v_c)  : {:,.2f} [V]'.format(margin * v_l * g))
    print('\t - Somme des tensions : {:,.2f} [V]'.format((margin * v_l + v_l) * g))
    if find_pramp() > 100000:
        print('\t - \033[91mAttention, cette valeur est impossible à obtenir. \033[0m')
    if (v_l + find_prb()[1]) * g > v_cc:
        print('\t - \033[91mAttention, a cette valeur, l\'ampli-op va saturer. \033[0m')
    print()

    print('\033[93m{:,.0f} ohms < pRref < {:,.0f} ohms \033[0m'.format(find_prref()[0], find_prref()[1]))
    print('\t - Vref tension : {:.2f} [V] < Vref < {:.2f} [V]'.format(find_prref()[2], find_prref()[3]))
    print('\t - À positionner le plus bas possible.')
    if find_prref()[0] > 100000:
        print('\t - \033[91mAttention, la borne inférieur est impossible. \033[0m')
    if find_prref()[1] > 100000:
        print('\t - \033[91mAttention, la borne supérieur est impossible. \033[0m')
