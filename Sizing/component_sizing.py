import numpy 
import sys
sys.path.append("../Python_Codes")
from Class130 import SimpleFuelCell

def electric_motor_mass(P_continuous):
    '''
    electric_motor_mass
    Simple function to calcualte electric motor mass based on continuous required power

    Inputs:
        P_continuous: Maximum continuous power output of the elctric motor in W
            

    Outputs:
        engine_mass: Uninstalled engine wegiht in kg
           
    Calls:
        {none}

    Notes:
        1. 

    History:
        02.16.2021: Created and debugged. TVG
    '''

    engine_mass = 0.2322*P_continuous*1e-3
    return engine_mass


def power_system_mass_sizing(distr, rho_battery, E, P_req_H2, battery_reserve):
    '''
    power_system_mass_sizing
    Function to calculate power system mass based on the energy density of the power system and the energy required.

    Inputs:
        distr: fraction of battery energy to total energy (1 = no hydrogen, 0 = no battery)
        rho_battery: energy density of battery in Wh/kg 
        E: Energy required in Wh
        P_req_H2: Power required from hydrogen fuel system in W
        battery_reserve: fraction of battery energy left as reserve
            

    Outputs:
        power_system_mass: power system mass
        fuel_cell_name: model of fuel cell required 
           
    Calls:
        {none}

    Notes:
        1. Fuel cell data comes from:
            https://www.ballard.com/about-ballard/publication_library/product-specification-sheets/fcvelocity-md30-spec-sheet
            https://www.ballard.com/about-ballard/publication_library/product-specification-sheets/fcvelocity-hd-spec-sheet
            https://www.ballard.com/about-ballard/publication_library/product-specification-sheets/fcmovetm-spec-sheet
        
        2. ******
        CURRENT IMPLEMENTATION DOES NOT INCLUDE A RESERVE FOR THE H2 ENERGY SIDE. REVISION NEEDED 
        *********


    History:
        02.16.2021: Created and debugged. TVG
    '''

    if P_req_H2 <= 30e3:
        SimpleFuelCell.rated_power = 30e3   #W
        SimpleFuelCell.cell_weight = 175    #kg
        SimpleFuelCell.name = "30kW fcvelocity-md30"
    elif P_req_H2 > 30e3 and P_req_H2 <= 70e3:
        SimpleFuelCell.rated_power = 70e3   #W
        SimpleFuelCell.cell_weight = 250    #kg
        SimpleFuelCell.name = "70kW fcvelocity-hd"
    elif P_req_H2 > 70e3 and P_req_H2 <= 85e3:
        SimpleFuelCell.rated_power = 85e3   #W
        SimpleFuelCell.cell_weight = 361    #kg
        SimpleFuelCell.name =  "85kW fcmovetm"
    elif P_req_H2 > 85e3 and P_req_H2 <= 100e3:
        SimpleFuelCell.rated_power = 100e3   #W
        SimpleFuelCell.cell_weight = 385    #kg 
        SimpleFuelCell.name = "100kW fcmovetm"
    elif P_req_H2 > 100e3 and P_req_H2 <= 140e3:
        SimpleFuelCell.rated_power = 70e3*2   #W
        SimpleFuelCell.cell_weight = 250*2    #kg
        SimpleFuelCell.name = "Two 70kW fcvelocity-hd"
    elif P_req_H2 > 140e3 and P_req_H2 <= 170e3:
        SimpleFuelCell.rated_power = 85e3*2   #W
        SimpleFuelCell.cell_weight = 361*2    #kg
        SimpleFuelCell.name =  "Two 85kW fcmovetm"
    elif P_req_H2 > 170e3 and P_req_H2 <= 200e3:
        SimpleFuelCell.rated_power = 100e3*2   #W
        SimpleFuelCell.cell_weight = 385*2    #kg 
        SimpleFuelCell.name =  "Two 100kW fcmovetm"
    else:
        SimpleFuelCell.name = "No Single Suitable Fuel Cell"

    battery_energy = E*distr/(1-battery_reserve)
    battery_mass = battery_energy/rho_battery

    rho_H2 = 120e6  #J/kg 
    cell_efficiency = 0.57 # This is an approximation
    # Assume 11.3% of the weight of the hydrogen fuel storage system is actually hydrogen, rest is storage system
    ratio = 0.05
    H2_energy = E*(1-distr)
    H2_mass = ((H2_energy/rho_H2)/cell_efficiency)/ratio

    power_system_mass = H2_mass+battery_mass


    misc_elec_mass = 20

    power_system_mass += misc_elec_mass

    fuel_cell_name = SimpleFuelCell.name

    return power_system_mass, fuel_cell_name


