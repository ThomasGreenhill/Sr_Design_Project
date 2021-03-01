import numpy
from scipy import interpolate
from scipy.interpolate import PchipInterpolator

from prop_analysis_TVG import prop_analysis
from Class130 import AtmData, Propeller



def prop_analysis_var_pitch(v_in, v_climb, P_eng, P_eng_data, AtmData, Propeller):
    # Return deta_P, dT, delta_beta, RPM_fix

    def get_P_eng(P_eng_data, RPM):
        x: list[float] = [item[0] for item in reversed(P_eng_data)]
        y: list[float] = [item[1] for item in reversed(P_eng_data)]
        interp_func: PchipInterpolator = interpolate.PchipInterpolator(x, y, extrapolate=True)
        cur_power = 745.7 * interp_func(RPM)    # hp to W
        return cur_power

    def get_m0(Ma):
        if Ma < 0:
            raise ValueError("Ma cannot be negative in get_m0 function")
        if Ma <= 0.9:
            m0 = 2 * numpy.pi / numpy.sqrt(1 - Ma ** 2)
        else:
            m0 = 2 * numpy.pi / numpy.sqrt(1 - 0.9 ** 2)
        return m0

    def get_Cd(Cl):
        Cd = 0.0095 + 0.0040 * (Cl - 0.2) ** 2
        return Cd

    """
    Continue to TGreenhill's propeller analysis code, for variable pitch propeller design

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
    tol = 1e-12
    iter_lim = 1e3
    iter_num = 1
    n_fix = Propeller.RPM / 60
    Pd_fix = 0
    v_inf = AtmData.vel

    while round(Pd_fix, 4) != round(get_P_eng(P_eng_data, n_fix * 60), 4) and iter_num <= iter_lim:
        Pn_fix = get_P_eng(P_eng_data, n_fix * 60)
        J_fix, P_design_fix, _, T_design_fix, _, eta_P_fix = prop_analysis(AtmData, Propeller, get_m0, get_Cd)

        if Pd_fix < Pn_fix:
            n_fix = n_fix * (1 + 0.5 * (Pn_fix - Pd_fix) / (Pn_fix + Pd_fix))
        elif Pd_fix > Pn_fix:
            n_fix = n_fix * (1 + 0.5 * (Pn_fix - Pd_fix) / (Pn_fix + Pd_fix))
        else:
            break
        iter_num += 1

    # Optimize the blade variation for climb:
    # initial values for iteration
    if v_in < v_inf:
        d_bet = 5 * numpy.pi / 180 / (v_inf - v_climb) * v_in - 5 * numpy.pi / \
            180 / (v_inf - v_climb) * v_inf
    else:
        d_bet = 2 * numpy.pi / 180

    iter_num = 1
    P_design_Var = 0

    while round(P_design_Var, 6) != round(get_P_eng(P_eng_data, n_fix * 60), 6) and iter_num <= iter_lim:
        Propeller.bet += d_bet
        J_var, P_design_var, _, T_design_var, _, eta_P_var = prop_analysis(AtmData, Propeller, get_m0, get_Cd)

        P_design_Var = P_design_var if P_design_var > 0 else 10
        if d_bet < 0:
            d_bet *= (1 - 2 * (P_eng - P_design_Var) / (P_eng + P_design_var))
        else:
            d_bet *= (1 + 2 * (P_eng - P_design_var) / (P_eng + P_design_var))
            if round(d_bet, 14) <= tol:
                break
        iter_num += iter_num

    # Difference in efficiency between fixed and variable pitch
    deta_P = (-eta_P_fix + eta_P_var) / eta_P_fix
    dT = (-T_design_fix + T_design_var) / T_design_fix
    delta_beta = d_bet
    RPM_fix = n_fix * 60

    return deta_P, dT, delta_beta, RPM_fix


if __name__ == '__main__':

    P_eng_data = [[2400, 177],
                  [2300, 170],
                  [2200, 165],
                  [2100, 158],
                  [2000, 150],
                  [1900, 141],
                  [1800, 131]]

    # Atm
    P_eng = 177 * 745.7         # W
    vel = 154 * 0.514444        # m/s
    v_climb = 87 * 0.514444     # m/s
    h = 8000 * 0.3048           # m
    is_SI = True
    atm_trial = AtmData(vel, h, is_SI)
    atm_trial.expand(1.4, 287)

    # Propeller
    radius = 6.8333 * 0.3048 / 2    # m
    numB = 3
    Cl = 0.4
    RPM = 2400
    alp0 = numpy.radians(-2)
    num = 11
    bet = [-6 for i in range(num)]
    prop_trial = Propeller(radius, numB, RPM, Cl=Cl, chord=1, alp0=alp0, bet=bet)

    deta_P, dT, delta_beta, RPM_fix = prop_analysis_var_pitch(vel, v_climb, P_eng, P_eng_data, atm_trial, prop_trial)