import numpy as np

# -- Components values --

# Time value
steps = 2000  # [#]
begin = -2 # [ms]
end = 2  # [ms]
time = np.linspace(begin, end, steps)

# Circuit
v_cc = 5  # [V]
v_ss = 0  # [V]

# Bobine
N = 1  # Number of turns of the wire [#]
B_cst_val = 1500  # Value en B near the magnet [mT]
r = 20  # Magnet radius [mm]
b = 20  # Coil radius [mm]
r_bobine = 5  # [ohms]

# Amplification
r_amp = 5600  # [ohms]
p_r_amp_vals = [1, 100000]  # [ohms]
p_r_amp = np.linspace(p_r_amp_vals[0], p_r_amp_vals[1], steps)  # [ohms]

# Filter
r_f = 1200  # [ohms]
c_f = 0.000001  # [F]

# Comparator
r_c = 560  # [ohms]
p_r_ref_vals = [1, 100000]  # [ohms]
p_r_ref = np.linspace(p_r_ref_vals[0], p_r_ref_vals[1], steps)  # [ohms]

# Interrupter
r_b = 10000  # [ohms]
p_r_b_vals = [1, 50000]  # [ohms]
p_r_b = np.linspace(p_r_ref_vals[0], p_r_ref_vals[1], steps)  # [ohms]
v_d = v_zk = 3.3  # [V]
beta = 375  # [#]


# Main Program
if __name__ == '__main__':
    pass
