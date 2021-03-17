import numpy


def propeller_in_cruise(W_initial, W_final, c_p, AtmData, Propeller, Wing, const_logic):
    # return R, E
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
                R: (m) range
                E: (s) endurance

        Notes:

        History:
            02.14.2021: Created. XTang
            02.15.2021: Briefly debugged. XTang
            02.15.2021: Reviewed by TVG
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
        R = (Propeller.eta_P / c_p) / (a1 * a2) * (numpy.arctan(W_initial * a2 / a1) -
                                                   numpy.arctan(W_final * a2 / a1))
        # Endurance
        E = R / AtmData.vel
        return R, E

    else:  # Unknown error
        print("Error: unknown case_num in assigning based on const_logic, check function!")
        return


if __name__ == '__main__':
    from Class130 import AtmData, Propeller, Wing

    #****** The range and endurance is too low for our mission

    g = 9.81    # m/s^2
    W_initial = 13000  # N
    m_loss = 20         # this affects the output tremendously
    W_final = 13000 - 2 * (m_loss * g)  # N
    W_diff = W_initial - W_final

    # atm data
    h = 6000 * 0.3048  # m
    vel = 62  # m/s
    is_SI = True
    atm = AtmData(vel, h, is_SI)
    atm.expand(1.4, 287)

    # prop data
    eta_P = 0.82
    prop = Propeller('radius', 'numB', 'RPM', eta_P=eta_P)

    const_logic = [True, True, False]  # [CL, v_inf, h]

    area = 16  # m^2
    span = 4.70460 * 2  # m
    CL = (W_initial + W_final) / (atm.dens * atm.vel ** 2 * area)

    # CL = 0.4128
    CD = 0.018  # from drag polar with no flap, 62 m/s, 6000 ft
    CD_0 = 0.012

    wing = Wing(area, span, e=0.7, CL=CL, CD=CD, CD_0=CD_0)

    # c_p
    P_fuelcell_cont = 100 * 1000  # W
    t_flight_normal = 2200  # s
    t_flight_divert = 500  # s
    t_flight_total = t_flight_normal + t_flight_divert
    Drag = 0.5 * CD * atm.dens * atm.vel**2 * wing.area

    c_p = Drag / (P_fuelcell_cont * t_flight_total)     # N / (W s)

    R, E = propeller_in_cruise(W_initial, W_final, c_p, atm, prop, wing, const_logic)

    print("Range is {:.2f} km".format(R / 1000))
    print("Endurance is {:.2f} hr".format(E / 3600))
