"""
Script for de-icing operations
Including de-icing rate, power consumption estimation

Note:
    1. Power estimation based on paper "Estimation of Power Requirements for Electrical De-Icing Systems".
        The paper is in Google doc > References

History
    05.05.2021, XT. Created
    05.05.2021, XT. Roughly debugged, still has unit confusion from paper but limited effect on final value
"""

from Class130 import AtmData
import numpy as np

def main_deIcing_power(AtmData, x_loc, thickness, span, freeze_factor, C_liquid, C_ice, C_p_air, L_f, L_e, T_target, T_inf, T_skin, k_air, R_h,
                      rho_LWC, v_wall):
    """
    Approximate the de-icing power required
    :param AtmData: Class130, contains atmospheric data
    :param x_loc: m, location of interest (usually 0.0005 mm past leading edge)
    :param thickness: m, maximum airfoil thickness
    :param span: m, wing span
    :param freeze_factor: Non-dimensional, 0-1, freezing fraction, indicates the amount of liquid water that turns into ice
    :param C_liquid: J/(kg K), specific heat capacity of liquid water
    :param C_ice: J/(kg K), specific heat capacity of ice
    :param C_p_air: J/(kg K), specific heat capacity under constant pressure for air
    :param L_f: J/kg, latent heat of water fusion
    :param L_e: J/kg, latent heat of water evaporation
    :param T_target: deg C, target heating temperature
    :param T_inf: deg C, environment temperature
    :param T_skin: deg C, temperature at surface
    :param k_air: W/(mK), thermal conductivity of air
    :param R_h: Non-dimensional, relative humidity, actual / saturated vapor pressure
    :param rho_LWC: kg/m^3, liquid water content, mass of supercooled water per volume
    :param v_wall: m/s, (not sure) surface layer velocity (can assume 0 due to laminar flow)
    :return: required power
    """

    q_load = deIcing_heat_load(AtmData, x_loc, thickness, span, freeze_factor, C_liquid, C_ice, C_p_air, L_f, L_e,
                               T_target, T_inf, T_skin, k_air, R_h, rho_LWC, v_wall)

    P_req = deIcing_power_calculation(q_load, thickness, span)

    return P_req


def deIcing_power_calculation(q_load, thickness, span):
    """
    Calculates the de-icing power requirement
    :param q_load: float, (W/m^2), total heating load required
    :param thickness: float, (m), iced thickness
    :param span: float, (m), iced span of wing
    :return: P_req, (W), power required for de-icing
    """
    S_ice = thickness * span  # m^2, area of imaginary sieve
    P_req = q_load * S_ice  # W, required power

    return P_req


