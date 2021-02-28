import os
import numpy
import std_atm
import matplotlib.pyplot as plt
import pandas as pd
# Import pyxfoil from a different folder as a module
import sys

sys.path.append('../Utilities')
import pyxfoil

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
    def __init__(self, vel, h, is_SI):
        self.alt = h  # altitude (m) or (ft)
        self.vel = vel  # freestream velocity (m/s) or (ft/s)
        self.is_SI = is_SI  # is_SI = True for SI units, is_SI = False for British units
        temp, pres, dens, c_sound, visc, g = std_atm.std_atm(h, is_SI)
        self.temp = temp  # static temperature (K) or (R)
        self.pres = pres  # static pressure (Pa) or (psia)
        self.dens = dens  # air density (kg/m^3) or (slug/ft^3)
        self.visc = visc  # air viscosity (N·s/m^2) or (lbf·s/ft^2)
        self.sound_speed = c_sound  # speed of sound (m/s) or (ft/s)
        self.grav = g  # gravitational acceleration (m/s^2) or (ft/s^2)

    def expand(self, k, R) -> object:
        """
        :param k: specific heat ratio
        :param R: gas constant
        :return: None
        """
        self.k = k  # specific heat ratio
        self.R = R  # gas constant of air [J/(kg·K)] or [(ft·lbf)/(lbm·R)]
        return

    def print(self) -> None:
        """
        Prints out the existing attributes and values of AtmData class
        :return:
        """
        num_round: int = 5
        if self.is_SI:
            print("==========================================")
            print("At the height of {} m".format(round(self.alt, num_round)))
            print("==========================================")
            print("Air speed      (m/s)        :    {}".format(round(self.vel, num_round)))
            print("Temperature    (K)          :    {}".format(round(self.temp, num_round)))
            print("Pressure       (Pa)         :    {}".format(round(self.pres, num_round)))
            print("Density        (kg/m^3)     :    {}".format(round(self.dens, num_round * 2)))
            print("Viscosity      (Ns/m^2)     :    {}".format(round(self.visc, num_round * 2)))
            print("Sound speed    (m/s)        :    {}".format(round(self.sound_speed, num_round)))
            print("Grav. accel    (m/s^2)      :    {}".format(round(self.grav, num_round)))
            print("==========================================")
        else:
            print("==========================================")
            print("At the height of {} ft".format(round(self.alt, num_round)))
            print("==========================================")
            print("Air speed      (ft/s)       :    {}".format(round(self.vel, num_round)))
            print("Temperature    (R)          :    {}".format(round(self.temp, num_round)))
            print("Pressure       (psia)       :    {}".format(round(self.pres, num_round)))
            print("Density        (slug/ft^3)  :    {}".format(round(self.dens, num_round * 2)))
            print("Viscosity      (lbfs/ft^2)  :    {}".format(round(self.visc, num_round * 2)))
            print("Sound speed    (ft/s)       :    {}".format(round(self.sound_speed, num_round)))
            print("Grav. accel    (ft/s^2)     :    {}".format(round(self.grav, num_round)))
            print("==========================================")
        return

    def convert(self) -> object:
        """
        Converts to the other unit system (SI to imperial or imperial to SI)
        :return: None
        """
        # All convertion factors from SI to imperial
        temp_conv = 1.8
        pres_conv = 0.000145038
        dens_conv = 0.00194032
        m2ft = 3.28084
        visc_conv = 0.224809 / (m2ft ** 2)
        if self.is_SI:
            self.is_SI = False
            self.temp *= temp_conv
            self.pres *= pres_conv
            self.dens *= dens_conv
            self.visc *= visc_conv
            self.sound_speed *= m2ft
            self.vel *= m2ft
            self.grav *= m2ft
        else:
            self.is_SI = True
            self.temp /= temp_conv
            self.pres /= pres_conv
            self.dens /= dens_conv
            self.visc /= visc_conv
            self.sound_speed /= m2ft
            self.vel /= m2ft
            self.grav /= m2ft
        return


