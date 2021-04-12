import numpy as np

from main.model.components import *
np.seterr(all='raise')


# Detection
def detection_b_const(t, m, v0):
    """
    Detection of magnet passage with a constant magnetic B.

    This function describes the behavior of the VL signal when the magnet passes over the coil.
    WARNING : the loop of the circuit is not taken into account. The influence of the current Ic is not taken into
    account.
    WARNING : N (number of wire turns), B_cst_val (Value en B near the magnet), r (Magnet radius), b (Coil radius) are
    defined in the components.py file.

    :param t: Time
    :type t: numpy.ndarray

    :param m: Slope of acceleration (a = mx + p; p = 0)
    :type m: float

    :param v0: Term in t of the position
    :type v0: float

    :return: The ordinates of the function vl, position, speed and acceleration
    :rtype: tuple of numpy.ndarray
    """
    d = lambda t: (m / 6) * t ** 3 + v0 * t  # Position, distance between the two centers
    v = lambda t: (m / 2) * t ** 2  # Speed
    a = lambda t: m * t  # Acceleration

    def dd(t):
        """
        Temporal derivative of the position (= speed)
        """
        return v(t)

    def h(t):
        """
        Auxiliary function
        """
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
        """
        Auxiliary function, temporal derivative of h(t)
        """
        return (dd(t) * ((r ** 2 - b ** 2) ** 2 - (d(t)) ** 4)) / \
               (2 * (d(t)) ** 3 * np.sqrt(
                   2 * (r ** 2 + b ** 2) - ((r ** 2 - b ** 2) ** 2 + ((d(t)) ** 4)) / ((d(t)) ** 4)))

    def area(t):
        """
        Calculation of the intersection area
        """
        s = (((h(t)) ** 2 * dh(t)) / (np.sqrt(r ** 2 - (h(t)) ** 2))) - \
            (np.sqrt(r ** 2 - (h(t)) ** 2) * dh(t)) + ((r * dh(t)) / (np.sqrt(1 - ((h(t)) ** 2) / (r ** 2)))) \
            + (((h(t)) ** 2 * dh(t)) / (np.sqrt(b ** 2 - (h(t)) ** 2))) \
            - (np.sqrt(b ** 2 - (h(t)) ** 2) * dh(t)) \
            + ((b * dh(t)) / (np.sqrt(1 - ((h(t)) ** 2) / (b ** 2))))
        for i in range(len(s)):
            if s[i] == 'nan':
                s[i] = 0
        return s

    return N * B_cst_val * area(t), d(t), v(t), a(t)


# Amplification
def amplification(t, vl):
    """
    Amplification of the V_L signal

    This function describes the behavior of the amplifier block. It amplifies the signal by a certain factor determined
    by the value of the resistances p_r_amp and r_amp.
    WARNING: the values of these two resistances are given in the file components.py


    :param t: Time
    :type t: numpy.ndarray

    :param vl: Amplified signal
    :type vl: numpy.ndarray

    :return: The amplified signal
    :rtype: (numpy.ndarray, numpy.ndarray)
    """
    if len(t) != len(vl):
        raise ValueError("Time and V_L signal MUST BE have the same length. (For a time value, a V_L value.)")
    #if isinstance(p_r_amp, float):
     #   p_r_amp = np.full(steps, p_r_amp)

    s = np.zeros(len(t))
    for i in range(len(t)):
        test = vl[i] * (1 + (p_r_amp[i] / r_amp))
        if test < 0:
            s[i] = 0
        elif test > 5:
            s[i] = 5
        else:
            s[i] = test
    return s, vl


# Filter
def filter(t, a, f, resolution='sinus'):
    """
    Filter a sinusoidal signal

    This function describes the behavior of the filter block. The filter can either be considered as perfect or act in a
    more precise way.
    WARNING: the input signal must be a sinus !

    :param t: Time
    :type t: numpy.ndarray

    :param a: Amplitude of the sinus that enter into the filter
    :type a: float

    :param f:  Frequency of the sinus that enter into the filter
    :type f: float or numpy.ndarray

    :param resolution: Hypothesis on the filter: perfect or solved with a sine
    :type resolution: str

    :return: The filtered signal and the signal that filtered is
    :rtype: (numpy.ndarray, numpy.ndarray)
    """
    # Create the into signal (signal that will be filtered)
    omega = 2 * np.pi * f

    def into(t):
        return a * np.sin(omega * t) + a

    # Sinus resolution
    if resolution == 'sinus':
        phi = np.arctan(-r_f * c_f * omega)
        b = a / ((np.cos(np.arctan(-r_f * c_f * omega))) - (r_f * c_f * omega * np.sin(np.arctan(-r_f * c_f * omega))))
        return into(t), b * np.sin(omega * t + phi) + a

    # Perfect resolution
    elif resolution == 'perfect':
        f_c = 1 / (2 * np.pi * r_f * c_f)
        s = np.empty_like(t)
        for i in range(len(t)):
            if f[i] <= f_c:
                s[i] = into(t[i])
            else:
                s[i] = 0
        return into(t), s


# Comparator
def comparator(t, vf):
    """
    Comparator of vf signal

    This function describes the comparator block of the circuit. For a certain input signal, it compares it to a
    reference signal determined by the value of p_r_ref.
    WARNING: the value of this resistor is given in the file components.py

    :param t: Time
    :type t: numpy.ndarray

    :param vf: Compared signal
    :type vf: numpy.ndarray

    :return: the output signal of the comparator, the signal to which it is compared, and the referent value
    :rtype: (numpy.ndarray, numpy.ndarray, numpy.ndarray)
    """
    s = np.zeros(len(t))
    v_ref = p_r_ref * (v_zk / p_r_ref_vals[1])
    if isinstance(v_ref, float):
        v_ref = np.full(len(t), v_ref)
    for i in range(len(t)):
        v_e = v_ref[i] - vf[i]
        if v_e > 0:
            s[i] = v_cc
        else:
            s[i] = v_ss
    return s, vf, v_ref


# Interrupter
def interrupter(t, vcomp):
    """
    Tension and current switch

    This function describes the behavior of the switch. Depending on the vcomp signal, the switch sends a certain
    current or not.
    WARNING: the value of the resistors are given in the file components.py

    :param t: Time
    :type t: numpy.ndarray

    :param vcomp: Used signal which determines whether the switch should open
    :type vcomp: numpy.ndarray

    :return: The values of the induced voltages and currents (v_b, v_c, i_n and i_c)
    :rtype: (numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray)
    """
    v_b = np.zeros(len(t))
    v_c = np.zeros(len(t))
    i_b = np.zeros(len(t))
    i_c = np.zeros(len(t))
    for i in range(len(t)):
        if vcomp[i] == v_cc:  # blocked mode
            i_b[i] = 0
            i_c[i] = 0
            v_b[i] = v_cc
            v_c[i] = 0

        elif vcomp[i] == v_ss:  # linear mode
            i_b[i] = 4.3 / (p_r_b[i] + r_b)
            i_c[i] = (4.3 * beta) / (p_r_b[i] + r_b)
            v_b[i] = v_cc - 0.7
            v_c[i] = r_bobine * i_c[i]

        else:
            raise ValueError('The vl signal must always be either equal to v_ss or v_cc')
    return v_b, v_c, vcomp, i_b, i_c


if __name__ == '__main__':
    pass
