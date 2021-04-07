from main.circuit.circuit import *

# ==== Electrical components and essentially informations ====
t = np.linspace(-20, 20, 2000)  # Time [ms]
R_F = 1200                      # Resistor [ohms]
C_F = 0.000001                  # Capacitor [F]
f_c = 1 / (2 * np.pi * R_F * C_F)  # Frequency [Hz]


# === Functions ====
def parfait(t, fx, f_c):
    if fx <= f_c:
        return t
    else:
        return 0


def sinus(a, omega, t):
    phi = np.arctan(-R_F * C_F * omega)
    b = a / ((np.cos(np.arctan(-R_F * C_F * omega))) - (R_F * C_F * omega * np.sin(np.arctan(-R_F * C_F * omega))))
    return b * np.sin(omega * t + phi)


c = lambda x: np.cos(x ** 2)

# ==== Signals ====
# 1. Perfect signal
cos_carre = Signal('cos_carre', ['ms', 'V'], t, f=c)
filtre_parfait = Block('Filtre Parfait', [cos_carre], f=parfait())
