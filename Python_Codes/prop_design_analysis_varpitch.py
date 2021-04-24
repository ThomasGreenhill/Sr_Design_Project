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
import scipy.interpolate as sci
import copy
from plot_propeller_3D import plot_propeller_3D

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

Emrax188_HV_CC_Q = numpy.array([[45],
                                [49],
                                [52],
                                [52.5],
                                [52],
                                [50],
                                [48]])

is_HP = False


def m0_fn(Ma):
    if numpy.any(Ma <= 0.9):
        return (2 * numpy.pi) / numpy.sqrt(1 - Ma ** 2)
    else:
        return (2 * numpy.pi) / numpy.sqrt(1 - 0.9 ** 2)


def Cd_fn(Cl):
    return 0.0095 + 0.0040 * (Cl - 0.2) ** 2


# Variable pitch analysis
# Design a propeller
diameter = 1.78
radius = diameter / 2
LD = 15  # Assumed
is_SI = True

# 3 Blades
numB = 3

# Design condition
T_req = 13000 / (8) * 1.2 * 0.601  # N (TOGW/(L/D))
Cl = 0.4
alp0 = numpy.radians(-2)

v_hover = 2.54
v_cruise = 62
v_design = 30
atm = AtmData(v_design, 0, is_SI)
atm.expand(1.4, 287)
v_seq = numpy.arange(-10, 68, 2)
ll = numpy.size(v_seq)

Design_RPM = 3000

prop = Propeller(radius, numB, Design_RPM, eta_P=0, CP=0, CT=0, CQ=0, Cl=Cl)
r, prop.chord, prop.bet, P_design, T_design, Q_design, eta_P, prop.theta = prop_design(atm, prop, T_req, m0_fn, Cd_fn)

num_len = len(prop.bet)
beta_75_index = int(num_len * 0.75)
x = numpy.linspace(0, 1, num_len)
x_need = x[x >= 0.15]
c_need = prop.chord[x >= 0.15]
AF = 10 ** 5 / 16 * numpy.trapz(c_need / diameter * x_need ** 3, x_need)  # activity factor
CL_design = 4 * numpy.trapz(Cl * x_need ** 3, x_need)
print('====================== Propeller Design Parameters ======================')
print("Beta angle at 75% is {:.5f} degree".format(numpy.rad2deg(prop.bet[beta_75_index])))
print("Activity factor is {:.2f}, which corresponds to {:.2f} in openVSP (Source checked)".format(AF, AF * 2))
print("CL_design is {:.2f}".format(CL_design))

"""
# Plot the propeller design
in_line = [0] * len(r)
# in_line = 0.15*r**2
show = False
save = True
path = './Figures/Prop3Dplot.png'
plot_propeller_3D(r, prop.chord, prop.bet, prop, in_line, show, save, path)

print("The required power for the propeller design at the design condition with \nv_design = " + str(
    v_design) + " is P_design = " + str(P_design))
print("Adjusting the engine power curve accordingly...")
Emrax188_HV_CC_mod = copy.deepcopy(Emrax188_HV_CC)
Emrax188_HV_CC_mod[:, 1] = P_design / Emrax188_HV_CC[3, 1] * Emrax188_HV_CC[:, 1]
print("Adjusting the engine torque curve accordingly...")
Emrax188_HV_CC_mod_Q = Q_design / Emrax188_HV_CC_Q[3, 0] * Emrax188_HV_CC_Q[:, 0]

plt.show()
"""