def power_requirements(eta_mech, eta_p, V_hover_climb, V_climb, V_cruise, W_TOGW, f, M, S_disk, S_wing, rho, CD0, AR, e, gam_climb):
    '''
    power_requirements
    Function to calculate the power and energy requirements 

    Inputs:
        eta_mech: mechanical efficiency
        eta_p: propeller efficiency
        V_hover_climb: hover climb velocity in m/s
        V_climb: forward flight climb velocity in m/s
        V_cruise: cruise velocity in m/s
        W_TOGW: takeoff gross weight in N
        f: adjustment for downwash of fuselage
        M: measure of merit
        S_disk: total aircraft disk area in m^2
        S_wing: wing planform are in m^2
        rho: air density in kg/m^3
        CD0: zero-lift drag coefficient of total aircraft
        AR: wing aspect ratio
        e: wing span efficiency factor
        gam_climb: climb angle in radians


    Outputs:
        P_cruise: Cruise power (forward flight configuration) in W
        P_climb: Climb power (forward flight configuration) in W
        P_hover_climb: Climb power (hover flight configuration) in W
           
    Calls:
        {none}

    Notes:
        1. 

    History:
        02.16.2021: Created and debugged. TVG
    '''

    P_hover_climb = (1/eta_mech)*((W_TOGW*V_hover_climb)/2 + f*W_TOGW/M)*numpy.sqrt(f*(W_TOGW/S_disk)/(2*rho))
    P_hover_descent = (1/eta_mech)*(f*W_TOGW/M)*numpy.sqrt(f*(W_TOGW/S_disk)/(2*rho))
    
    L = W_TOGW
    K = 1/(numpy.pi*e*AR)

    # Cruise drag calculation
    CL_cruise = L/(0.5*rho*V_cruise**2*S_wing)
    if CL_cruise > 0.6:
        print("Cruise CL exceeds 0.6")
    
    CD_cruise = CD0 + K*CL_cruise**2
    D_cruise = 0.5*rho*V_cruise**2*S_wing*CD_cruise

    # Climb drag calculation
    CL_climb = L/(0.5*rho*V_climb**2*S_wing)
    if CL_climb > 1:
        print("Climb CL exceeds 1")
    CD_climb = CD0 + K*CL_climb**2
    D_climb = 0.5*rho*V_climb**2*S_wing*CD_climb

    # Cruise and climb power calculations
    P_cruise = (D_cruise*V_cruise/eta_p)/eta_mech
    P_climb = V_climb/eta_p*(D_climb+W_TOGW*numpy.sin(gam_climb))*(1/eta_mech)

    return P_cruise, P_climb, P_hover_climb, P_hover_descent

if __name__ == "__main__":

    # Test electric_motor_weight
    print("\n Testing Electric Motor Weight Function \n")
    engine_mass = electric_motor_mass(70e3)
    print("\t Engine Mass", engine_mass)

    # Test 
    print("\n Testing Power System Mass Function \n")
    power_system_mass, power_system_name = power_system_mass_sizing(0.5, 260, 70e3, 70e3, 0.2)
    print("\t Power System Mass", power_system_mass)
    print("\t Power System Model:", power_system_name)

    # Test power_requirements
    print("\n Testing Power Requirements Function \n")
    P_cruise, P_climb, P_hover_climb = power_requirements(0.9, 0.85, 2.4, 44, 62, 757*9.81, 0.1, 0.8, 10, 16.2, 1.225, 0.02, 8, 0.7, numpy.arctan(1/20))
    print("\t Cruise Power = ", P_cruise, "\n \t Forward Flight Climb Power = ", P_climb, "\n \t Hover Climb Power = ", P_hover_climb,"\n")