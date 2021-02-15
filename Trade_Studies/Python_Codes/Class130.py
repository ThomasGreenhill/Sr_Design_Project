
import numpy

# Atmospheric information
class AtmData:
    def __init__(self, vel, temp, pres, dens, visc, k, R, is_SI):
        AtmData.vel = vel               # freestream velocity (m/s) or (ft/s)
        AtmData.temp = temp             # static temperature (K) or (R)
        AtmData.pres = pres             # static pressure (Pa) or (psia)
        AtmData.dens = dens             # air density (kg/m^3) or (slug/ft^3)
        AtmData.visc = visc             # air viscosity (N·s/m^2) or (lbf·s/ft^2)
        AtmData.k = k                   # specific heat ratio
        AtmData.R = R                   # gas constant of air [J/(kg·K)] or [(ft·lbf)/(lbm·R)]
        AtmData.is_SI = is_SI           # is_SI = True for SI units, is_SI = False for British units


# Propeller information
class Propeller:
    # All in SI unit
    def __init__(self, radius, RPM, eta_P, CP, CT, CQ, Cl = 0.4, chord = 1, numB = 3, alp0 = 0,
                 alpha = None, beta = None, theta = None, phi = None):
        Propeller.radius = radius       # propeller radius (m)
        Propeller.RPM = RPM             # rotation per minute
        Propeller.eta_P = eta_P         # propeller efficiency
        Propeller.CP = CP               # power coeff.
        Propeller.CT = CT               # thrust coeff.
        Propeller.CQ = CQ               # torque coeff.
        Propeller.Cl = Cl               # lift coeff. distr.
        Propeller.chord = chord         # chord distr. (m)
        Propeller.numB = numB           # number of blades
        Propeller.alp0 = alp0           # zero-lift AoA (rad)
        Propeller.alpha = alpha         # AoA distr. (rad)
        Propeller.beta = beta           # pitch angle distr. (rad)
        Propeller.theta = theta         # induced angle distr. (rad)
        Propeller.phi = phi             # blade angle distr. (rad)


# Airfoil information
class Airfoil:
    # All in SI unit
    # Will possibly be used with XFOIL
    def __init__(self, name, chord, alp0, alpha, Cla, Cl_max, Cl, Cd, Cm):
        Airfoil.name = name             # name
        Airfoil.chord = chord           # chord length list (m)
        Airfoil.alp0 = alp0             # zero lift AoA (rad)
        Airfoil.alpha = alpha           # AoA list
        Airfoil.Cla = Cla               # lift curve slope
        Airfoil.Cl_max = Cl_max         # max Cl
        Airfoil.Cl = Cl                 # Cl list w.r.t. alpha
        Airfoil.Cd = Cd                 # Cd list w.r.t. alpha
        Airfoil.Cm = Cm                 # Cm list w.r.t. alpha


# Wing information
class Wing:
    # All in SI unit
    def __init__(self, area, span, e, alpha, chord, c_bar, CL, CL_max, CD, CD_0, airfoil):
        Wing.area = area                # wing area (m^2)
        Wing.span = span                # wing span (m)
        Wing.chord = chord              # chord distr. (m)
        Wing.c_bar = c_bar              # average chord length (m)
        Wing.e = e                      # Oswald's span efficiency ratio
        Wing.alpha = alpha              # wing AoA
        Wing.CL = CL                    # wing 3D CL
        Wing.CL_max = CL_max            # wing stall CL
        Wing.CD = CD                    # wing 3D CD
        Wing.CD_0 = CD_0                # zero lift CD
        Wing.airfoil = airfoil          # wing sectional airfoil type list
        Wing.AR = span ** 2 / area      # wing aspect ratio
        Wing.CD_i = CL ** 2 / (e * Wing.AR * numpy.pi)
