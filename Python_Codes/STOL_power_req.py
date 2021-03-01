import numpy
from prop_design_TVG import prop_design

def STOL_power_req(m, dist_to, mot_distr, AtmData, Wing, Propeller_list):
    '''

     Provides calculation for the least required power of STOL aircraft

        Inputs:
            m: kg, airplane mass
            dist_to: m, target rakeoff distance
            motDistr: 1xn vector of motor power distribution
            Wing.S: m^2, wing area
            Wing.CL_max: max CL during takeoff
            AtmData.dens: air density (to get ratio compared to standard sea level atm.)
            Propeller_list: list of class "Propeller" for power calculation in FAR 25



        Outputs:
            outVec: if FAR 23, 1xn vector of motor power (hp)
                    if FAR 25, 1xn vector of motor thrust (N)

    Calls:
        {none}

    Notes:
        1. Function uses empirical expression provided in Roskam Part I
        2. FAR 23/25 based on aircraft mass included
        3. When integrating functions, mute the FAR23/25 fprintf sections
        4. Not well tested yet

    History:
            2.9.2021, created by X.Tang in Matlab
            2.14.2021, translated to Python by X.Tang
            2.14.2021, still has problem in FAR25 power with [1,1] distr, power way too high
   '''

    std_sl_dens_SI = 1.225          # kg/m^3
    std_sl_dens_Brit = 0.002377     # slug/ft^3
    g = 9.81        # m/s^2
    if AtmData.is_SI:
        sigma = AtmData.dens / std_sl_dens_SI
    else:
        sigma = AtmData.dens / std_sl_dens_Brit

    # FAR 23 / 25 check
    dist_to_Brit = dist_to * 3.28084    # meter to feet
    W = m * g                           # N
    W_Brit = W * 0.224809               # N to lbf
    S_Brit = Wing.area * 3.28084 ** 2   # m^2 to ft^2
    bdy = 12500 * 0.453592              # kg
    tol = 1e-3                          # tolerance for compare between double

    if m <= bdy:    # FAR 23
        a1 = 8.134
        a2 = 0.0149
        TOP23 = [0] * 2
        delta = a2 ** 2 - 4 * a1 * (-dist_to_Brit)

        # Check real
        if delta > 0:
            TOP23[0] = (-a2 + numpy.sqrt(delta)) / (2 * a1)
            TOP23[1] = (-a2 - numpy.sqrt(delta)) / (2 * a1)

            # Check positive num
            if TOP23[0] > 0 and TOP23[1] <= 0:
                TOP23_val = TOP23[0]
            elif TOP23[0] <= 0 and TOP23[1] > 0:
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

        else:   # imaginary
            print("Error: No real root for TOP23")
            return

        # Calculation for power in hp
        PTO = (W_Brit ** 2 / S_Brit) / (TOP23_val * sigma * Wing.CL_max)

        # Power distribution
        if numpy.size(mot_distr) > 1:
            sum_distr = sum(mot_distr)
            power_vec = [0] * len(mot_distr)

            for i in range(len(mot_distr)):
                cur_distr = mot_distr[i] / sum_distr
                power_vec[i] = cur_distr * PTO

        else:
            power_vec = PTO

        # Can mute this following message
        print("Aircraft category: FAR 23, motor POWER vector output")
        return power_vec

    else:       # FAR 25
        a3 = 37.5
        TOP25 = S_Brit / a3
        TTO_lbf = (W_Brit ** 2 / S_Brit) / (TOP25 * sigma * Wing.CL_max)
        TTO = TTO_lbf * 4.44822     # from lbf to N

        print("Thrust is " + str(TTO) + " N")
        # Thrust distribution
        if numpy.size(mot_distr) > 1:
            sum_distr = sum(mot_distr)
            power_vec = [0] * len(mot_distr)
            for i in range(len(mot_distr)):
                cur_distr = mot_distr[i] / sum_distr
                cur_thrust = cur_distr * TTO

                # Calculating power using propeller design function
                _, _, _, power_vec[i], _, _, _, _ = prop_design(AtmData, Propeller_list, cur_thrust)
                power_vec[i] *= 0.00134102      # Converts to hp

        else:
            _, _, _, power_vec, _, _, _, _ = prop_design(AtmData, Propeller_list, TTO)
            power_vec *= 0.00134102     # Converts to hp

        # Can mute this following message
        print("Aircraft category: FAR 25, motor POWER vector output")
        return power_vec


if __name__ == '__main__':
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
    mot_distr = [1, 1]
    print(numpy.size(mot_distr))
    dist_to = 2000
    power_vec = STOL_power_req(m, dist_to, mot_distr, atm_check, wing_check, prop_check)
    print(power_vec)

    a = power_vec[0] / 2
    print(a)