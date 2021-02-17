from typing import Any, Union

import numpy


def std_atm(h, is_SI):
    # return temp, press, dens, c_sound, visc, g

    def get_val(H):
        if H < 11000:
            b = 0
            H_b = 0
            L_mb = -0.0065
            T_mb = 288.15
            P_b = 1.01325000000000E+05
            return b, H_b, L_mb, T_mb, P_b

        elif 11000 <= H < 20000:
            b = 1
            H_b = 11000
            L_mb = 0
            T_mb = 216.65
            P_b = 2.26320639734629E+04
            return b, H_b, L_mb, T_mb, P_b

        elif 20000 <= H < 32000:
            b = 2
            H_b = 20000
            L_mb = 0.001
            T_mb = 216.65
            P_b = 5.47488866967777E+03
            return b, H_b, L_mb, T_mb, P_b

        elif 32000 <= H < 47000:
            b = 3
            H_b = 32000
            L_mb = 0.0028
            T_mb = 228.65
            P_b = 8.68018684755228E+02
            return b, H_b, L_mb, T_mb, P_b

        elif 47000 <= H < 51000:
            b = 4
            H_b = 47000
            L_mb = 0
            T_mb = 270.65
            P_b = 1.10906305554966E+02
            return b, H_b, L_mb, T_mb, P_b

        elif 51000 <= H < 71000:
            b = 5
            H_b = 51000
            L_mb = -0.0028
            T_mb = 270.65
            P_b = 6.69388731186873E+01
            return b, H_b, L_mb, T_mb, P_b

        elif 71000 <= H < 84852:
            b = 6
            H_b = 71000
            L_mb = -0.002
            T_mb = 214.65
            P_b = 3.95642042804073E+00
            return b, H_b, L_mb, T_mb, P_b

        else:   # H > 84852
            b = 7
            H_b = 84852
            L_mb = 0
            T_mb = 186.946
            P_b = 3.73383589976215E-01
            return b, H_b, L_mb, T_mb, P_b

    '''
    Computes the standard atmospheric data at a given height
    Based on the report found in https://apps.dtic.mil/sti/pdfs/ADA588839.pdf
    Viscosity is based on the report: http://www.cnofs.org/Handbook_of_Geophysics_1985/Chptr14.pdf

    Outer function
    Inputs:
            h: (m) or (ft) height
            is_SI: True for using SI unit, false for using British unit

    Outputs:
            temp: (k) or (R) absolute temperature 
            press: (Pa) or (psia) pressure
            dens: (kg/m^3) or (slug/ft^3) air density
            c_sound: (m/s) or (ft/s) speed of sound
            visc: (N*s/m^2) or (lbf*s/ft^2) air viscosity
            g: (m/s^2) or (ft/s^2) gravitational acceleration

    Inner function
    Input:
            H_b: (m') geopotential height

    Output:
            b, L_mb, T_mb, P_b: used in atm calculation

    Notes:
            1. All information based on 1976 US standard atmosphere
            2. Output may have insignificant difference from literature data, especially at high altitudes
            3. Checked with 1976 US Standard Atmosphere, close enough for trade studies & rough calculations
            4. Viscosity values have relatively large error from 1976 Standard Atmosphere, although still within
                exceptable range
            

    History:
            02.14.2021, Created. XT
            02.15.2021, Debugged and checked with literature values. XT
            02.15.2021, Added viscosity. XT
    '''
    # Constants
    R_bar = 8314.32     # (N*m)/(kmol*K), universal gas constant
    r_o = 6356766       # m, effective radius of the earth
    gam = 1.400         # specific heat ratio
    g_o_prime = 9.80665 # m^2/(s^2m'), geopotential constant
    g_o = 9.80665       # m^2/(s^2), gravitational-field strength at sea level
    Gam = 1             # m'/m, unit-converting constant
    MW_air = 28.9644    # kg/kmol, mean molecular weight of air

    # Convert ft to m if is in British unit
    if not is_SI:       # if British unit
        h *= 0.3048

    # Check valid height
    if (h < -5000) and (h >= 86000):     # Limit of this model
        if is_SI:
            print("At height " + str(h) + "m, the function \"std_atm\" is not valid")
        else:
            print("At height " + str(h * 3.28084) + "ft, the function \"std_atm\" is not valid")
        return

    # Geopotential height
    H: float = (Gam * r_o * h) / (r_o + h)
    b, H_b, L_mb, T_mb, P_b = get_val(H)

    # Temperature based on Molecular-scale temperature in K
    T_m: float = T_mb + L_mb * (H - H_b)
    if h < 80000:
        temp = T_m
    else:
        temp = T_m
        print("Above 80000m height, molecular-scale temp may differ from absolute temp, as large as 0.0787K at h = "
              "86000m")

    # Pressure in Pa
    tol = 1E-06
    if abs(L_mb) <= tol:    # L_mb == 0
        press = P_b * numpy.exp((-g_o_prime * MW_air * (H - H_b)) / (R_bar * T_mb))
    else:   # L_mb != 0
        press = P_b * (T_mb / (T_mb + L_mb * (H - H_b))) ** ((g_o_prime * MW_air) / (R_bar * L_mb))

    # Density in kg/m^3
    dens = (press * MW_air) / (R_bar * T_m)

    # Speed of sound in m/s
    c_sound = numpy.sqrt((gam * R_bar * T_m) / MW_air)

    # Dynamic Viscosity in (N*s/m^2) or (Pa*s)
    beta_const = 1.458E-06              # kg s^-1 m^-1 k^-0.5
    S_const = 110.4                     # K
    visc = (beta_const * temp ** (3/2)) / (temp + S_const)

    # Gravity in m/s^2
    g = g_o * (r_o / (r_o + h)) ** 2

    # Output based on input unit of height
    if is_SI:       # SI unit
        return temp, press, dens, c_sound, visc, g
    else:           # British unit
        temp *= 1.8                         # K to R
        press *= 0.000145038                # Pa to psia
        dens *= 0.00194032                  # kg/m^3 to slug/ft^3
        c_sound *= 3.2808399                # m/s to ft/s
        visc *= (0.224809 / 3.28084 ** 2)   # (N*s)/m^2 to (lbf*s)/ft^2
        g *= 3.2808399                      # m/s^2 to ft/s^2
        return temp, press, dens, c_sound, visc, g





