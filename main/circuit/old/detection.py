# ==== Imports ====
from main.circuit.old.circuit import *
np.seterr(all='raise')

# ==== Analytic solution ====
"""
V_L = N d/dt int_A(t) B ds
"""

# ==== Electrical components and essentially information's ====
begin = -5
end = 5
steps = 2000
time = np.linspace(begin, end, steps)

N = 1  # Number of turns of the wire [#]
B_cst_val = 1500  # Value en B near the magnet [mT]
r = 20  # Magnet radius [mm]
b = 20  # Coil radius [mm]

v0 = 100
a = lambda t: -1 / 4 * t
v = lambda t: -1 / 8 * t ** 2


# ==== Functions =====
# 1. B is considered constant, only the intersection area is taken into account
def d(t):
    return -1 / 24 * t ** 3 + v0 * t


def b_const(t):

    def dd(t):
        return v(t)

    def h(t):
        s = np.zeros(len(t))
        for i in range(len(s)):
            try:
                s[i] = np.sqrt(r ** 2 - ((r ** 2 - b ** 2 + (d(t[i])) ** 2) / (2 * d(t[i]))) ** 2)
            except FloatingPointError:
                msg = 'Error in sqrt, line 35. i = {}'.format(i)
                # print(warningText(msg))
                s[i] = 0
        return s

    def dh(t):
        return (dd(t) * ((r ** 2 - b ** 2) ** 2 - (d(t)) ** 4)) / \
               (2 * (d(t)) ** 3 * np.sqrt(
                   2 * (r ** 2 + b ** 2) - ((r ** 2 - b ** 2) ** 2 + ((d(t)) ** 4)) / ((d(t)) ** 4)))

    def area(t):
        return (((h(t)) ** 2 * dh(t)) / (np.sqrt(r ** 2 - (h(t)) ** 2))) - \
               (np.sqrt(r ** 2 - (h(t)) ** 2) * dh(t)) + ((r * dh(t)) / (np.sqrt(1 - ((h(t)) ** 2) / (r ** 2)))) \
               + (((h(t)) ** 2 * dh(t)) / (np.sqrt(b ** 2 - (h(t)) ** 2))) \
               - (np.sqrt(b ** 2 - (h(t)) ** 2) * dh(t)) \
               + ((b * dh(t)) / (np.sqrt(1 - ((h(t)) ** 2) / (b ** 2))))

    return N * B_cst_val * area(t)


# ==== Main program ====
if __name__ == '__main__':
    # 0. Acceleration and spreed of magnet
    print("==== Acceleration and spreed of magnet ====")
    A = Signal('a', ['s', '$m/s^2$'], time, f=a)
    A.setAxisNames('Temps', 'Accélération')
    A.plot()
    V = Signal('v', ['s', '$m/s$'], time, f=v)
    V.setAxisNames('Temps', 'Vitesse')
    V.plot()
    D = Signal('Position', ['s', 'm'], time, f=d)
    D.setAxisNames('Temps', 'Distance')
    D.plot()
    print('Done\n')

    # 1. With a B constant
    print("==== With a B constant ====")
    VL_bconst = Signal('$V_L$', ['ms', 'mV'], time, f=b_const)
    VL_bconst.plot()
    print('Done\n')
