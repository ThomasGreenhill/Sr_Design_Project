
import numpy

'''
Useful Python classes in senior design project

Classes included:
        AtmData: records atmospheric conditions and airspeed
        Propeller: records propeller information
        Airfoil: records airfoil (sectional) information
        Wing: records wing (3D) information and distributions of parameters
        FuelCell: fuel cell with all useful parameters
        SimpleFuelCell: fuel cell with only a few parameters relating to initial sizing

Notes:
        1. Use dummy variables
        2. Wing.AR and Wing.CD_i are calculated based on input. Throw some random number as dummy variables       

History:
        02.13.2021, Created AtmData. XT
        02.13.2021, Added Propeller. XT
        02.14.2021, Added Wing & Airfoil. XT
        02.14.2021, Minor change: added attributes. XT
        02.16.2021, Added class for H2 fuel cells. TVG
'''

# Atmospheric information
class AtmData:
    # In either base SI of British units
    def __init__(self, vel, temp, pres, dens, visc, k, R, is_SI):
        self.dens = None
        self.vel = vel               # freestream velocity (m/s) or (ft/s)
        self.temp = temp             # static temperature (K) or (R)
        self.pres = pres             # static pressure (Pa) or (psia)
        self.dens = dens             # air density (kg/m^3) or (slug/ft^3)
        self.visc = visc             # air viscosity (N·s/m^2) or (lbf·s/ft^2)
        self.k = k                   # specific heat ratio
        self.R = R                   # gas constant of air [J/(kg·K)] or [(ft·lbf)/(lbm·R)]
        self.is_SI = is_SI           # is_SI = True for SI units, is_SI = False for British units


# Propeller information
class Propeller:
    # All in base SI units
    def __init__(self, radius, numB, RPM, eta_P, CP, CT, CQ, Cl, chord = 1, alp0 = 0,
                 alpha = None, beta = None, theta = None, phi = None):
        self.radius = radius       # propeller radius (m)
        self.RPM = RPM             # rotation per minute
        self.eta_P = eta_P         # propeller efficiency
        self.CP = CP               # power coeff.
        self.CT = CT               # thrust coeff.
        self.CQ = CQ               # torque coeff.
        self.Cl = Cl               # lift coeff. distr.
        self.chord = chord         # chord distr. (m)
        self.numB = numB           # number of blades
        self.alp0 = alp0           # zero-lift AoA (rad)
        self.alpha = alpha         # AoA distr. (rad)
        self.beta = beta           # pitch angle distr. (rad)
        self.theta = theta         # induced angle distr. (rad)
        self.phi = phi             # blade angle distr. (rad)


# Airfoil information
class Airfoil:
    # All in base SI units
    # Will possibly be used with XFOIL
    def __init__(self, name, chord, alp0, alpha, Cla, Cl_max, Cl, Cd, Cm):
        self.name = name             # name
        self.chord = chord           # chord length list (m)
        self.alp0 = alp0             # zero lift AoA (rad)
        self.alpha = alpha           # AoA list
        self.Cla = Cla               # lift curve slope
        self.Cl_max = Cl_max         # max Cl
        self.Cl = Cl                 # Cl list w.r.t. alpha
        self.Cd = Cd                 # Cd list w.r.t. alpha
        self.Cm = Cm                 # Cm list w.r.t. alpha


# Wing information
class Wing:
    # All in base SI units
    def __init__(self, area, span, e, alpha, chord, c_bar, CL, CL_max, CD, CD_0, airfoil):
        self.area = area                # wing area (m^2)
        self.span = span                # wing span (m)
        self.chord = chord              # chord distr. (m)
        self.c_bar = c_bar              # average chord length (m)
        self.e = e                      # Oswald's span efficiency ratio
        self.alpha = alpha              # wing AoA
        self.CL = CL                    # wing 3D CL
        self.CL_max = CL_max            # wing stall CL
        self.CD = CD                    # wing 3D CD
        self.CD_0 = CD_0                # zero lift CD
        self.airfoil = airfoil          # wing sectional airfoil type list
        self.AR = span ** 2 / area      # wing aspect ratio
        self.CD_i = CL ** 2 / (e * Wing.AR * numpy.pi)


# Fuel cell information
class FuelCell:
    # All in base SI units
    def __init__(self, name, rated_power, min_voltage, max_voltage, max_current, cell_dimensions, cell_weight, coolant_dimensions, coolant_weight, air_dimensions, air_weight, oxidant, fuel_flow_rate, fuel_efficiency, sound_level):
        self.name = name
        self.rated_power = rated_power
        self.min_voltage = min_voltage
        self.max_voltage = max_voltage
        self.max_current = max_current
        self.cell_dimensions = cell_dimensions
        self.cell_weight = cell_weight
        self.coolant_dimensions = coolant_dimensions
        self.coolant_weight = coolant_weight
        self.air_dimensions = air_dimensions
        self.air_weight = air_weight
        self.oxidant = oxidant
        self.fuel_flow_rate = fuel_flow_rate
        self.fuel_efficiency = fuel_efficiency
        self.sound_level = sound_level


# Simplified fuel cell information
class SimpleFuelCell:
    # All in base SI units
    def __init__(self, rated_power, cell_weight, cell_efficiency):
        self.rated_power = rated_power
        self.cell_weight = cell_weight
        self.cell_efficiency = cell_efficiency
        self.name = name


# Class for sizing purpose
class Sizing:
    # All in base SI units
    def __init__(self, eta_mech, eta_p, V_hover_climb, V_hover_descent, V_climb, V_cruise,
                 f, M, S_disk, S_wing, S_wetted_fuse, rho, e, AR, CD0, gam_climb, distr,
                 rho_battery, battery_reserve, dist_climb, dist_cruise, payload,
                 time_climb, time_hover_climb, time_cruise, time_hover_descent):
        self.eta_mech = eta_mech
        self.eta_p = eta_p
        self.V_hover_climb = V_hover_climb
        self.V_hover_descent = V_hover_descent
        self.V_climb = V_climb
        self.V_cruise = V_cruise
        self.f = f
        self.M = M
        self.S_disk = S_disk
        self.S_wing = S_wing
        self.S_wetted_fuse = S_wetted_fuse
        self.rho = rho
        self.e = e
        self.AR = AR
        self.CD0 = CD0
        self.gam_climb = gam_climb
        self.distr = distr
        self.rho_battery = rho_battery
        self.battery_reserve = battery_reserve
        self.dist_climb = dist_climb
        self.dist_cruise = dist_cruise
        self.payload = payload
        self.time_climb = time_climb
        self.time_hover_climb = time_hover_climb
        self.time_cruise = time_cruise
        self.time_hover_descent = time_hover_descent
        

