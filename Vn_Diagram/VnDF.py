import numpy as np

## General Calulation for Vs
def Cal_Vs(W,S,rho,CL_max):
    Vs = np.sqrt((W/S)*(2/rho)*(1/CL_max))
    return Vs

## Structural limit on load factor

def SLLF(V, n_max):
    n_SL = np.ones(len(V))*n_max
    return n_SL

## Structural limit on turning radius

def SLtr(V, n_max, unit): #### use either 'e' (English) or 's' (SI)
    if unit == 'e':
        g = 32.2
    elif unit == 's':
        g = 9.81
    else:
        print("Wrong unit!")
        exit()
    Rmin_SL = V**2/(g*np.sqrt(n_max**2-1))
    return Rmin_SL

## Aerodynamic limit on load factor
def ALLF(V,Vs):
    n_AL = (V/Vs)**2
    return n_AL

## Aerodynamic limit on turning radius
def ALtr(V, Vs, unit): #### use either 'e' (English) or 's' (SI)
    if unit == 'e':
        g = 32.2
    elif unit == 's':
        g = 9.81
    else:
        print("Wrong unit!")
        exit()
    Rmin_AL = V**2/(g*np.sqrt((V/Vs)**4-1))
    return Rmin_AL

## Generic V-n maneuver diagram
def Vspn(W,S,rho,CL_max,CL_min):
    Vsp = Cal_Vs(W,S,rho,CL_max) #### Vs_1
    Vsn = Cal_Vs(-W,S,rho,CL_min) #### Vs_-1
    return Vsp, Vsn

## Generic V-n gust diagram
def Calc_Vgust(V,W,S,rho,c_av,CLa,condition):
    g_e = 32.2
    mu_g = (W/S)/(0.5*rho*c_av*g_e*CLa)
    K_g = (0.88*mu_g)/(5.3+mu_g)
    if condition == 'B':
        Ude = 66
    elif condition == 'C':
        Ude = 50
    elif condition == 'D':
        Ude = 25
    else:
        print("Wrong codition!")
        exit()            
    n_GD = 1 + K_g*(CLa*Ude*0.5*rho*V)/(W/S)
    return n_GD
