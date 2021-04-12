# ==== Import ====
import numpy as np

from main.circuit.old.circuit import Signal

# ==== Analytic solution ====


# ==== Electrical components and essentially information's ====
begin = -0.1
end = 0.1
steps = 200
time = np.linspace(begin, end, steps)

pR_ref_val = [0, 100000]
pR_ref = np.linspace(pR_ref_val[0], pR_ref_val[1], steps)

V_D = V_zk = 3.3  # Tension [V]
V_cc = 5  # [V]
V_ss = 0  # [V]

a = 2  # Amplitude [#]
f = 30
omega = 2 * np.pi * f  # Angular velocity

# ==== Functions =====
# 1. Entering functions
vl = lambda t: a * np.sin(omega * t) + a


# ==== Functions ====
v_ref = pR_ref * (V_zk / pR_ref_val[1])


def V_comp(t):
    def comp(ve):
        if ve < 0:
            return V_cc
        else:
            return V_ss

    ret = np.zeros(len(t))
    for i in range(len(t)):
        v_e = v_ref[i] - vl(t)[i]
        ret[i] = comp(v_e)

    return ret


# ==== Main program ====
if __name__ == '__main__':
    V_L = Signal("$V_L$", ['s', 'V'], time, f=vl)
    V_COMP = Signal("$V_{comp}$", ['s', 'V'], time, f=V_comp)
    VREF = Signal("$VR_{ref}$", ['s', 'V'], time, y=v_ref)
    V_L.compareSignals(V_COMP, VREF)
