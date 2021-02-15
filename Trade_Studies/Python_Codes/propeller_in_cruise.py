import numpy
from Class130 import AtmData, Propeller, Wing


def propeller_in_cruise(W_initial, W_final, c_p, AtmData, Propeller, Wing, const_logic):
    '''
        Based on EAE 130A lecture slide on Jan 27, 2021
        Computes the range and endurance of a propeller-thrusted, fuel-burning, air-breathing airplane cruise
        When constant lift coeff. and constant airspeed
        Inputs:
                W_initial: (N) initial weight of aircraft
                W_final: (N) final weight of aircraft
                c_p: (1/m) brake specific fuel consumption
                const_logic: 1x3 logical array, indicating constants in the function
                            [CL, v_inf, h] for lift coeff., airspeed, altitude
                            must only have 2 True and 1 False

        Outputs:
            {none}

        Notes:

        History:
            02.14.2021: Created. XTang
            02.15.2021: Briefly debugged. XTang
    '''

    # Checking the size of const_logic
    if numpy.size(const_logic) != 3:
        print("Boolean list \"const_logic\" must have a size of 3")
        return

    # Checking const_logic has 2 True and 1 False
    if sum(const_logic) != 2:
        print("Boolean list \"const_logic\" must have 2 True and 1 False")
        return

    # Assigning case numbers based on const_logic
    case_num = const_logic[0] * 100 + const_logic[1] * 10 + const_logic[2]

    if case_num == 110:  # Constant Cl and v_inf
        # Range
        R = (Propeller.eta_P / c_p) * (Wing.CL / Wing.CD) * numpy.log(W_initial / W_final)
        # Endurance
        E = R / AtmData.vel
        return R, E

    elif case_num == 101:  # Constant Cl and altitude
        # Range
        R = (Propeller.eta_P / c_p) * (Wing.CL / Wing.CD) * numpy.log(W_initial / W_final)
        # Endurance
        E = 2 * (Propeller.eta_P / c_p) * (Wing.CL ** 1.5 / Wing.CD) * \
            numpy.sqrt(AtmData.dens * Wing.area / 2) * (W_final ** -0.5 - W_initial ** -0.5)
        return R, E

    elif case_num == 11:  # Constant v_inf and altitude
        a1 = numpy.sqrt(Wing.CD_0 * 0.5 * AtmData.dens * AtmData.vel ** 2 * Wing.area)
        a2 = numpy.sqrt(1 / (numpy.pi * Wing.e * Wing.span ** 2 * 0.5 * AtmData.dens * AtmData.vel ** 2))

        # Range
        R = (Propeller.eta_P / c_p) / (a1 * a2) * (numpy.arctan(W_initial * a2 / a1) - \
                                                   numpy.arctan(W_final * a2 / a1))
        # Endurance
        E = R / AtmData.vel
        return R, E

    else:  # Unknown error
        print("Error: unknown case_num in assigning based on const_logic, check function!")
        return