"""
# Set the cruise RPM to something lower, say 1500 at cruise and make an inline function to determine propeller RPM at any airspeed
Cruise_RPM = 1000
RPM_fn = lambda v: (Cruise_RPM - Hover_RPM) / (v_cruise - v_hover) * (v - v_hover) + Hover_RPM

J_var = [0] * ll
P_design_var = [0] * ll
T_design_var = [0] * ll
Q_design_var = [0] * ll
eta_P_var = [0] * ll
d_bet = [0] * ll

# Prepare the figures
plt.figure(figsize=(13, 17))

sp1 = plt.subplot(3, 1, 1)
plt.xlabel("Inlet Airspeed (m/s)")
plt.ylabel("Propeller Thrust (N)")
plt.gca().set_title("Thrust vs. Inlet Airspeed")

# sp2 = plt.subplot(3, 1, 2)
# plt.xlabel("Inlet Airspeed (m/s)")
# plt.ylabel("Propeller Torque (Nm)")
# plt.gca().set_title("Torque vs. Inlet Airspeed")

# sp3 = plt.subplot(3, 1, 3)
# plt.xlabel("Inlet Airspeed (m/s)")
# plt.ylabel("Propeller Power (W)")
# plt.gca().set_title("Power vs. Inlet Airspeed")

sp4 = plt.subplot(3, 1, 2)
plt.xlabel("Inlet Airspeed (m/s)")
plt.ylabel("Propeller Efficiency $\eta_p$")
plt.gca().set_title("Propeller Efficiency vs. Inlet Airspeed")

sp5 = plt.subplot(3, 1, 3)
plt.xlabel("Inlet Airspeed (m/s)")
plt.ylabel(r"Pitch Variation $\Delta_\beta$ (deg)")
plt.gca().set_title("Propeller Pitch Variation vs. Inlet Airspeed")

# Analyze the propeller with the variable pitch propeller function
# Plotting with several different RPM values
lstyles = ["-", "--", "-.", ":", "-", "--", "-.", ":"]
jj = 0
for RPM in range(500, 3500, 500):
    for ii in range(ll):
        prop.RPM = RPM
        J_var[ii], P_design_var[ii], T_design_var[ii], Q_design_var[ii], eta_P_var[ii], d_bet[
            ii] = prop_analysis_var_pitch(v_seq[ii], v_design, Emrax188_HV_CC_mod, is_HP, atm, prop, m0_fn, Cd_fn)
    sp1.plot(v_seq, T_design_var, lstyles[jj], label='RPM = {}'.format(RPM))
    # sp2.plot(v_seq, Q_design_var,label='RPM = {}'.format(RPM))
    # sp3.plot(v_seq, P_design_var,label='RPM = {}'.format(RPM))
    sp4.plot(v_seq, eta_P_var, lstyles[jj], label='RPM = {}'.format(RPM))
    sp5.plot(v_seq, d_bet, lstyles[jj], label='RPM = {}'.format(RPM))
    jj += 1

sp1.legend()
# sp2.legend()
# sp3.legend()
sp4.legend()
sp5.legend()

plt.tight_layout(rect=(0, 0.03, 1, 0.95))
plt.suptitle(
    "Analysis of Variable-Pitch Propeller Design (Single Rotor) with \n Varying RPM and Airspeeds at the Propeller Inlet ",
    fontsize=24)
plt.savefig('./Figures/variable_pitch_analysis_trunc.png', bbox_inches='tight')

# Plotting for motor selection (vin held constant with RPM sweep)

plt.figure(figsize=(13, 17))
sp1 = plt.subplot(3, 1, 1)
plt.xlabel("Rotor Angular Rate (RPM)")
plt.ylabel("Propeller Thrust (N)")
plt.gca().set_title("Thrust vs. Rotor Angular Rate")

sp2 = plt.subplot(3, 1, 2)
plt.xlabel("Rotor Angular Rate (RPM)")
plt.ylabel("Propeller Torque (Nm)")
plt.gca().set_title("Torque vs. Rotor Angular Rate")

sp3 = plt.subplot(3, 1, 3)
plt.xlabel("Rotor Angular Rate (RPM)")
plt.ylabel("Propeller Power (W)")
plt.gca().set_title("Power vs. Inlet Rotor Angular Rate")

RPM = numpy.linspace(500, 3000, ll)

jj = 0
for v_in in range(2, 76, 16):
    for ii in range(ll):
        prop.RPM = copy.deepcopy(RPM[ii])
        J_var[ii], P_design_var[ii], T_design_var[ii], Q_design_var[ii], eta_P_var[ii], d_bet[
            ii] = prop_analysis_var_pitch(v_in, v_design, Emrax188_HV_CC_mod, is_HP, atm, prop, m0_fn, Cd_fn)
    sp1.plot(RPM, T_design_var, lstyles[jj], label=r'$Vin = {}$ m/s'.format(v_in))
    jj += 1

sp2.plot(RPM, Q_design_var, label='Propeller')
sp3.plot(RPM, P_design_var, label='Propeller')

x = numpy.flip(Emrax188_HV_CC_mod[:, 0], 0)
P = numpy.flip(Emrax188_HV_CC_mod[:, 1], 0)
Q = Emrax188_HV_CC_mod_Q

xx = numpy.linspace(x.min(), x.max(), 100)
PP = sci.CubicSpline(x, P)
QQ = sci.CubicSpline(x, Q)

nn = 3
frac = numpy.linspace(1, 0.9, nn)

for jj in range(nn):
    sp2.plot(xx, QQ(xx) * frac[jj], lstyles[jj], label='{}\% of Max Continuous (Motor)'.format(int(frac[jj] * 100)),
             linestyle='dashed')

sp3.plot(xx, PP(xx) * 1, label='{}\% of Max Continuous (Motor)'.format(int(100)), linestyle='dashed')
sp1.legend()
sp2.legend()
sp3.legend()
sp2.set_xlim((0, 3000))
sp3.set_xlim((0, 3000))

plt.tight_layout(rect=(0, 0.03, 1, 0.95))
plt.suptitle(
    "Analysis of Variable-Pitch Propeller Design (Single Rotor) with \n Varying RPM and Airspeeds at the Propeller Inlet, Compared to Engine Performance ",
    fontsize=24)
plt.savefig('./Figures/variable_pitch_and_motor.png', bbox_inches='tight')

try:
    import formatfigures

    formatfigures.formatfigures()
    latex = True
except:
    pass
    print("Not using latex formatting")
    latex = False

plt.figure(figsize=(14, 12))
plt.subplot(2, 1, 1)
plt.plot(xx, PP(xx))
plt.xlabel("Angular Rate (RPM) ")
plt.ylabel("Power (W)")

plt.title("Required Torque vs. Angular Rate for General 3-Phase Motor \n Based on EMRAX 188C Motor")

plt.subplot(2, 1, 2)
plt.plot(xx, QQ(xx))
plt.xlabel("Angular Rate (RPM) ")
plt.ylabel("Torque (Nm)")

plt.tight_layout()
plt.savefig('./Figures/motor_performance_required.png', bbox_inches='tight')

plt.show()
"""