
from STOL_initial_sizing import STOL_initial_sizing
from std_atm import std_atm
from Class130 import AtmData

v_stall_TO = 61 * 0.514444     # m/s, stall airspeed
sigma = 1
vel = v_stall_TO
h = 0                       # m, sea level
is_SI = True
k = 1.4
R = 287
S_TO = 1000     # m
S_L = 1000      # m
sigma = 1
CL_max = 2.0

print(v_stall_TO)


temp, pres, dens, c_sound, visc, g = std_atm(h, is_SI)
atm_TO = AtmData(vel, temp, pres, dens, visc, k, R, is_SI)
atm_L = AtmData(vel, temp, pres, dens, visc, k, R, is_SI)

wing_load_TO, wing_load_L, weight_power_TO = STOL_initial_sizing(v_stall_TO, sigma, CL_max, S_TO, S_L, atm_TO, atm_L)


print(wing_load_TO)
print(wing_load_L)
print(weight_power_TO)