# -*- coding: utf-8 -*-

# Imports
import numpy as np
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

sys.path.append("../Utilities")
import formatfigures

try:
    formatfigures.formatfigures()
    latex = True
except ValueError:
    print("Not using latex formatting")
    latex = False
    
### Carpet Plot Data ###

## Conditions
# Cruise speed
V = 202.537 # 120 kts in ft/s
# 6000 ft altitude
rho = 0.00237717 # slugs/ft^3

## Sweep Parameters
# CD0
CD0_min = 0.005
CD0_max = 0.03
CD0_n = 6
# AR e
ARe_min = 2.5
ARe_max = 12.5
ARe_n = 5
# Number of points along each line
fine_n = 100

## Cd0 sweep
CD0_vec = np.linspace(CD0_min,CD0_max,CD0_n)
ARe_vec = np.linspace(ARe_min,ARe_max,fine_n)
CD0_sweep = np.zeros(shape=(CD0_n,fine_n,2))
for (n, CD0) in enumerate(CD0_vec):
    CL = np.sqrt(CD0*np.pi*ARe_vec)
    LD_max = 0.5*np.sqrt(np.pi*ARe_vec/CD0)
    wing_load = 0.5*CL*rho*V**2
    CD0_sweep[n,:,0] = wing_load
    CD0_sweep[n,:,1] = LD_max
    
## AR e sweep
CD0_vec = np.linspace(CD0_min,CD0_max,fine_n)
ARe_vec = np.linspace(ARe_min,ARe_max,ARe_n)
ARe_sweep = np.zeros(shape=(ARe_n,fine_n,2))
for (n, ARe) in enumerate(ARe_vec):
    CL = np.sqrt(CD0_vec*np.pi*ARe)
    LD_max = 0.5*np.sqrt(np.pi*ARe/CD0_vec)
    wing_load = 0.5*CL*rho*V**2
    ARe_sweep[n,:,0] = wing_load
    ARe_sweep[n,:,1] = LD_max
    
## Plot ##

# Vectors for naming
CD0_vec = np.linspace(CD0_min,CD0_max,CD0_n)
ARe_vec = np.linspace(ARe_min,ARe_max,ARe_n)

CD0_text_x_offset = 1
CD0_text_y_offset = 1
ARe_text_x_offset = 1
ARe_text_y_offset = -3
    
# Plot lines and add labels
for n in range(CD0_n):
    plt.plot(CD0_sweep[n,:,0],CD0_sweep[n,:,1],'b-')
    plt.text(CD0_sweep[n,-1,0]+CD0_text_x_offset,
             CD0_sweep[n,-1,1]+CD0_text_y_offset,
             '{:.3f}'.format(CD0_vec[n]))
for n in range(ARe_n):
    plt.plot(ARe_sweep[n,:,0],ARe_sweep[n,:,1],'b-')
    plt.text(ARe_sweep[n,-1,0]+ARe_text_x_offset,
             ARe_sweep[n,-1,1]+ARe_text_y_offset,
             '{:.3f}'.format(ARe_vec[n]))
plt.plot(38.7,20,'ro',markersize=15)

plt.text(36,36,"Zero-lift Drag\nCoefficient $C_{D_0}$")
plt.text(40,2,"Effective Aspect\nRatio $AR\cdot e$")

plt.xlim(5,1.2*np.max(CD0_sweep[:,:,0]))
plt.ylim(0,1.2*np.max(CD0_sweep[:,:,1]))
plt.xlabel("Wing Loading (lbf/ft$^2$)")
plt.ylabel("Maximum Lift-Drag Ratio")
plt.title("Cruise Altitude 6,000 ft (SA), Cruise Speed 120 kts")
plt.savefig('Figures/carpet_plot_1.png')
plt.show()