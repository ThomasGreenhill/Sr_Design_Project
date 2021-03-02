import numpy
from scipy import interpolate
from scipy.interpolate import PchipInterpolator

from prop_design_TVG import prop_design
from prop_analysis import prop_analysis
from Class130 import AtmData, Propeller
import matplotlib.pyplot as plt
import copy

'''  ### THIS IS THE ORIGINAL FUNC
def prop_analysis_var_pitch(v_in, P_eng_data, is_HP, AtmData, Propeller, m0_fn, Cd_fn):
    # Return deta_P, dT, delta_beta, RPM_fix

    def get_P_eng(P_eng_data, RPM):
        x: list[float] = [item[0] for item in reversed(P_eng_data)]
        y: list[float] = [item[1] for item in reversed(P_eng_data)]
        interp_func: PchipInterpolator = interpolate.PchipInterpolator(x, y, extrapolate=True)
        if is_HP:
            cur_power = 745.7 * interp_func(RPM)    # hp to W
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

    History:
            02.28.2021, XT. Translated to python
    """
    tol = 1e-6
    iter_lim = 1e3
    res = 1
    iter_num = 1
    n_fix = Propeller.RPM / 60
    Pd_fix = 0
    AtmData.vel = copy.deepcopy(v_in)
    bet_original = copy.deepcopy(Propeller.bet)

    while res > tol and iter_num <= iter_lim:
        Pn_fix = get_P_eng(P_eng_data, n_fix * 60)
        res = numpy.absolute(Pd_fix-Pn_fix)
        J_fix, P_design_fix, _, T_design_fix, _, _, _, eta_P_fix = prop_analysis(AtmData, Propeller, m0_fn, Cd_fn)

        if Pd_fix < Pn_fix:
            n_fix = n_fix * (1 + 0.5 * (Pn_fix - Pd_fix) / (Pn_fix + Pd_fix))
        elif Pd_fix > Pn_fix:
            n_fix = n_fix * (1 + 0.5 * (Pn_fix - Pd_fix) / (Pn_fix + Pd_fix))
        else:
            break
        iter_num += 1

    # Optimize the blade beta variation for v_in. Make a good initial guess; initial values for iteration:
    v_inf = 263.29*0.3048
    if v_in < v_inf:
        d_bet = -2 * numpy.pi / 180
    else:
        d_bet = 2 * numpy.pi / 180

    iter_num = 1
    P_design_var = 0
    res = 1

    while res > tol and iter_num <= iter_lim:
        P_eng = get_P_eng(P_eng_data, Propeller.RPM)
        Propeller.bet += d_bet
        J_var, P_design_var, _, T_design_var, _, _, _, eta_P_var = prop_analysis(AtmData, Propeller, m0_fn, Cd_fn)
        Propeller.bet = copy.deepcopy(bet_original)

        P_design_var = P_design_var if P_design_var > 0 else 10*750
        factor = numpy.absolute(1/d_bet*2*numpy.pi/180)*0.5
        if d_bet < 0:
            d_bet *= (1 - factor*(P_eng - P_design_var) / (P_eng + P_design_var))
        else:
            d_bet *= (1 + factor*(P_eng - P_design_var) / (P_eng + P_design_var))
            if numpy.round(d_bet, 14) <= tol:
                break

        res = numpy.absolute(P_design_var-P_eng)
        # print(res)
        iter_num += 1

        if iter_lim == iter_num:
            print("Iteration Limit Reached")
        
    # print(d_bet)
    # Difference in efficiency between fixed and variable pitch
    deta_P = (-eta_P_fix + eta_P_var) / eta_P_fix
    dT = (-T_design_fix + T_design_var) / T_design_fix
    delta_beta = d_bet
    RPM_fix = n_fix * 60

    return J_var, P_design_var, T_design_var, eta_P_var, deta_P, dT, delta_beta, RPM_fix
'''


def prop_analysis_var_pitch(v_in, P_eng_data, is_HP, AtmData, Propeller, m0_fn, Cd_fn):
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

    History:
            02.28.2021, XT. Translated to python
    """
    tol = 1e-6
    iter_lim = 1e3
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

    # Optimize the blade beta variation for v_in. Make a good initial guess; initial values for iteration:
    v_inf = 263.29 * 0.3048
    if v_in < v_inf:
        d_bet = -2 * numpy.pi / 180
    else:
        d_bet = 2 * numpy.pi / 180

    iter_num = 1
    P_design_var = 0
    res = 1

    while res > tol and iter_num <= iter_lim:
        P_eng = get_P_eng(P_eng_data, Propeller.RPM)
        Propeller.bet += d_bet
        J_var, P_design_var, _, T_design_var, _, _, _, eta_P_var = prop_analysis(AtmData, Propeller, m0_fn, Cd_fn)
        # Propeller.bet = copy.deepcopy(bet_original)
        Propeller.bet = bet_original
        ### Instead of deepcopy, used normal assignment as deepcopy is already used for bet_original

        P_design_var = P_design_var if P_design_var > 0 else 10 * 750
        factor = numpy.absolute(1 / (d_bet * 2 * numpy.pi / 180)) * 0.5
        ### (d_bet * 2 * numpy.pi / 180) should have parentheses (as a convertion if I am correct)
        if d_bet < 0:
            d_bet *= (1 - factor * (P_eng - P_design_var) / (P_eng + P_design_var))
        else:
            d_bet *= (1 + factor * (P_eng - P_design_var) / (P_eng + P_design_var))
            # if numpy.round(d_bet, 14) <= tol:
            if d_bet <= tol:
                break

        res = numpy.absolute(P_design_var - P_eng)
        # print(res)
        iter_num += 1

        if iter_lim == iter_num:
            print("Iteration Limit Reached")

    # print(d_bet)
    # Difference in efficiency between fixed and variable pitch
    deta_P = (-eta_P_fix + eta_P_var) / eta_P_fix
    dT = (-T_design_fix + T_design_var) / T_design_fix
    delta_beta = d_bet
    RPM_fix = n_fix * 60

    return J_var, P_design_var, T_design_var, eta_P_var, deta_P, dT, delta_beta, RPM_fix


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
    vel = 154 * 0.514444  # m/s
    v_climb = 87 * 0.514444  # m/s
    h = 8000 * 0.3048  # m
    is_SI = True
    is_HP = True
    atm_check = AtmData(vel, h, is_SI)
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
    P_design_Var = numpy.zeros((ll,))
    T_design_var = numpy.zeros((ll,))
    eta_P_var = numpy.zeros((ll,))
    deta_P = numpy.zeros((ll,))
    dT = numpy.zeros((ll,))
    delta_bet = numpy.zeros((ll,))
    RPM_fix = numpy.zeros((ll,))
    for ii in range(ll):
        J_var[ii], P_design_Var[ii], T_design_var[ii], eta_P_var[ii], deta_P[ii], dT[ii], delta_bet[ii], RPM_fix[
            ii] = prop_analysis_var_pitch(v_seq[ii], P_eng_data, is_HP, atm_check, prop_check, m0_fn, Cd_fn)

    plt.plot(v_seq * 1.94384, delta_bet * 180 / numpy.pi)
    plt.show()
