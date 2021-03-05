import numpy
from scipy import interpolate
from scipy.interpolate import PchipInterpolator

from prop_design_TVG import prop_design
from prop_analysis import prop_analysis
from Class130 import AtmData, Propeller
import matplotlib.pyplot as plt
import copy


def prop_analysis_var_pitch(v_in, v_des, P_eng_data, is_HP, AtmData, Propeller, m0_fn, Cd_fn):
    # Return deta_P, dT, delta_beta, RPM_fix

    def get_P_eng(P_eng_data, RPM):
        x: list[float] = [item[0] for item in reversed(P_eng_data)]
        y: list[float] = [item[1] for item in reversed(P_eng_data)]
        interp_func: PchipInterpolator = interpolate.PchipInterpolator(x, y, extrapolate=True)
        if is_HP:
            cur_power = 745.7 * interp_func(RPM)  # hp to W
        else:
            cur_power = interp_func(RPM)
        return cur_power

    """
    Continuation of TGreenhill's propeller analysis code, for variable pitch propeller design

    Outer function
    Input:

    Output:
        deta_P: difference in efficiency
        dT: difference in thrust
        delta_beta: difference in pitch
        RPM_fix: fixed RPM

    Inner function
        get_P_eng
    Input: 
            P_eng_data: nx2 data set for RPM and power in hp:   [RPM, Power in hp]
            RPM: (1/min) rotation per minute
    Output:
            cur_power: (W) current power at the given RPM in watt

        m0_func
    Input:
            Ma: mach number
    Output:
            m0: lift curve slope

        Cd_func
    Input:
            Cl: lift coefficient
    Output:
            Cd: drag coefficient

    Call:
            {None}

    Notes:
            1. For a single input velocity
            2. Not fully debugged yet

    History:
            02.28.2021, XT. Translated to python
            03.01.2021, TG. Refined
            03.02.2021, XT. Debugged (Not fully, awaits further testings)
    """
    tol = 1e-6  ### Changed to debug by XT
    iter_lim = 1e2
    res = 1
    iter_num = 1
    n_fix = Propeller.RPM / 60
    P_design_fix = 0
    AtmData.vel = copy.deepcopy(v_in)
    bet_original = copy.deepcopy(Propeller.bet)

    while res > tol and iter_num <= iter_lim:
        Pn_fix = get_P_eng(P_eng_data, n_fix * 60)
        res = numpy.absolute(P_design_fix - Pn_fix)
        J_fix, P_design_fix, _, T_design_fix, _, _, _, eta_P_fix = prop_analysis(AtmData, Propeller, m0_fn, Cd_fn)
        ### Debugged: P_design_fix instead of Pd_fix in the following expression
        if P_design_fix < Pn_fix:
            n_fix = n_fix * (1 + 0.5 * (Pn_fix - P_design_fix) / (Pn_fix + P_design_fix))
        elif P_design_fix > Pn_fix:
            n_fix = n_fix * (1 + 0.5 * (Pn_fix - P_design_fix) / (Pn_fix + P_design_fix))
        else:
            break
        iter_num += 1

    # Optimize the blade beta variation for v_in. Make a good initial guess:
    P_eng = get_P_eng(P_eng_data, Propeller.RPM)
    if v_in < v_des:
        d_bet_old = numpy.radians(-10)
        d_bet = numpy.radians(-5)
        factor = 1
    else:
        d_bet_old = numpy.radians(30)
        d_bet = numpy.radians(10)
        factor = 1

    # Initial values for iteration:
    iter_num = 1
    P_design_var = 0
    res = 1

    # before the first iteration, apply delta beta old the fixed pitch propeller and compute the power
    Propeller.bet += d_bet_old
    _, P_design_var_old, _, _, _, _, _, _ = prop_analysis(AtmData, Propeller, m0_fn, Cd_fn)
    Propeller.bet = copy.deepcopy(bet_original)


    while res > tol and iter_num <= iter_lim:
        # Apply delta beta to the fixed pitch propeller and compute the power
        if iter_num > 1:
            P_design_var_old = P_design_var
        Propeller.bet += d_bet
        J_var, P_design_var, _, T_design_var, _, Q_design_var, _, eta_P_var = prop_analysis(AtmData, Propeller, m0_fn, Cd_fn)
        Propeller.bet = copy.deepcopy(bet_original)

        # Use the secant method to converge
        temp = d_bet
        d_bet = d_bet - (P_design_var-P_eng)/((P_design_var - P_design_var_old)/(d_bet-d_bet_old))
        d_bet_old = temp

        # d_bet = d_bet if P_design_var > 0 else -d_bet*0.5
        if P_design_var > 0:
            P_design_var = P_design_var  
        else:
            P_design_var = 0.2*P_eng
            print("Power is negative, resetting")        

        res = numpy.absolute(P_design_var - P_eng)
        print(iter_num)
        iter_num += 1

        if iter_lim == iter_num:
            print("Error: Iteration Limit Reached")
            return
            # Note for Xuchang: I don't like using exit because it sometimes ruins a lot of data with just one error.
            # exit()      ### Added exit()

    # print(d_bet)
    # Difference in efficiency between fixed and variable pitch
    deta_P = (-eta_P_fix + eta_P_var) / eta_P_fix           # W
    dT = (-T_design_fix + T_design_var) / T_design_fix      # N
    delta_beta = numpy.degrees(d_bet)       # deg   ### Converted directly to degrees by XT
    RPM_fix = n_fix * 60

    return J_var, P_design_var, T_design_var, Q_design_var, eta_P_var, deta_P, dT, delta_beta, RPM_fix


