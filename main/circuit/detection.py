from main.circuit.circuit import *

# ==== Electrical components and essentially informations ====
time = np.linspace(10, -10, 2000)

N = 100  # Number of turns of the wire [#]
B_cst_val = 1.5  # Value en B near the magnet [T]
a = 2  # Magnet radius [m]
b = 2  # Coil radius [m]
v = 2  # Magnet speed [m/s]


# ==== Functions =====
# 1. B is considered constant, only the intersection area is taken into account
def b_const(t):
    # todo: DON'T WORK A LOT...

    def d(t):
        return np.abs(v * t)

    def dd(t):
        # todo: DON'T WORK WHEN 'return v' => why ?
        return t

    def h(t):
        return np.sqrt(a ** 2 - ((a ** 2 - b ** 2 + (d(t)) ** 2) / (2 * d(t))) ** 2)

    def dh(t):
        return (dd(t) * ((a ** 2 - b ** 2) ** 2 - (d(t)) ** 4)) / \
               (2 * (d(t)) ** 3 * np.sqrt(
                   2 * (a ** 2 + b ** 2) - ((a ** 2 - b ** 2) ** 2 + ((d(t)) ** 4)) / ((d(t)) ** 4)))

    def area(t):
        return (((h(t)) ** 2 * dh(t)) / (np.sqrt(a ** 2 - (h(t)) ** 2))) - \
               (np.sqrt(a ** 2 - (h(t)) ** 2) * dh(t)) + ((a * dh(t)) / (np.sqrt(1 - ((h(t)) ** 2) / (a ** 2)))) \
               + (((h(t)) ** 2 * dh(t)) / (np.sqrt(b ** 2 - (h(t)) ** 2))) \
               - (np.sqrt(b ** 2 - (h(t)) ** 2) * dh(t)) \
               + ((b * dh(t)) / (np.sqrt(1 - ((h(t)) ** 2) / (b ** 2))))

    return N * B_cst_val * area(t)


# ==== Main program ====
if __name__ == '__main__':
    # 1. With a B constant
    VL_bconst = Signal('$V_L$', ['s', 'mV'], time, f=b_const)
    VL_bconst.plot()
