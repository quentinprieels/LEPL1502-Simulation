from main.circuit.circuit import *

# ==== Electrical components and essentially informations ====
t = np.linspace(0, 0.05, 2000)  # Time [ms]
R_F = 1200  # Resistor [ohms]
C_F = 0.000001  # Capacitor [F]
f_c = 1 / (2 * np.pi * R_F * C_F)  # Cutoff frequency[Hz]

a = 2.5  # Amplitude [#]
f = np.linspace(10, 200, 2000)  # Frequency of entering signal [Hz]
omega = 2 * np.pi * f  # Angular velocity

# === Functions ====
# 2. Entering functions
filtre_in = lambda t: a * np.sin(omega * t) + a


def filtre_in_2(t, w_t):
    return a * np.sin(w_t * t) + a


# 1. Filter functions
def parfait(t):
    out = np.empty_like(t)
    for i in range(len(t)):
        if f[i] <= f_c:
            out[i] = filtre_in_2(t[i], omega[i])
        else:
            out[i] = 0
    return out


def sinus(t):
    phi = np.arctan(-R_F * C_F * omega)
    b = a / ((np.cos(np.arctan(-R_F * C_F * omega))) - (R_F * C_F * omega * np.sin(np.arctan(-R_F * C_F * omega))))
    return b * np.sin(omega * t + phi) + a


# ==== Main program ====
if __name__ == '__main__':
    # ==== Signals ====
    Vamp = Signal('$V_{amp}$', ['ms', 'V'], t, f=filtre_in)
    # 1. Perfect filter
    VF_p = Signal('$V_F$', ['ms', 'V'], t, f=parfait)
    Vamp.compareSignals(VF_p)

    # 2. Filtre simulation with sinus
    VF_s = Signal('$V_F$', ['ms', 'V'], t, f=sinus)
    Vamp.compareSignals(VF_s)
