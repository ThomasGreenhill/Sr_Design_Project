'''
prop_design_analysis
Propeller design and analysis (fixed and variable pitch)

Calls:
    prop_design_TVG

Notes:

History:
    02.28.2021: 

'''

from prop_design_TVG import prop_design
import numpy
import matplotlib.pyplot as plt
from Class130 import AtmData, Propeller
import sys
sys.path.append("../Utilities")
import formatfigures

try:
    formatfigures.formatfigures()
    latex = True
except ValueError:
    print("Not using latex formatting")
    latex = False

def m0_fn(Ma):
    if Ma <= 0.9:
        return (2 * math.pi) / numpy.sqrt(1 - Ma ** 2)
    else:
        return (2 * math.pi) / numpy.sqrt(1 - 0.9 ** 2)

def Cd_fn(Cl):
    return 0.0095 + 0.0040 * (Cl - 0.2) ** 2    

nn = 51
temp = 272.31667
h = 1828
pres = 8.988e4
dens = 1.112
visc = 1.758e-5
k = 1.4
R = 287
is_SI = True
numB = 3

radius = 1.78/2
RPM = numpy.linspace(500,2950,nn)
LD = 15
T_req = 13000/8 #N (TOGW/(L/D))
Cl = 0.4
alp0 = numpy.radians(-2)

for v_inf in range(22,72,10):
    P_design = [0] * nn
    T_design = [0] * nn
    Q_design = [0] * nn
    eta_P = [0] * nn
    for ii in range(0,nn):
        atm = AtmData(v_inf, h, is_SI)
        atm.expand(1.4, 287)
        prop = Propeller(radius, numB, RPM[ii], eta_P, CP = 0, CT = 0, CQ = 0, Cl = 0.4,)
        [_, _, _, P_design[ii], T_design[ii], Q_design[ii], eta_P[ii], _] = prop_design(atm, prop, T_req)
    label = "$V_\infty$ = " + str(v_inf) + " (m/s)"
    plt.figure(1)
    plt.plot(RPM,Q_design,label=label)    
    plt.figure(2)
    plt.plot(RPM,eta_P,label=label)
    plt.figure(3)
    plt.plot(RPM,P_design,label=label)
    # plt.figure(7)
    # plt.plot(RPM,T_design,label=label)

plt.figure(1)
plt.legend()    
plt.xlabel("RPM")
plt.ylabel("Torque (Nm)")
plt.title("Torque vs. RPM for Propeller Design \n With Different Inlet Velocity Design Condition")
plt.savefig('./Figures/Torque_vs_RPM_hover.jpg', bbox_inches='tight')

plt.figure(2)
plt.legend() 
plt.xlabel("RPM")
plt.ylabel("$\eta_p$")
plt.title("Efficiency vs. RPM for Propeller Design \n With Different Inlet Velocity Design Condition")
plt.savefig('./Figures/Efficiency_vs_RPM_hover.jpg', bbox_inches='tight')

plt.figure(3)
plt.legend() 
plt.xlabel("RPM")
plt.ylabel("Power (W)")
plt.title("Power vs. RPM for Propeller Design \n With Different Inlet Velocity Design Condition")
plt.savefig('./Figures/Power_vs_RPM_hover.jpg', bbox_inches='tight')

plt.show()

# Choose the prop design with the highest cruise efficiency
m = numpy.argmax(eta_P)

prop = Propeller(radius, numB, RPM[ii], eta_P, CP = 0, CT = 0, CQ = 0, Cl = 0.4,)
[_, _, _, P_design[m], T_design[m], Q_design[m], eta_P[m], _] = prop_design(atm, prop, T_req)




