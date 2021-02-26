
import numpy
import component_sizing
import mass_estimate
#import sys
#sys.path.append("../Utilities")
#import formatfigures
#formatfigures.formatfigures()

def sizing_process(time_hover_climb, time_climb, time_cruise, time_hover_descent,
                   eta_mech, eta_p, V_hover_climb,
                   V_hover_descent, V_climb, V_cruise,
                   f, M, rho, e, AR, CD0, gam_climb, distr,
                   S_disk, S_wing, S_wetted_fuse,
                   rho_battery, battery_reserve, payload):

    '''
    The sizing analysis process loop based on Fig.4 of the report
        from the report "eVTOL Sizing"
        shared by TVG in Discord #Sizing channel 02.16.2021 12:29pm

    Input:
            time_hover_climb: (s) hover climbing time
            time_climb: (s) climbing time
            time_cruise: (s) cruising time
            UPDATE
            payload: (kg) payload

    Output:
            TOGW_est: (N) estimated takeoff gross weight

    Calls:
            component_sizing.power_requirements()
            component_sizing.power_system_mass_sizing()
            component_sizing.electric_motor_weight()
            mass_estimate.mass_estimate()

    Notes:
        1.  ******
        WHEN ADJUSTING 'distr' TO REFLECT NONZERO BATTERY WEIGHT THE CONVERGENCE FAILS. NEEDS DEBUGGING
            ******

    History:
        02.16.2021: Created, XT & TVG & MP
        02.16.2021: Briefly debugged, TVG & XT

    '''

    ## Assumed properties:

    # Initial guess of TOGW
    g = 9.81
    TOGW_guess = 760 * g

    # Start of iteration
    tol = 1E-12         # tolerance for convergence
    iter_num = 0    # time of iteration
    MAX_ITER = 1e4 # maximum number of iteration

    while True:
        # Power in W
        P_cruise, P_climb, P_hover_climb, P_hover_descent = component_sizing.power_requirements(
            eta_mech, eta_p, V_hover_climb, V_climb, V_cruise,
            TOGW_guess, f, M, S_disk, S_wing, rho, CD0, AR, e, gam_climb
        )

        # Energy calculation
        E_cruise = P_cruise * time_cruise
        E_hover_climb = P_hover_climb * time_hover_climb
        E_climb = P_climb * time_climb
        E_hover_descent = P_hover_descent * time_hover_descent
        E_est = E_cruise + E_hover_climb + E_climb + E_hover_descent

        # Maximum continuously required power
        P_req = max(P_cruise, P_climb, P_hover_climb)

        # Final power system weight, find & record battery size
        power_system_mass, power_system_name = component_sizing.power_system_mass_sizing(distr, rho_battery, E_est, P_req, battery_reserve)
        print("\t Power System Model:", power_system_name)
        

        # Electric Motor mass
        engine_mass = component_sizing.electric_motor_mass(P_req)

        # Check guess TOGW
        TOGM_est = mass_estimate.mass_estimate(S_wing, S_wetted_fuse, engine_mass, power_system_mass, payload)
        TOGW_est = TOGM_est * g

        if abs(TOGW_est - TOGW_guess) < tol:    # if converges
            print("Ended conversion in " + str(iter_num) + " iterations.")
            power_loading = TOGW_est / (P_req * 1.5)    # N/W
            disk_loading = TOGW_est / S_disk            # N/m^2
            wing_loading = TOGW_est / S_wing / g        # kg/m^2
            return TOGW_est, power_loading, disk_loading, wing_loading, P_req

        else:       # not yet converging
            TOGW_guess = TOGW_est

            if TOGW_guess > 100000:  # N
                power_loading = TOGW_est / (P_req * 1.5)    # N/W
                disk_loading = TOGW_est / S_disk            # N/m^2
                wing_loading = TOGW_est / S_wing / g  # kg/m^2
                print("No Convergence, guessed TOGW larger than 100 kN")
                return TOGW_guess, power_loading, disk_loading, wing_loading, P_req

            elif TOGW_guess < 2700:  # N
                power_loading = TOGW_est / (P_req * 1.5)    # N/W
                disk_loading = TOGW_est / S_disk            # N/m^2
                wing_loading = TOGW_est / S_wing / g  # kg/m^2
                print("No Convergence, guessed TOGW smaller than 2700 N")
                return TOGW_guess, power_loading, disk_loading, wing_loading, P_req

        iter_num += 1

        if iter_num > MAX_ITER:
            print("Iteration number exceeded limit: " + str(MAX_ITER) + ".")
            print("Function not showing convergence.")
            print("Consider re-evaluating assumptions and requirements.")
            return


if __name__ == "__main__":

    # Efficiencies:
    eta_mech = 0.7
    eta_p = 0.8

    # Velocities:
    V_hover_climb = 2.54  # m/s (equivalent to 500 ft/min)
    V_hover_descent = 0  # m/s (equivalent to 300 ft/min descent)

    V_climb = 44  # m/s (equivalent to 85.53 knots)
    V_cruise = 62  # m/s (equivalent to 120.52 knots) // Increase later

    # Rotor Stuff:
    f = 0.1 # "adjustment for downwash of fuselage"
    M = 0.6 # measure of merit

    # Reference Areas:
    S_disk = 20  # m^2 (ROUGH APPROXIMATION, no actual aircraft to compare to)
    S_wing = 26  # m^2 (taken from Cessna 172)
    S_wetted_fuse = 24.3  # m^2 (taken from Cessna 182RG)

    # Air Properties:
    rho = 1.05 # Assumed as a kind of "average" over the flight trajectory

    # Geometric and Drag Properties:
    e = 0.75
    AR = 10
    CD0 = 0.02 # Assumed, slightly smaller than C182RG CD0 with landing gear retracted



    # Forward flight climb angle
    gam_climb = numpy.arctan(1 / 16)     # Based on mission requirements

    # Distribution between battery and H2 fuel
    distr = 0 # fully H2, no battery

    # Battery info
    rho_battery = 260  # Wh/kg for high performance battery
    battery_reserve = 0.2 # 20% battery reserve

    climb_1 = 4 * 1609.34       # m
    climb_2 = 2 * 1609.34       # m
    climb_3_time = 4 * 60       # s
    cruise_1 = 7 * 1609.34      # m
    cruise_2 = 15 * 1609.34     # m
    cruise_3 = 30 * 1609.34     # m
    # Distances:
    dist_climb = ((climb_1 + climb_2) + V_climb * climb_3_time)     # m, horizontal dist of climb
    dist_cruise = (cruise_1 + cruise_2 + cruise_3)                  # m

    # Times:
    dist_sac_davis = 24462.03       # m
    time_climb = dist_climb / V_climb
    time_hover_climb = 60 * 2      # s, included hovering when landing aborted
    time_cruise = dist_cruise / V_cruise + dist_sac_davis / V_cruise   # s, included Sac to Davis
    time_hover_descent = 60 * 2

    payload = 300

    print("Running the test of \"sizing_process\" function")
    TOGW, power_loading, disk_loading, wing_loading, P_req = sizing_process(time_hover_climb, time_climb, time_cruise, time_hover_descent,
                                eta_mech, eta_p, V_hover_climb,
                                V_hover_descent, V_climb, V_cruise,
                                f, M, rho, e, AR, CD0, gam_climb, distr,
                                S_disk, S_wing, S_wetted_fuse,
                                rho_battery, battery_reserve, payload)
    print("========================================")
    print("The converged TOGW is " + str(TOGW) + " N")


