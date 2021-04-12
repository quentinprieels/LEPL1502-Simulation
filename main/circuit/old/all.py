# Imports
import numpy as np

from main.circuit.old.circuit import Signal
from main.circuit.old.detection import b_const
# from main.circuit.amplificateur import vamp

# Components values
r_bobine = 5  # [ohms]
r_amp = 5600  # [ohms]
p_r_amp_vals = [0, 100000]  # [ohms]
p_r_amp = 80000
r_f = 1200  # [ohms]
c_f = 0.0000001  # [F]
r_c = 560  # [ohms]
p_r_ref_vals = [0, 100000]  # [ohms]
p_r_ref = 80000
r_b = 10000  # [ohms]
p_r_b_vals = [0, 50000]  # [ohms]
p_r_b = 25000

# Time value
steps = 2000
begin = -5  # [ms]
end = 5  # [ms]
time = np.linspace(begin, end, steps)


# Functions
def vamp(t):
    vl = VL.getY() / 1000
    s = np.zeros(len(t))
    for i in range(len(t)):
        test = vl[i] * (1 + (p_r_amp / r_amp))
        if test < 0:
            s[i] = 0
        elif test > 5:
            s[i] = 5
        else:
            s[i] = test
    return s


# Signals
if __name__ == '__main__':
    VL = Signal('$V_L$', ['ms', 'mV'], time, f=b_const)
    VL.plot()

    VAMP = Signal('$V_{amp}$', ['ms', 'V'], time, f=vamp)
    VAMP.compareSignals(VL)
