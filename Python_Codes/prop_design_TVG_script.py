import numpy
import math
import prop_design_TVG
from Class130 import AtmData, Propeller
import matplotlib.pyplot as plt


# History: 02.14.2021: Created by XT using climb design conditions 02.15.2021: Modified by TVG using cruise design
# conditions for cross-checking against project 2 results. Passed check 02.28.2021: Modified by TVG to refelect
# changes in prop_design_TVG.py


# Check script
def m0_fn(Ma):
    if Ma <= 0.9:
        return (2 * math.pi) / numpy.sqrt(1 - Ma ** 2)
    else:
        return (2 * math.pi) / numpy.sqrt(1 - 0.9 ** 2)


def Cd_fn(Cl):
    return 0.0095 + 0.0040 * (Cl - 0.2) ** 2


# The following code is for propeller design in openVSP
# 04.21.2021 by XT.

# atmospheric parameters
v_inf = 121 * 0.514444
h = 0  # sea level assumed
is_SI = True
atm_check = AtmData(v_inf, h, is_SI)
k = 1.4
R = 287
atm_check.expand(1.4, 287)

# propeller parameters
radius = 1.78 / 2  # m
RPM = 2400
T_req = 1170.0  # N
numB = 3
alp0 = numpy.deg2rad(-2)
prop_check = Propeller(radius, numB, RPM, eta_P=0, CP=0, CT=0, CQ=0, Cl=0.4)

# calling propeller design function
[r, prop_check.chord, prop_check.beta, P_design, T_design, Q_design, eta_P,
 prop_check.theta] = prop_design_TVG.prop_design(atm_check, prop_check, T_req, m0_fn, Cd_fn)

beta_length = len(prop_check.beta)
beta_index_75 = round(beta_length * 0.75)
print("Beta angle (deg) at 75% chord length is {:.2f}".format(numpy.rad2deg(prop_check.beta[beta_index_75])))
