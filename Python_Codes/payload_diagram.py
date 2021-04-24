## Set-up

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("../Utilities")
import os
savedir = os.path.abspath(os.path.dirname(__file__))

try:
    import formatfigures
    formatfigures.formatsubfigures()
    formatfigures.formatfigures()
    latex = True
except:
    pass
    print("Not using latex formatting")
    latex = False

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
E_reserve = E_1*2.77778e-7
E_b = E_0*2.77778e-7

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
plt.text(55, 7600, "Operating\nEmpty\nWeight")

plt.annotate('', xy=(50,Woe), xytext=(50,Woe+Wp), arrowprops=dict(arrowstyle="<->",
             connectionstyle="arc3", color=color1, lw=2))
plt.text(55, 11700, "Max Payload")

#### Adding Twin Axes to plot another datasets
ax2 = ax1.twinx() 
  
#### Battery Charge vs. Range
ax2.set_ylabel('Available Hydrogen Energy (kWh)', color = color2) 
ax2.plot([0, Range[-1]], [E_reserve, E_reserve], color = color2, linestyle='-')  
ax2.plot(Range, [E_reserve, E_b+E_reserve, E_b+E_reserve], color = color2, linestyle='--') 
ax2.tick_params(axis ='y', labelcolor = color2) 
ax2.set_ylim([0, np.amax(E_b)*1.25])

#### Notations for Battery Charge vs. Range part
plt.annotate('', xy=(230,0), xytext=(230,E_reserve), arrowprops=dict(arrowstyle="<->",
             connectionstyle="arc3", color=color2, lw=2))
plt.text(173, 5, "Fuel Reserves")

plt.annotate('', xy=(240,0), xytext=(240,E_b+E_reserve), arrowprops=dict(arrowstyle="<->",
             connectionstyle="arc3", color=color2, lw=2))
plt.text(217, 98, "Full\nFuel\nTank")

#### Final Step 
plt.title('Impact of Payload on Range') 
plt.savefig('%s/Payload_Diagram_SI.png'%(savedir))
plt.show()

### ======================== ###
### REPEAT IN IMPERIAL UNITS ###
### ======================== ###

km_to_miles = 0.621371
N_to_lbs    = 0.224809

Range = [0, R_B*km_to_miles, R_C*km_to_miles]
Wp = (MTOW-OEW) * N_to_lbs
Woe = OEW * N_to_lbs
E_reserve = E_1*2.77778e-7
E_b = E_0*2.77778e-7

## Payload Diagram Formulation
color1 = 'tab:blue'; color2 = 'tab:red'

fig, ax1 = plt.subplots() 

#### Weight vs. Range

ax1.set_xlabel('Range (miles)') 
ax1.set_ylabel('Weight (lbs)', color = color1) 
ax1.plot([0, Range[-1]], [Woe, Woe], color = color1, linestyle='-')  
ax1.plot(Range, [Wp+Woe, Wp+Woe, Woe], color = color1, linestyle='--')  
ax1.tick_params(axis ='y', labelcolor = color1) 
ax1.set_xlim([0, np.amax(Range)*1])
ax1.set_ylim([0, np.amax(Wp+Woe)*1.25])

#### Notations for Weight vs. Range part
plt.annotate('', xy=(50*km_to_miles,0), xytext=(50*km_to_miles,Woe), arrowprops=dict(arrowstyle="<->",
              connectionstyle="arc3", color=color1, lw=2))
plt.text(55*km_to_miles, 7600*N_to_lbs, "Operating\nEmpty\nWeight")

plt.annotate('', xy=(50*km_to_miles,Woe), xytext=(50*km_to_miles,Woe+Wp), arrowprops=dict(arrowstyle="<->",
              connectionstyle="arc3", color=color1, lw=2))
plt.text(55*km_to_miles, 11700*N_to_lbs, "Max Payload")

#### Adding Twin Axes to plot another datasets
ax2 = ax1.twinx() 
  
#### Battery Charge vs. Range
ax2.set_ylabel('Available Hydrogen Energy (kWh)', color = color2) 
ax2.plot([0, Range[-1]], [E_reserve, E_reserve], color = color2, linestyle='-')  
ax2.plot(Range, [E_reserve, E_b+E_reserve, E_b+E_reserve], color = color2, linestyle='--') 
ax2.tick_params(axis ='y', labelcolor = color2) 
ax2.set_ylim([0, np.amax(E_b)*1.25])

#### Notations for Battery Charge vs. Range part
plt.annotate('', xy=(230*km_to_miles,0), xytext=(230*km_to_miles,E_reserve), arrowprops=dict(arrowstyle="<->",
              connectionstyle="arc3", color=color2, lw=2))
plt.text(173*km_to_miles, 5, "Fuel Reserves")

plt.annotate('', xy=(240*km_to_miles,0), xytext=(240*km_to_miles,E_b+E_reserve), arrowprops=dict(arrowstyle="<->",
              connectionstyle="arc3", color=color2, lw=2))
plt.text(217*km_to_miles, 98, "Full\nFuel\nTank")

#### Final Step 
plt.title('Impact of Payload on Range') 
plt.savefig('%s/Payload_Diagram_Imperial.png'%(savedir))
plt.show()
