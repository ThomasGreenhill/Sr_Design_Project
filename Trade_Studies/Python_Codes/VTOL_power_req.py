
import numpy
import math
import Class130
from prop_design_TVG import prop_design

def VTOL_power_req(m, g_factor, mot_distr, AtmData, Propeller_list):

    def m0_fn(Ma):
        if Ma <= 0.9:
            return (2 * math.pi) / numpy.sqrt(1 - Ma ** 2)
        else:
            return (2 * math.pi) / numpy.sqrt(1 - 0.9 ** 2)

    def Cd_fn(Cl):
        return 0.0095 + 0.0040 * (Cl - 0.2) ** 2

    '''
    VTOL_power_req
    provides data and figures for required power of VTOL aircraft
    
    Input:
            m: kg, aircraft mass
            g_factor = loading factor (1 = hovering)
            mot_distr = Thrust distribution of motors (1xn)
                        Ex. Enter [1,1,1] for same distr. with 3 motors
                        Accepts single value
            AtmData = Class "AtmData" including atmospheric information, see Class130 file
            Propeller_list = list of Class "Propeller" including each propeller information, see Class130 file\
                             Please make sure the sequence are right!
    
    Outputs:
            powerVec = hp, list of power required by each motor
            
    Inner function:
        m0_fn: Kind of like lift curve slope function -- typical:
            m0_fn = @(Ma) (2 * pi ./ sqrt(1 - Ma.^2)) .* (Ma <= 0.9) + (2 * pi ./ ...
            sqrt(1 - 0.9^2)) .* (Ma > 0.9);
        Cd_fn: Blade sectional drag coefficient -- typical:
            Cd_fn = @(Cl) 0.0095 + 0.0040 * (Cl - 0.2).^2;
    
    Calls:
        prop_design_TVG: written by TGreenhill, translated and editted by XTang
    
    History:
        2.09.2021, created by XTang
        2.13.2021, translated by XTang
        2.13.2021, briefly debugged by XTang
    '''

    # Input size check
    if numpy.size(Propeller_list) != numpy.size(mot_distr):
        print("Error: Unequal number of propeller and motors")
        print("Number of propellers: " + str(numpy.size(Propeller_list)))
        print("Number of motors: " + str(numpy.size(mot_distr)))
        return

    g_accel = 9.81      # constant
    T_total = m * g_factor * g_accel

    if numpy.size(mot_distr) != 1:      # Having a list of motor distribution
        for item in mot_distr:
            if item < 0:
                print("Error: mot_distr entry values have to be at least 0")
                return

        sum_distr = sum(mot_distr)
        power_vec = [0] * len(mot_distr)
        eta_vec = [0] * len(mot_distr)

        for i in range(len(mot_distr)):
            cur_distr = mot_distr[i] / sum_distr
            cur_T = cur_distr * T_total
            [_, _, _, power_vec[i], _, _, eta_vec[i], _] = prop_design(AtmData, Propeller_list[i], cur_T)
            power_vec[i] *= 0.00134102    # Converts to hp
            return power_vec, eta_vec

    else:           # Having only one motor
        if mot_distr == 0:
            print("Cannot have 0 as value of mot_distr")
            return

        _, _, _, power_vec, _, _, eta_vec, _ = prop_design(AtmData, Propeller_list, T_total)
        power_vec *= 0.00134102             # Converts to hp
        return power_vec, eta_vec



