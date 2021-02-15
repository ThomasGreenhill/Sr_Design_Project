
import math
import numpy
from typing import Any, Union
from Class130 import AtmData, Propeller



def prop_design(AtmData, Propeller, T_req):

    def m0_fn(Ma):
        if Ma <= 0.9:
            return (2 * math.pi) / numpy.sqrt(1 - Ma ** 2)
        else:
            return (2 * math.pi) / numpy.sqrt(1 - 0.9 ** 2)

    def Cd_fn(Cl):
        return 0.0095 + 0.0040 * (Cl - 0.2) ** 2

    '''
    prop_design_TVG
    Version of prop_design from TGreenhill
    Based on constant Cl
    Code to design a propeller, based on EAE 130A project 2

    Outer function:
    Inputs:
            AtmData: class including v_inf, temp, pres, k, Re, etc
            R: (m) Propeller radius
            n: (Hz) Propeller angular rate 
            T_req: (N) Required thrust
            Cl: Blade sectional lift coefficient -- typical 0.4
            B: Number of blades
            a_0: (rad) Blade sectional zero-lift angle of attack
            

    Outputs:
           r: Vector of nn points from 0 to R along a blade
           c: Vector of blade design chord distribution
           beta: Vector of blade design pitch angle distribution
           P_design: Propeller design power
           T_design: Propeller design thrust
           Q_design: Propeller design torque
           eta_p: Propeller design efficiency
           the: Propeller design theta angle
           
    Inner function:
            m0_fn: Kind of like lift curve slope function -- typical:
                m0_fn = @(Ma) (2 * pi ./ sqrt(1 - Ma.^2)) .* (Ma <= 0.9) + (2 * pi ./ ...
                sqrt(1 - 0.9^2)) .* (Ma > 0.9);
            Cd_fn: Blade sectional drag coefficient -- typical:
                Cd_fn = @(Cl) 0.0095 + 0.0040 * (Cl - 0.2).^2;

    Calls:
        {none}

    Notes:
        1. 02.09.2021 implementation uses sea level standard atmosphere

    History:
        02.09.2021 imported from previous project, TGreenhill
        02.13.2021 translated and editted by XTang
        02.13.2021 briefly debugged by XTang
        02.15.2021 verified by TVG and improved iteration tolerance from 0 decimal places to 12 decimal places
    '''

    if not AtmData.is_SI:
        AtmData.vel *= 0.3048       # ft/s to m/s
        AtmData.temp *= 0.555556    # R to K
        AtmData.press *= 6894.76    # psia to Pa
        AtmData.dens *= 515.379     # slug.ft^3 to kg/m^3

    # Unpacking Propeller class
    R = Propeller.radius
    n = Propeller.RPM / 60
    Cl = Propeller.Cl
    B = Propeller.numB
    a_0 = Propeller.alp0

    num = 201
    D = 2 * R
    r = numpy.linspace(0.15 * R, R, num)
    x = r / R
    t_c = 0.04 / x ** 1.2
    a = numpy.sqrt(AtmData.k * AtmData.R * AtmData.temp)
    M_DD = 0.94 - t_c - Cl / 10     # Given

    J = AtmData.vel / (n * D)
    omega = 2 * math.pi * n     # rad/s
    phi = numpy.arctan(J / (math.pi * x))   # rad
    VR = numpy.sqrt([AtmData.vel ** 2 + item ** 2 for item in (omega * r)])
    Ma = VR / a

    if max(Ma) > max(M_DD):
        print("Error: Local Ma larger than M_DD:")
        print("Ma = " + str(max(Ma)))
        print("M_DD = " + str(max(M_DD)))
        print("Drag Divergence Mach Number Exceeded\n")
        drag_diverg = True
    else:
        drag_diverg = False

    m_0 = [m0_fn(num) for num in Ma]

    # Iteration
    v_0 = [0.05 * AtmData.vel] * num
    T_design = 2e3
    iter = 1
    iterLim = 1e3

    if T_design == T_req:
        print("Error: Trequired = Tdesign. Either change Trequired or modify initial value of Tdesign in code")
        return

    while (numpy.round(T_design, 12) != numpy.round(T_req, 12)) and (iter < iterLim):
        theta = numpy.arctan(([AtmData.vel + item for item in v_0]) / (2 * math.pi * n * r)) - phi

        # For a fixed Cl, calculate c
        sigma = 8 * x * theta * numpy.cos(phi) * numpy.tan(theta + phi) / Cl        #rad
        c = sigma * math.pi * R / B

        alpha = [Cl / item + a_0 for item in m_0]
        beta = alpha + phi + theta
        Cd = Cd_fn(Cl)

        lam_T = 1 / (numpy.cos(phi))**2 * (Cl * numpy.cos(phi + theta) - Cd * numpy.sin(phi + theta))
        lam_Q = 1 / (numpy.cos(phi))**2 * (Cl * numpy.sin(phi + theta) + Cd * numpy.cos(phi + theta))

        dCTdx = sigma * math.pi**3 * x**2 / 8 * lam_T
        dCQdx = sigma * math.pi**3 * x**3 / 16 * lam_Q

        x_need = x[x >= 0.15]
        dCTdx_need = dCTdx[x >= 0.15]
        dCQdx_need = dCQdx[x >= 0.15]
        c_need = c[x >= 0.15]

        CT: float = numpy.trapz(dCTdx_need, x_need)
        CQ: float = numpy.trapz(dCQdx_need, x_need)

        AF = 10**5 / 16 * numpy.trapz(c_need / D * x_need ** 3, x_need)
        CL_design = 4 * numpy.trapz(Cl * x_need ** 3, x_need)

        CP: float = 2 * math.pi * CQ

        eta_P = CT / CP * J
        T_design = CT * AtmData.dens * n**2 * D**4

        if T_design < T_req:
            v_0 = [item * (1 - (T_design - T_req) / abs(T_design + T_req)) for item in v_0]
        elif T_design > T_req:
            v_0 = [item * (1 - (T_design - T_req) / abs(T_design + T_req)) for item in v_0]
        else:
            break

        iter += 1
    # End of while loop
    P_design = CP * AtmData.dens * n ** 3 * D ** 5
    Q_design = CQ * AtmData.dens * n ** 2 * D ** 5

    if drag_diverg:
        return

    return r, c, beta, P_design, T_design, Q_design, eta_P, theta