import numpy
import sys
from Class130 import AtmData, Propeller

sys.path.append("../Utilities")
import newton


def rotor_hover_power(Weight, gamma, num_rotor, f_body, AtmData, Propeller, Cd_bar=None):
    # return P_aero, power_distr
    """
    Calculates the total rotor power related to hte thrust generation
    based on P_parasitic-body, P_profile-rotor, P_induced-rotor, and P_climb

    Input:
            Weight: (N) aircraft weight
            gamma: (deg) angle btw. v_inf and the horizon
            num_rotor: number of rotors
            f_body: (m^2) equivalent flat plate area of the body
            AtmData: need vel, dens, visc, sound_speed
            Propeller: need radius, numB, c_bar, RPM

    Output:
            P_aero: (W) total rotor power
            power_list: (W) list of power distribution
                        [P_parasitic, P_profile, P_induced, P_climb]
            Propeller assigned Cl_bar

    Calls:
        {None}

    Note:
            1. Can include improvement to accommodate motor thrust distribution if needed
            2. Iteration based on provided doc by Prof. Van Dam does not output correct numbers,
                so the func takes an additional RPM input to bypass the error
            3. Will possibly replace the Cd_bar input to another function call on xfoil
            4. Values of the downwash solution is not quite right in induced power,
                but its effect on output is small. Consider improving the solving method in future

    History:
            03.03.2021, XT. Created
            03.04.2021, XT. Error bypassed, briefly debugged.
    """
    # General
    K_induced = 1.15  # typicaly 1.13 - 1.15, pick largest for safety
    c_bar = Propeller.c_bar
    if c_bar is None:
        raise TypeError("Please remember to set c_bar into Propeller class")
    v_inf = AtmData.vel
    q_inf = 0.5 * AtmData.dens * v_inf ** 2
    D_body = f_body * q_inf
    Thrust = numpy.sqrt(D_body ** 2 + Weight ** 2 + 2 * D_body * Weight * numpy.sin(numpy.deg2rad(gamma)))
    alpha = numpy.rad2deg(numpy.arctan((-D_body - Weight * numpy.sin(numpy.deg2rad(gamma))) /
                                       (Weight * numpy.cos(numpy.deg2rad(gamma)))))

    # P_parasitic-body
    P_parasitic = D_body * v_inf  # W

    # P_profile-rotor
    area = numpy.pi * Propeller.radius ** 2
    sigma = (Propeller.numB * c_bar) / (numpy.pi * Propeller.radius)
    Thrust_each = Thrust / num_rotor

    Cl_bar_new = 0.4  # initial guess
    V_T = (2 * numpy.pi * Propeller.RPM / 60) * Propeller.radius
    rot_adv_ratio = v_inf / V_T
    C_T = Thrust_each / (AtmData.dens * area * V_T ** 2)
    iter_num = 1
    iter_lim = 1e3
    tol = 1e-12
    res = tol + 1
    while res > tol:
        Cl_bar_old = Cl_bar_new
        Cl_bar_new = (6 * C_T) / (sigma * (1 + (3 / 2) * rot_adv_ratio ** 2))
        res = abs(Cl_bar_new - Cl_bar_old)
        iter_num += 1
        if iter_num >= iter_lim:
            raise Exception("Iteration limit exceeded in iterating Cl")

    Cl_bar = Cl_bar_new

    Re = (AtmData.dens * V_T * (2 / 3) * c_bar) / AtmData.visc
    M_T = V_T / AtmData.sound_speed
    if M_T >= 0.9:
        print("Warning: Blade tip mach number exceeds 0.9")
    elif M_T >= 1:
        print("Warning: Blade tip mach number exceeds 1.0")

    if Cd_bar is None:
        print("According to iteration:\nCl_bar is {:.3f}\nRe is {:.1e}".format(Cl_bar, Re))
        while True:
            Cd_bar_str = input("Please enter Cd_bar based on drag polar: ")
            # FIXME: Maybe add a func for calculating Cd_bar in the future (Xfoil)
            if Cd_bar_str.replace('.', '', 1).isdigit():
                Cd_bar = float(Cd_bar_str)
                break

    P_profile_each = AtmData.dens * area * V_T ** 3 * sigma * Cd_bar * (1 + 3 * rot_adv_ratio ** 2) / 8
    P_profile = P_profile_each * num_rotor

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
    # FIXME: Solution to w still has about 20% error compared to provided values, but acceptable.
    P_induced_ideal = num_rotor * (Thrust_each * (w_sol - v_inf * numpy.sin(numpy.deg2rad(alpha))))  # W
    P_induced = K_induced * P_induced_ideal

    # P_climb
    P_climb = Weight * v_inf * numpy.sin(numpy.deg2rad(gamma))  # W

    # Total power
    P_aero = P_parasitic + P_profile + P_induced + P_climb  # W

    # Outputs power distributions of components
    power_distr = [P_parasitic, P_profile, P_induced, P_climb]

    return P_aero, power_distr


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    ## ******The resulting graph does not make sense to XT


    Weight = 13000  # N
    f_body = 0.001  # m^2, almost neglected
    gamma = 0  # deg
    num_rotor = 8

    # prop
    radius = 1.78 / 2  # m
    numB = 3
    c_bar = 0.1  # m, assumed
    RPM = 2500  # assumed
    prop_trial = Propeller(radius, numB, RPM, c_bar=c_bar)

    # atm
    h = 500  # m
    is_SI = True

    num = 101
    vel_start = -10
    vel_end = 20
    vel_vec = numpy.linspace(vel_start, vel_end, num)

    Cd_bar_start = 0.01
    Cd_bar_end = 0.05
    Cd_bar_num = 5
    Cd_bar_vec = numpy.linspace(Cd_bar_start, Cd_bar_end, Cd_bar_num)

    # P_aero vs. v_inf
    plt.figure(figsize=[20, 15])
    for i in range(Cd_bar_num):
        Cd_bar = Cd_bar_vec[i]
        P_aero_vec = [0] * num
        for j in range(num):
            atm_trial = AtmData(vel_vec[j], h, is_SI)
            P_aero_vec[j], _ = rotor_hover_power(Weight, gamma, num_rotor, f_body, atm_trial, prop_trial, Cd_bar=Cd_bar)

        plt.plot(vel_vec, P_aero_vec, label='Cd_bar = {:.2f}'.format(Cd_bar))

    title = 'Total Climb Power versus. Climb Speed'
    plt.title(title)
    plt.xlabel(r'Climb Speed $V_\infty$ (m/s)')
    plt.ylabel(r'Total Power $P_{aero}$ (W)')
    plt.grid()
    plt.legend(loc='upper right')
    plt.show()