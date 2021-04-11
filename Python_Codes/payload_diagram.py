# -*- coding: utf-8 -*-

## Set-up

import numpy as np
import matplotlib.pyplot as plt
import os
savedir = os.path.abspath(os.path.dirname(__file__))

## Payload Diagram Calculation

# Fuel masses
H2_Mass    = 5 #kg
H2_Reserve = 0.1*H2_Mass #kg

# "Battery" charges w/ hydrogen as "charge"
E_0 = H2_Mass*120e6     # Fuel mass times energy density
E_1 = H2_Reserve*120e6

# Efficiencies
n_fc   = 0.57 # Fuel cell efficiency
n_mech = 0.75 # Mechanical efficiency
n_prop = 0.85 # Propellor efficiency
n_tot  = n_fc*n_mech*n_prop # Total efficiency

# Lift over drag
LD = 15

# Mass
MTOW = 1325.24*9.8
OEW  = 1131.94*9.8

R_B = n_tot*LD*(E_0-E_1)/MTOW/1000 # Range of point B in km
R_C = n_tot*LD*(E_0-E_1)/OEW/1000  # Range of point C in km

Range = [0, R_B, R_C]
Wp = MTOW-OEW
Woe = OEW
E_reserve = E_1
E_b = E_0

## Payload Diagram Formulation
color1 = 'tab:blue'; color2 = 'tab:red'

fig, ax1 = plt.subplots() 

#### Weight vs. Range
ax1.set_xlabel('Range (km)') 
ax1.set_ylabel('Weight (N)', color = color1) 
ax1.plot([0, Range[-1]], [Woe, Woe], color = color1, linestyle='-')  
ax1.plot(Range, [Wp+Woe, Wp+Woe, Woe], color = color1, linestyle='--')  
ax1.tick_params(axis ='y', labelcolor = color1) 
ax1.set_xlim([0, np.amax(Range)*1])
ax1.set_ylim([0, np.amax(Wp+Woe)*1.25])

#### Notations for Weight vs. Range part
plt.annotate('', xy=(50,0), xytext=(50,Woe), arrowprops=dict(arrowstyle="<->",
             connectionstyle="arc3", color=color1, lw=2))
plt.text(55, 8000, "Operating\nEmpty\nWeight")

plt.annotate('', xy=(50,Woe), xytext=(50,Woe+Wp), arrowprops=dict(arrowstyle="<->",
             connectionstyle="arc3", color=color1, lw=2))
plt.text(55, 12000, "Max Payload")

#### Adding Twin Axes to plot another datasets
ax2 = ax1.twinx() 
  
#### Battery Charge vs. Range
ax2.set_ylabel('Battery Charge (J)', color = color2) 
ax2.plot([0, Range[-1]], [E_reserve, E_reserve], color = color2, linestyle='-')  
ax2.plot(Range, [E_reserve, E_b+E_reserve, E_b+E_reserve], color = color2, linestyle='--') 
ax2.tick_params(axis ='y', labelcolor = color2) 
ax2.set_ylim([0, np.amax(E_b)*1.25])

#### Notations for Battery Charge vs. Range part
plt.annotate('', xy=(230,0), xytext=(230,E_reserve), arrowprops=dict(arrowstyle="<->",
             connectionstyle="arc3", color=color2, lw=2))
plt.text(160, 0.25e8, "Reserve Charge")

plt.annotate('', xy=(240,0), xytext=(240,E_b+E_reserve), arrowprops=dict(arrowstyle="<->",
             connectionstyle="arc3", color=color2, lw=2))
plt.text(205, 3.8e8, "Battery\nCharge")

#### Final Step 
plt.title('Impact of Payload on Range') 
plt.savefig('%s/Payload_Diagram.png'%(savedir))
plt.show()
