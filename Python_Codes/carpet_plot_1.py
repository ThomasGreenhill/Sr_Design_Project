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

# Conditions
# 6000 ft altitude
rho = 0.00237717 # slugs/ft^3
# Aircraft characteristics
W = 1325.24*2.20462 # Weight (lbf)
e = 0.8 # wing oswald efficiency factor (ASSUMED)
f_rest = (0.420699-0.147834)*10.7639 # flat plate area of plane minus wing, m^2 to ft^2
CD0w = 0.00924 # zero-lift drag coefficient of wing

# # TEST
# rho = 0.000857050
# W = 60000
# e = 0.75
# f_rest = 7.5
# CD0w = 0.004

## Sweep Parameters
# V
V_min = 100 # V IN KNOTS (converted to ft later)
V_max = 140
V_n = 5
# AR
AR_min = 6
AR_max = 16
AR_n = 6
# Number of points along each line
fine_n = 100

# # TEST
# # V
# V_min = 0.6*990.347
# V_max = 0.7*990.347
# V_n = 5
# # AR
# AR_min = 6
# AR_max = 16
# AR_n = 6
# # Number of points along each line
# fine_n = 100

## V sweep
V_vec = np.linspace(V_min,V_max,V_n)
AR_vec = np.linspace(AR_min,AR_max,fine_n)
V_sweep = np.zeros(shape=(V_n,fine_n,2))
CD0 = np.ones_like(AR_vec)
for (n, V) in enumerate(V_vec):
    for i in range(100): # Fixed number of iterations... whatever
        CL = np.sqrt(CD0*np.pi*AR_vec*e)
        LD_max = 0.5*np.sqrt(np.pi*AR_vec*e/CD0)
        wing_load = 0.5*CL*rho*(V*1.68781)**2 # notice conversion from kts to ft/s
        # wing_load = 0.5*CL*rho*V**2 # USING V IN FT/S
        S = W/wing_load
        CD0_old = CD0
        CD0 = f_rest/S + CD0w
    V_sweep[n,:,0] = wing_load
    V_sweep[n,:,1] = LD_max
    
## AR sweep
V_vec = np.linspace(V_min,V_max,fine_n)
AR_vec = np.linspace(AR_min,AR_max,AR_n)
AR_sweep = np.zeros(shape=(AR_n,fine_n,2))
CD0 = np.ones_like(V_vec)
for (n, AR) in enumerate(AR_vec):
    for i in range(100): # Fixed number of iterations... whatever
        CL = np.sqrt(CD0*np.pi*AR*e)
        LD_max = 0.5*np.sqrt(np.pi*AR*e/CD0)
        wing_load = 0.5*CL*rho*(V_vec*1.68781)**2 # notice conversion from kts to ft/s
        # wing_load = 0.5*CL*rho*V_vec**2 # USING V IN FT/S
        S = W/wing_load
        CD0_old = CD0
        CD0 = f_rest/S + CD0w
    AR_sweep[n,:,0] = wing_load
    AR_sweep[n,:,1] = LD_max
    
## Plot ##

# Vectors for naming
V_vec = np.linspace(V_min,V_max,V_n)
AR_vec = np.linspace(AR_min,AR_max,AR_n)

V_text_x_offset = 1
V_text_y_offset = 0.2
AR_text_x_offset = 1
AR_text_y_offset = -0.5
    
# Plot lines and add labels
for n in range(V_n):
    plt.plot(V_sweep[n,:,0],V_sweep[n,:,1],'b-')
    plt.text(V_sweep[n,-1,0]+V_text_x_offset,
              V_sweep[n,-1,1]+V_text_y_offset,
              '{:d}'.format(int(V_vec[n])))
for n in range(AR_n):
    plt.plot(AR_sweep[n,:,0],AR_sweep[n,:,1],'b-')
    plt.text(AR_sweep[n,-1,0]+AR_text_x_offset,
              AR_sweep[n,-1,1]+AR_text_y_offset,
              '{:d}'.format(int(AR_vec[n])))
# plt.plot(38.7,20,'ro',markersize=15)

plt.text(110,11,"Cruise Velocity $V$ (kts)")
plt.text(125,5.5,"Aspect Ratio $AR$")

plt.xlim(5,1.2*np.max(V_sweep[:,:,0]))
plt.ylim(5,1.2*np.max(V_sweep[:,:,1]))
plt.xlabel("Wing Loading (lbf/ft$^2$)")
plt.ylabel("Maximum Lift-Drag Ratio")
# plt.title("Cruise Altitude 6,000 ft (SA), Cruise Speed 120 kts")
plt.savefig('Figures/carpet_plot_2.png')
plt.show()