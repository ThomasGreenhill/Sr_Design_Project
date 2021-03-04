"""
prop_design_analysis_varpitch
Propeller design and analysis (variable pitch, variable airspeed)

Calls:
    prop_design_TVG

Notes:

History:
    02.28.2021: TG. Created
    03.02.2021: XT. Changed for the purpose of debugging

"""

from prop_design_TVG import prop_design
from prop_analysis_var_pitch import prop_analysis_var_pitch
import numpy
import matplotlib.pyplot as plt
from Class130 import AtmData, Propeller
import sys

sys.path.append("../Utilities")

try:
    import formatfigures
    formatfigures.formatsubfigures()
    latex = True
except:
    pass
    print("Not using latex formatting")
    latex = False

# Emrax 188 Engine data (continuous performance)
# Nomeclature: enginename_voltagelevel_coolingtype
Emrax188_HV_CC = numpy.flip(numpy.array([[0, 0],
                                         [1000, 5000],
                                         [2000, 10500],
                                         [3000, 16000],
                                         [4000, 22000],
                                         [5000, 26000],
                                         [6000, 28000]]), 0)

is_HP = False


def m0_fn(Ma):
    if numpy.any(Ma <= 0.9):
        return (2 * numpy.pi) / numpy.sqrt(1 - Ma ** 2)
    else:
        return (2 * numpy.pi) / numpy.sqrt(1 - 0.9 ** 2)


def Cd_fn(Cl):
    return 0.0095 + 0.0040 * (Cl - 0.2) ** 2


# Variable pitch analysis
# Design a propeller with the hover conditions 
radius = 1.78 / 2
LD = 15
is_SI = True
numB = 3
T_req = 13000 / 8 * 1.2  # N (TOGW/(L/D))
Cl = 0.4
alp0 = numpy.radians(-2)
#v_design = 30  # IDK why I'm choosing this, lol. Just trying to debug since the code isn't behaving
v_hover = 2.54
v_cruise = 62
v_design = v_hover
atm = AtmData(v_design, 0, is_SI)
atm.expand(1.4, 287)
#v_seq = numpy.arange(0, 72, 2)
v_seq = numpy.arange(0, 68, 2)  ### Changed by XT
ll = numpy.size(v_seq)
Hover_RPM = 3000

prop = Propeller(radius, numB, Hover_RPM, eta_P=0, CP=0, CT=0, CQ=0, Cl=0.4)
r, prop.chord, prop.bet, P_design, T_design, Q_design, eta_P, prop.theta = prop_design(atm, prop, T_req, m0_fn, Cd_fn)

print("The required power for the propeller design at the design condition with \nv_design = " + str(v_design) + " is P_design = " + str(P_design))
print("Adjusting the engine power curve accordingly...")
Emrax188_HV_CC_mod = Emrax188_HV_CC
Emrax188_HV_CC_mod[:,1] = P_design/Emrax188_HV_CC[3,1]*Emrax188_HV_CC[:,1]

# Set the cruise RPM to something lower, say 1500 at cruise and make an inline function to determine propeller RPM at any airspeed
Cruise_RPM = 1000
RPM_fn = lambda v: (Cruise_RPM-Hover_RPM)/(v_cruise-v_hover)*(v-v_hover) + Hover_RPM

J_var = [0] * ll
P_design_var = [0] * ll
T_design_var = [0] * ll
Q_design_var = [0] * ll
eta_P_var = [0] * ll
deta_P = [0] * ll
dT = [0] * ll
delta_bet = [0] * ll
RPM_fix = [0] * ll

# Prepare the figures
plt.figure(figsize=(13, 19.5))

sp1 = plt.subplot(5, 1, 1)
plt.xlabel("Inlet Airspeed (m/s)")
plt.ylabel("Propeller Thrust (N)")
plt.gca().set_title("Thrust vs. Inlet Airspeed")

sp2 = plt.subplot(5, 1, 2)
plt.xlabel("Inlet Airspeed (m/s)")
plt.ylabel("Propeller Torque (Nm)")
plt.gca().set_title("Torque vs. Inlet Airspeed")

sp3 = plt.subplot(5, 1, 3)
plt.xlabel("Inlet Airspeed (m/s)")
plt.ylabel("Propeller Power (W)")
plt.gca().set_title("Power vs. Inlet Airspeed")

sp4 = plt.subplot(5, 1, 4)
plt.xlabel("Inlet Airspeed (m/s)")
plt.ylabel("Propeller Efficiency $\eta_p$")
plt.gca().set_title("Propeller Efficiency vs. Inlet Airspeed")

sp5 = plt.subplot(5, 1, 5)
plt.xlabel("Inlet Airspeed (m/s)")
plt.ylabel(r"Pitch Variation $\delta_\beta$ (deg)")
plt.gca().set_title("Propeller Pitch Variation vs. Inlet Airspeed")

# Analyze the propeller with the variable pitch propeller function
for RPM in range(1000, 4000, 500):
    for ii in range(ll):
        prop.RPM = RPM
        J_var[ii], P_design_var[ii], T_design_var[ii], Q_design_var[ii], eta_P_var[ii], deta_P[ii], dT[ii], delta_bet[ii], RPM_fix[
            ii] = prop_analysis_var_pitch(v_seq[ii], v_design, Emrax188_HV_CC_mod, is_HP, atm, prop, m0_fn, Cd_fn)
    sp1.plot(v_seq, T_design_var,label='RPM = {}'.format(RPM))
    sp2.plot(v_seq, Q_design_var,label='RPM = {}'.format(RPM))
    sp3.plot(v_seq, P_design_var,label='RPM = {}'.format(RPM))
    sp4.plot(v_seq, eta_P_var,label='RPM = {}'.format(RPM))
    sp5.plot(v_seq, delta_bet,label='RPM = {}'.format(RPM))

sp1.legend()
sp2.legend()
sp3.legend()
sp4.legend()
sp5.legend()

plt.tight_layout(rect=(0, 0.03, 1, 0.95))
plt.suptitle("Analysis of Variable-Pitch Propeller Design (Single Rotor) with \n Varying RPM and Airspeeds at the Propeller Inlet ", fontsize=24)
plt.savefig('./Figures/variable_pitch_analysis.png', bbox_inches='tight')

plt.show()