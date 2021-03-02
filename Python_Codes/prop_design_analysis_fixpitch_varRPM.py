'''
prop_design_analysis
Propeller design and analysis (fixed pitch, varying RPM)

Calls:
    prop_design_TVG

Notes:

History:
    02.28.2021: 

'''

from prop_design_TVG import prop_design
from prop_analysis import prop_analysis
import numpy
import matplotlib.pyplot as plt
from Class130 import AtmData, Propeller
import sys
sys.path.append("../Utilities")
import formatfigures

# Emrax 188 Engine data (continuous performance)
# Nomeclature: enginename_voltagelevel_coolingtype
Emrax188_HV_CC = numpy.array([[0, 0],
                            [1000, 5000],
                            [2000, 10500],
                            [3000, 16000],
                            [4000, 22000],
                            [5000, 26000],
                            [6000, 28000]])

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
        prop = Propeller(radius, numB, RPM[ii], eta_P, CP=0, CT=0, CQ=0, Cl=0.4)
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

prop = Propeller(radius, numB, RPM[m], eta_P, CP=0, CT=0, CQ=0, Cl=0.4)
r, prop.chord, prop.bet, P_design, T_design, Q_design, eta_P, prop.theta = prop_design(atm, prop, T_req, m0_fn, Cd_fn)
ll = 101
Vseq = numpy.linspace(0,70,ll)

J = numpy.zeros((ll,))
Pdesign = numpy.zeros((ll,))
CP = numpy.zeros((ll,))
Tdesign = numpy.zeros((ll,))
CT = numpy.zeros((ll,))
Qdesign = numpy.zeros((ll,))
CQ = numpy.zeros((ll,))
etap = numpy.zeros((ll,))


plt.figure(figsize=(13, 19.5))

sp1 = plt.subplot(6,1,1)
plt.gca().set_title("Propeller Power vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Power (W)")

sp2 = plt.subplot(6,1,2)
plt.gca().set_title("Propeller Power Coefficient vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Power Coefficient $C_P$")

sp3 = plt.subplot(6,1,3)
plt.gca().set_title("Propeller Thrust vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Thrust (N)")

sp4 = plt.subplot(6,1,4)
plt.gca().set_title("Propeller Thrust Coefficient vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Thrust Coefficient $C_T$")

sp5 = plt.subplot(6,1,5)
plt.gca().set_title("Propeller Efficiency vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Efficiency $\eta_p$")

sp6 = plt.subplot(6,1,6)
plt.gca().set_title("Propeller Torque vs. Airspeed")
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Torque (Nm)")

for RPM in range(1500, 3500, 500):
    for ii in range(0,ll):
        atm = AtmData(Vseq[ii], h, is_SI)
        atm.expand(k, R)
        prop = Propeller(radius, numB, RPM, eta_P, CP=0, CT=0, CQ=0, Cl=0.4, chord=prop.chord, bet=prop.bet)
        J[ii], Pdesign[ii], CP[ii], Tdesign[ii], CT[ii], Qdesign[ii], CQ[ii], etap[ii] = prop_analysis(atm, prop, m0_fn, Cd_fn)
    
    sp1.plot(Vseq,Pdesign,label='RPM = {}'.format(RPM))
    sp2.plot(Vseq,CP,label='RPM = {}'.format(RPM))
    sp3.plot(Vseq,Tdesign,label='RPM = {}'.format(RPM))
    sp4.plot(Vseq,CT,label='RPM = {}'.format(RPM))
    sp5.plot(Vseq,etap,label='RPM = {}'.format(RPM))
    sp6.plot(Vseq,Qdesign,label='RPM = {}'.format(RPM))
    

sp1.legend()
sp2.legend()
sp3.legend()
sp4.legend()
sp5.legend()
sp6.legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.92])
plt.suptitle("Analysis of Fixed-Pitch Propeller Design with \n Various Airspeeds and RPM\n\n",fontsize=24)
plt.savefig('./Figures/fixed_pitch_analysis.png', bbox_inches='tight')
try:
    formatfigures.formatfigures()
    latex = True
except ValueError:
    print("Not using latex formatting")
    latex = False

# Design a propeller with the cruise conditions 
atm = AtmData(62, 6000*0.3048, is_SI)
atm.expand(1.4, 287)
prop = Propeller(radius, numB, 1800, eta_P, CP=0, CT=0, CQ=0, Cl=0.4)
r, prop.chord, prop.bet, P_design, T_design, Q_design, eta_P, prop.theta = prop_design(atm, prop, T_req, m0_fn, Cd_fn)

RPMseq = numpy.linspace(500,3000,ll)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax2 = ax1.twinx()

for v_inf in range(2,72,20):
    for ii in range(0,ll):
        atm = AtmData(v_inf, h, is_SI)
        atm.expand(k, R)
        prop = Propeller(radius, numB, RPMseq[ii], eta_P, CP=0, CT=0, CQ=0, Cl=0.4, chord=prop.chord, bet=prop.bet)
        J[ii], Pdesign[ii], CP[ii], Tdesign[ii], CT[ii], Qdesign[ii], CQ[ii], etap[ii] = prop_analysis(atm, prop, m0_fn, Cd_fn)

    ax1.plot(RPMseq,Pdesign,label='$V_\infty$ = {}'.format(v_inf))
    ax2.plot(RPMseq,Tdesign,linestyle='dashdot')

ax1.plot(Emrax188_HV_CC[0:4,0],Emrax188_HV_CC[0:4,1],label='EMRAX 188 HV, Combined Cooling',linestyle='dashed',color='black')
plt.title("Power vs. RPM for Fixed Pitch Propeller Designed for Cruise Flight at \n 1800 RPM Compared to EMRAX 188 High Voltage with Combined Cooling")
ax1.set_xlabel("RPM")
ax1.set_ylabel("-- Power (W)")
ax1.legend()
ax1.set_ylim([0, 20000])
ax1.set_xlim([1000,2500])
ax2.yaxis.set_label_position("right")
ax2.set_ylabel("$\cdot$- Thrust (N)")
plt.savefig('./Figures/fixed_pitch_Power_vs_RPM.png', bbox_inches='tight')