if __name__ == '__main__':

    P_eng_data = [[2400, 177],
                  [2300, 170],
                  [2200, 165],
                  [2100, 158],
                  [2000, 150],
                  [1900, 141],
                  [1800, 131]]


    def m0_fn(Ma):
        if numpy.any(Ma <= 0.9):
            return (2 * numpy.pi) / numpy.sqrt(1 - Ma ** 2)
        else:
            return (2 * numpy.pi) / numpy.sqrt(1 - 0.9 ** 2)


    def Cd_fn(Cl):
        return 0.0095 + 0.0040 * (Cl - 0.2) ** 2

        # Atm


    # P_eng = 177 * 745.7         # W
    v_des = 154 * 0.514444  # m/s
    v_climb = 87 * 0.514444  # m/s
    h = 8000 * 0.3048  # m
    is_SI = True
    is_HP = True
    atm_check = AtmData(v_des, h, is_SI)
    atm_check.expand(1.4, 287)

    # Propeller
    radius = 41 * 0.0254  # m
    numB = 3
    Cl = 0.4
    RPM = 2400
    alp0 = numpy.radians(-2)
    dens = atm_check.dens
    CT = 0.0509
    T_req = CT * dens * (RPM / 60) ** 2 * (radius * 2) ** 4

    v_seq = numpy.arange(v_climb - 30 * 0.3048, v_climb + 126 * 0.3048, 2)
    prop_check = Propeller(radius, numB, RPM, eta_P=0, CP=0, CT=0, CQ=0, Cl=0.4)
    r, prop_check.chord, prop_check.bet, P_design, T_design, Q_design, eta_P, prop_check.theta = prop_design(atm_check,
                                                                                                             prop_check,
                                                                                                             T_req,
                                                                                                             m0_fn,
                                                                                                             Cd_fn)

    ll = numpy.size(v_seq)

    J_var = numpy.zeros((ll,))
    P_design_var = numpy.zeros((ll,))
    T_design_var = numpy.zeros((ll,))
    eta_P_var = numpy.zeros((ll,))
    deta_P = numpy.zeros((ll,))
    dT = numpy.zeros((ll,))
    delta_bet = numpy.zeros((ll,))
    RPM_fix = numpy.zeros((ll,))
    for ii in range(ll):
        J_var[ii], P_design_var[ii], T_design_var[ii], Q_design_var[ii], eta_P_var[ii], deta_P[ii], dT[ii], delta_bet[ii], RPM_fix[
            ii] = prop_analysis_var_pitch(v_seq[ii], v_des, P_eng_data, is_HP, atm_check, prop_check, m0_fn, Cd_fn)

    plt.plot(v_seq * 1.94384, delta_bet)
    plt.figure()
    plt.plot(v_seq * 1.94384, T_design_var*0.224809)
    plt.figure()
    plt.plot(v_seq * 1.94384, eta_P_var)
    plt.show()
