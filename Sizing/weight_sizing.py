import numpy

def weight_sizing(AR, B_w, D, H_tv, L, L_m, L_n, L_t, N_eng, N_l, N_z, q,
                  S_f, S_ht, S_vt, S_w, t_c, W_dg, W_eng, W_fw, W_l, W_press, W_uav,
                  Lamb, Lamb_ht, Lamb_vt, lamb, lamb_ht, lamb_vt):

    # return: W_av, W_eng_total, W_f, W_fc, W_furnish, W_ht, W_lg, W_vt, W_w
    '''
    Computes weight sizing based on component weight estimation equations provided
        in Raymer 5th ed.
    It is a more accurate sizing function. For very rough sizing, use weight_estimate.py

    Inputs:
        AR: aspect ratio
        B_w: (ft) wing span
        D: (ft) fuselage structural depth
        H_tv: 0.0 for conventional tail, 1.0 for "T" tail
        L: (ft) fuselage structural length (excludes radome cowling, tail cap)
        L_m: (in) extended length of main landing gear
        L_n: (in) extended nose gear length
        L_t: (ft) tail length, wing quarter-MAC to tail quarter_MAC
        N_eng: number of engines (total for aircraft)
        N_l: ultimate landing load factor = N_gear * 1.5
        N_z: ultimate load factor = limit load factor * 1.5
        q: (lbf/ft^2) dynamic pressure at cruise
        S_f: (ft^2) fuselage wetted area
        S_ht: (ft^2) horizontal tail area
        S_vt: (ft^2) vertical tail area
        S_w: (ft^2) trapezoidal wing area
        t_c: thickness-to-chord ratio
            (if not constant, use average of portion of wing inboard of C_bar)
        W_dg: (lbf) flight design gross weight
        W_eng: (lbf) engine weight (each)
        W_fw: (lbf) weight of fuel in wing (if zero, ignore the term)
        W_l: (lbf) landing design gross weight
        W_press: (lbf) weight penalty due to pressurization
                = 11.9 * (V_pr * P_delta) ** 0.271
                where V_pr is (ft^3) volume of pressurized section
                      P_delta (psia) is cabin pressure differential, typically 8 psia
        W_uav: (lbf) uninstalled avionics weight (typically 800 - 1400 lbf)
        Lamb: (rad) wing sweep at 25% MAC
        Lamb_ht: (rad) horizontal tail sweep at 25% MAC
        Lamb_vt: (rad) vertical tail sweep at 25% MAC
        lamb: wing taper ratio
        lamb_ht: horizontal tail taper ratio
        lamb_vt: vertical tail taper ratio (if less than 0.2, use 0.2)

    Outputs:
        W_av: (lbf) weight of avionics
        W_eng_total: (lbf) weight of total installed engine
                    (including propeller and engine mounts)
        W_f: (lbf) weight of fuselage
        W_fc: (lbf) weight of flight control systems
        W_furnish: (lbf) weight of furnishing
        W_ht: (lbf) weight of horizontal tail
        W_lg: (lbf) weight of main & nose (total) landing gear
                (reduce total landing gear weight by 1.4% of TOGW if nonretractable)
        W_vt: (lbf) weight of vertical tail
        W_w: (lbf) weight of wing

    Calls:
        {None}

    Note:
        1. Please keep a close attention at the units
        2. Equations comes from Reymer 5th edition, only included major components
        3. Not yet checked with certified data

    History:
        02.16.2021: Created, XT
        02.16.2021: Visually inspected, runs without error, not checked with real numbers, XT

    '''

    # FIXME: Add Convert to British units if needed

    # Sizing Functions:
    # Fuselage          Reymer 15.49
    W_f = 0.052 * (S_f ** 1.086) * (N_z * W_dg) ** 0.177 * \
          L_t ** -0.051 * (L / D) ** -0.072 * \
          q ** 0.241 + W_press

    # Wing              Reymer 15.46
    W_w = 0.036 * (S_w ** 0.758) * (W_fw ** 0.0035) * \
          (AR / (numpy.cos(Lamb) ** 2)) ** 0.6 * q * 0.006 * \
          lamb ** 0.04 * ((100 * t_c) / numpy.cos(Lamb)) ** -0.3 * \
          (N_z * W_dg) ** 0.49

    # Horizontal tail   Reymer 15.47
    W_ht = 0.016 * (N_z * W_dg) ** 0.414 * q ** 0.168 * \
           S_ht ** 0.896 * ((100 * t_c) / numpy.cos(Lamb)) ** -0.12 * \
           (AR / (numpy.cos(Lamb_ht)) ** 2) ** 0.043 * \
           lamb_ht * -0.02

    # Vertical tail     Reymer 15.48
    W_vt = 0.073 * (1 + 0.2 * H_tv) * (N_z * W_dg) ** 0.376 * \
           q ** 0.122 * S_vt ** 0.873 * \
           ((100 * t_c) / numpy.cos(Lamb_vt)) ** -0.49 * \
           (AR / (numpy.cos(Lamb_vt)) ** 2) ** 0.357 * lamb_vt ** 0.039

    # Landing gear      Reymer 15.50 + 15.51
    # Main landing gear
    W_lg_m = 0.095 * (N_l * W_l) ** 0.768 * (L_m / 12) ** 0.409
    # Nose landing gear
    W_lg_n = 0.125 * (N_l * W_l) ** 0.566 * (L_n / 12) ** 0.845
    # Total landing gear
    W_lg = W_lg_n + W_lg_m

    # Avionics          Reymer 15.57
    W_av = 2.117 * W_uav ** 0.933

    # Flight controls   Reymer 15.54
    W_fc = 0.053 * L ** 1.536 * B_w ** 0.371 * \
           (N_z * W_dg * 1E-04) ** 0.80

    # Furnishing        Reymer 15.59
    W_furnish = 0.0582 * W_dg - 65

    # Installed engine (total, includes propeller & engine mounts)  Reymer 15.52
    W_eng_total = 2.575 * W_eng ** 0.922 * N_eng

    # FIXME: return total weight + printing components weight as improvement

    return W_av, W_eng_total, W_f, W_fc, W_furnish, W_ht, W_lg, W_vt, W_w