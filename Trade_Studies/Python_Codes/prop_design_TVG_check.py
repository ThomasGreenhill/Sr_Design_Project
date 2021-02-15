

import numpy
import math
import prop_design_TVG
from Class130 import AtmData, Propeller


# Check script
v_inf = 87 * 0.514444
temp = 288
pres = 101250
dens = 1.225
visc = 3E-6
k = 1.4
R = 287
is_SI = True
atm_check = AtmData(v_inf, temp, pres, dens, visc, k, R, is_SI)

radius = 41 * 0.0254
RPM = 1854.4805
T_req = 425.6896 * 4.44822
Cl = 0.4
numB = 3
alp0 = numpy.radians(-2)
prop_check = Propeller(radius, RPM, Cl, "chord", numB, alp0)

[r, prop_check.chord, prop_check.beta, P_design, T_design, Q_design, eta_P, prop_check.theta] = prop_design_TVG.prop_design(AtmData, Propeller, T_req)
print(P_design * 0.00134102)
print(T_design)
print(T_req)

