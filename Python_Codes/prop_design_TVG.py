
import math
import numpy
import matplotlib.pyplot as plt
from typing import Any, Union
from Class130 import AtmData, Propeller
import sys
sys.path.append("../Utilities")
# Ignore warnings because runtime warnings pop up due to division by almost zero (propeller properties at the blade root)
import warnings
warnings.filterwarnings("ignore")

try:
    import formatfigures
    formatfigures.formatsubfigures()
    latex = True
except:
    print("Not using latex formatting")
    latex = False

def prop_design(AtmData, Propeller, T_req, m0_fn, Cd_fn):
    # return r, c, beta, P_design, T_design, Q_design, eta_P, theta
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
        02.25.2021 added initial propeller design as: if __name__ == "main", TVG
        02.27.2021 basic design in if __name__ == "main"
        02.28.2021 added Cd_fn and m0_fn as inputs to function
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
    r = numpy.linspace(0, R, num)
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
        print("RPM = ", Propeller.RPM)
        drag_diverg = True
        
    else:
        drag_diverg = False

    m_0 = [m0_fn(num) for num in Ma]

    # Iteration
    v_0 = [0.05 * AtmData.vel] * num
    T_design = 2e3
    iter = 1
    iterLim = 5e2

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
        
    # print("iter = " + str(iter))
    # End of while loop
    P_design = CP * AtmData.dens * n ** 3 * D ** 5
    Q_design = CQ * AtmData.dens * n ** 2 * D ** 5

    if drag_diverg:
        return

    return r, c, beta, P_design, T_design, Q_design, eta_P, theta


if __name__ == "__main__":

    def m0_fn(Ma):
        if Ma <= 0.9:
            return (2 * math.pi) / numpy.sqrt(1 - Ma ** 2)
        else:
            return (2 * math.pi) / numpy.sqrt(1 - 0.9 ** 2)

    def Cd_fn(Cl):
        return 0.0095 + 0.0040 * (Cl - 0.2) ** 2

    nn = 101

    # v_inf = 62
    # temp = 272.31667
    # pres = 8.988e4
    # dens = 1.112
    # visc = 1.758e-5
    # k = 1.4
    # R = 287
    # is_SI = True
    # atm = AtmData(v_inf, temp, pres, dens, visc, k, R, is_SI)

    # radius = 1.78/2
    # RPM = numpy.linspace(500,2950,nn)
    # LD = 15
    # T_req = 13000/LD/8 #N (TOGW/(L/D))
    # Cl = 0.4
    # numB = 3
    # alp0 = numpy.radians(-2)
    
    # P_design = [0] * nn
    # T_design = [0] * nn
    # Q_design = [0] * nn
    # eta_P = [0] * nn

    # for ii in range(0,nn):
    #     prop = Propeller(radius, RPM[ii], Cl, "chord", numB, alp0)
    #     [_, _, _, P_design[ii], T_design[ii], Q_design[ii], eta_P[ii], _] = prop_design(atm, prop, T_req)
    
    # plt.figure()
    # plt.plot(RPM,Q_design)
    # plt.xlabel("RPM")
    # plt.ylabel("Torque (Nm)")
    # plt.title("Torque vs. RPM for Propeller Design at 62 m/s Design Condition")
    # plt.savefig('./Torque_vs_RPM_cruise.jpg', bbox_inches='tight')

    # plt.figure()
    # plt.plot(RPM,eta_P)
    # plt.xlabel("RPM")
    # plt.ylabel("$\eta_p$")
    # plt.title("Efficiency vs. RPM for Propeller Design at 62 m/s Design Condition")
    # plt.savefig('./Efficiency_vs_RPM_cruise.jpg', bbox_inches='tight')

    # plt.figure()
    # plt.plot(RPM,P_design)
    # plt.xlabel("RPM")
    # plt.ylabel("Power (W)")
    # plt.title("Power vs. RPM for Propeller Design at 62 m/s Design Condition")
    # plt.savefig('./Power_vs_RPM_cruise.jpg', bbox_inches='tight')
    # # plt.show()


    temp = 272.31667
    h = 1828
    pres = 8.988e4
    dens = 1.112
    visc = 1.758e-5
    k = 1.4
    R = 287
    is_SI = True
    numB = 3

    radius = 1.78/2
    RPM = numpy.linspace(500,2950,nn)
    LD = 15
    T_req = 13000/8 #N (TOGW/(L/D))
    Cl = 0.4
    alp0 = numpy.radians(-2)
    
    for v_inf in range(20,70,10):
        P_design = [0] * nn
        T_design = [0] * nn
        Q_design = [0] * nn
        eta_P = [0] * nn
        for ii in range(0,nn):
            atm = AtmData(v_inf, h, is_SI)
            atm.expand(1.4, 287)
            prop = Propeller(radius, numB, RPM[ii], eta_P, CP=0, CT=0, CQ=0, Cl=0.4)
            [_, _, _, P_design[ii], T_design[ii], Q_design[ii], eta_P[ii], _] = prop_design(atm, prop, T_req, m0_fn, Cd_fn)
        label = "$V_\infty$ = " + str(v_inf) + " (m/s)"
        plt.figure(4)
        plt.plot(RPM,Q_design,label=label)    
        plt.figure(5)
        plt.plot(RPM,eta_P,label=label)
        plt.figure(6)
        plt.plot(RPM,P_design,label=label)
        # plt.figure(7)
        # plt.plot(RPM,T_design,label=label)
    
    plt.figure(4)
    plt.legend()    
    plt.xlabel("RPM")
    plt.ylabel("Torque (Nm)")
    plt.title("Torque vs. RPM for Propeller Design \n With Different Inlet Velocity Design Condition")
    plt.savefig('./Figures/Torque_vs_RPM_hover.jpg', bbox_inches='tight')

    plt.figure(5)
    plt.legend() 
    plt.xlabel("RPM")
    plt.ylabel("$\eta_p$")
    plt.title("Efficiency vs. RPM for Propeller Design \n With Different Inlet Velocity Design Condition")
    plt.savefig('./Figures/Efficiency_vs_RPM_hover.jpg', bbox_inches='tight')

    plt.figure(6)
    plt.legend() 
    plt.xlabel("RPM")
    plt.ylabel("Power (W)")
    plt.title("Power vs. RPM for Propeller Design \n With Different Inlet Velocity Design Condition")
    plt.savefig('./Figures/Power_vs_RPM_hover.jpg', bbox_inches='tight')

    # plt.figure(7)
    # plt.legend() 
    # plt.xlabel("RPM")
    # plt.ylabel("Thrust (N)")
    # plt.title("Thrust vs. RPM for Propeller Design \n With Different Inlet Velocity Design Condition")
    # plt.savefig('./Figures/Thrust_vs_RPM_hover.jpg', bbox_inches='tight')
    plt.show()

    
