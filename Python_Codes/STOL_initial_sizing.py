
import numpy
from std_atm import std_atm
from Class130 import AtmData

# FAR 23 only, Based on 02.09.2021 lecture


def STOL_initial_sizing(v_stall_TO, sigma, CL_max, S_TO, S_L, atm_TO, atm_L):
    # return wing_load_TO, wing_load_L, weight_power_TO

    # Now working in British unit
    S_TO_Brit = S_TO * 3.28084      # m to ft
    S_L_Brit = S_L * 3.28084        # m to ft

    # Stall Speed Sizing
    wing_load_TO = v_stall_TO ** 2 * atm_TO.dens * CL_max / 2    # N/m^2
    wing_load_TO_Brit = wing_load_TO * (0.224809 / 3.28084 ** 2)              # to lbf/ft^2

    # Takeoff
    a1 = 8.134      # ft^3 hp / lbf^2
    a2 = 0.0149     # ft^5 hp^2 / lbf^4

    TOP23 = [0] * 2
    delta = a2 ** 2 - 4 * a1 * (-S_TO_Brit)
    tol = 1E-06

    # Check real
    if delta > 0:
        TOP23[0] = (-a2 + numpy.sqrt(delta)) / (2 * a1)
        TOP23[1] = (-a2 - numpy.sqrt(delta)) / (2 * a1)

        # Check positive num
        if TOP23[0] > 0 >= TOP23[1]:
            TOP23_val = TOP23[0]
        elif TOP23[0] <= 0 < TOP23[1]:
            TOP23_val = TOP23[1]
        elif TOP23[0] > 0 and TOP23[1] > 0:
            print("Error: TOP23 has two positive roots")
            return
        else:
            print("Error: TOp23 has two negative roots")
            return

    elif abs(delta) <= tol:
        TOP23_val = numpy.mean(TOP23)
        if TOP23_val <= 0:
            print("Error: TOP23 has one negative root")
            return

    else:   # imaginary
        print("Error: No real root for TOP23")
        return

    weight_power_Brit = TOP23_val / wing_load_TO_Brit * sigma * CL_max      # lbf / hp
    weight_power_TO = weight_power_Brit * 4.44822                           # N / hp

    # Landing
    a4 = 0.5136                 # ft/knots^2
    v_stall_L = numpy.sqrt(S_L_Brit / a4)   # knots
    v_stall_L *= 0.514444                   # knots to m/s
    wing_load_L = v_stall_L ** 2 * atm_L.dens * CL_max / 2

    return wing_load_TO, wing_load_L, weight_power_TO