def deIcing_heat_load(AtmData, x_loc, thickness, span, freeze_factor, C_liquid, C_ice, C_p_air, L_f, L_e,
                      T_target, T_inf, T_skin, k_air, R_h, rho_LWC, v_wall):

    """
    Calculates the de-icing heat load under given condition
    Parameters all the same as the main_deIcing_power
    :param AtmData: Class130, contains atmospheric data
    :param x_loc: m, location of interest (usually 0.0005 mm past leading edge)
    :param thickness: m, maximum airfoil thickness
    :param span: m, wing span
    :param freeze_factor: Non-dimensional, 0-1, freezing fraction, indicates the amount of liquid water that turns into ice
    :param C_liquid: J/(kg K), specific heat capacity of liquid water
    :param C_ice: J/(kg K), specific heat capacity of ice
    :param C_p_air: J/(kg K), specific heat capacity under constant pressure for air
    :param L_f: J/kg, latent heat of water fusion
    :param L_e: J/kg, latent heat of water evaporation
    :param T_target: deg C, target heating temperature
    :param T_inf: deg C, environment temperature
    :param T_skin: deg C, temperature at surface
    :param k_air: W/(mK), thermal conductivity of air
    :param R_h: Non-dimensional, relative humidity, actual / saturated vapor pressure
    :param rho_LWC: kg/m^3, liquid water content, mass of supercooled water per volume
    :param v_wall: m/s, (not sure) surface layer velocity (can assume 0 due to laminar flow)
    :return: q_load, heat_load_required
    """


    v_inf = AtmData.vel  # m/s, free stream velocity
    mu_inf = AtmData.visc  # (Pa s), free stream viscosity
    rho_inf = AtmData.dens  # (kg/m^3), free stream air density
    P_inf = AtmData.pres  # (Pa), free stream pressure
    E_m = 0.00324 * (v_inf / thickness) ** 0.613  # Non-dimensional, 0-1, water catch efficiency (1 for full catch)
             # E_m is func(airspeed, droplet size, airfoil thickness, shape, viscosity, air density)

    m_dot_local = E_m * v_inf * thickness * span * rho_LWC  # kg/(s m^2), local water catch

    ### power requirement for continuously heated surfaces
    # sensible heating
    dT = T_target - T_inf  # deg C or K, change in temperature
    q_dot_sens = m_dot_local * (dT * ((1 - freeze_factor) * C_liquid + freeze_factor * C_ice) + freeze_factor * L_f)

    # convection heat loss

    Re_x = (rho_LWC * v_inf * x_loc) / mu_inf  # Reynolds number
    alpha = k_air / (C_p_air * rho_inf)  # thermal diffusivity of air
    Pr = mu_inf / alpha  # Prandtl number, ratio of viscosity over thermal diffusivity
    Nu = 0.0296 * Re_x ** 0.8 * Pr * (1 / 3)  # Nusselt number
    h_0 = Nu * k_air / x_loc  # W/K, local heat transfer coefficient
    q_dot_conv = h_0 * (T_skin - T_inf)

    # evaporative heat loss
    e_inf = saturation_pressure(T_inf)  # Pa, ambient saturation pressure
    e_surf = saturation_pressure(T_skin)  # Pa, surface saturation pressure
    q_dot_evap = 0.7 * h_0 * L_e * (R_h * e_inf - e_surf) / (P_inf * C_p_air)

    # kinetic heating
    q_dot_KE = m_dot_local * 0.5 * v_inf ** 2

    # aerodynamic heating
    R_c = 1 - ((0.99 * v_wall ** 2) / (v_inf ** 2)) * (1 - Pr ** freeze_factor)  # boundary recovery factor with n = 0.5 due to laminar boundary layer
    q_dot_aero = R_c * h_0 * (v_inf ** 2) / (2 * C_p_air)

    # total heat rate
    q_dot_PS = q_dot_sens + q_dot_conv + q_dot_evap + q_dot_KE + q_dot_aero

    ### power requirements for cyclic heated surfaces
    m_dot_ice = thickness * rho_LWC  # local ice mass flow rate per unit area
    eff_heat = 0.7  # heating efficiency
    q_dot_cycl = eff_heat * (m_dot_ice / thickness) * (dT * C_ice + L_f)
    # the unit in the paper is SUPER weird, but this q_dot_cycl doesn't affect that much

    ### Total heating power, with k-factors
    K_PS = 0.19  # ratio of the area of continuously heated parting strips against total area to be de-iced
    # Adopted from general layout
    K_cycl = 0.05  # ratio of cyclic heat on time against total cycle time.
    # Take 9s heat-on time in 3 min = 180 sec, yield 5%
    q_load = q_dot_PS * K_PS + q_dot_cycl * K_cycl

    return q_load


def saturation_pressure(T):
    """
    Calculates saturation pressure of water vapor
    :param T: float, (deg C), temperature of interest
    :return: (Pa), saturation pressure
    """
    T_k = T + 273.15  # convert from C to K
    # from https://www.engineeringtoolbox.com/water-vapor-saturation-pressure-air-d_689.html
    exp_power = (77.3450 + 0.0057 * T_k - 7235 / T_k) / (T_k ** 8.2)  # empirical
    return np.exp(exp_power)


if __name__ == '__main__':
    # needed inputs
    vel = 121 * 0.514444  # airspeed, 121 knots to m/s
    h = 6000 * 0.3048  # altitude, 6000 ft to m
    atm = AtmData(vel, h, is_SI=True)
    x_loc = 0.0005  # m, location of interest (just 0.5 mm past leading edge)
    C_liquid = 4184  # J/(kg K), specific heat capacity of liquid water
    C_ice = 2093  # J/(kg K), specific heat capacity of ice
    L_f = 3.34e5  # J/kg, latent heat of water fusion
    T_target = 6  # deg C, target heating temperature
    T_inf = atm.temp - 273.15  # deg C, environment temperature (assume under standard atmosphere)
    T_skin = T_target  # deg C, temperature at surface
    k_air = 0.0227  # W/(mK), thermal conductivity of air at 255.3 K
    R_h = 1  # Non-dimensional, relative humidity, actual / saturated vapor pressure
    C_p_air = 1000  # J/(kg K), specific heat capacity under constant pressure for air (at 300K)
    L_e = 2.257e6  # J/kg, latent heat of water evaporation
    rho_LWC = 4.5e-4  # kg/m^3, liquid water content, mass of supercooled water per volume (assume stratocumulus)
    thickness = 0.14166 * 1.26491  # m, maximum airfoil thickness, using mean chord length
    span = 12.65  # m, airfoil span-wise extension for total wing
    v_wall = 0  # m/s, (Seems to be) surface layer velocity (assumed 0 due to laminar flow)
    freeze_factor = 0.5  # Non-dimensional, 0-1, freezing fraction, indicates the amount of liquid water that turns into ice

    # function call
    P_req = main_deIcing_power(atm, x_loc, thickness, span, freeze_factor, C_liquid, C_ice, C_p_air, L_f, L_e,
                               T_target, T_inf, T_skin, k_air, R_h, rho_LWC, v_wall)

    print('The approximate power required for electrical de-icing is {:.2f} W'.format(P_req))