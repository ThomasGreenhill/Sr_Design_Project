# -*- coding: utf-8 -*-

import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import sys

sys.path.append("../Utilities/")
try:
    import formatfigures
    formatfigures.formatsubfigures()
    formatfigures.formatfigures()
    latex = True
except:
    print("Not using latex formatting")
    latex = False

# Name of file to read
# filename = "./Pressures/max_pos_upper.txt"
filename = "./Pressures/max_pos_lower.txt"
# filename = "./Pressures/max_neg_upper.txt"
# filename = "./Pressures/max_neg_lower.txt"

# Grid positions to interpolate
# x_pos = np.linspace(0, 1.58, 30)
# z_pos = np.linspace(-6.33, 0, 200)
x_pos = np.linspace(0, 1.58, 120)
z_pos = np.linspace(-6.33, 0, 1000)
xx, zz = np.meshgrid(x_pos, z_pos)

# Read content of file and strip header/footer
with open(filename) as f:
    lines = [line.rstrip() for line in f]
    lines = lines[31:-7]

# Initialize data arrays
x  = np.empty(len(lines))
z  = np.empty(len(lines))
cp = np.empty(len(lines))

# Parse each line and extract coordinates and pressure coeff
for (i, line) in enumerate(lines):
    dat = line.split(',')
    x[i]  = dat[0]
    z[i]  = dat[1]
    cp[i] = dat[4]
    
# Move points to have same coords as PATRAN
x -= 3
z *= -1

# Find pressure from pressure coefficient
rho_inf = 1.22500
v_inf = 80.6 # FOR POSITIVE LOAD
p = cp*0.5*rho_inf*v_inf**2 # Note this is gauge pressure

# Interpolate to get pressure on regular grid
p_new = griddata((x, z), p, (xx, zz), fill_value=0, method='linear')

plt.pcolor(xx, zz, p_new, shading='auto')
plt.colorbar()