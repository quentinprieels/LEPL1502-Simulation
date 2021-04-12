import numpy as np

# Components values
N = 1  # Number of turns of the wire [#]
B_cst_val = 1500  # Value en B near the magnet [mT]
r = 20  # Magnet radius [mm]
b = 20  # Coil radius [mm]
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

