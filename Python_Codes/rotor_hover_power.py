import numpy
import sympy

def rotor_hover_power(Thrust, alpha, f_body, r_list, Cd_list, chord_list, AtmData, Propeller):
    """
    Calculates the total rotor power related to hte thrust generation
    based on P_parasitic-body, P_profile-rotor, P_induced-rotor, and P_climb

    Input:
            Thrust: (N) propeller thrust
            alpha: (deg) angle bt. rotor platform and free stream (90 as perpendicular)
            f_body: (m^2) equivalent flat plate area of the body
            r_list: (0 ~ 1) list of sectional radius r normalized by total radius R
            Cd_list: list of sectional drag coefficient of propeller
            chord_list: (m) list of sectional chord lengths

    Output:
            P_total: (W) total rotor power

    Calls:
        {None}

    Note:

    History:
            03.03.2021, XT. Created
    """
    # P_parasitic-body
    v_inf = AtmData.vel
    P_parasitic = f_body * 0.5 * AtmData.dens * v_inf ** 2

    # P_profile-rotor
    if len(r_list) == 1:
        raise Exception("Error: Please provide a list (min: 0, max: 1) for the variable r_list")
    if len(r_list) != len(Cd_list):
        raise Exception("Error: Size of r_list and Cd_list should match.")
    V_T = Propeller.RPM * Propeller.radius
    rot_adv_ratio = v_inf / V_T
    v_bar3 = [0] * len(r_list)
    integ_val = [0] * len(r_list)
    for i, x_loc in enumerate(r_list):
        v_bar3[i] = x_loc**3 * V_T**3 + (3/2) * x_loc * V_T**3 * rot_adv_ratio**2
        integ_val[i] = Cd_list[i] * 0.5 * AtmData.dens * v_bar3[i] * chord_list[i]
    P_profile = Propeller.numB * numpy.trapz(integ_val, r_list)


    # P_induced-rotor
    A = numpy.pi * Propeller.radius ** 2
    a4 = 1
    a3 = -2 * v_inf * numpy.sin(numpy.deg2rad(alpha))
    a2 = v_inf ** 2
    a1 = 0
    a0 = -1 * (Thrust / (2 * AtmData.dens * A)) ** 2

    w = sympy.Symbol('w')
    w_sol = sympy.solvers.solve(a4 * w**4 + a3 * w**3 + a2 * w**2 + a1 * w + a0, w)

    