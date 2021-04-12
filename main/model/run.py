import numpy as np

from main.model.functions import *
from main.plots import plot_signals

if __name__ == '__main__':
    # Détection
    VL = detection_b_const(time, -1/4, 100)
    VL_list = []
    VL_list.append(VL[0])
    plot_signals(time, VL_list, ['$V_L$'], x_label="Temps [s]", y_label="Tension [mV]")

    # Amplificateur
    VL = VL[0] / 1000
    VAMP = amplification(time, VL)
    plot_signals(time, VAMP, ['$V_{amp}$', '$V_L$'], x_label="Temps [ms]", y_label="Tension [V]")

    # Filter
    VF = filter(np.linspace(0, 0.1, steps), 2.5, np.linspace(10, 200, steps), resolution='sinus')
    plot_signals(np.linspace(0, 0.1, steps), VF, ['$V_F$', '$V_{amp}$'], x_label="Temps [ms]", y_label="Tension [V]")

    # Comparator
    sin = lambda t: 2 * np.sin(10 * t) + 2
    VCOMP = comparator(time, sin(time))
    plot_signals(time, VCOMP, ['$V_{comp}$', '$V_{F}$', "$V_{ref}$"], x_label="Temps [ms]", y_label="Tension [V]")

    # Interrupter
    VCOMP_out = VCOMP[0]
    VSWITCH = interrupter(time, VCOMP_out)[:3]
    ISWITCH = interrupter(time, VCOMP_out)[2:]
    plot_signals(time, VSWITCH, ['$V_{B}$', '$V_{C}$', "$V_{comp}$"], x_label="Temps [ms]", y_label="Tension [V]")
    plot_signals(time, ISWITCH, ['$I_{B}$', '$I_{C}$', "$V_{comp}$"], x_label="Temps [ms]", y_label="Tension [A]")

