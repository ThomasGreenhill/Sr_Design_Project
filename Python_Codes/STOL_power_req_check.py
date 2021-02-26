
# Check STOL_power_req
import numpy
from STOL_power_req import STOL_power_req
from Class130 import AtmData, Wing, Propeller

# History:
#   02.14.2021: Created by XT
#   02.15.2021: Reviewed by TVG. 
#       Changed line 32 to reflect changes in Wing class (added alpha and CD as dummy values). 
#       Not verified relative to literature values


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

# wing data
area = 16
span = 5
e = 0.9
CL_max = 2.1

wing_check = Wing(area, span, e, "alpha", "chord", 1, 1, CL_max, "CD", "CD_0", "airfoil")

# function call
m = 6000
mot_distr = [1,1]
print(numpy.size(mot_distr))
dist_to = 2000
power_vec = STOL_power_req(m, dist_to, mot_distr, atm_check, wing_check, prop_check)
print(power_vec)

a = power_vec[0] / 2
print(a)