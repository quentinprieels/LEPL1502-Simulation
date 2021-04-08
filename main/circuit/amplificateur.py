from main.circuit.circuit import *

# ==== Electrical components and essentially informations ====
begin = -0.05
end = 0.05
steps = 200
time = np.linspace(begin, end, steps)

R_amp = 56000
pR_amp_val = [0, 100000]
pR_amp = np.linspace(pR_amp_val[0], pR_amp_val[1], steps)

a = 0.2  # Amplitude [#]
f = 50  # Frequency of entering signal [Hz]
omega = 2 * np.pi * f  # Angular velocity
V_L = lambda t: a * np.sin(omega * t)


# ==== Functions =====
def vamp(t):
    to_return = np.zeros(len(t))
    for i in range(len(t)):
        test = V_L(t[i]) * (1 + (pR_amp[i] / R_amp))
        if test < 0:
            to_return[i] = 0
        elif test > 5:
            to_return[i] = 5
        else:
            to_return[i] = test
    return to_return


# ==== Main program ====
if __name__ == '__main__':
    # ==== Signals ====
    VL = Signal('$V_{amp}$', ['s', 'V'], time, f=V_L)
    Vamp = Signal('$V_{amp}$', ['s', 'V'], time, f=vamp)
    Vamp.compareSignals(VL)