# Propeller information
class Propeller:
    # All in base SI units
    def __init__(self, radius, RPM, eta_P, CP, CT, CQ, Cl=0.4, chord=1, numB=3, alp0=0,
                 alpha=None, beta=None, theta=None, phi=None):
        self.radius = radius  # propeller radius (m)
        self.RPM = RPM  # rotation per minute
        self.eta_P = eta_P  # propeller efficiency
        self.CP = CP  # power coeff.
        self.CT = CT  # thrust coeff.
        self.CQ = CQ  # torque coeff.
        self.Cl = Cl  # lift coeff. distr.
        self.chord = chord  # chord distr. (m)
        self.numB = numB  # number of blades
        self.alp0 = alp0  # zero-lift AoA (rad)
        self.alpha = alpha  # AoA distr. (rad)
        self.beta = beta  # pitch angle distr. (rad)
        self.theta = theta  # induced angle distr. (rad)
        self.phi = phi  # blade angle distr. (rad)


# Airfoil information
class Airfoil:
    # All in base SI units
    # Used with XFOIL.exe

    def __init__(self, foilname: str):
        """
        :param is_NACA: True for NACA airfoil, false for other airfoild
        :param foil: If NACA, input series number (2412, etc)
                     If not NACA, input geometry file directory
        """
        if type(foilname) != str:
            raise TypeError("Please input type: str for airfoil name")
        cur_name = ""
        cur_series = ""
        for letter in foilname:
            if letter.isalpha():
                cur_name += letter.lower()
            elif letter.isspace():
                pass
            elif letter.isnumeric():
                cur_series += letter.lower()
            else:
                raise NameError("Airfoil name only excepts letters, numbers, or whitespaces")
        if cur_name == 'naca':
            self.NACA = True  # True for NACA airfoils, False for other
        else:
            self.NACA = False
        self.foil = cur_series  # Serie number for airfoil
        self.foilname = foilname.replace(" ", "")  # Name of airfoil
        self.geom_file_path = None
        self.iter_num = 100  # Default
        self.num_alfs = 10  # Default
        self.polar = None  # Initialized to store polar data

    def iter_num(self, new_iter_num: int):
        """
        Changes the attribute iteration number
        :param new_iter_num: number to update
        :return: None
        """
        self.iter_num = new_iter_num
        return

    def num_alfs(self, new_num_alfs: int):
        """
        Changes the attribute number of AoA's
        :param new_num_alfs: number to update
        :return: None
        """
        self.num_alfs = new_num_alfs
        return

    def add_geom_file(self, geom_file_path: str):
        """
        Attaches the geometry file to the class
        :param geom_file_path: (str) path to attach
        :return: None
        """
        if os.path.isfile(geom_file_path):
            self.geom_file_path = geom_file_path
            print("Geometry file successfully attached")
        else:
            raise FileExistsError

    def get_polar(self, Re, alf_start, alf_end):
        """
        :param Re: Reynold's number !!! Shall not be 0 otherwise have unknown problems
        :param alf_start: (deg) first AoA
        :param alf_end: (deg) last AoA
        :return: None
        """
        self.Re = Re
        self.num_alfs = (alf_end - alf_start + 1) * 2
        alfs = numpy.linspace(alf_start, alf_end, self.num_alfs)
        if self.NACA:  # NACA airfoil
            self.foilname: str = 'naca' + str(self.foil)
            self.geom_file_path: str = './Data/' + self.foilname + '/' + self.foilname + '.dat'
            pyxfoil.GetPolar(self.foil, self.NACA, alfs, Re, SaveCP=False, Iter=self.iter_num, quiet=True)
            polar_file: str = '{}_polar_Re{:.2e}a{:.1f}-{:.1f}.dat'.format(self.foilname, Re, alf_start, alf_end)
            polar_path: str = './Data/{}/{}'.format(self.foilname, polar_file)
            self.polar = pyxfoil.ReadXfoilPolar(polar_path)
            return self.polar
        else:  # Not NACA airfoil
            if self.geom_file_path is None:
                raise Exception("Please use obj.add_geom_file func to add file path first.")
            else:
                pyxfoil.GetPolar(self.geom_file_path, self.NACA, alfs, Re, SaveCP=False, Iter=self.iter_num, quiet=True)
                polar_file: str = '{}_polar_Re{:.2e}a{:.1f}-{:.1f}.dat'.format(self.foilname, Re, alf_start, alf_end)
                polar_path: str = './Data/{}/{}'.format(self.foilname, polar_file)
                self.polar = pyxfoil.ReadXfoilPolar(polar_path)
                return self.polar

    def geom_plot(self, save=False, show=True):
        """
        Plots the airfoil geometry
        :return: None
        """
        if self.geom_file_path is None:
            raise FileNotFoundError("Please attach geom files using obj.add_geom_file or call obj.polar first")

        self.geom = pyxfoil.ReadXfoilAirfoilGeom(self.geom_file_path)
        geom_fig = plt.figure()
        plt.title('Airfoil geometry of {}'.format(self.foilname))
        plt.plot(self.geom['x'], self.geom['z'])
        plt.axis('equal')
        plt.xlabel('x/c')
        plt.grid()
        plt.ylabel('z/c')
        if show:
            plt.show()
        if save:
            save_path: str = 'Data/{}/{}_geom'.format(self.foilname, self.foilname)
            geom_fig.savefig(save_path, bbox_inches='tight')
        return

    def lift_curve(self, save=False, show=True):
        """
        Plots the lift curve of the airfoil.
        :return: alfs: list of AoA
                 Cls: list of Cl
        """
        if self.polar is None:
            raise Exception("Please call obj.polar first.\nFunc call hint: polar(Re, alf_start, alf_end)")
        lift_curve_fig = plt.figure()
        plt.title('Lift curve of {} at Re = {:.2e}'.format(self.foilname, self.Re))
        plt.plot(self.polar['alpha'], self.polar['Cl'])
        plt.xlabel('Angle of attack (alpha)')
        plt.grid()
        plt.ylabel('Lift coefficient (Cl)')
        if show:
            plt.show()
        if save:
            save_path: str = 'Data/{}/{}_lift_curve'.format(self.foilname, self.foilname)
            lift_curve_fig.savefig(save_path, bbox_inches='tight')
        return self.polar['alpha'], self.polar['Cl']

    def drag_polar(self, save=False, show=True):
        """
        Plots the drag polar of the airfoil.
        :return: alfs: list of AoA in deg
                 Cds: list of cd
        """
        if self.polar is None:
            raise Exception("Please call obj.polar first.\nFunc call hint: polar(Re, alf_start, alf_end)")
        drag_polar_fig = plt.figure()
        plt.title('Drag polar of {} at Re = {:.2e}'.format(self.foilname, self.Re))
        plt.plot(self.polar['Cl'], self.polar['Cd'])
        plt.xlabel('Lift coefficient (Cl)')
        plt.grid()
        plt.ylabel('Drag coefficient (Cd)')
        if show:
            plt.show()
        if save:
            save_path: str = 'Data/{}/{}_drag_polar'.format(self.foilname, self.foilname)
            drag_polar_fig.savefig(save_path, bbox_inches='tight')
        return self.polar['Cl'], self.polar['Cd']


