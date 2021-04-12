from main.circuit.components import *


# Detection
v0 = 100
a = lambda t: -1 / 4 * t
v = lambda t: -1 / 8 * t ** 2


def detect_funct(t):
    def d(t):
        return -1 / 24 * t ** 3 + v0 * t

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


# Amplification
def ampl_funct(t, vl):
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


# Filtre
def filtre_funct_parf(t):
    def sinus_2(t, w_t):
        return a * np.sin(w_t * t) + a

    out = np.empty_like(t)
    for i in range(len(t)):
        if f[i] <= f_c:
            out[i] = sinus_2(t[i], omega[i])
        else:
            out[i] = 0
    return out


def filtre_funct_sin(t):
    phi = np.arctan(-R_F * C_F * omega)
    b = a / ((np.cos(np.arctan(-R_F * C_F * omega))) - (R_F * C_F * omega * np.sin(np.arctan(-R_F * C_F * omega))))
    return b * np.sin(omega * t + phi) + a
