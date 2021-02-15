
# Check VTOL_power_req
import numpy
from VTOL_power_req import VTOL_power_req
from Class130 import AtmData, Propeller

# atm data
v_inf = 87 * 0.514444
temp = 288
pres = 101250
dens = 1.225
visc = 3E-6
k = 1.4
R = 287
is_SI = True
atm_check = AtmData(v_inf, temp, pres, dens, visc, k, R, is_SI)

# prop. data
radius = 41 * 0.0254
RPM = 1854.4805
Cl = 0.4
numB = 3
alp0 = numpy.radians(-2)
prop_check = Propeller(radius, RPM, Cl, "chord", numB, alp0)

# function call
m = 1893.560992512 / 9.81       # Same weight as thrust used to check prop_design
g_factor = 1
mot_distr = 1
power_vec, eta_vec = VTOL_power_req(m, g_factor, mot_distr, AtmData, prop_check)
print(power_vec)