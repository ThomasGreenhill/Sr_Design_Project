import math
import numpy
import matplotlib.pyplot as plt
from typing import Any, Union
from Class130 import AtmData, Propeller
from prop_design_TVG import prop_design

def prop_analysis(AtmData, Propeller, m0_fn, Cd_fn):

    # def newton(f, fprime, guess, tolerance)

    #     xx(1:2) = [0, guess]

    #     ii = 2;
    #     iter = 1;

    #     while abs(tolerance) < abs(xx(ii)-xx(ii - 1)) || iter == 1
    #         ffprime = fprime(xx(ii));

    #         ff = f(xx(ii));


    #         if ffprime == 0
    #             fprintf('Error, slope at point = 0. Choose a different initial condition')
    #             break
    #         end

    #         xx(ii+1) = xx(ii) - ff / ffprime;
    #         ii = ii + 1;
    #         iter = iter + 1;
    #     end
    #     x_zero = xx(end);

    #     return x_zero, iter
    '''
    prop_analysis_TVG
    Version of prop_analysis from TGreenhill
    Code to analyze a propeller (fixed or variable pitch), based on EAE 130A project 2

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
            

    Calls:
        {none}

    Notes:
        1. 

    History:
        02.27.2021
    '''
    pi = numpy.pi

    Vinf = AtmData.vel
    Rgas = AtmData.R
    k = AtmData.k
    T = AtmData.temp
    rho = AtmData.dens

    n = Propeller.RPM/60
    R = Propeller.radius
    B = Propeller.numB
    c = Propeller.chord
    bet = Propeller.bet
    a0 = Propeller.alp0

    nn = bet.size
    
    D = 2*R
    r = numpy.linspace(0, R, nn)
    x = r / R

    J = Vinf/(n*D)

    ome = 2 * pi * n

    phi = numpy.arctan(J/(pi * x))

    VR = numpy.sqrt(Vinf**2+(ome * r)**2)
    a = numpy.sqrt(k*Rgas*T)
    M = VR/a

    m0 = m0_fn(M)
    sig = B*c/(pi*Propeller.radius)
    the = numpy.zeros((nn,))


    for ii in range(1,nn):
        aa = numpy.cos(phi[ii]) - sig[ii]*m0[ii]/(8*x[ii]) * numpy.tan(phi[ii])
        bb = Vinf / VR[ii] + ((bet[ii] - phi[ii] - a0) * numpy.tan(phi[ii]) + 1) * sig[ii] * m0[ii] / (8 * x[ii])
        cc = -(bet[ii] - phi[ii] - a0) * sig[ii] * m0[ii] / (8 * x[ii])

        # quadratic formula (this was way too slow in ML so I eventually used Newton's method):
        the[ii] = (-bb + numpy.sqrt(bb**2-4*aa*cc))/(2*aa)

    alp = bet - phi - the
    Cl = m0*(alp-a0*pi/180)
    Cd = Cd_fn(Cl)
    lamT = 1 / (numpy.cos(phi))**2 * (Cl * numpy.cos(phi + the) - Cd * numpy.sin(phi + the))
    lamQ = 1 / (numpy.cos(phi))**2 * (Cl * numpy.sin(phi + the) + Cd * numpy.cos(phi + the))

    dCTdx = sig * pi**3 * x**2 / 8 * lamT
    dCQdx = sig * pi**3 * x**3 / 16 * lamQ

    xx = x[x >= 0.15]

    CT = numpy.trapz(dCTdx[x >= 0.15], xx)
    CQ = numpy.trapz(dCQdx[x >= 0.15], xx)
    CP = 2 * pi * CQ

    etap = CT / CP * J
    Pdesign = CP * rho * n**3 * D**5

    Tdesign = CT * rho * n**2 * D**4
    Qdesign = CQ * rho * n**2 * D**5
        
    return J, Pdesign, CP, Tdesign, CT, etap


if __name__ == "__main__":

    def m0_fn(Ma):
        if numpy.any(Ma <= 0.9):
            return (2 * math.pi) / numpy.sqrt(1 - Ma ** 2)
        else:
            return (2 * math.pi) / numpy.sqrt(1 - 0.9 ** 2)

    def Cd_fn(Cl):
        return 0.0095 + 0.0040 * (Cl - 0.2) ** 2  

    v_inf = 156 * 0.514444
    h = 2438.4
    k = 1.4
    R = 287
    is_SI = True
    atm_check = AtmData(v_inf, h, is_SI)
    atm_check.expand(k, R)
    dens = atm_check.dens
    radius = 41 * 0.0254
    RPM = 2400
    CT = 0.0509
    T_req = CT*dens*(RPM/60)**2*(radius*2)**4
    # T_req = 425.6896 * 4.44822
    Cl = 0.4
    numB = 3
    alp0 = numpy.radians(-2)
    prop_check = Propeller(radius, numB, RPM, eta_P = 0, CP = 0, CT = 0, CQ = 0, Cl = 0.4)

    [r, prop_check.chord, prop_check.bet, P_design, T_design, Q_design, eta_P, prop_check.theta] = prop_design(atm_check, prop_check, T_req, m0_fn, Cd_fn)

    # Fixed pitch check
    ll = 101
    Vseq = numpy.linspace(55,160,101) * 1.68781*0.3048

    J = numpy.zeros((ll,))
    Pdesign = numpy.zeros((ll,))
    CP = numpy.zeros((ll,))
    Tdesign = numpy.zeros((ll,))
    CT = numpy.zeros((ll,))
    etap = numpy.zeros((ll,))

    for ii in range(0,ll):
        atm_check = AtmData(Vseq[ii], h, is_SI)
        atm_check.expand(k, R)
        J[ii], Pdesign[ii], CP[ii], Tdesign[ii], CT[ii], etap[ii] = prop_analysis(atm_check, prop_check, m0_fn, Cd_fn)

    plt.figure(1)
    plt.plot(J,Pdesign*0.00134102)
    plt.figure(2)
    plt.plot(J,CP)
    plt.figure(3)
    plt.plot(J,Tdesign)
    plt.figure(4)
    plt.plot(J,CT)
    plt.figure(5)
    plt.plot(J,etap)
    plt.show()