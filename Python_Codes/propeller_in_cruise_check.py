
import numpy
from propeller_in_cruise import propeller_in_cruise
from Class130 import AtmData, Wing, Propeller

# History:
#   02.14.2021: Created by XT
#   02.15.2021: Reviewed for bugs by TVG but not compared to literature values

# Test A, constant Cl and airspeed, numbers from lecture 01.27.2021
const_logic = [True, True, False]
W_initial = 2500 * 4.4482216153     # lbf to N
W_final = 2215 * 4.4482216153       # lbf to N
vel = 124 * 0.514444                # m/s
c_p = 0.51 / (1980000 * 0.3048)     # lb/(hp*hr) to 1/ft to 1/m
eta_P = 0.85
CD_0 = 0.0340
CL = 0.305
CD = 0.0401
# Just to make class work
area = 200 * 0.092903   # ft^2 to m^2
span = 1 / (numpy.pi * 0.0657)
e = 1

atm = AtmData(vel, 'temp', 'pres', 'dens', 'visc', 'k', 'R', 'is_SI')
wing = Wing(area, span, e, 'alpha', 'chord', 'c_bar', CL, 'CL_max', CD, CD_0, 'airfoil')
prop = Propeller('radius', 'RPM', eta_P, 'CP', 'CT', 'CQ', 'Cl = 0.4', 'chord = 1', 'numB = 3', 'alp0 = 0',
'alpha = None', 'beta = None', 'theta = None', 'phi = None')

R, E = propeller_in_cruise(W_initial, W_final, c_p, atm, prop, wing, const_logic)

R *= 0.000539957        # m to nmi
E /= 3600               # s to hr

#print(R)    # should be ~500 nmi
#print(E)    # should be ~4.03 hr
# Checked!


# Test B, constant Cl and altitude, numbers from lecture 01.27.2021
const_logic = [True, False, True]
W_initial = 2500 * 4.4482216153     # lbf to N
W_final = 2215 * 4.4482216153       # lbf to N
area = 200 * 0.092903   # ft^2 to m^2
vel = 124 * 0.514444    # m/s
dens = 0.962870         # kg/m^3
c_p = 0.51 / (1980000 * 0.3048)     # lb/(hp*hr) to 1/ft to 1/m
eta_P = 0.85
CD_0 = 0.0340
CL = 0.305
CD = 0.0401
# Just to make class work
span = 1 / (numpy.pi * 0.0657)
e = 1


atm = AtmData(vel, 'temp', 'pres', dens, 'visc', 'k', 'R', 'is_SI')
wing = Wing(area, span, e, 'alpha', 'chord', 'c_bar', CL, 'CL_max', CD, CD_0, 'airfoil')
prop = Propeller('radius', 'RPM', eta_P, 'CP', 'CT', 'CQ', 'Cl = 0.4', 'chord = 1', 'numB = 3', 'alp0 = 0',
'alpha = None', 'beta = None', 'theta = None', 'phi = None')

R, E = propeller_in_cruise(W_initial, W_final, c_p, atm, prop, wing, const_logic)

R *= 0.000539957        # m to nmi
E /= 3600               # s to hr

#print(R)    # should be ~500 nmi
#print(E)    # should be ~4.13 hr (got 4.15 hr)
# Checked! not ideal but very close


# Test C, constant airspeed and altitude, numbers from lecture 01.27.2021
const_logic = [False, True, True]
W_initial = 2500 * 4.4482216153     # lbf to N
W_final = 2215 * 4.4482216153       # lbf to N
area = 200 * 0.092903   # ft^2 to m^2
vel = 124 * 0.514444    # m/s
dens = 0.962870         # kg/m^3
c_p = 0.51 / (1980000 * 0.3048)     # lb/(hp*hr) to 1/ft to 1/m
eta_P = 0.85
CD_0 = 0.0340
CL = 0.305
CD = 0.0401
span = 1 / (numpy.pi * 0.0657)
e = 1


atm = AtmData(vel, 'temp', 'pres', dens, 'visc', 'k', 'R', 'is_SI')
wing = Wing(area, span, e, 'alpha', 'chord', 'c_bar', CL, 'CL_max', CD, CD_0, 'airfoil')
prop = Propeller('radius', 'RPM', eta_P, 'CP', 'CT', 'CQ', 'Cl = 0.4', 'chord = 1', 'numB = 3', 'alp0 = 0',
'alpha = None', 'beta = None', 'theta = None', 'phi = None')

R, E = propeller_in_cruise(W_initial, W_final, c_p, atm, prop, wing, const_logic)

R *= 0.000539957        # m to nmi
E /= 3600               # s to hr

print(R)
print(E)
# Checked! No reference from lecture, but the value sits within expected range