# Wing information
class Wing:
    # All in base SI units
    def __init__(self, area, span, e, alpha, chord, c_bar, CL, CL_max, CD, CD_0, airfoil):
        self.area = area  # wing area (m^2)
        self.span = span  # wing span (m)
        self.chord = chord  # chord distr. (m)
        self.c_bar = c_bar  # average chord length (m)
        self.e = e  # Oswald's span efficiency ratio
        self.alpha = alpha  # wing AoA
        self.CL = CL  # wing 3D CL
        self.CL_max = CL_max  # wing stall CL
        self.CD = CD  # wing 3D CD
        self.CD_0 = CD_0  # zero lift CD
        self.airfoil = airfoil  # wing sectional airfoil type list
        self.AR = span ** 2 / area  # wing aspect ratio
        self.CD_i = CL ** 2 / (e * Wing.AR * numpy.pi)


# Fuel cell information
class FuelCell:
    # All in base SI units
    def __init__(self, name, rated_power, min_voltage, max_voltage, max_current, cell_dimensions, cell_weight,
                 coolant_dimensions, coolant_weight, air_dimensions, air_weight, oxidant, fuel_flow_rate,
                 fuel_efficiency, sound_level):
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


if __name__ == '__main__':
    # AtmData
    '''
    is_SI = True
    vel = 300
    h = 0
    atm = AtmData(vel, h, is_SI)
    atm.convert()
    atm.expand(1.4, 53.35)
    atm.print()
    '''

    # Airfoil
    #foil = Airfoil("NACA 2412")
    Re = 5e6
    alf_start = 0
    alf_end = 5
    #foil.get_polar(Re, alf_start, alf_end)
    #foil.geom_plot(save=True, show=False)
    #foil.lift_curve(save=True, show=False)
    #foil.drag_polar(save=True, show=False)

    foil = Airfoil("P51D")
    foil.add_geom_file("./Data/p51d/p51d.dat")
    foil.get_polar(Re, alf_start, alf_end)
    #foil.geom_plot(save=True, show=False)
    #foil.lift_curve(save=True, show=False)
    #foil.drag_polar(save=True, show=False)