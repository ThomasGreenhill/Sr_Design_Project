import numpy
import sys
from Class130 import AtmData, Propeller

sys.path.append("../Utilities")
import newton


def rotor_hover_power(Weight, gamma, num_rotor, f_body, AtmData, Propeller):
    """
    Calculates the total rotor power related to hte thrust generation
    based on P_parasitic-body, P_profile-rotor, P_induced-rotor, and P_climb

    Input:
            Weight: (N) aircraft weight
            gamma: (deg) angle btw. v_inf and the horizon
            num_rotor: number of rotors
            f_body: (m^2) equivalent flat plate area of the body
            AtmData: need vel, dens, visc, sound_speed
            Propeller: need radius, numB, c_bar

    Output:
            P_aero: (W) total rotor power
            Propeller assigned Cl_bar

    Calls:
        {None}

    Note:
            1. Can include improvement to accommodate motor thrust distribution if needed

    History:
            03.03.2021, XT. Created
            03.04.2021, XT. ****Debugging not finished!!
    """
    # General
    K_induced = 1.15  # typicaly 1.13 - 1.15, pick largest for safety
    c_bar = Propeller.c_bar
    if c_bar is None:
        raise TypeError("Please remember to set c_bar into Propeller class")
    v_inf = AtmData.vel
    q_inf = 0.5 * AtmData.dens * v_inf**2
    D_body = f_body * q_inf
    Thrust = numpy.sqrt(D_body ** 2 + Weight ** 2 + 2 * D_body * Weight * numpy.sin(numpy.deg2rad(gamma)))
    alpha = numpy.rad2deg(numpy.arctan((-D_body - Weight * numpy.sin(numpy.deg2rad(gamma))) / \
                                       (Weight * numpy.cos(numpy.deg2rad(gamma)))))
    print("alpha is {}".format(alpha))

    # P_parasitic-body
    P_parasitic = D_body * v_inf    # W
    print("P_parasitic is {} W".format(P_parasitic))

    # P_profile-rotor
    area = numpy.pi * Propeller.radius ** 2
    sigma = (Propeller.numB * c_bar) / (numpy.pi * Propeller.radius)
    Thrust_each = Thrust / num_rotor
    print("sigma is {}".format(sigma))

    # Try iteration for C_T and rot_adv_ratio
    iter_num = 1
    iter_lim = 1e3
    tol = 1e-12
    res = tol + 1
    rot_adv_ratio = 0.098   # initial guess
    Cl_bar = 0.4        # initial guess
    V_T = 122.6 ### Trial
    C_T = Thrust_each / (AtmData.dens * area * V_T**2)
    #C_T = sigma * Cl_bar * (1 + 1.5 * rot_adv_ratio ** 2) / 6
    #V_T = numpy.sqrt((Thrust_each / num_rotor) / (AtmData.dens * area * C_T))
    Cl_bar_new = (6 * C_T) / (sigma * (1 + (3 / 2) * rot_adv_ratio ** 2))
    print("****C_T is {}".format(C_T))
    print("****Cl_bar_new is {}".format(Cl_bar_new))
    '''
    while res > tol:
        rot_adv_ratio_old = rot_adv_ratio
        Cl_bar_old = Cl_bar
        C_T = sigma * Cl_bar_old * (1 + (3 / 2) * rot_adv_ratio_old**2) / 6
        V_T = numpy.sqrt((Thrust_each / num_rotor) / (AtmData.dens * area * C_T))
        rot_adv_ratio = v_inf / V_T
        Cl_bar = (6 * C_T) / (sigma * (1 + (3 / 2) * rot_adv_ratio ** 2))
        res_1 = abs(rot_adv_ratio - rot_adv_ratio)
        res_2 = abs(Cl_bar - Cl_bar_old)
        res = max(res_1, res_2)
        iter_num += 1

        if iter_num >= iter_lim:
            raise Exception("Iteration limit exceeded in iterating for C_T and mu")
    '''

    Re = (AtmData.dens * V_T * (2 / 3) * c_bar) / AtmData.visc
    M_T = V_T / AtmData.sound_speed
    if M_T >= 0.9:
        print("Warning: Blade tip mach number exceeds 0.9")
    elif M_T >= 1:
        print("Warning: Blade tip mach number exceeds 1.0")

    #print("According to iteration, Cl_bar is {}, Re is {}".format(Cl_bar, Re))
    #Cd_bar = float(input("Please enter Cd_bar based on drag polar: "))
    Cd_bar = 0.015

    if Cd_bar is None:
        Cd_bar = 0.01   # Default

    P_profile_each = AtmData.dens * area * V_T**3 * sigma * Cd_bar * (1 + 3 * rot_adv_ratio**2) / 8
    P_profile = P_profile_each * num_rotor
    print("V_T is {0}m/s".format(str(V_T)))
    print("Cl_bar is {}".format(Cl_bar))
    print("Re is {}".format(Re))
    print("mu is {}".format(rot_adv_ratio))
    print("C_T is {}".format(C_T))
    print("P_profile is {} W".format(P_profile))

    # P_induced-rotor
    a4 = 1
    a3 = -2 * v_inf * numpy.sin(numpy.deg2rad(alpha))
    a2 = v_inf ** 2
    a1 = 0
    a0 = -1 * (Thrust_each / (2 * AtmData.dens * area)) ** 2
    func = lambda w: (a4 * w ** 4) + (a3 * w ** 3) + (a2 * w ** 2) + (a1 * w) + a0
    func_prime = lambda w: (4 * a4 * w ** 3) + (3 * a3 * w ** 2) + (2 * a2 * w) + a1
    guess = 100
    tol = 1e-12
    w_sol = newton.newton(func, func_prime, guess, tol)
    print("w_sol is " + str(w_sol) + " m/s")
    P_induced_ideal = num_rotor * (Thrust_each * (w_sol - v_inf * numpy.sin(numpy.deg2rad(alpha))))  # W
    P_induced = K_induced * P_induced_ideal
    print("P_induced is {} W".format(P_induced))

    # P_climb
    P_climb = Weight * v_inf * numpy.sin(numpy.deg2rad(gamma))  # W
    print("P_climb is {} W".format(P_climb))

    # Total power
    P_aero = P_parasitic + P_profile + P_induced + P_climb  # W
    return P_aero


if __name__ == "__main__":
    Weight = 9.81   # N
    f_body = 0.00605    # m^2
    gamma = 0   # deg
    num_rotor = 4

    vel = 12    # m/s
    h = 0       # m
    is_SI = True
    atm_trial = AtmData(vel, h, is_SI)

    radius = 0.071  # m
    numB = 2
    c_bar = 0.014   # m
    prop_trial = Propeller(radius, numB, "RPM", c_bar=c_bar)

    P_aero = rotor_hover_power(Weight, gamma, num_rotor, f_body, atm_trial, prop_trial)
    print("P_aero is {} w".format(P_aero))