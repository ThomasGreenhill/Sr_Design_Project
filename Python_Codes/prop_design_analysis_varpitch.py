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
# import formatfigures
'''
try:
    formatfigures.formatsubfigures()
    latex = True
except ValueError:
    print("Not using latex formatting")
    latex = False
'''
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
T_req = 13000 / 8 * 2  # N (TOGW/(L/D))
Cl = 0.4
alp0 = numpy.radians(-2)
#v_design = 30  # IDK why I'm choosing this, lol. Just trying to debug since the code isn't behaving
v_design = 60   ### changed by XT
atm = AtmData(v_design, 6000 * 0.3048, is_SI)
atm.expand(1.4, 287)
#v_seq = numpy.arange(0, 72, 2)
v_seq = numpy.arange(0, 75, 5)  ### Changed by XT
prop = Propeller(radius, numB, 3000, eta_P=0, CP=0, CT=0, CQ=0, Cl=0.4)
r, prop.chord, prop.bet, P_design, T_design, Q_design, eta_P, prop.theta = prop_design(atm, prop, T_req, m0_fn, Cd_fn)

ll = numpy.size(v_seq)

'''
J_var = numpy.zeros((ll,))
P_design_Var = numpy.zeros((ll,))
T_design_var = numpy.zeros((ll,))
eta_P_var = numpy.zeros((ll,))
deta_P = numpy.zeros((ll,))
dT = numpy.zeros((ll,))
delta_bet = numpy.zeros((ll,))
RPM_fix = numpy.zeros((ll,))
'''
### Changed to [0] * ll for quicker allocation
J_var = [0] * ll
P_design_Var = [0] * ll
T_design_var = [0] * ll
eta_P_var = [0] * ll
deta_P = [0] * ll
dT = [0] * ll
delta_bet = [0] * ll
RPM_fix = [0] * ll

# Analyze the propeller with the variable pitch propeller function
for ii in range(ll):
    J_var[ii], P_design_Var[ii], T_design_var[ii], eta_P_var[ii], deta_P[ii], dT[ii], delta_bet[ii], RPM_fix[
        ii] = prop_analysis_var_pitch(v_seq[ii], Emrax188_HV_CC, is_HP, atm, prop, m0_fn, Cd_fn)

### Following is changed by XT, see original commented out below
plt.figure(figsize=(13, 19.5))
plt.subplot(4, 1, 1)
plt.plot(v_seq, P_design_Var)
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Power (W)")
plt.gca().set_title("Power vs. Airspeed")

plt.subplot(4, 1, 2)
plt.plot(v_seq, T_design_var)
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Thrust (N)")
plt.gca().set_title("Thrust vs. Airspeed")

plt.subplot(4, 1, 3)
plt.plot(v_seq, eta_P_var)
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Efficiency eta_p")
plt.gca().set_title("Propeller Efficiency vs. Airspeed")

plt.subplot(4, 1, 4)
plt.plot(v_seq, delta_bet)      ### Fixed list / float issue, simplified by XT (changed to already deg from function)
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Pitch Variation delta_beta (deg)")
plt.gca().set_title("Propeller Pitch Variation vs. Airspeed")

plt.tight_layout(rect=(0, 0.03, 1, 0.92))
plt.suptitle("Analysis of Variable-Pitch Propeller Design with \n Various Airspeeds ", fontsize=24)
plt.savefig('./Figures/variable_pitch_analysis.png', bbox_inches='tight')

plt.show()

### Original plot codes (I don't have latex so I pasted to avoid overwriting)
'''
plt.figure(figsize=(13, 19.5))
plt.subplot(4,1,1)
plt.plot(v_seq,P_design_Var)
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Power (W)")
plt.gca().set_title("Power vs. Airspeed")

plt.subplot(4,1,2)
plt.plot(v_seq,T_design_var)
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Thrust (N)")
plt.gca().set_title("Thrust vs. Airspeed")

plt.subplot(4,1,3)
plt.plot(v_seq,eta_P_var)
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Propeller Efficiency $\eta_p$")
plt.gca().set_title("Propeller Efficiency vs. Airspeed")

plt.subplot(4,1,4)
plt.plot(v_seq,delta_bet*180/numpy.pi)
plt.xlabel("Airspeed (m/s)")
# plt.ylabel("Pitch Variation $\delta_{\beta}$")
plt.gca().set_title("Propeller Pitch Variation vs. Airspeed")

plt.tight_layout(rect=[0, 0.03, 1, 0.92])
plt.suptitle("Analysis of Variable-Pitch Propeller Design with \n Various Airspeeds ",fontsize=24)
plt.savefig('./Figures/variable_pitch_analysis.png', bbox_inches='tight')

plt.show()
'''
