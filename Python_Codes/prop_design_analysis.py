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
from prop_analysis_TVG import prop_analysis
import numpy
import matplotlib.pyplot as plt
from Class130 import AtmData, Propeller
import sys
sys.path.append("../Utilities")
import formatfigures

def m0_fn(Ma):
    if numpy.any(Ma <= 0.9):
        return (2 * numpy.pi) / numpy.sqrt(1 - Ma ** 2)
    else:
        return (2 * numpy.pi) / numpy.sqrt(1 - 0.9 ** 2)

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
RPM = numpy.linspace(500,3000,nn)
LD = 15
T_req = 13000/8/LD #N (TOGW/(L/D))
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
        [_, _, _, P_design[ii], T_design[ii], Q_design[ii], eta_P[ii], _] = prop_design(atm, prop, T_req, m0_fn, Cd_fn)
    label = "$V_\infty$ = " + str(v_inf) + " (m/s)"
    plt.figure(1)
    plt.plot(RPM,Q_design,label=label)    
    plt.figure(2)
    plt.plot(RPM,eta_P,label=label)
    plt.figure(3)
    plt.plot(RPM,P_design,label=label)
    # plt.figure(7)
    # plt.plot(RPM,T_design,label=label)

try:
    formatfigures.formatfigures()
    latex = True
except ValueError:
    print("Not using latex formatting")
    latex = False

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


# Choose the prop design with the highest cruise efficiency and run a fixed pitch analysis
try:
    formatfigures.formatsubfigures()
    latex = True
except ValueError:
    print("Not using latex formatting")
    latex = False
m = numpy.argmax(eta_P)

prop = Propeller(radius, numB, RPM[m], eta_P, CP = 0, CT = 0, CQ = 0, Cl = 0.4,)
r, prop.chord, prop.bet, P_design, T_design, Q_design, eta_P, prop.theta = prop_design(atm, prop, T_req, m0_fn, Cd_fn)
ll = 101
Vseq = numpy.linspace(0,70,ll)

J = numpy.zeros((ll,))
Pdesign = numpy.zeros((ll,))
CP = numpy.zeros((ll,))
Tdesign = numpy.zeros((ll,))
CT = numpy.zeros((ll,))
etap = numpy.zeros((ll,))

plt.figure(figsize=(13, 19.5))

sp1 = plt.subplot(5,1,1)
plt.gca().set_title("Propeller Power vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Power (W)")

sp2 = plt.subplot(5,1,2)
plt.gca().set_title("Propeller Power Coefficient vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Power Coefficient $C_P$")

sp3 = plt.subplot(5,1,3)
plt.gca().set_title("Propeller Thrust vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Thrust (N)")

sp4 = plt.subplot(5,1,4)
plt.gca().set_title("Propeller Thrust Coefficient vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Thrust Coefficient $C_T$")

sp5 = plt.subplot(5,1,5)
plt.gca().set_title("Propeller Efficiency vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Efficiency $\eta_p$")

for RPM in range(1500, 3500, 500):
    for ii in range(0,ll):
        atm = AtmData(Vseq[ii], h, is_SI)
        atm.expand(k, R)
        prop = Propeller(radius, numB, RPM, eta_P, CP = 0, CT = 0, CQ = 0, Cl = 0.4, bet=prop.bet, chord = prop.chord)
        J[ii], Pdesign[ii], CP[ii], Tdesign[ii], CT[ii], etap[ii] = prop_analysis(atm, prop, m0_fn, Cd_fn)
    
    sp1.plot(Vseq,Pdesign,label='RPM = {}'.format(RPM))
    sp2.plot(Vseq,CP,label='RPM = {}'.format(RPM))
    sp3.plot(Vseq,Tdesign,label='RPM = {}'.format(RPM))
    sp4.plot(Vseq,CT,label='RPM = {}'.format(RPM))
    sp5.plot(Vseq,etap,label='RPM = {}'.format(RPM))

sp1.legend()
sp2.legend()
sp3.legend()
sp4.legend()
sp5.legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.92])
plt.suptitle("Analysis of Fixed-Pitch Propeller Design with \n Various Airspeeds and RPM\n\n",fontsize=24)
plt.savefig('./Figures/fixed_pitch_analysis.png', bbox_inches='tight')
plt.show()
