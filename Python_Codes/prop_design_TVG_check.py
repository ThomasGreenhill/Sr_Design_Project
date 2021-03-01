

import numpy
import math
import prop_design_TVG
from Class130 import AtmData, Propeller

# History: 
#   02.14.2021: Created by XT using climb design conditions
#   02.15.2021: Modified by TVG using cruise design conditions for cross-checking against project 2 results. Passed check
#   02.28.2021: Modified by TVG to refelect changes in prop_design_TVG.py


# Check script
def m0_fn(Ma):
    if Ma <= 0.9:
        return (2 * math.pi) / numpy.sqrt(1 - Ma ** 2)
    else:
        return (2 * math.pi) / numpy.sqrt(1 - 0.9 ** 2)

def Cd_fn(Cl):
    return 0.0095 + 0.0040 * (Cl - 0.2) ** 2
    
v_inf = 156 * 0.514444
h = 2438.4
visc = 3E-6
k = 1.4
R = 287
is_SI = True
atm_check = AtmData(v_inf, h, is_SI)
atm_check.expand(1.4, 287)
dens = atm_check.dens
radius = 41 * 0.0254
RPM = 2400
CT = 0.0509
T_req = CT*dens*(RPM/60)**2*(radius*2)**4
# T_req = 425.6896 * 4.44822
Cl = 0.4
numB = 3
alp0 = numpy.radians(-2)
prop_check = Propeller(radius, numB, RPM, eta_P=0, CP=0, CT=0, CQ=0, Cl=0.4)

[r, prop_check.chord, prop_check.beta, P_design, T_design, Q_design, eta_P, prop_check.theta] = prop_design_TVG.prop_design(atm_check, prop_check, T_req, m0_fn, Cd_fn)
print(P_design * 0.00134102)
print(T_design)
print(T_req)

